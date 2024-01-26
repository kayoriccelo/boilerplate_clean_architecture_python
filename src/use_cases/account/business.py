
from src.use_cases.account.rules import AccountRules
from src.use_cases._common.business import BaseBusiness
from src.domain.entities.account import Account


class AccountBusiness(BaseBusiness):
    entity_class = Account
    rules_class = AccountRules
