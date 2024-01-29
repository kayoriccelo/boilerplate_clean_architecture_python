
from src.core.exceptions import UseCaseBusinessException
from src.use_cases.account.business import AccountBusiness

from tests._common.use_case import BaseUseCaseBusinessTest


class TestAccountBusiness(BaseUseCaseBusinessTest):
    business_class = AccountBusiness

    def test_create(self, account_business, account_entity, account_repository):
        try:
            account_business.create(instance=account_entity, repository=account_repository)

            assert True

        except UseCaseBusinessException:
            assert False

    def test_update(self, account_business, account_entity, account_repository):
        try:
            instance = account_entity

            instance.first_name = 'Kayo Update'
            instance.last_name = 'Riccelo Update'

            account_business.update(instance=instance, repository=account_repository)

            assert True

        except UseCaseBusinessException:
            assert False

    def test_get(self, account_data, account_business):
        try:
            account_business.get(account_data['id'])

            assert True

        except UseCaseBusinessException:
            assert False

    def test_get_create_the_record(self, account_data, account_business):
        entity_class = account_business.entity_class
        account_business.entity_class = None
        
        try:
            account_business.get(account_data['id'])

            assert True

        except UseCaseBusinessException as err:
            assert err.message == 'create the record'
        
        finally:
            account_business.entity_class = entity_class

    def test_get_availables(self, account_business):
        try:
            account_business.get_availables(0, 10)

            assert True

        except UseCaseBusinessException:
            assert False

    def test_get_availables_access_page_listing(self, account_business):
        try:
            account_business.get_availables(-1, -1)

            assert False

        except UseCaseBusinessException as err:
            assert err.message == 'access page -1 of the listing'

    def test_delete(self, account_business, account_entity):
        try:
            account_business.delete(instance=account_entity)

            assert True

        except UseCaseBusinessException:
            assert False
