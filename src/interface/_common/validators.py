from datetime import datetime

from src.core.exceptions import ValidatorException


class BaseValidator:
    _params = {}
    _errors = []
    _data = {}

    def __init__(self):
        self.clean_attributes()

    @property
    def errors(self):
        return self._errors

    @property
    def data(self):
        return self._data

    @property
    def params(self):
        return self._params

    def clean_attributes(self):
        self._params = {}
        self._errors = []
        self._data = {}

    def set_errors(self, error):
        self._errors.append(error)

    def is_valid(self, params, show_errors=True):
        self.clean_attributes()

        self._params = params

        if not self._params:
            raise ValidatorException('', 'information required.')

        self._validate()

        if show_errors:
            self.show_errors()

        return len(self._errors) > 0

    def _validate(self):
        for attribute in dir(self):
            if not '__' in attribute and hasattr(self, attribute):
                field = getattr(self, attribute)

                if field and hasattr(field, 'validate'):
                    value = field.validate(self, attribute)

                    self._data[attribute] = value

    def show_errors(self):
        if len(self._errors) > 0:
            message = ''

            for index, error in enumerate(self._errors):
                message += error if index == len(self._errors) - 1 else f'{error}, '

            raise ValidatorException('', f'there are outstanding criticisms: {message}.')


class ValidatorField:
    validator = None
    field_name = None
    label = None
    required = True

    def __init__(self, label, required=True, field_name_extract=None):
        self.label = label
        self.required = required
        self.field_name_extract = field_name_extract

    def get_value(self):
        value = self.validator.params.get(self.field_name, None)

        if self.field_name_extract:
            value = self.validator.params.get(self.field_name_extract, None)

        if type(value) == str:
            value = value.replace('undefined', '')

        return value

    def validate(self, validator, field_name):
        self.validator = validator
        self.field_name = field_name


class DateValidatorField(ValidatorField):
    def validate(self, validator, field_name):
        super().validate(validator, field_name)

        date = self.get_value()

        if not date or not bool(date):
            if self.required:
                self.validator.set_errors(f'{self.label} not informed.')

        else:
            try:
                date = datetime.strptime(date, '%Y-%m-%d')

            except:
                self.validator.set_errors(f'{self.label} is in an invalid format.')

        return date


class DateTimeValidatorField(ValidatorField):
    def validate(self, validator, field_name):
        super().validate(validator, field_name)

        date = self.get_value()

        if not date or not bool(date):
            if self.required:
                self.validator.set_errors(f'{self.label} not informed.')

        else:
            try:
                date = datetime.strptime(date, '%Y-%m-%dT%H:%M')

            except:
                self.validator.set_errors(f'{self.label} is in an invalid format.')

        return date


class ChoiceValidatorField(ValidatorField):
    choices = None

    def __init__(self, label, choices, required=True, field_name_extract=None):
        super().__init__(label, required, field_name_extract)

        self.choices = choices

    def validate(self, validator, field_name):
        super().validate(validator, field_name)

        choice = self.get_value()

        if not choice or not bool(choice):
            if self.required:
                self.validator.set_errors(f'{self.label} not informed.')

        else:
            try:
                choice = int(choice)

                try:
                    choice = self.choices.__getitem__(choice - 1)[0]

                except:
                    self.validator.set_errors(f"{self.label} it's an invalid choice.")

            except:
                self.validator.set_errors(f'{self.label} is in an invalid format.')

        return choice


class CharValidatorField(ValidatorField):
    def validate(self, validator, field_name):
        super().validate(validator, field_name)

        value = self.get_value()

        if not value or not bool(value):
            if self.required:
                self.validator.set_errors(f'{self.label} not informed.')

        return value


class FileValidatorField(ValidatorField):
    format = None

    def __init__(self, label, format, required=True, field_name_extract=None):
        super().__init__(label, required, field_name_extract)

        self.format = format

    def validate(self, validator, field_name):
        super().validate(validator, field_name)

        anexo = self.get_value()

        if not anexo or not bool(anexo):
            if self.required:
                self.validator.set_errors(f'{self.label} not informed.')

        else:
            if not 'pdf' in anexo.content_type:
                self.validator.set_errors(f'{self.label} is in an invalid format.')

        return anexo
