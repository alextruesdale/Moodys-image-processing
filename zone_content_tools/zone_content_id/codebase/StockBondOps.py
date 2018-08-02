"""Module containing test functions for Stock / Bond Table zones."""

from re import finditer
import numpy as np
import pandas as pd
import re

def test_stock_records(value):
    """Search zone content for 'Stock Records' string."""

    test_string_stock = r'.*[Tt][OoCcEe\d]{2}k\s+[Rr].{1,4}[OoCcEe\d].[DdOo].*'
    print_test_stock = r'.[Tt][OoCcEe\d]{2}k\s+[Rr].{1,4}[OoCcEe\d].[DdOo].'

    if re.match(test_string_stock, value):
        value_out = 0

        test_string_table = r'.*able\s[Bb].*'
        test_string_based = r'.*[Bb].{1,2}[Ee][Dd]\son\s.*'
        test_string_ratings = r'.*[Aa].{1,2}\s[Rr].[TtIiLl]{2}.{1,2}g.*'
        test_string_caps = r'.*(BASIS|RATINGS).*'

        print_string_table = r'able\s[Bb]'
        print_string_based = r'[Bb].{1,2}[Ee][Dd]\son\s'
        print_string_ratings = r'[Aa].{1,2}\s[Rr].[TtIiLl]{2}.{1,2}g'
        print_string_caps = r'(BASIS|RATING)'

        for match in finditer(print_test_stock, value):
            substring = value[match.span()[0]:match.span()[0]+120]

        th00 = r'.*\sRate\s+of\s.*'
        th01 = r'.*\sAuth.{2}i.{2}d\s.*'
        th02 = r'.*\sO.{2}st.{2}d.{2}g\s.*'
        th03 = r'.*\sAve.{2}g.\s.*'
        th04 = r'.*\sRat.{2}g\s.*'
        th05 = r'.*\sMe.{1,3}\s.*'
        th06 = r'.*\sReq.{2}re.*\s.*'
        th07 = r'.*\sS.l.b.{1,3}ty\s.*'
        th08 = r'.*\sInc.{2}e\s.*'
        th09 = r'.*\sDiv.{2}end\s.*'

        table_header_list = [th00, th01, th02, th03, th04, th05, th06, th07, th08, th09]
        table_header_count = sum(1 for th in table_header_list if re.match(th, substring))

        if (re.match(test_string_table, value) or re.match(test_string_based, value) or
            re.match(test_string_ratings, value) or re.match(print_string_caps, value)):

            match_beginning_table = []
            match_beginning_based = []
            match_beginning_ratings = []
            match_beginning_caps = []

            for match in finditer(print_test_stock, value):
                # print(match.span(), match.group())
                match_beginning = match.span()[0]
                match_end = match.span()[-1]

            for match in finditer(print_string_table, value):
                # print(match.span(), match.group())
                match_beginning_table.append(match.span()[0])

            for match in finditer(print_string_based, value):
                # print(match.span(), match.group())
                match_beginning_based.append(match.span()[0])

            for match in finditer(print_string_ratings, value):
                # print(match.span(), match.group())
                match_beginning_ratings.append(match.span()[0])

            for match in finditer(print_string_caps, value):
                # print(match.span(), match.group())
                match_beginning_caps.append(match.span()[0])

            distance_list_table = [True for match in match_beginning_table if abs(match_end - match) < 25]
            distance_list_based = [True for match in match_beginning_based if abs(match_end - match) < 35]
            distance_list_ratings = [True for match in match_beginning_ratings if abs(match_end - match) < 25]
            distance_list_caps = [True for match in match_beginning_caps if abs(match_end - match) < 120]

            if (any(distance_list_table) or any(distance_list_based) or any(distance_list_ratings) or
                any(distance_list_caps) or table_header_count >= 2):

                value_out = 1

    else:
        value_out = 0

    return value_out

