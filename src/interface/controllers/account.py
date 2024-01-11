from src.interface._common.controller import BaseController
from src.use_cases.account.business import AccountBusiness


class AccountController(BaseController):
    business_class = AccountBusiness
