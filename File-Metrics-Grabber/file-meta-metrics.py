"""
    Filename:
        file-meta-metrics.py

    Description:
        Will grab the specified data we need from TRLA's CSV exports in order to assist with the migration of their data to SharePoint.
    
    Author:
        Jonathan Jang
    
    Company:
        Longi Engineering
"""

import os, re, csv, time, math
from traceback import print_tb
import pandas as pd


def get_meta_data(param1, param2):
    """
        Grabbing the number of files/rows and other metrics that we need for metrics to check
    
    :param param1:
    :return:
    """
    # doc index export.csv
    df_doc_index_export = pd.read_csv(param1).fillna('NONE-NAN')
    # Getting the numbers
    df_caseid_doc_ie_col = df_doc_index_export['Immigration_List_caseid_'].unique()
    df_di_folder = df_doc_index_export['DI_INDEX_di_folder_'].unique()
    print(f"{df_doc_index_export.shape[0]}\t== Total Number of items - doc index export.csv")
    print(f"{df_caseid_doc_ie_col.shape[0]}\t: Unique from col - caseid")
    # print(f"{len(df_caseid_doc_ie_col)}\t: Unique from col - caseid")
    print(f"{df_di_folder.shape[0]}\t: Unique count of files from doc index export.csv\n")
    # # To CSV
    # dict_di_file = {'caseid': df_caseid_doc_ie_col}
    # tmp_df = pd.DataFrame(dict_di_file)
    # tmp_df.to_csv('\\\\ledc2017\\itsupport\\TRLA\\CTS Exports\\unique-caseid-doc_index_export_csv.csv')

    # Docket.csv
    df_docket = pd.read_csv(param2).fillna('NONE-NAN')
    # Getting the numbers
    df_caseid_col = df_docket['caseid'].unique()
    df_doc_filena = df_docket['doc_filena'].unique()
    print(f"{df_docket.shape[0]}\t== Total Number of items - Docket.csv")
    print(f"{df_caseid_col.shape[0]}\t: Unique from col - caseid")
    print(f"{df_doc_filena.shape[0]}\t: Unique count of files from Docket.csv\n\n")
    # # TO CSV
    # dict_caseid = {'caseid': df_caseid_col}
    # tmp_df = pd.DataFrame(dict_caseid)
    # tmp_df.to_csv('\\\\ledc2017\\itsupport\\TRLA\\CTS Exports\\unique-caseid-Docket_csv.csv')

    # Sum - Totals
    sum_total_col = df_doc_index_export.shape[0] + df_docket.shape[0]
    # sum_total_unique_id = df_caseid_doc_ie_col.shape[0] + df_caseid_col.shape[0]
    sum_total_unique_files = df_di_folder.shape[0] + df_doc_filena.shape[0]
    print(f"{sum_total_col}\t== Total Number of files from BOTH CSV")
    # print(f"{sum_total_unique_id}\t: Total Number of unique count from caseid cols")
    print(f"{sum_total_unique_files}\t: Total Number of unique files from BOTH CSV\n")
    ## Getting new unique list
    # temp-unique-case-id-unfiltered.csv
    temp_fp = '\\\\ledc2017\\itsupport\\TRLA\\CTS Exports\\temp-unique-case-id-unfiltered.csv'
    df_docket = pd.read_csv(temp_fp).fillna('NONE-NAN')
    # Getting the numbers
    df_all_unique_caseid = df_docket['caseid'].unique()
    total_unique_id = df_all_unique_caseid.shape[0]
    print(f"{total_unique_id}\t: Total Number of unique count from caseid cols\n\n")
    # TO CSV
    dict_caseid = {'all unique caseid': df_all_unique_caseid}
    tmp_df = pd.DataFrame(dict_caseid)
    tmp_df.to_csv('\\\\ledc2017\\itsupport\\TRLA\\CTS Exports\\all-unique-caseid.csv')



def main():
    """
        Main function of the python project
    """
    csv_f_1 = '\\\\ledc2017\\itsupport\\TRLA\\CTS Exports\\docs index export.csv'
    csv_f_2 = '\\\\ledc2017\\itsupport\\TRLA\\CTS Exports\\Docket.csv'
    get_meta_data(csv_f_1, csv_f_2)


if __name__ == "__main__":
    main()