def test_bond_records(value):
    """Search zone content for 'Bond Records' string."""

    test_string_bond = r'.*[^d][OoCcEe\d][MmNn][Dd]\s+[Rr].{1,4}[OoCcEe\d].[DdOo].*'
    print_test_bond = r'[^d][OoCcEe\d][MmNn][Dd]\s+[Rr].{1,4}[OoCcEe\d].[DdOo].'

    if re.match(test_string_bond, value):
        value_out = 0

        test_string_table = r'.*able\s[Aa].*'
        test_string_based = r'.*[Bb].{1,2}[Ee][Dd]\son\s.*'
        test_string_ratings = r'.*[Aa].{1,2}\s[Rr].[TtIiLl]{2}.{1,2}g.*'
        test_string_caps = r'.*(BASIS|RATINGS).*'

        print_string_table = r'able\s[Bb]'
        print_string_based = r'[Bb].{1,2}[Ee][Dd]\son\s'
        print_string_ratings = r'[Aa].{1,2}\s[Rr].[TtIiLl]{2}.{1,2}g'
        print_string_caps = r'(BASIS|RATING)'

        for match in finditer(print_test_bond, value):
            substring = value[match.span()[0]:match.span()[0]+140]

        th00 = r'.*\sPa\w{1,2}\W{0,2}\s.*'
        th01 = r'.*\sMa.{2}r.ty\s.*'
        th02 = r'.*\sAuth.{2}i.{2}d\s.*'
        th03 = r'.*\sO.{2}st.{2}d.{2}g\s.*'
        th04 = r'.*\sAve.{2}g.\s.*'
        th05 = r'.*\sRat.{2}g\s.*'
        th06 = r'.*\sAble\s.*'
        th07 = r'.*\sReq.{2}re.*\s.*'
        th08 = r'.*\sS.l.b.{1,3}ty\s.*'
        th09 = r'.*\sInc.{2}e\s.*'
        th10 = r'.*\sSe.{2}r.{2}y\s.*'
        th11 = r'.*\sS.f.{2}y\s.*'
        th12 = r'.*\sPer\s+Annum\s.*'
        th13 = r'.*\sF.ct.r\s.*'

        table_header_list = [th00, th01, th02, th03, th04, th05, th06, th07,
                             th08, th09, th10, th11, th12, th13]

        table_header_count = sum(1 for th in table_header_list if re.match(th, substring))

        if (re.match(test_string_table, value) or re.match(test_string_based, value) or
            re.match(test_string_ratings, value) or re.match(print_string_caps, value)):

            match_beginning_table = []
            match_beginning_based = []
            match_beginning_ratings = []
            match_beginning_caps = []

            for match in finditer(print_test_bond, value):
                # print(match.span(), match.group())
                match_beginning = match.span()[0]
                match_end = match.span()[-1]

            for match in finditer(print_string_table, value):
                # print(match.span(), match.group())
                match_beginning_table.append(match.span()[0])

            for match in finditer(print_string_based, value):
                # print(match.span(), match.group())
                match_beginning_based.append(match.span()[0])

            for match in finditer(print_string_ratings, value):
                # print(match.span(), match.group())
                match_beginning_ratings.append(match.span()[0])

            for match in finditer(print_string_caps, value):
                # print(match.span(), match.group())
                match_beginning_caps.append(match.span()[0])

            distance_list_table = [True for match in match_beginning_table if abs(match_end - match) < 25]
            distance_list_based = [True for match in match_beginning_based if abs(match_end - match) < 35]
            distance_list_ratings = [True for match in match_beginning_ratings if abs(match_end - match) < 25]
            distance_list_caps = [True for match in match_beginning_caps if abs(match_end - match) < 120]

            if (any(distance_list_table) or any(distance_list_based) or any(distance_list_ratings) or
                any(distance_list_caps) or table_header_count >= 2):

                value_out = 1

    else:
        value_out = 0

    return value_out
