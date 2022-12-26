import string
import functools

__author__ = """Robert Alexander"""
__email__ = 'raalexander.phi@gmail.com'
__version__ = '0.1.0'


_MAX_LABEL_LENGTH = 63
_DOMAIN_CHARS = string.digits + string.ascii_lowercase
_DOMAIN_BASE = len(_DOMAIN_CHARS)
_DOMAIN_CHARS_WITH_HYPHEN = '-' + _DOMAIN_CHARS

def count_domains_with_length(length: int) -> int:
    if length <= 0 or length > 63:
        raise Exception("Invalid unput")
    if length < 3:
        return _DOMAIN_BASE**length
    return _DOMAIN_BASE**2 * _count_domains_with_length_r(length-2)

# recursive helper
@functools.cache
def _count_domains_with_length_r(length: int) -> int:
    if length == 1:
        return (
            _DOMAIN_BASE + # any base character
            1              # or a hyphen
        )
    if length == 2:
        return (
            _DOMAIN_BASE * _DOMAIN_BASE + # base base
            _DOMAIN_BASE * 1            + # base hyphen
            1 * _DOMAIN_BASE              # hyphen base
        )

    return (
        _DOMAIN_BASE * _count_domains_with_length_r(length-1) +   # base (any n-1 sequence)
        1 * _DOMAIN_BASE * _count_domains_with_length_r(length-2) # hyphen base (any n-2 sequence)
    )

@functools.cache
def first_index_with_domain_length(length: int) -> int:
    if length > _MAX_LABEL_LENGTH or length < 1:
        raise Exception(f"Supported domain name labels are between 1 and 63 characters long, requested {length}")
    sum = 0
    for i in range(1, length):
        sum += count_domains_with_length(i)
    return sum

def compute_domain_length(index: int) -> int:
    for n in range(1, _MAX_LABEL_LENGTH + 1):
        domains_of_length_n = count_domains_with_length(n)
        if index >= domains_of_length_n:
            index -= domains_of_length_n
        else:
            return n
    else:
        raise Exception("DNS wire format does not support domains longer than 63 characters")

def generate_domain_name_label(index: int):
    len_remaining = compute_domain_length(index)
    return _generate_domain_name_label_r(index, len_remaining, True)

def _generate_domain_name_label_r(index: int, len_remaining: int, is_first: bool) -> str:
    if len_remaining == 1:
        return _DOMAIN_CHARS[index]
    elif len_remaining == 2:
        last_char = _DOMAIN_CHARS[index % _DOMAIN_BASE]
        index = index // _DOMAIN_BASE
        if is_first:
            index -= 1  # trim an extra, we'll avoid padding leading zeros on earlier numbers
        first_char = _DOMAIN_CHARS[index]
        return first_char + last_char
    else:
        # Process from the next most significant character
        first_char, index = _trim_most_significant_as_alphanumeric(index, len_remaining, is_first)

        # from here, we can either have a hypen followed by any valid domain of len-2
        # or any valid domain of len-1
        # let's check if this should have a hyphen first, as it's the smallest character

        domain_suffixes_with_hyphen = count_domains_with_length(len_remaining-2)
        has_hyphen_next = index < domain_suffixes_with_hyphen

        if has_hyphen_next:
            # we have a zero value in the highest character, this maps to hyphen
            return first_char + "-" + _generate_domain_name_label_r(index, len_remaining - 2, False)
        else:
            # the next char needs to be an alphanumeric, so the remaining is a valid domain
            # divide off extra as we already covered some with the leading hyphen
            index -= domain_suffixes_with_hyphen
            return first_char + _generate_domain_name_label_r(index, len_remaining - 1, False)

def _trim_most_significant_as_alphanumeric(index: int, len_remaining: int, is_first: bool):
    if is_first:
        # we need to reduce this as the first domain of a given length
        # comes after fall the domains of shorter lengths
        index = index - first_index_with_domain_length(len_remaining)

    # the divisor is the increment between 0zzz and 1zzz
    increment_divisor = count_domains_with_length(len_remaining) // _DOMAIN_BASE

    first_char_index = index // increment_divisor
    assert first_char_index >= 0 and first_char_index < _DOMAIN_BASE
    first_char = _DOMAIN_CHARS[first_char_index]

    remainder = index % increment_divisor
    return first_char, remainder

