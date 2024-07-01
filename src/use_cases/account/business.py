
from src.core.exceptions.messages import (
    ACCESS_PAGE_LISTING_MESSAGE_EXCEPTION, CREATE_LISTING_RECORD_MESSAGE_EXCEPTION, 
    CREATE_RECORD_MESSAGE_EXCEPTION
)
from src.core.exceptions.types import UseCaseBusinessException
from src.use_cases.account.builders import AccountStateBuilder
from src.use_cases.account.rules import AccountRules
from src.use_cases._common.business import BaseBusiness
from src.domain.entities.account import Account


class AccountBusiness(BaseBusiness):
    entity_class = Account
    rules_class = AccountRules
    state_builder_class = AccountStateBuilder

    def get(self, pk: int) -> object:
        instance = self.repository.get(pk)

        try:
            instance_entity = self.entity_class(**instance.asdict())
        
        except Exception as err:
            raise UseCaseBusinessException(err, CREATE_RECORD_MESSAGE_EXCEPTION)
        
        return instance_entity

    def available(self, page: int, page_size: int) -> dict:
        pages = []
        results = []

        available = self.repository.available()

        try:
            available = [self.entity_class(**available.asdict()) for available in available]

        except Exception as err:
            raise UseCaseBusinessException(err, CREATE_LISTING_RECORD_MESSAGE_EXCEPTION)
        
        if len(available) > 0:
            try:
                pages = [available[i:i+page_size] for i in range(0, len(available), page_size)]
            
                results = pages[page - 1]

            except Exception as err:
                raise UseCaseBusinessException(err, ACCESS_PAGE_LISTING_MESSAGE_EXCEPTION % page)
        
        return {
            'count': len(available),
            'pages': len(pages),
            'results': results
        }

    def create(self, **kwargs):
        self._kwargs = kwargs

        self.rule.can_create(**kwargs)

        return self.repository.create(kwargs['instance'])

    def update(self, **kwargs):
        self.state.can_update(**kwargs)

        self.rule.can_update(**kwargs)

        return self.repository.update(kwargs['instance'])

    def delete(self, **kwargs):
        self.state.can_delete(**kwargs)

        self.rule.can_delete(**kwargs)

        return self.repository.delete(kwargs['instance'])
