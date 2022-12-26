#!/usr/bin/env python

"""Tests for `domain_name_label_indexes` package."""

import pytest

from domain_name_label_indexes import count_domains_with_length, generate_domain_name_label, _DOMAIN_CHARS_WITH_HYPHEN, _DOMAIN_CHARS, compute_domain_length, first_index_with_domain_length, index_of_domain_name_label


def test_success():
    assert True

def test_single_char_domain():
    assertEqual(36, count_domains_with_length(1))

def test_double_char_domain():
    assertEqual(36*36, count_domains_with_length(2))

def test_triple_char_domain():
    assertEqual(36*37*36, count_domains_with_length(3))

def test_quadruple_char_domain():
    assertEqual(
        36 * # first character
        (
            36 * 36 + # BB
            36 *  1 + # B-
                1 * 36   # -B
        ) *
        36, # last character
        count_domains_with_length(4)
    )

def test_quintuple_char_domain():
    assertEqual(
        36 * # first character
        (
            36 * 36 * 36 + # BBB
            36 * 1 * 36  + # B-B
            1 * 36 * 36  + # -BB
            36 * 36 * 1  + # BB-
            1 * 36 * 1     # -B-
        ) *
        36,   # last character
        count_domains_with_length(5)
    )

def test_sextuple_char_domain():
    assertEqual(
        36 * # first character
        (
            36 * 36 * 36 * 36 + # BBBB

            1  * 36 * 36 * 36 + # -BBB
            36 *  1 * 36 * 36 + # B-BB
            36 * 36 *  1 * 36 + # BB-B
            36 * 36 * 36 *  1 + # BBB-

                1 * 36 *  1 * 36 + # -B-B
                1 * 36 * 36 *  1 + # -BB-
            36 *  1 * 36 *  1   # B-B-
        ) *
        36,   # last character
        count_domains_with_length(6)
    )

def test_septtuple_char_domain():
    assertEqual(
        36 * # first character
        (
            36 * 36 * 36 * 36 * 36 + # BBBBB

                1 * 36 * 36 * 36 * 36 + # -BBBB
            36 *  1 * 36 * 36 * 36 + # B-BBB
            36 * 36 *  1 * 36 * 36 + # BB-BB
            36 * 36 * 36 *  1 * 36 + # BBB-B
            36 * 36 * 36 * 36 *  1 + # BBBB-

                1 * 36 *  1 * 36 * 36 + # -B-BB
                1 * 36 * 36 *  1 * 36 + # -BB-B
                1 * 36 * 36 * 36 *  1 + # -BBB-

                36 * 1 * 36 *  1 * 36 + # B-B-B
                36 * 1 * 36 * 36 *  1 + # B-BB-

                36 * 36 * 1 * 36 *  1 + # BB-B-

                1 * 36 * 1 * 36 *  1   # -B-B-
        ) *
        36,   # last character
        count_domains_with_length(7)
    )

def test_lengths_specific_values():
    assertEqual(compute_domain_length(0), 1)
    assertEqual(compute_domain_length(1), 1)
    assertEqual(compute_domain_length(2), 1)
    assertEqual(compute_domain_length(35), 1)

    assertEqual(compute_domain_length(36), 2)
    assertEqual(compute_domain_length(37), 2)

    assertEqual(compute_domain_length(36**2+35), 2)
    assertEqual(compute_domain_length(36**2+36), 3)

    assertEqual(compute_domain_length(36*36*37+36**2+35), 3)
    assertEqual(compute_domain_length(36*36*37+36**2+36), 4)

def test_generation():
    assertEqual(generate_domain_name_label(0), "0")
    assertEqual(generate_domain_name_label(35), "z")
    assertEqual(generate_domain_name_label(36), "00")
    assertEqual(generate_domain_name_label(36**2 + 35), "zz")
    assertEqual(generate_domain_name_label(36**2 + 36), "0-0")
    assertEqual(generate_domain_name_label(36*37*36 + 36**2 + 35), "zzz")
    assertEqual(generate_domain_name_label(36*37*36 + 36**2 + 36), "0-00")
    assertEqual(generate_domain_name_label(36*37*36 + 36**2 + 36 + 36), "0-10")
    assertEqual(generate_domain_name_label(36*37*36 + 36**2 + 36 + 2*36), "0-20")
    assertEqual(generate_domain_name_label(36*37*36 + 36**2 + 36 + 35*36 + 35), "0-zz")
    assertEqual(generate_domain_name_label(36*37*36 + 36**2 + 36 + 36*36), "00-0")

    assertEqual(generate_domain_name_label(1870163), "0-zzz")
    assertEqual(generate_domain_name_label(1870164), "00-00")

