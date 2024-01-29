
from src.interface._common.presenter import BasePresenter


class AccountPresenter(BasePresenter):
    def __init__(self, serializer_class: any):
        self.serializer_class = serializer_class
