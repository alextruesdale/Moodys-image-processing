"""Module containing test functions for Income Account/Statement zones."""

from re import finditer
import numpy as np
import pandas as pd
import re

def test_caps_income_account(value):
    """Search zone content for 'INCOME ACCOUNT' string."""

    def caps_ratio(value):
        """Define ratio of capital characters."""

        cap_count = 0
        for char in value.replace(' ', ''):
            if char.isupper():
                cap_count += 1

        caps_ratio = cap_count / len(value.replace(' ', ''))
        return caps_ratio

    test_string = r'.*[Iil][Nnm][CcOo0Ee]{2}.{1,4}[Aa][CcOoEe0]{3}[Uu].*'
    print_test = r'[Iil][Nnm][CcOo0Ee]{2}.{1,4}[Aa][CcOoEe0]{3}[Uu].{1,3}'

    if re.match(test_string, value):
        value_out = 0

        for match in finditer(print_test, value):
            if caps_ratio(match.group()) > .2:
                # print(match.span(), match.group())
                value_out = 1
    else:
        value_out = 0

    return value_out

def test_income_account(value):
    """Search zone content for 'Income Account' string."""

    test_string_account = r'.*[Iil][nm][coe0]{2}.{1,4}[Aa][coe0]{3}[u].*'
    print_test_account = r'[Iil][nm][coe0]{2}.{1,4}[Aa][coe0]{3}[u].{1,3}'

    if re.match(test_string_account, value):
        value_out = 0

        test_string_year = r'.*[Yy][er][as].{1,10}[Eet][no]d*.*'
        test_string_month = r'.*[Mm][o][n\.].{1,9}[\s][Eet][no]d*.*'
        test_string_period = r'.*[Pp][eo]ri.{1,30}[Eet]*[no]*d*.*'
        test_string_to = r'.*\d{3,4}.{1,3}to.*'

        print_test_year = r'[Yy][er][as].{1,10}[Eet\&][no]d*'
        print_test_month = r'[Mm][o][n\.].{1,9}[\s][Eet\&][no]d*'
        print_test_period = r'[Pp][eo]ri.{1,30}[Eet\&]*[no]*d*'
        print_test_to = r'\d{3,4}.{1,3}to'

        if (re.match(test_string_year, value) or re.match(test_string_month, value) or
            re.match(test_string_period, value) or re.match(test_string_to, value)):

            match_beginning_year = []
            match_beginning_month = []
            match_beginning_period = []
            match_beginning_to = []

            for match in finditer(print_test_account, value):
                # print(match.span(), match.group())
                match_beginning = match.span()[0]
                match_end = match.span()[-1]

            for match in finditer(print_test_year, value):
                # print(match.span(), match.group())
                match_beginning_year.append(match.span()[0])

            for match in finditer(print_test_month, value):
                match_beginning_month.append(match.span()[0])

            for match in finditer(print_test_period, value):
                match_beginning_period.append(match.span()[0])

            for match in finditer(print_test_to, value):
                match_beginning_to.append(match.span()[0])

            sub_match_list = match_beginning_year + match_beginning_month + match_beginning_period + match_beginning_to
            distance_list = [True for match in sub_match_list if abs(match_end - match) < 45]
            if any(distance_list):
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

    test_string = r'.*[Iil][Nnm][CcOo0Ee]{2}.{1,4}[Aa][CcOoEe0]{3}[Uu].*'
    print_test = r'[Iil][Nnm][CcOo0Ee]{2}.{1,4}[Aa][CcOoEe0]{3}[Uu].{1,3}'

    if re.match(test_string, current_zone):
        for match in finditer(print_test, current_zone):
            # print(match.span(), match.group())
            # print(row.name)
            match_beginning = match.span()[0]
            len_to_end = len(current_zone) - match_beginning
            if len_to_end < 350:
                overflow = 350 - len_to_end
                test_string = current_zone[match_beginning:] + zone_next[:overflow]
            else:
                test_string = current_zone[match_beginning:match_beginning + 350]

            test_string_digit_ratio = digit_ratio(test_string)
            test_string_dollar_count = count_dollars(test_string)

            if test_string_digit_ratio > .15 and test_string_dollar_count > 3:
                value_out = 1

    return value_out

def test_trailing_colon(value):
    """ID trailing colons and semi-colons"""

    test_string = r'.*[Iil][Nnm][CcOo0Ee]{2}.{1,4}[Aa][CcOoEe0]{3}[Uu].{1,3}\s*[\;\:].*'
    if re.match(test_string, str(value)):
        value_out = 1
    else:
        value_out = 0

    return value_out
