
import copy
import pytest

from src.core.exceptions.messages import (
    ACCESS_PAGE_LISTING_MESSAGE_EXCEPTION, CREATE_RECORD_MESSAGE_EXCEPTION
)
from src.core.exceptions.types import UseCaseBusinessException
from src.use_cases.account.business import AccountBusiness

from tests._common.use_case import BaseUseCaseBusinessTest


class TestAccountBusiness(BaseUseCaseBusinessTest):
    business_class = AccountBusiness

    def test_create(self, account_business, account_entity, account_repository):
        try:
            account_business.create(instance=account_entity, repository=account_repository)

        except UseCaseBusinessException:
            assert False

    def test_update(self, account_business, account_entity, account_repository):
        try:
            instance = copy.copy(account_entity)

            instance.first_name = 'Kayo Update'
            instance.last_name = 'Riccelo Update'
            account_business.update(instance=instance, repository=account_repository)

            del instance

        except UseCaseBusinessException:
            assert False

    def test_get(self, account_data, account_business):
        try:
            account_business.get(account_data['id'])

        except UseCaseBusinessException:
            assert False

    def test_get_create_the_record(self, account_data, account_business):
        with pytest.raises(UseCaseBusinessException) as info:
            business = copy.copy(account_business)

            business.entity_class = None
            business.get(account_data['id'])

            del business

        assert info.value.message == CREATE_RECORD_MESSAGE_EXCEPTION

    def test_available(self, account_business):
        try:
            account_business.available(0, 10)

        except UseCaseBusinessException:
            assert False

    def test_available_access_page_listing(self, account_business):
        with pytest.raises(UseCaseBusinessException) as info:
            account_business.available(-1, -1)

        assert info.value.message == ACCESS_PAGE_LISTING_MESSAGE_EXCEPTION % -1

    def test_delete(self, account_business, account_entity):
        try:
            account_business.delete(instance=account_entity)

        except UseCaseBusinessException:
            assert False
