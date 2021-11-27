from django.core import validators
from django.utils.deconstruct import deconstructible


@deconstructible
class PhoneNumberValidator(validators.RegexValidator):

    regex = r'^\d{10}'

    message = 'Enter a valid phone number.'

    flags = 0
