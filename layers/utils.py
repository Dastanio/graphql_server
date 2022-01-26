from re import sub, search
import math
import uuid


# The function converts the string to camel case.
def camel_case(string):
    string = sub(r'([_\-])+', ' ', string).title().replace(' ', '')
    return string[0].lower() + string[1:]


# The function converts the string to snake case.
def snake_case(string):
    return sub(r'(?<!^)(?=[A-Z])', '_', string).lower()


def date_time_formatter(string):
    regex = "[0-9]{4}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|3[0-1]) (2[0-3]|[01][0-9]):[0-5][0-9]:[0-5][0-9].[0-9]{3}"
    formatted_date_time = search(regex, string).group()
    return formatted_date_time


def convert_int_to_string(number, alphabet, padding=None):
    """
    Convert a number to a string, using the given alphabet.
    The output has the most significant digit first.
    """
    output = ""
    alpha_length = len(alphabet)
    while number:
        number, digit = divmod(number, alpha_length)
        output += alphabet[digit]
    if padding:
        remainder = max(padding - len(output), 0)
        output = output + alphabet[0] * remainder
    return output[::-1]


def convert_string_to_int(string, alphabet):
    """
    Convert a string to a number, using the given alphabet.
    The input is assumed to have the most significant digit first.
    """
    number = 0
    alpha_length = len(alphabet)
    for char in string:
        number = number * alpha_length + alphabet.index(char)
    return number


class ShortUUID(object):
    def __init__(self):
        self._alphabet = list("123456789AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz")
        self._alpha_length = len(self._alphabet)

    @property
    def _length(self):
        """
        Return the necessary length to fit the entire UUID given the current alphabet.
        """
        return int(math.ceil(math.log(2 ** 128, self._alpha_length)))

    def encode(self, uuid_value, padding_length=None):
        """
        Encode a UUID into a string (LSB first) according to the alphabet
        If leftmost (MSB) bits are 0, the string might be shorter.
        """
        if padding_length is None:
            padding_length = self._length
        return convert_int_to_string(uuid_value.int, self._alphabet, padding=padding_length)

    def decode(self, string_value, legacy=False):
        """
        Decode a string according to the current alphabet into a UUID.
        Raises ValueError when encountering illegal characters or a too-long string.
        If string too short, fills leftmost (MSB) bits with 0.
        """
        if legacy:
            string_value = string_value[::-1]
        return uuid.UUID(int=convert_string_to_int(string_value, self._alphabet))
