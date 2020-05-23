from rest_framework import status
from rest_framework.views import APIView, Response, Request
from ApiRequesters.utils import get_token_from_request
from ApiRequesters.Auth.permissions import IsAuthenticated
from ApiRequesters.exceptions import BaseApiRequestError, UnexpectedResponse
from ApiRequesters.Places.PlacesRequester import PlacesRequester
from ApiRequesters.Media.MediaRequester import MediaRequester


class GetPlacesView(APIView):
    """
    Вьюха для получения списка мест
    """
    permission_classes = (IsAuthenticated, )

    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        self.requester = PlacesRequester()
        self.token = get_token_from_request(request)

    def get(self, request: Request):
        try:
            resp, places = self.requester.get_places(token=self.token)
        except BaseApiRequestError:
            return Response({'error': 'error on getting places'}, status=status.HTTP_502_BAD_GATEWAY)

        result_data = []
        for place in places:
            try:
                resp, images = MediaRequester().get_typed_images(object_type=MediaRequester.IMAGE_OBJ_TYPES.PLACE,
                                                                 object_id=place['id'], token=self.token)
                place['images'] = images
                for i in range(len(place['images'])):
                    place['images'][i]['image_url'] = 'http://127.0.0.1:8005' + place['images'][i]['image_url']
            except BaseApiRequestError:
                place['images'] = []
            result_data.append(place)

        return Response(result_data, status=status.HTTP_200_OK)


class GetPlaceView(APIView):
    """
    Вьюха для получения одного места
    """
    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        self.requester = PlacesRequester()
        self.token = get_token_from_request(request)

    def get(self, request: Request, place_id):
        try:
            resp, place = self.requester.get_place(place_id=place_id, token=self.token)
        except UnexpectedResponse as e:
            return Response({'error': str(e)}, status=e.code)
        except BaseApiRequestError:
            return Response({'error': 'error on getting place'}, status=status.HTTP_502_BAD_GATEWAY)

        try:
            resp, images = MediaRequester().get_typed_images(object_type=MediaRequester.IMAGE_OBJ_TYPES.PLACE,
                                                             object_id=place['id'], token=self.token)
            place['images'] = images
            for i in range(len(place['images'])):
                place['images'][i]['image_url'] = 'http://127.0.0.1:8005' + place['images'][i]['image_url']
        except BaseApiRequestError:
            place['images'] = []

        return Response(place, status=status.HTTP_200_OK)


