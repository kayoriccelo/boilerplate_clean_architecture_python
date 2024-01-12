import json
from django.http import HttpRequest, HttpResponse
from django.views import View

from src.infrastructure._common.views import BaseViewSet


class BaseGetViewSet(BaseViewSet, View):
    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        payload, status = self.controller.get(kwargs.get('pk'))

        data = self.serializer.dumps(payload)

        return HttpResponse(data, content_type='application/json', status=status)
    

class BaseListViewSet(BaseViewSet, View):
    serializer_many = True

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        page = request.GET.get('page', 1)
        page_size = request.GET.get('page_size', 10)

        payload, status = self.controller.list(page, page_size)

        results = self.serializer.dump([item for item in payload['results']])

        data = json.dumps({
            'results': results,
            'count': payload['count'],
            'pages': payload['pages']
        }, indent=4)

        return HttpResponse(data, content_type='application/json', status=status)
    

class BaseCreateViewSet(BaseViewSet, View):
    def create(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        params = request.CREATE

        payload, status = self.controller.create(params)

        data = self.serializer.dump(payload)

        return HttpResponse(data, content_type='application/json', status=status)
    

class BaseUpdateViewSet(BaseViewSet, View):
    def update(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        params = request.CREATE
        
        payload, status = self.controller.create(params)

        data = self.serializer.dump(payload)

        return HttpResponse(data, content_type='application/json', status=status)


class BaseDeleteViewSet(BaseViewSet, View):
    def delete(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        status = self.controller.delete(kwargs.get('pk'))

        return HttpResponse({}, status=status)
