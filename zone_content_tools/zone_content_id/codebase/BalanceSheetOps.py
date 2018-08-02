"""Module containing test functions for Balance Sheet zones."""

from re import finditer
import numpy as np
import pandas as pd
import re

def test_caps_balance_sheet(value):
    """Search zone content for 'BALANCE SHEET' string."""

    def caps_ratio(value):
        """Define ratio of capital characters."""

        cap_count = 0
        for char in value.replace(' ', ''):
            if char.isupper():
                cap_count += 1

        caps_ratio = cap_count / len(value.replace(' ', ''))
        return caps_ratio

    test_string = r'.*[Aa][LlIi\d].[NnMm].{1,4}[Ss.].{1,2}[CcOoEe0]{2}[TtFfl].*'
    print_test = r'.[Aa][LlIi\d].[NnMm].{1,4}[Ss.].{1,2}[CcOoEe0]{2}[TtFfl]'

    if re.match(test_string, value):
        value_out = 0

        for match in finditer(print_test, value):
            if caps_ratio(match.group()) > .2:
                # print(match.span(), match.group())
                value_out = 1
    else:
        value_out = 0

    return value_out

def test_balance_sheet(value):
    """Search zone content for 'Balance Sheet' string."""

    test_string_account = r'.*a[li\d].[nm].{1,4}[Ss.].{1,2}[coe0]{2}[tfl].*'
    print_test_account = r'.a[li\d].[nm].{1,4}[Ss.].{1,2}[coe0]{2}[tfl]'

    if re.match(test_string_account, value):
        value_out = 0

        test_string_as_of = r'.*\s[Aa][Ss]\s.{0,2}[Oo][Ff]\s.*'
        test_string_assets = r'.*[Aa].{1,9}[Ss]\s*[\:\;]\s.*'
        test_string_liabilities = r'.*[LlIi]{1,2}[Aa][Bb].{1,7}[Ss][\:\;]\s.*'

        print_test_as_of = r'\s[Aa][Ss]\s.{0,2}[Oo][Ff]\s'
        print_test_assets = r'[Aa].{1,9}[Ss]\s*[\:\;]\s'
        print_test_liabilities = r'[LlIi]{1,2}[Aa][Bb].{1,7}[Ss][\:\;]\s'

        if (re.match(test_string_as_of, value) or re.match(test_string_assets, value) or
            re.match(test_string_liabilities, value)):

            match_beginning_as_of = []
            match_beginning_assets = []
            match_beginning_liabilities = []

            for match in finditer(print_test_account, value):
                match_beginning = match.span()[0]
                match_end = match.span()[-1]

            for match in finditer(print_test_as_of, value):
                match_beginning_as_of.append(match.span()[0])

            for match in finditer(print_test_assets, value):
                match_beginning_assets.append(match.span()[0])

            for match in finditer(print_test_liabilities, value):
                match_beginning_liabilities.append(match.span()[0])

            distance_list_as_of = [True for match in match_beginning_as_of if abs(match_end - match) < 20]
            distance_list_assets = [True for match in match_beginning_assets if abs(match_end - match) < 65]
            distance_list_liabilities = [True for match in match_beginning_liabilities if abs(match_end - match) < 110]

            if any(distance_list_as_of) or any(distance_list_assets) or any(distance_list_liabilities):
                value_out = 1

    else:
        value_out = 0

    return value_out

def trailing_number_content(row):
    """Search current or next zone string for high-density of numbers (indicating table)."""

    value_out = 0
    current_zone = str(row['text'])
    zone_next = str(row['zone_next'])

    def digit_ratio(test_string):
        """Define ratio of capital characters."""

        digit_count = 0
        for char in test_string.replace(' ', ''):
            if char.isdigit():
                digit_count += 1

        digit_ratio = digit_count / len(test_string.replace(' ', ''))
        return digit_ratio

    def count_dollars(test_string):
        """Define ratio of capital characters."""

        dollar_count = 0
        for char in test_string.replace(' ', ''):
            if char == '$' or char == '£':
                dollar_count += 1

        return dollar_count

    test_string = r'.*[Aa][LlIi\d].[NnMm].{1,4}[Ss.].{1,2}[CcOoEe0]{2}[TtFfl].*'
    print_test = r'.[Aa][LlIi\d].[NnMm].{1,4}[Ss.].{1,2}[CcOoEe0]{2}[TtFfl]'

    if re.match(test_string, current_zone):
        for match in finditer(print_test, current_zone):
            # print(match.span(), match.group())
            # print(row.name)
            match_beginning = match.span()[0]
            len_to_end = len(current_zone) - match_beginning
            if len_to_end < 550:
                overflow = 550 - len_to_end
                test_string = current_zone[match_beginning:] + zone_next[:overflow]
            else:
                test_string = current_zone[match_beginning:match_beginning + 550]

            test_string_digit_ratio = digit_ratio(test_string)
            test_string_dollar_count = count_dollars(test_string)

            if test_string_digit_ratio > .1:
                value_out = 1

    return value_out

def test_trailing_colon(value):
    """ID trailing colons and semi-colons"""

    test_string = r'.*[Aa][LlIi\d].[NnMm].{1,4}[Ss.].{1,2}[CcOoEe0]{2}[TtFfl]\s*[\;\:].*'
    if re.match(test_string, str(value)):
        value_out = 1
    else:
        value_out = 0

    return value_out
