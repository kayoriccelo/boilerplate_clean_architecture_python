from src.use_cases.account.rules import AccountRules
from src.use_cases._common.business import BaseBusiness


class AccountBusiness(BaseBusiness):
    rules_class = AccountRules
