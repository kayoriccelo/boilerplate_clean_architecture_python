
class BaseBusiness:
    """
    Base Business class that implements the core business logic for the application.

    This class is responsible for enforcing business rules, managing the state of the system, and interacting with the data store.

    Attributes:
        repository (object): The repository object that is used to interact with the data store.
        entity_class (type): The entity class that is used to map data between the business layer and the data store.
        rules_class (type): The rules class that is used to enforce business rules.
        state_class (type): The state class that is used to manage the state of the system.
    """

    _kwargs: dict = {}
    entity_class: any = None
    rules_class: any = None
    state_builder_class: any = None

    def __init__(self, repository: object):
        self.repository = repository

    @property
    def state(self):
        if not hasattr(self, '_state'):
            builder_state = self.state_builder_class()
            state = builder_state.build(instance=self._kwargs['instance'])

            setattr(self, '_state', state)

        return getattr(self, '_state')

    @property
    def _rule(self):
        self.rule = self.rules_class()
