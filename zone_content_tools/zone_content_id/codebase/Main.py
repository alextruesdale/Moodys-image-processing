"""Top-level project Main Module."""

from IncomeAccountOverhead import income_account_overhead
from BalanceSheetOverhead import balance_sheet_overhead
from StockBondOverhead import stock_bond_overhead
from ReferenceOverhead import reference_overhead
import ZoneNeutralOps as zno

import sys
sys.path.append('../../../runtime_data/')
import RunTimeData

def main():
    """Top-level project Main function."""

    # trigger console printing function and define variables for mid-runtime print statements.
    starting_data = RunTimeData.starting_print_statement()
    start_time = starting_data[0]
    time_elapsed = starting_data[1]

    # read in ZoneClassifications files.
    zones_full = '../from_summit/ZoneClassifications.csv'
    zones_small = '../from_summit/ZoneClassifications_Smaller.csv'

    # trigger file_operations classes to search zones in zone files for identifying strings.
    zone_data_account = income_account_overhead(zones_full, zones_small)
    zone_data_balance = balance_sheet_overhead(zones_full, zones_small)
    zone_data_stock_bond = stock_bond_overhead(zones_full, zones_small)
    zone_data_reference = reference_overhead(zones_full, zones_small)

    # prepare output dataframes from above classes as part of original zoning file and save.
    zno.update_and_output(zones_small, zone_data_account.output_dataframe,
                          zone_data_balance.output_dataframe,
                          zone_data_stock_bond.output_dataframe,
                          zone_data_reference.output_dataframe)

    # print concluding job console statement with summarising data.
    RunTimeData.concluding_print_statement(start_time, time_elapsed)

if __name__ == '__main__':
    main()
