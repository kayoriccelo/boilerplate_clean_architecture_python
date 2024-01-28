import pytest
from http.client import INTERNAL_SERVER_ERROR, OK

from src.interface.controllers.account.controller import AccountController

from tests._common.controller import BaseControllerTest


@pytest.mark.order(40000)
class TestAccountController(BaseControllerTest):
    controller_class = AccountController

    def test_validator_exception_information_required(self, account_controller):
        payload, status = account_controller.create(**{})

        assert status == INTERNAL_SERVER_ERROR.value
        
        assert 'type' in payload and payload['type'] == 'validator'

        assert 'message' in payload and payload['message'] == 'information required.'

    def test_create(self, account_data, account_entity, account_controller):
        payload, status = account_controller.create(**account_data)

        assert status == OK.value

        assert account_entity.asdict() == payload.asdict()

    def test_update(self, account_data, account_entity, account_controller):
        payload, status = account_controller.update(**account_data, status=1)

        assert status == OK.value

        assert account_entity.asdict() == payload.asdict()

    def test_get(self, account_entity, account_controller):
        _, status = account_controller.get(account_entity.id)

        assert status == OK.value

    def test_list(self, account_controller):
        payload, status = account_controller.list(1, 10)

        assert status == OK.value and payload['count'] > 0

    def test_delete(self, account_entity, account_controller):
        _, status = account_controller.delete(instance=account_entity)

        assert status == OK.value