def test_first_and_lasts():
    for i in range(3, 20):
        first_of_length = first_index_with_domain_length(i)
        # previous is all zzz
        print(i)
        assert generate_domain_name_label(first_of_length-1) == "z" * (i-1)

def test_huge_indexes():
    FIRST_50_CHAR_INDEX = 65427785365883453123247467896816512104667636251413310915715696907770774956868
    assert FIRST_50_CHAR_INDEX == first_index_with_domain_length(50)
    assert generate_domain_name_label(FIRST_50_CHAR_INDEX) == "0-" * 24 + "00"

    FIRST_63_CHAR_INDEX = 15789373303661443521599244438613998517958614539664139856248437529326757922995905152597652453206852
    assert FIRST_63_CHAR_INDEX == first_index_with_domain_length(63)
    assert generate_domain_name_label(FIRST_63_CHAR_INDEX) == "0-" * 31 + "0"

    LAST_63_CHAR_INDEX = 583791014263271482476326569507663027313555716330347307932966791104859150313363146960655804883807043
    # this one intentionally fails as 64 is an invalid label length
    #assert LAST_63_CHAR_INDEX == first_index_with_domain_length(64)-1
    assert generate_domain_name_label(LAST_63_CHAR_INDEX) == "z" * 63

def test_first_index():
    assertEqual(first_index_with_domain_length(1), 0)
    assertEqual(first_index_with_domain_length(2), 36)
    assertEqual(first_index_with_domain_length(3), 36 + 36**2)
    assertEqual(first_index_with_domain_length(4), 36 + 36**2 + 36*37*36)

# This test takes a long time with large numbers
BRUTE_TEST_STOP_AT = 1_000
def test_matches_brute():
    index = 0
    previous = ""
    for expected in gen_brute():
        actual = generate_domain_name_label(index)
        assertEqual(actual, expected)
        if len(previous) == len(actual):
            # assert domains are orders
            assertLess(previous, actual)
        else:
            # assort domain length never shrinks
            assertLess(len(previous), len(actual))
        previous = actual
        index += 1
        # stop after covering a sufficient amount
        if index > BRUTE_TEST_STOP_AT:
            break

def gen_brute_r(length: int):
    if length == 1:
        for c in _DOMAIN_CHARS:
            yield c
    else:
        for prefix in _DOMAIN_CHARS_WITH_HYPHEN:
            for lower in gen_brute_r(length - 1):
                item = prefix + lower
                if '--' in item:
                    continue
                yield item

def gen_brute():
    length = 1
    while True:
        for item in gen_brute_r(length):
            if item[0] == '-' or item[-1] == '-':
                continue
            elif '--' in item:
                continue
            else:
                yield item
        length += 1

def test_reverse():
    assert 0 == index_of_domain_name_label("0")
    assert 35 == index_of_domain_name_label("z")
    assert 36 == index_of_domain_name_label("00")
    assert 36*36+35 == index_of_domain_name_label("zz")
    assert 36*36+36 == index_of_domain_name_label("0-0")
    assert 36*36+37 == index_of_domain_name_label("0-1")
    assert 36*37*36+36*36+35 == index_of_domain_name_label("zzz")

    YAHOO_INDEX = 64297428
    assert YAHOO_INDEX == index_of_domain_name_label("yahoo")
    assert "yahoo" == generate_domain_name_label(YAHOO_INDEX)

    GOOGLE_INDEX = 1191294986
    assert GOOGLE_INDEX == index_of_domain_name_label("google")
    assert "google" == generate_domain_name_label(GOOGLE_INDEX)

def assertEqual(a, b):
    assert a == b

def assertLess(a, b):
    assert a < b

def test_docs_examples():
    assert generate_domain_name_label(0)  == "0"
    assert generate_domain_name_label(1)  == "1"
    assert generate_domain_name_label(10) == "a"
    assert generate_domain_name_label(35) == "z"
    assert generate_domain_name_label(36) == "00"
    assert generate_domain_name_label(37) == "01"
    assert generate_domain_name_label(72) == "10"
    assert generate_domain_name_label(1331) == "zz"
    assert generate_domain_name_label(1332) == "0-0"

    assert compute_domain_length(0) == 1
    assert compute_domain_length(36) == 2

    assert first_index_with_domain_length(1) == 0
    assert first_index_with_domain_length(2) == 36

    assert count_domains_with_length(1) ==  36
    assert count_domains_with_length(2) == 1296

