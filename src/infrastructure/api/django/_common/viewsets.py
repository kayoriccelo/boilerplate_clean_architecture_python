import json
from http.client import OK
from django.http import HttpRequest, HttpResponse
from rest_framework.views import APIView

from src.infrastructure._common.views import BaseViewSet


class BaseGetViewSet(BaseViewSet, APIView):
    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        payload, status = self.controller.get(kwargs.get('pk'))

        data = json.dumps(payload, indent=4)

        return HttpResponse(data, content_type='application/json', status=status)
    

class BaseListViewSet(BaseViewSet, APIView):
    presenter_many = True

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        page = request.GET.get('page', 1)
        page_size = request.GET.get('page_size', 10)

        payload, status = self.controller.list(page, page_size)

        data = json.dumps(payload, indent=4)

        return HttpResponse(data, content_type='application/json', status=status)
    

class BaseCreateViewSet(BaseViewSet, APIView):
    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        params = request.data

        payload, status = self.controller.create(**params)

        if status == OK:
            data = json.dumps({'message': 'Operation carried out successfully.'}, indent=4)

        else:
            data = json.dumps(payload, indent=4)

        return HttpResponse(data, content_type='application/json', status=status)
    

class BaseUpdateViewSet(BaseViewSet, APIView):
    def update(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        params = request.data
        
        payload, status = self.controller.update(**params)

        if status == OK:
            data = json.dumps({'message': 'Operation carried out successfully.'}, indent=4)

        else:
            data = json.dumps(payload, indent=4)

        return HttpResponse(data, content_type='application/json', status=status)


class BaseDeleteViewSet(BaseViewSet, APIView):
    def delete(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        payload, status = self.controller.delete(kwargs.get('pk'))

        if status == OK:
            data = json.dumps({'message': 'Operation carried out successfully.'}, indent=4)
        
        else:
            data = json.dumps(payload, indent=4)    

        return HttpResponse(data, status=status)


class BaseActionViewSet(BaseViewSet, APIView):
    def do_action(self, **kwargs):
        raise NotImplementedError('Implementation of the required method.')
    
    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        params = request.data

        payload, status = self.do_action(**params)

        if status == OK:
            data = json.dumps({'message': 'Operation carried out successfully.'}, indent=4)

        else:
            data = json.dumps(payload, indent=4)

        return HttpResponse(data, content_type='application/json', status=status)
