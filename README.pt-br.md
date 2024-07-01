<h1 align="center">Boilerplate - Arquitetura Limpa para Python</h1>

<p align="center"><i>Repositório para projetos que utilizam arquitetura limpa.</i></p>

[![en](https://img.shields.io/badge/lang-en-red)](README.md)
[![Static Badge](https://img.shields.io/badge/python-3.8-blue)](https://docs.python.org/3.8/)
[![Static Badge](https://img.shields.io/badge/framework-django-3fb950)](https://docs.djangoproject.com/pt-br/4.2/)
[![Static Badge](https://img.shields.io/badge/test-pytest-orange)](https://docs.pytest.org/en/7.4.x/contents.html)
[![Static Badge](https://img.shields.io/badge/env-docker-blue)](https://docs.docker.com/)
[![Static Badge](https://img.shields.io/badge/tools-vscode-1158c7)](https://code.visualstudio.com/docs)

## Sobre este projeto

  Este é um repositório usado como uma referência para projetos que iram utilizar arquitetura limpa em python.

  Abaixo será mostrada as 4 camadas da arquitetura limpa usadas nesse boilerplate, subdivido em: 
  - Domain: onde possui a camada de Entity.
  - Use Case: com as camadas de State, Rule e Business. 
  - Interface: com as camadas de Controller e Presenter.
  - Infrastructure: com os externos API e ORM

## Camadas

- ### 1 - Domain

    #### 1.1 - Na camada Entity está concentrada as regras de negócio do sistema.

    Uma Entidade é um objeto do sistema que possui um pequeno conjunto de regras cruciais de negócios genéricas que operam com base em dados, também contém os dados cruciais de negócios ou tem acesso muito fácil a esses dados.

    > _**NOTA I:** Se você estiver procurando informações sobre Entidade, consulte as páginas 198 e 209 do livro **Arquitetura Limpa - O Guia do Artesão para Estrutura e Design de Software (Robert C. Martin)**._
    
    Abaixo será exibida uma classe base chamada **BaseEntity**, está classe fornece as funcionalidades básicas para uma entidade, incluindo a funcionalidade de converter uma entidade em um dicionário.

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

    Também possui uma classe meta chamada **EntityMetaclass**, está classe é responsável por invocar o método set_name dos atributos tipados com **ValueObject**.

    > _**NOTA II:** Se você estiver procurando informações sobre Encapsulamento com Descritores, consulta [Encapsulamento com Descritores em Python](https://pt.slideshare.net/ramalho/encapsulamento-com-descritores-em-python)_ 

    ```python
    class EntityMetaclass(type):
        def __init__(cls, name, bases, dictionary):
            super(EntityMetaclass, cls).__init__(name, bases, dictionary)

            for key, attribute in dictionary.items():
                if hasattr(attribute, 'set_name'):
                    attribute.set_name(f'__{name}', key)
    ```

    O **ValueObject** visto anteriormente, tem como papel principal de encapsular com prefixo e chave os atributos, melhorando o desempenho das instâncias ao serem alimentadas ou consultadas, também é possível criar validações por atributo.

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

- ### 2 - Use Case
    
    Um caso de uso é um objeto que tem uma ou mais funções que implementam as regras de negócio específicas da aplicação. Também tem
    elementos de dados que incluem os dados de entrada, os dados de saída e as referências para as devidas Entidades com as quais interage.

    > _**NOTA:** Como mencionado anteriormente, a camada de **Use Case** foi dividida em três camadas: **State**, **Rule** e **Business**, facilitando a organização das permissões por situação, regras e negócio. Se você estiver procurando informações sobre **Use Case**, consulte a página 199 e 209 do livro **Arquitetura Limpa - O Guia do Artesão para Estrutura e Design de Software (Robert C. Martin)**._

    #### 2.1 - A camada State controla a mudança de situação e as permissões por situação.

    O **State** é um padrão de projeto comportamental que permite que um objeto altere o comportamento quando seu estado interno for alterado. 
    
    > _**NOTA I:** Se você estiver procurando informações sobre o padrão **_State_**, consulte [State em Python / Padrões de Projeto](https://refactoring.guru/pt-br/design-patterns/state/python/example)._
    
    Abaixo será exibido 
     classe base chamada **BaseState**, está classe é responsável por fornecedor métodos para auxiliar na mudança de situação do objeto e o controle das permissões conforme a situação atual, também possui métodos para auxiliar na execução de exceções e coleta de dados no kwargs.

    ```python
    class BaseState:
        _exception: bool = True
        _can: bool = True
        _kwargs: dict = {}
        _field_name: str = 'status'
        _status_permission: list = []
        _instance: object = None

        def __init__(self, instance) -> None:
            self._instance = instance

        def _get_value_in_kwargs(self, name: str, required: bool = True) -> any:
            value = self._kwargs.get(name, None)

            if not value and required:
                raise SystemException(None, NOT_FOUND_IN_MESSAGE_EXCEPTION % (name, type(self).__name__))

            return value

        def execute_exception(self) -> bool:
            self._exception = self._kwargs.get('exception', self._exception)

            if not self._can and self._exception:
                raise UseCaseStateException(None, OPERATION_WITHOUT_PERMISSION_MESSAGE_EXCEPTION)

            return self._can
        
        def set_status(self, status):
            if not status in self._status_permission:
                raise UseCaseStateException(None, CHANGE_STATUS_NOT_ALLOWED_MESSAGE_EXCEPTION)

            setattr(self._instance, self._field_name, status)
            self._instance.save()
    
    ```

    Exemplo:

    ```python
    class AccountState(BaseState):
        def situation_active(self):
            return self.status == StatusAccount.ACTIVE.value

        def situation_inactive(self):
            return self.status == StatusAccount.INACTIVE.value
            
        def can_update(self, **kwargs):
            return False
        
        def can_delete(self, **kwargs):
            return False


    class AccountActiveState(AccountState):
        _status_permission = [StatusAccount.INACTIVE.value]

        def can_update(self, **kwargs):
            return True
        
        def can_delete(self, **kwargs):
            return True


    class AccountInactiveState(AccountState):
        _status_permission = []

    ```

    > _**NOTA II:** A criação do **State** é realizado com auxilio do padrão de projeto criacional **Builder**, que permite a construção de objetos complexos. Se você estiver procurando informações sobre **Builder**, consulte [Builder em Python / Padrões de Projeto](https://refactoring.guru/pt-br/design-patterns/builder/python/example)._

    Abaixo será exibido uma classe base chamada **BaseStateBuilder**, está classe é respónsavel por auxiliar na construção do **State**.

    ```python
    class BaseBuilder:
        def build(self, **kwargs) -> object:
            raise NotImplementedError('Implementation of the required method.')


    class BaseStateBuilder(BaseBuilder):
        STATE_CLASSES = {}
            
        def build(self, **kwargs) -> object:
            state_class = self.STATE_CLASSES.get(kwargs['status'])

            return state_class(kwargs['model_object'])
    ```

    Exemplo:

    ```python
    class AccountStateBuilder(BaseStateBuilder):
        STATE_CLASSES = {
            StatusAccount.ACTIVE: AccountActiveState,
            StatusAccount.ACTIVE: AccountInactiveState,
        }
    ```

    #### 2.2 - Na camada Rule será implementada as regras relacionadas ao negócio.

    Eu criei essa camada separando as regras do negócio com o intuito de organizar em um único local, fazendo com fique fácil a localização e a manutenção.

    Abaixo será exibida uma classe base chamada **BaseRules**, está classe é responsável por fornecedor métodos para auxiliar na verificação das regras e na execução de exceções caso existam, também possui um método para auxiliar na coleta de dados no kwargs.

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

    #### 2.3 - Na camada Business encontra-se toda lógica de negócio do sistema.

    Também criei essa camada separando a lógica de negócio das regras com o intuito de organizar em um único local, fazendo com fique fácil a localização e a manutenção.

    Abaixo será exibida uma classe base chamada **BaseBusiness**, está classe tem como principal responsabilidade realizar a lógica de negócio do sistema, também é responsável por interagir com o armazenamento de dados por meio do **Repository**.

    ```python
    class BaseBusiness:
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
    ```

    Exemplo:

    ```python
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

    ```

- ### 3 - Interface
    A inteface tem como principal papel converter dados no formato que seja mais conveniente para os casos de usos e entidades, também tem o papel de converter os dados no formato mais conveniente para infrastructure (frameworks e drivers).

    > _**NOTA:** Se você estiver procurando informações sobre **Adaptadores de interface**, consulte as páginas 209 e 210 do livro **Arquitetura Limpa - O Guia do Artesão para Estrutura e Design de Software (Robert C. Martin)**._

    #### 3.1 - A camada Controller controla a entrada de dados das solicitações, validando e convertendo para um formato reconhecido pelo negócio.

    ```python
    class BaseController:
        business_class = None
        presenter_class = None

        def __init__(self, repository: object, serializer_class: object):
            self.business = self.business_class(repository)
            self.presenter = self.presenter_class(serializer_class)

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
                send_email_error(err)

                return {
                    'type': 'business',
                    'message': INCONSISTENCY_MESSAGE_FOUND % err.message
                }, INTERNAL_SERVER_ERROR.value

            except RepositoryException as err:
                send_email_error(err)

                return {
                    'type': 'repository',
                    'message': INCONSISTENCY_MESSAGE_FOUND_SYSTEM
                }, INTERNAL_SERVER_ERROR.value

            except Exception as err:
                send_email_error(err)

                return {
                    'type': 'generic',
                    'message': INCONSISTENCY_MESSAGE_FOUND_SYSTEM
                }, INTERNAL_SERVER_ERROR.value

            return payload, OK.value
    ```

    Exemplo:

    ```python
    class AccountController(BaseController):
        business_class = AccountBusiness
        presenter_class = AccountPresenter

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

        def create(self, **kwargs) -> int:
            def do_create():
                validator = AccountCreateValidator()
                validator.is_valid(kwargs)

                account = Account(**validator.data)

                payload = self.business.create(instance=account, repository=self.business.repository)

                return self.presenter.parse(payload)

            return self._to_try(do_create)

        def update(self, **kwargs) -> int:
            def do_update():
                validator = AccountUpdateValidator()
                validator.is_valid(kwargs)

                account = Account(**validator.data)

                payload = self.business.update(instance=account, repository=self.business.repository)
            
                return self.presenter.parse(payload)
            
            return self._to_try(do_update)

        def delete(self, **kwargs) -> int:
            def do_delete():
                return self.business.delete(**kwargs)

            return self._to_try(do_delete)


    ```

    #### 3.2 - A camada Presenter converte os dados retornado pelo negócio em dicionário.

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

- ### 4 - Infrastructure 
    #### 4.1 - API
    #### 4.2 - ORM

## Instalação

## Referências
  - [Encapsulamento com Descritores em Python](https://pt.slideshare.net/ramalho/encapsulamento-com-descritores-em-python)
  - [LIVE: Clean Architecture](https://metal-flea-041.notion.site/LIVE-Clean-Architecture-79e14d28f54c4484bcce129c1fd80591)
  - [Implementing Clean Architecture - Of controllers and presenters](https://www.plainionist.net/Implementing-Clean-Architecture-Controller-Presenter/)
  - [A quick introduction to clean architecture](https://www.freecodecamp.org/news/a-quick-introduction-to-clean-architecture-990c014448d2/)
  - [Python & the Clean Architecture in 2021](https://breadcrumbscollector.tech/python-the-clean-architecture-in-2021/)

## Diagrama

<!-- ![boilerplate_clean_architecture_python drawio](https://github.com/kayoriccelo/boilerplate_clean_architecture_python/assets/19672365/6faabac4-a728-4c68-aef1-fe13f1fe4cbe) -->


