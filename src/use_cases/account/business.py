
from src.use_cases.account.rules import AccountRules
from src.use_cases._common.business import BaseBusiness
from src.domain.entities.account import Account
from src.use_cases.account.state import AccountState


class AccountBusiness(BaseBusiness):
    entity_class = Account
    rules_class = AccountRules
    state_class = AccountState
