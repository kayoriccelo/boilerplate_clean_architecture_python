from datetime import datetime
from typing import Dict, List

from src.core.exceptions.types import ValidatorException
from src.core.exceptions.messages import (
    INFORMATION_REQUIRED_MESSAGE_EXCEPTION, THERE_ARE_OUTSTANDING_CRITICISMS_MESSAGE_EXCEPTION
)


class BaseValidator:
    """
    Base class for all validators.

    This class provides a set of methods for validating data and returning errors.
    It also provides a set of properties for accessing the data and errors that
    occurred during validation.

    Attributes:
        _params (dict): The parameters passed to the validator.
        _errors (list): A list of errors that occurred during validation.
        _data (dict): The data that was validated.
    """

    def __init__(self):
        """
        Initialize the validator.

        This method resets the attributes of the validator to their initial
        values.
        """
        
        self.clean_attributes()

    @property
    def errors(self) -> List[Dict[str, str]]:
        """
        Returns a list of errors that occurred during validation.

        Returns:
            A list of dictionaries, where each dictionary represents an error.
            The dictionary contains two keys: 'field_name' and 'error'. The
            'field_name' key contains the name of the field that generated the
            error, and the 'error' key contains a message describing the error.
        """

        return self._errors

    @property
    def data(self):
        """
        Returns the data that was validated.

        Returns:
            The data that was validated.
        """

        return self._data

    @property
    def params(self) -> dict:
        """
        Returns the parameters passed to the validator.

        Returns:
            The parameters passed to the validator.
        """

        return self._params

    def clean_attributes(self):
        """
        Reset the attributes of the validator to their initial values.

        This method resets the attributes of the validator to their initial
        values. This includes the _params, _errors, and _data attributes.
        """

        self._params = {}
        self._errors = []
        self._data = {}

    def set_errors(self, field_name, error):
        """
        Add an error to the list of errors.

        Args:
            field_name (str): The name of the field that generated the error.
            error (str): The error message.
        """

        self._errors.append({'field_name': field_name, 'error': error})

    def is_valid(self, params, show_errors=True):
        """
        Validate the given parameters.

        Args:
            params (dict): The parameters to be validated.
            show_errors (bool, optional): Whether to show errors or not.
                Defaults to True.

        Returns:
            bool: Whether the parameters are valid or not.

        Raises:
            ValidatorException: If there are errors during validation.
        """

        self.clean_attributes()

        self._params = params

        if not self._params:
            raise ValidatorException(None, INFORMATION_REQUIRED_MESSAGE_EXCEPTION)

        self._validate()

        if show_errors:
            self.show_errors()

        return len(self._errors) > 0

    def _validate(self):
        """
        Validate the given parameters.

        This method is called by is_valid() and is responsible for validating
        the given parameters. It loops through all the attributes of the
        validator and calls the validate() method of any attributes that are
        instances of ValidatorField.
        """

        for attribute in dir(self):
            if not '__' in attribute and hasattr(self, attribute):
                field = getattr(self, attribute)

                if field and hasattr(field, 'validate'):
                    value = field.validate(self, attribute)

                    self._data[attribute] = value

    def show_errors(self):
        """
        Show the errors that occurred during validation.

        This method is called by is_valid() if show_errors=True. It raises an
        exception if there are errors during validation.
        """

        if len(self._errors) > 0:
            raise ValidatorException(None, THERE_ARE_OUTSTANDING_CRITICISMS_MESSAGE_EXCEPTION, self._errors)


