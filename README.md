<h1 align="center">Boilerplate - Clean Architecture for Python</h1>

<p align="center"><i>Repository for projects that use clean architecture.</i></p>

[![ptBr](https://img.shields.io/badge/lang-pt-green)](README.pt-br.md)
[![Static Badge](https://img.shields.io/badge/python-3.8-blue)](https://docs.python.org/3.8/)
[![Static Badge](https://img.shields.io/badge/framework-django-3fb950)](https://docs.djangoproject.com/pt-br/4.2/)
[![Static Badge](https://img.shields.io/badge/test-pytest-orange)](https://docs.pytest.org/en/7.4.x/contents.html)
[![Static Badge](https://img.shields.io/badge/env-docker-blue)](https://docs.docker.com/)
[![Static Badge](https://img.shields.io/badge/tools-vscode-1158c7)](https://code.visualstudio.com/docs)

## About this project

  This is a repository that serves as a reference for projects that use clean architecture in python.

  It uses the 4 layers of clean architecture subdiveded into:
  - Domain: where there is an entity layer.
  - Use case: with layers of business, rules and state.
  - Interface: with controller and presenter layers.
  - Infrastructure: with API and ORM layers.

## Layers

- ### 1 - Domain
    #### 1.1 - Entity is where the system rules are concentrated.

    _There is a base class called **BaseEntity**, this class provides basic functionalily for an entity, including functionality to convert an entity to a dictionary._

    ```python
    class BaseEntity:
        __metaclass__ = EntityMetaclass

        def __init__(self, **kwargs):
            for attribute, value in kwargs.items():
                if not attribute.startswith('__'):
                    setattr(self, attribute, value)

        def asdict(self):
            dictionary = dict()

            for attribute in dir(self):
                if attribute.startswith('__'): continue
                if callable(getattr(self, attribute)): continue
                if getattr(self, attribute) is None: continue

                dictionary[attribute] = getattr(self, attribute)

            return dictionary
    ```

    Example:

    ```python
    class Account(BaseEntity):
        id = UUIDValue()
        created = DateTimeValue(auto_add=True, default=datetime.now())
        first_name = CharValue(max_length=200)
        last_name = CharValue(max_length=200)
        number_identity = CharValue(max_length=20)
        date_birth = DateValue()
        gender = ChoiceValue(enum=GenderAccount)
        status = ChoiceValue(enum=StatusAccount, default=StatusAccount.ACTIVE.value)
    ```

    _It also has a metaclass called **EntityMetaclass**, this class is responsible for invoking the set_name method of attributes typed with **ValueObject**._

    ```python
    class EntityMetaclass(type):
        def __init__(cls, name, bases, dictionary):
            super(EntityMetaclass, cls).__init__(name, bases, dictionary)

            for key, attribute in dictionary.items():
                if hasattr(attribute, 'set_name'):
                    attribute.set_name(f'__{name}', key)
    ```

    _The **ValueObject** seen previously has the main function of encapsulating attributes with prefix and key, improving the performance of instances when fed or consulted, it is also possible to create rules per attribute._

    ```python
    class ValueObject:
        default: any = None

        def __init__(self, **kwargs) -> None:
            self.default = kwargs.get('default', self.default)

            self.set_name(self.__class__.__name__, id(self))

        def set_name(self, prefix: str, key: int) -> None:
            self.target_name = f"__{prefix.lower()}_{key}"

        def __get__(self, instance: any, owner: any) -> any:       
            value = self.default

            if hasattr(instance, self.target_name):
                value = getattr(instance, self.target_name)

            else:
                setattr(instance, self.target_name, value)

            return value

        def __set__(self, instance: any, value: any = None) -> None:
            setattr(instance, self.target_name, value)
    ```

    Example:

    ```python
    class CharValue(ValueObject):
        max_length = -1

        def __init__(self, **kwargs) -> None:
            self.max_length = kwargs.get('max_length', self.max_length)

            super().__init__(**kwargs)

        def __set__(self, instance, value=None):
            if type(value) == str:
                if len(value) > self.max_length:
                    ValueObjectException(MAX_LENGHT_MESSAGE_EXCEPTION % self.max_length)

            else:
                ValueObjectException(FORMAT_INVALID_MESSAGE_EXCEPTION)
                
            setattr(instance, self.target_name, value)
    ```


- ### 2 - Use case
    #### 2.1 - Rules is where you find business rules.

    _There is a base class called **BaseRules**, this class is responsible for providing methods to assist in checking the rules and executing exceptions if they exist, it also has a method to assist in collecting data in kwargs._

    ```python
    class BaseRules:
    _exception: bool = True
    _can: bool = True
    _kwargs: dict = {}

    def _get_value_in_kwargs(self, name: str, required: bool = True) -> Any:
        value = self._kwargs.get(name, None)

        if not value and required:
            raise SystemException(None, NOT_FOUND_IN_MESSAGE_EXCEPTION % (name, type(self).__name__))

        return value

    def execute_exception(self, message: str) -> bool:
        if self._exception:
            raise UseCaseRuleException("", message)

        return self.can

    def execute_callback(self, callback: Callable[[], bool]) -> None:
        self._exception = self._kwargs.get('exception', self._exception)

        if not self._can:
            self._can = callback()

        else:
            callback()

    ```

    Example:

    ```python
    class AccountRules(BaseRules):
        def __account_already_created(self):
            repository = self._get_value_in_kwargs('repository')
            account = self._get_value_in_kwargs('instance')

            account_exists = repository.account_exists(account)

            if account_exists:
                return self.execute_exception(ALREADY_CREATED_MESSAGE_EXCEPTION % 'account')
            
            return False
        
        def can_create(self, **kwargs):
            self._kwargs = kwargs

            self.execute_callback(self.__account_already_created)

            return self._can
    ```

    #### 2.2 - State is where status permissions are controlled.

    #### 2.3 - Business is where you find business rules.

    _There is a base class called **BaseBusiness**, this class is mainly responsible for carrying out the system's business logic, it is also responsible for interacting with the data storage._

    ```python
    class BaseBusiness:
        entity_class = None
        rules_class = None
        state_class = None

        def __init__(self, repository: object):
            self.repository = repository
            self.rule = self.rules_class()
            self.state = self.state_class()

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

    ```

    Example:

    ```python
    class AccountBusiness(BaseBusiness):
        entity_class = Account
        rules_class = AccountRules
        state_class = AccountState
    ```
  
- ### 3 - Interface
    #### 3.1 - Controller

    ```python
    class BaseController:
        business_class = None
        presenter_class = None

        def __init__(self, repository: object, serializer_class: object):
            self.business = self.business_class(repository)
            self.presenter = self.presenter_class(serializer_class)

        def _send_email_error(self, exception: Exception):
            exc_type, exc_value, exc_traceback = sys.exc_info()
            trace = exception.__traceback__

            print(f"""
                *****************************************************
                
                WARNING: Exception generated by the system.

                type               : {exc_type.__name__}
                message            : {exc_value.message if hasattr(exc_value, 'message') else ''}
                error              : {exc_value.error if hasattr(exc_value, 'error') else ''}
                tracking lines     : 
            """)

            while trace is not None:
                print(f"""
                    -------------------------------------------------  
                    ---> path and file name : {trace.tb_frame.f_code.co_filename}
                    ---> line code          : {trace.tb_lineno}
                    ---> method name        : {trace.tb_frame.f_code.co_name}
                    -------------------------------------------------
                """)

                trace = trace.tb_next

            print(f"""
                *****************************************************
            """)

        def _to_try(self, callback):
            try:
                payload = callback()

            except ValidatorException as err:
                return {
                    'type': 'validator',
                    'message': err.message,
                    'errors': err.errors
                }, INTERNAL_SERVER_ERROR.value

            except UseCaseRuleException as err:
                return {
                    'type': 'rule',
                    'message': err.message
                }, INTERNAL_SERVER_ERROR.value

            except UseCaseBusinessException as err:
                self._send_email_error(err)

                return {
                    'type': 'business',
                    'message': INCONSISTENCY_MESSAGE_FOUND % err.message
                }, INTERNAL_SERVER_ERROR.value

            except RepositoryException as err:
                self._send_email_error(err)

                return {
                    'type': 'repository',
                    'message': INCONSISTENCY_MESSAGE_FOUND_SYSTEM
                }, INTERNAL_SERVER_ERROR.value

            except Exception as err:
                self._send_email_error(err)

                return {
                    'type': 'generic',
                    'message': INCONSISTENCY_MESSAGE_FOUND_SYSTEM
                }, INTERNAL_SERVER_ERROR.value

            return payload, OK.value

        def get(self, pk: int) -> Tuple[dict, int]:
            def do_get():
                result = self.business.get(pk)

                return self.presenter.parse(result)

            return self._to_try(do_get)

        def list(self, page: int, page_size: int) -> Tuple[list, int]:            
            def do_list():
                payload = self.business.available(page, page_size)

                data = ([self.presenter.parse(item) for item in payload['results']])

                return {
                    'results': data,
                    'count': payload['count'],
                    'pages': payload['pages']
                }

            return self._to_try(do_list)

    ```

    Example:

    ```python
    class AccountController(BaseController):
        business_class = AccountBusiness
        presenter_class = AccountPresenter

        def create(self, **kwargs) -> int:
            def do_create():
                validator = AccountCreateValidator()
                validator.is_valid(kwargs)

                account = Account(**validator.data)

                payload = self.business.create(instance=account, repository=self.business.repository)

                return self.presenter.parse(payload)

            return self._to_try(do_create)

    ```

    #### 3.2 - Presenter

    ```python
    class BasePresenter:    
        serializer_class = None

        def __init__(self, serializer_class: any) -> None:
            self.serializer_class = serializer_class

        def parse(self, instance: object) -> dict:
            result = self.serializer_class(instance)

            if hasattr(result, 'data'):
                self.data = result.data

            else:
                self.data = result

            return self.data
    ```

    Example:

    ```python
    class AccountPresenter(BasePresenter):
        def __init__(self, serializer_class: any):
            self.serializer_class = serializer_class
    ```

- ### 4 - Infrastructure
    #### 4.1 - API
    #### 4.2 - ORM

## Installation

## References
  - [Encapsulamento com Descritores em Python](https://pt.slideshare.net/ramalho/encapsulamento-com-descritores-em-python)
  - [LIVE: Clean Architecture](https://metal-flea-041.notion.site/LIVE-Clean-Architecture-79e14d28f54c4484bcce129c1fd80591)
  - [Implementing Clean Architecture - Of controllers and presenters](https://www.plainionist.net/Implementing-Clean-Architecture-Controller-Presenter/)
  - [A quick introduction to clean architecture](https://www.freecodecamp.org/news/a-quick-introduction-to-clean-architecture-990c014448d2/)
  - [Python & the Clean Architecture in 2021](https://breadcrumbscollector.tech/python-the-clean-architecture-in-2021/)


## Diagram