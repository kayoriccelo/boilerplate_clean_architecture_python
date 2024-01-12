from http import HTTPStatus
from typing import Tuple


class BaseController:
    business_class = None
    
    def __init__(self, repository: object):
        self.business = self.business_class(repository)

    def get(self, pk: int) -> Tuple[dict, int]:
        try:
            instance = self.business.get(pk)

        except Exception as err:
            return {'error': err.message}, HTTPStatus.NOT_FOUND.value

        return instance, HTTPStatus.OK.value

    def list(self, page: int, page_size: int) -> Tuple[list, int]:
        try:
            instances = self.business.get_availables(page, page_size)
            
        except Exception as err:
            return {'error': err.message}, HTTPStatus.BAD_REQUEST.value

        return instances, HTTPStatus.OK.value

    def create(self, **kwargs) -> int:
        try:
            self.business.create(**kwargs)

        except Exception as err:
            return {'error': err.message}, HTTPStatus.BAD_REQUEST.value
        
        return HTTPStatus.OK.value

    def update(self, **kwargs) -> int:
        try:
            self.business.update(**kwargs)

        except Exception as err:
            return {'error': err.message}, HTTPStatus.BAD_REQUEST.value

        return HTTPStatus.OK.value

    def delete(self, **kwargs) -> int:
        try:
            self.business.delete(**kwargs)

        except Exception as err:
            return {'error': err.message}, HTTPStatus.BAD_REQUEST.value

        return HTTPStatus.OK.value
