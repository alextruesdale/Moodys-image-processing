"""Module containing test functions for Reference Notes zones."""

from re import finditer
import numpy as np
import pandas as pd
import re

def caps_ratio(value):
    """Define ratio of capital characters."""

    cap_count = 0
    for char in value.replace(' ', ''):
        if char.isupper():
            cap_count += 1

    caps_ratio = cap_count / len(value.replace(' ', ''))
    return caps_ratio

def test_caps_reference(value):
    """Search zone content for 'REFERENCE NOTE(S)' string."""

    test_string = r'.*.{1,2}[CcOo0Ee\d][Ff].{2,4}[Nn][Cc].{1,2}\s+[NnMn][CcOo0Ee\d\s][Tt].{1,3}\s.*'
    print_test = r'.{1,2}[CcOo0Ee\d][Ff].{2,4}[Nn][Cc].{1,2}\s+[NnMn][CcOo0Ee\d\s][Tt].{1,3}\s'

    if re.match(test_string, value):
        value_out = 0

        for match in finditer(print_test, value):
            if caps_ratio(match.group()) > .15:
                value_out = 1
    else:
        value_out = 0

    return value_out

def on_stocks(value):
    """Determine if reference note is for Stocks."""

    test_string = r'.*.{1,2}[CcOo0Ee\d][Ff].{2,4}[Nn][Cc].{1,2}\s+[NnMn][CcOo0Ee\d\s][Tt].{1,3}\s.*'
    print_test = r'.{1,2}[CcOo0Ee\d][Ff].{2,4}[Nn][Cc].{1,2}\s+[NnMn][CcOo0Ee\d\s][Tt].{1,3}\s'

    on_stocks_test = r'.*[CcOo0Ee\d][Nn].{0,2}\s+.[Tt].{1,2}[CcOo0Ee\d][Kk].{0,2}\s+.*'
    on_stocks_print = r'[CcOo0Ee\d][Nn].{0,2}\s+.[Tt].{1,2}[CcOo0Ee\d][Kk].{0,2}\s+'

    on_stocks_list = []
    if re.match(test_string, value):
        value_out = 0

        for match in finditer(print_test, value):
            if caps_ratio(match.group()) > .15:
                substring = value[match.span()[0]:match.span()[0]+50]
                if re.match(on_stocks_test, substring):
                    for match in finditer(on_stocks_print, substring):
                        if caps_ratio(match.group()) > .15:
                            on_stocks_list.append(True)

    if any(on_stocks_list):
        value_out = 1

    else:
        value_out = 0

    return value_out

def on_bonds(value):
    """Determine if reference note is for Bonds."""

    test_string = r'.*.{1,2}[CcOo0Ee\d][Ff].{2,4}[Nn][Cc].{1,2}\s+[NnMn][CcOo0Ee\d\s][Tt].{1,3}\s.*'
    print_test = r'.{1,2}[CcOo0Ee\d][Ff].{2,4}[Nn][Cc].{1,2}\s+[NnMn][CcOo0Ee\d\s][Tt].{1,3}\s'

    on_bonds_test = r'.*[CcOo0Ee\d][Nn].{0,2}\s+.[CcOo0Ee\d].{1,2}[Dd].{0,2}\s+.*'
    on_bonds_print = r'[CcOo0Ee\d][Nn].{0,2}\s+.[CcOo0Ee\d].{1,2}[Dd].{0,2}\s+'

    on_bonds_list = []
    if re.match(test_string, value):
        value_out = 0

        for match in finditer(print_test, value):
            if caps_ratio(match.group()) > .15:
                substring = value[match.span()[0]:match.span()[0]+50]
                if re.match(on_bonds_test, substring):
                    for match in finditer(on_bonds_print, substring):
                        if caps_ratio(match.group()) > .15:
                            on_bonds_list.append(True)

    if any(on_bonds_list):
        value_out = 1

    else:
        value_out = 0

    return value_out