class ValidatorField:
    """
    A class for validating fields in a validator.

    This class provides a set of methods for validating fields and returning
    errors. It also provides a set of properties for accessing the validator and
    field name that are associated with the field.

    Attributes:
        validator (BaseValidator): The validator that the field is associated
            with.
        field_name (str): The name of the field.
        label (str): The label of the field.
        required (bool): Whether the field is required or not.
    """

    def __init__(self, label, required=True, field_name_extract=None):
        """
        Initialize the validator field.

        Args:
            label (str): The label of the field.
            required (bool, optional): Whether the field is required or not.
                Defaults to True.
            field_name_extract (str, optional): The name of the field to extract
                the value from. If not provided, the field name will be used.
        """

        self.label = label
        self.required = required
        self.field_name_extract = field_name_extract

    def get_value(self):
        """
        Get the value of the field.

        This method returns the value of the field, after performing any
        necessary extraction.

        Returns:
            The value of the field.
        """

        value = self.validator.params.get(self.field_name, None)

        if self.field_name_extract:
            value = self.validator.params.get(self.field_name_extract, None)

        if type(value) == str:
            value = value.replace('undefined', '')

        return value

    def validate(self, validator, field_name):
        """
        Validate the field.

        This method is called by the validator that the field is associated
        with. It sets the validator and field name attributes of the field.

        Args:
            validator (BaseValidator): The validator that the field is
                associated with.
            field_name (str): The name of the field.
        """

        self.validator = validator
        self.field_name = field_name


class UUIDValidatorField(ValidatorField):
    def validate(self, validator, field_name):
        super().validate(validator, field_name)

        value = self.get_value()

        return value


class DateValidatorField(ValidatorField):
    def validate(self, validator, field_name):       
        super().validate(validator, field_name)

        date = self.get_value()

        if not date:
            if self.required:
                self.validator.set_errors(self.field_name, f'{self.label} not informed.')

        else:
            try:
                if type(date).__name__ == 'date':
                    date = date

                elif type(date).__name__ == 'datetime':
                    date = date.date()

                else:
                    date = datetime.strptime(date, '%Y-%m-%d').date()

            except:
                self.validator.set_errors(self.field_name, f'{self.label} is in an invalid format.')

        return date


class DateTimeValidatorField(ValidatorField):
    def validate(self, validator, field_name):           
        super().validate(validator, field_name)

        date = self.get_value()

        if not date:
            if self.required:
                self.validator.set_errors(self.field_name, f'{self.label} not informed.')

        else:
            try:
                date = datetime.strptime(date, '%Y-%m-%dT%H:%M')

            except:
                self.validator.set_errors(self.field_name, f'{self.label} is in an invalid format.')

        return date


class ChoiceValidatorField(ValidatorField):
    choices = None

    def __init__(self, label, choices, required=True, field_name_extract=None):
        super().__init__(label, required, field_name_extract)

        self.choices = choices

    def validate(self, validator, field_name):
        super().validate(validator, field_name)

        choice = self.get_value()

        if not choice:
            if self.required:
                self.validator.set_errors(self.field_name, f'{self.label} not informed.')

        else:
            try:
                choice = int(choice)

                try:
                    choice = self.choices.__getitem__(choice - 1)[0]

                except:
                    self.validator.set_errors(self.field_name,f"{self.label} it's an invalid choice.")

            except:
                self.validator.set_errors(self.field_name, f'{self.label} is in an invalid format.')

        return choice


class CharValidatorField(ValidatorField):
    def validate(self, validator, field_name):
        super().validate(validator, field_name)

        value = self.get_value()

        if not value:
            if self.required:
                self.validator.set_errors(self.field_name, f'{self.label} not informed.')

        return value


class FileValidatorField(ValidatorField):
    format = None

    def __init__(self, label, format, required=True, field_name_extract=None):
        super().__init__(label, required, field_name_extract)

        self.format = format

    def validate(self, validator, field_name):
        super().validate(validator, field_name)

        attachment = self.get_value()

        if not attachment:
            if self.required:
                self.validator.set_errors(self.field_name, f'{self.label} not informed.')

        else:
            if not 'pdf' in attachment.content_type:
                self.validator.set_errors(self.field_name, f'{self.label} is in an invalid format.')

        return attachment
