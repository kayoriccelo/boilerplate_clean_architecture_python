<h1 align="center">Boilerplate - Arquitetura Limpa para Python</h1>

<p align="center"><i>Repositório para projetos que utilizam arquitetura limpa.</i></p>

[![en](https://img.shields.io/badge/lang-en-red)](README.md)
![Static Badge](https://img.shields.io/badge/python-3.8-blue)
![Static Badge](https://img.shields.io/badge/orm-django-3fb950)
![Static Badge](https://img.shields.io/badge/test-pytest-orange)
![Static Badge](https://img.shields.io/badge/env-docker-blue)
![Static Badge](https://img.shields.io/badge/tools-vscode-1158c7)

## Sobre este projeto

  Este é um repositório usado para ser uma referência para projetos que iram utilizar arquitetura limpa em python.

  Utilizando as 4 camadas da arquitetura limpa subdivido em: 
  - Domínio: onde possui a camada entidade.
  - Caso de uso: com as camadas de negócio, regra e estado. 
  - Interface: com as camadas de controlador e apresentador.
  - Infraestrutura: com os externos API e ORM

## Camadas

- ### 1 - Domínio
    #### 1.1 - Entity é onde está concentrada as regras do sistema.
    
    _Existe uma classe base chamada **BaseEntity**, está classe fornece as funcionalidades básicas para uma entidade, incluindo a funcionalidade de converter uma entidade em um dicionário._

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

    Exemplo:

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

    _Também possui uma classe meta chamada **EntityMetaclass**, está classe é responsável por invocar o método set_name dos atributos tipados com **ValueObject**._

    ```python
    class EntityMetaclass(type):
        def __init__(cls, name, bases, dictionary):
            super(EntityMetaclass, cls).__init__(name, bases, dictionary)

            for key, attribute in dictionary.items():
                if hasattr(attribute, 'set_name'):
                    attribute.set_name(f'__{name}', key)
    ```

    _O **ValueObject** visto anteriormente tem como papel principal encapsular com prefixo e chave os atributos melhorando a desempenho das instâncias ao serem alimentadas ou consultadas, também é possível criar regras por atributo._

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

    Exemplo:

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

- ### 2 - Caso de uso
    #### 2.1 - Rule é onde se encontra as regras relacionadas ao negócio/business.

    _Existe uma classe base chamada **BaseRules**, está classe é responsável por fornecedor métodos para auxiliar na verificação das regras e na execução de exceções caso existam, também possui um método para auxiliar na coleta de dados no kwargs._

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

    Exemplo:

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

    #### 2.2 - State é onde será controlado as permissões por situação.
    
    <!-- _Existe uma classe base chamada **BaseState**, está classe é responsável por realizar as permissões referênte ao negócio conforme a situação atual da entidade._ -->

    #### 2.3 - Business é onde será realizado a lógica de negócio do sistema.

    _Existe uma classe base chamada **BaseBusiness**, está classe é tem como principal responsabilidade realizar a lógica de negócio do sistema, também é responsável por interagir com o armazenamento de dados._

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

    Exemplo:

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

    Exemplo:

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

    Exemplo:

    ```python
    class AccountPresenter(BasePresenter):
        def __init__(self, serializer_class: any):
            self.serializer_class = serializer_class
    ```

- ### 4 - Infraestrutura
    #### 4.1 - API
    #### 4.2 - ORM

## Instalação

## Referências
  - [Encapsulamento com Descritores em Python](https://pt.slideshare.net/ramalho/encapsulamento-com-descritores-em-python)
  - [LIVE: Clean Architecture](https://metal-flea-041.notion.site/LIVE-Clean-Architecture-79e14d28f54c4484bcce129c1fd80591)
  - [Implementing Clean Architecture - Of controllers and presenters](https://www.plainionist.net/Implementing-Clean-Architecture-Controller-Presenter/)
  - [A quick introduction to clean architecture](https://www.freecodecamp.org/news/a-quick-introduction-to-clean-architecture-990c014448d2/)
  - [Python & the Clean Architecture in 2021](https://breadcrumbscollector.tech/python-the-clean-architecture-in-2021/)

## Diagram

<!-- ![boilerplate_clean_architecture_python drawio](https://github.com/kayoriccelo/boilerplate_clean_architecture_python/assets/19672365/6faabac4-a728-4c68-aef1-fe13f1fe4cbe) -->


