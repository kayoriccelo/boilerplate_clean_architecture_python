

from src.core.builders import BaseStateBuilder
from src.domain.entities.enums import StatusAccount
from src.use_cases.account.state import AccountActiveState, AccountInactiveState


class AccountStateBuilder(BaseStateBuilder):
    STATE_CLASSES = {
        StatusAccount.ACTIVE: AccountActiveState,
        StatusAccount.ACTIVE: AccountInactiveState,
    }
