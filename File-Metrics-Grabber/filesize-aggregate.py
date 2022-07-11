"""
    Filename:
        filesize-aggregate.py

    Description:
        This program will open a csv file containing a column of data that consists of full file paths that will grab the filesize of each of those files and then calculate the sum of all the files in filepath column of the csv.
    
    Author:
        Jonathan Jang
    
    Company:
        Longi Engineering
"""

import os
import re
import csv
import shutil
import sys
import time
import math
import pandas as pd
from datetime import datetime


def get_filelocs(dir_path):
    """
        Getting the filesize of the file that gets fed in via the arguments of the functions
    
    :param dir_path: str
        Path of the directory/folder that we want to get the list of files with a full absolute path of
    :return:
    """
    list_of_files = os.listdir(dir_path)
    # print(list_of_files)
    re_list = []
    for file in list_of_files:
        full_path = os.path.join(dir_path, file)
        re_list.append(full_path)
        # print(full_path)
    print(f"{re_list}\n\n\n")
    return re_list


def get_filesize(filepath_loc):
    """
        Getting the filesize of the file that gets fed in via the arguments of the functions
    
    :param filepath_loc:
    :return:
    """
    # return os.path.getsize(filepath_loc)
    return os.stat(filepath_loc).st_size
    

def get_filepaths(csv_f, df_col):
    """
        Getting the dataframe set that has the entire list of all filepaths to traverese
    
    :param csv_f: str
        string of the csv file that we are using to feed in the data
    :param df_col: str
        string of the col name from the csv file that we are reading in with pandas
    :return:
    """
    # Need to change to read_csv for when using for prod; using read_excel for testing purposes
    # df = pd.read_excel(csv_f)['doc_filena']
    df = pd.read_csv(csv_f)[df_col].fillna(0)
    
    aggregate_filesize = 0
    for index, row in df.iteritems():
        if row != 0:
            try:
                aggregate_filesize += get_filesize(row)
                print(f"{row}\t{get_filesize(row)}")
            except FileNotFoundError:
                print(f"{row}\tfile was not found...skipping")
        else:
            print(f"{row}\tcell was blank - filesize: 0")
    print(f"aggregate filesize: {aggregate_filesize} bytes")
    print(convert_size(aggregate_filesize))


def convert_size(size_bytes):
    """
        Will convert the size of the bytes to either KB, MB, GB, etc
    
    :param size_bytes: int / big int
        The size in bytes that we want to convert
    """
    # Test 2
    # tags = [ "Byte", "Kilobyte", "Megabyte", "Gigabyte", "Terabyte" ]
    # i = 0
    # double_bytes = size_bytes
    # while (i < len(tags) and  size_bytes >= 1024):
    #     double_bytes = size_bytes / 1024.0
    #     i = i + 1
    #     size_bytes = size_bytes / 1024
    # return str(round(double_bytes, 2)) + " " + tags[i]
    # Test 1
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i])


def file_aggregate(csv_f, out_f, df_col):
    """
        main function in order to get the filesize aggregate
    """
    ### For the first part of getting the filesizes
    ## Sending output to an out file
    # sys.stdout = open('C:\\Users\\Admin\\Desktop\\FileSizeAggregate-DI-Output-6-29.txt', 'w')
    sys.stdout = open(out_f, 'w')

    ## For Testing purposes
    # dir_path = 'Z:\\TRLA\\CTS Exports\\testfilesize\\'
    # get_filelocs(dir_path)

    ## Getting the filesizes
    # csv_f = 'Z:\\TRLA\\CTS Exports\\FinalExport.csv'
    # csv_f = 'C:\\Users\\jjang\\Desktop\\testfilesizes.xlsx'
    # csv_f = 'C:\\Users\\Admin\\Desktop\\FinalExport.csv'
    # csv_f = 'C:\\Users\Admin\\Desktop\\docs index files.csv'
    get_filepaths(csv_f, df_col)

    ## Closing the out file
    sys.stdout.close()

    # ## Looping the out file to search for the files not found
    # # lines = open('C:\\Users\\Admin\\Desktop\\FileSizeAggregate-Output.txt', 'r').readlines()
    # # for line in lines:
    # #     # print(f"Line: {line}")
    # #     if "file:" in line:
    # df_txt = pd.read_csv(out_f, delimiter='\t')
    # # df_txt.to_csv('C:\\Users\\Admin\\Desktop\\FileSizeAggregate-DI-Output-6-29.csv', index=False)
    # df_txt.to_csv(out_f + '_to-csv.csv')


def stage_data(excel_f):
    """
        Prepping the data to get ready for the migration process
        For staging the data to get the files copied and ready for Migration Mover
    
    :param excel_f: str
        string of the csv file that we are using to feed in the data
    :return:
    """
    # if not os.path.exists("C:\\Users\\Admin\\Desktop\\output-docket.txt"):
    #         os.makedirs("C:\\Users\\Admin\\Desktop\\output-docket.txt")
    f = open("C:\\Users\\Admin\\Desktop\\output-docket.txt", "a")

    dst_parent_path = 'D:\\TRLA-PythonStagerMigration\\EXPORT-Docket\\'

    df_all = pd.read_excel(excel_f).fillna(0)
    df = pd.read_excel(excel_f)['doc_filena_FILEPATH'].fillna(0)

    for index, file_p in df.iteritems():
        # Having another variable for keeping track of which items are duplicates for the special file rename case. Setting up a way to get a solution for when there are duplicates of the entire absolute path.
        dup_df = df.duplicated(keep=False)

        # if index < 40:
        # Getting necessary variables initiated
        case_id = df_all.loc[df_all['doc_filena_FILEPATH'] == file_p, 'caseid'].iloc[0]
        filesize = df_all.loc[df_all['doc_filena_FILEPATH'] == file_p, 'filesize'].iloc[0]
        # print(f"duplicate: {dup_df.iloc[index]}")
        # print(f"Index : {index}, file_p : {file_p}")
        # print(f"\tfile_p: {file_p} \t {type(file_p)}")
        # print(f"\tcase_id: {case_id} \t {type(case_id)}")
        # print(f"\tfilesize: {filesize} \t {type(filesize)}\n")

        dst_folder_path = dst_parent_path + str(case_id) + '\\'
        # For handling base case of ensuring that the caseid filpath exists
        if not os.path.exists(dst_folder_path):
            os.makedirs(dst_folder_path)
        # For ensuring that the "Doc Index" folder exists as well
        if not os.path.exists(dst_folder_path + "Doc Index\\"):
            os.makedirs(dst_folder_path + "Doc Index\\")
        
        ## If 'cell was blank - filesize: 0' or 'file was not found...skipping' skip
        # Checking to make sure that the row we are on is a file that we can copy over
        if isinstance(file_p, (int)) or file_p == 0 or \
            isinstance(filesize, (str)) or 'cell was blank' in str(filesize) or \
            'file was not found' in str(filesize):
            # print(f"passing file! Index : {index}, file_p : {file_p}")
            # print(f"\tfile_p: {file_p} \t {type(file_p)}")
            # print(f"\tcase_id: {case_id} \t {type(case_id)}")
            # print(f"\tfilesize: {filesize} \t {type(filesize)}\n")
            print(f"DNE-SKIPPING\tSKIPPING")
            f.write(f"DNE-SKIPPING\tSKIPPING\n")
            pass
        else:
            new_styles_folder = str(df_all.iloc[index, 2])
            ## Checking to see if the value inside the cell for the styles is == 0
            if new_styles_folder == "0":
                print(f"The Styles Cell was BLANK.")
                new_styles_folder = ""
            ## Checking to make sure that the path and its sub directories exist before copying the flies over -- the styles Col
            # new_styles_folder = re.sub("\\", "-", re.sub("/", "-", re.sub("|", "-", re.sub(">", "-", re.sub("<", "-", re.sub("\"", "-", re.sub("?", "-", re.sub("*", "-", re.sub(":", "-", df_all.iloc[index, 2])))))))))
            new_styles_folder = re.sub(r"[/\"<>*?|:]", "-", new_styles_folder)
            if not os.path.exists(dst_folder_path + new_styles_folder + '\\'):
                os.makedirs(dst_folder_path + new_styles_folder + '\\')

            ## There was an issue with how some files had the same file name but existed in a different source folder which caused there to have some of the files get overwritten by the ones that popped up later on the list.
            ## In order to combat this, we will take the old absolute path and incorporate the name of the parent folders into the new destination filepath.
            temp_fp = file_p.split('\\')
            # temp_str = "-"
            # for each_i in range(1, len(temp_fp)-1):
            #     temp_str = temp_str + temp_fp[each_i]
            # new_dst = dst_folder_path + new_styles_folder + '\\' + temp_fp[-1].split('.PDF')[0] + temp_str
            new_dst = dst_folder_path + new_styles_folder + '\\' + temp_fp[-1].split('.PDF')[0]
            new_tmp_dst = new_dst + '.PDF'
            # ## Checking for when there is a duplicate in the 'doc_filena' col - Special Case
            # if dup_df.iloc[index]:
            ## Checking for if the path / filename already exists for an item if there is a duplicate item
            if os.path.exists(new_tmp_dst):
            # # getting the style column information to make sure the duplicates stay separate when copied over to the new location
            # styles = df_all.iloc[index, 5]
            # new_dst += styles
            # print(f"\n\nnew_dst = {new_dst}.PDF\n\n")

                # Checking to see if the file already exists in the destination and creating a copy with a number associated to it
                count = 2
                try_filename = os.path.exists(new_dst + '.PDF')
                while (try_filename):
                    new_tmp_dst = new_dst + '_' + str(count) + '.PDF'
                    try_filename = os.path.exists(new_tmp_dst)
                    count += 1

            # Copying the file over to the new Generated Staging Python Folders
            shutil.copy2(src=file_p, dst=new_tmp_dst)
            print(f"{file_p}\t{new_tmp_dst}")
            f.write(f"{file_p}\t{new_tmp_dst}\n")
    f.close()


def stage_data_di(excel_f):
    """
        Prepping the data to get ready for the migration process
        For staging the data to get the files copied and ready for Migration Mover
    
    :param excel_f: str
        string of the csv file that we are using to feed in the data
    :return:
    """
    # if not os.path.exists("C:\\Users\\Admin\\Desktop\\output-docket.txt"):
    #         os.makedirs("C:\\Users\\Admin\\Desktop\\output-docket.txt")
    f = open("C:\\Users\\Admin\\Desktop\\output-docket.txt", "a")

    dst_parent_path = 'D:\\TRLA-PythonStagerMigration\\DI_EXPORT\\'

    df_all = pd.read_excel(excel_f).fillna(0)
    df = pd.read_excel(excel_f)['DI FP'].fillna(0)

    for index, file_p in df.iteritems():
        # Having another variable for keeping track of which items are duplicates for the special file rename case. Setting up a way to get a solution for when there are duplicates of the entire absolute path.
        dup_df = df.duplicated(keep=False)

        # if index < 40:
        # Getting necessary variables initiated
        case_id = df_all.loc[df_all['DI FP'] == file_p, 'Immigration_List_caseid_'].iloc[0]
        filesize = df_all.loc[df_all['DI FP'] == file_p, 'Filesize'].iloc[0]
        # print(f"duplicate: {dup_df.iloc[index]}")
        # print(f"Index : {index}, file_p : {file_p}")
        # print(f"\tfile_p: {file_p} \t {type(file_p)}")
        # print(f"\tcase_id: {case_id} \t {type(case_id)}")
        # print(f"\tfilesize: {filesize} \t {type(filesize)}\n")

        dst_folder_path = dst_parent_path + str(case_id) + '\\'
        # For handling base case of ensuring that the caseid filpath exists
        if not os.path.exists(dst_folder_path):
            os.makedirs(dst_folder_path)
        # For ensuring that the "Doc Index" folder exists as well
        if not os.path.exists(dst_folder_path + "Doc Index\\"):
            os.makedirs(dst_folder_path + "Doc Index\\")
        
        ## If 'cell was blank - filesize: 0' or 'file was not found...skipping' skip
        # Checking to make sure that the row we are on is a file that we can copy over
        if isinstance(file_p, (int)) or file_p == 0 or \
            isinstance(filesize, (str)) or 'cell was blank' in str(filesize) or \
            'file was not found' in str(filesize):
            # print(f"passing file! Index : {index}, file_p : {file_p}")
            # print(f"\tfile_p: {file_p} \t {type(file_p)}")
            # print(f"\tcase_id: {case_id} \t {type(case_id)}")
            # print(f"\tfilesize: {filesize} \t {type(filesize)}\n")
            print(f"DNE-SKIPPING\tSKIPPING")
            f.write(f"DNE-SKIPPING\tSKIPPING\n")
            pass
        else:
            new_styles_folder = str(df_all.iloc[index, 3])
            ## Checking to see if the value inside the cell for the styles is == 0
            if new_styles_folder == "0":
                print(f"The Styles Cell was BLANK.")
                new_styles_folder = ""
            ## Checking to make sure that the path and its sub directories exist before copying the flies over -- the styles Col
            new_styles_folder = re.sub(r"[/\"<>*?|:]", "-", new_styles_folder)
            if not os.path.exists(dst_folder_path + new_styles_folder + '\\'):
                os.makedirs(dst_folder_path + new_styles_folder + '\\')

            ## There was an issue with how some files had the same file name but existed in a different source folder which caused there to have some of the files get overwritten by the ones that popped up later on the list.
            ## In order to combat this, we will take the old absolute path and incorporate the name of the parent folders into the new destination filepath.
            temp_fp = file_p.split('\\')
            # temp_str = "-"
            # for each_i in range(1, len(temp_fp)-1):
            #     temp_str = temp_str + temp_fp[each_i]
            # new_dst = dst_folder_path + new_styles_folder + '\\' + temp_fp[-1].split('.PDF')[0] + temp_str
            new_dst = dst_folder_path + new_styles_folder + '\\' + temp_fp[-1].split('.PDF')[0]
            new_tmp_dst = new_dst + '.PDF'
            # ## Checking for when there is a duplicate in the 'doc_filena' col - Special Case
            # if dup_df.iloc[index]:
            ## Checking for if the path / filename already exists for an item if there is a duplicate item
            if os.path.exists(new_tmp_dst):
            # # getting the style column information to make sure the duplicates stay separate when copied over to the new location
            # styles = df_all.iloc[index, 5]
            # new_dst += styles
            # print(f"\n\nnew_dst = {new_dst}.PDF\n\n")

                # Checking to see if the file already exists in the destination and creating a copy with a number associated to it
                count = 2
                try_filename = os.path.exists(new_dst + '.PDF')
                while (try_filename):
                    new_tmp_dst = new_dst + '_' + str(count) + '.PDF'
                    try_filename = os.path.exists(new_tmp_dst)
                    count += 1

            # Copying the file over to the new Generated Staging Python Folders
            shutil.copy2(src=file_p, dst=new_tmp_dst)
            print(f"{file_p}\t{new_tmp_dst}")
            f.write(f"{file_p}\t{new_tmp_dst}\n")
    f.close()


def main():
    """
        Main function of the python project
    """
    # start_time = time.time()
    start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # ### For the first part of getting the filesizes
    # csv_f_1 = 'C:\\Users\\Admin\\Desktop\\docs index export.csv'
    # csv_f_2 = 'C:\\Users\\Admin\\Desktop\\Docket.csv'
    # # csv_f_3 = 'C:\\Users\\Admin\\Desktop\\Docs Index with date.csv'
    # out_1 = 'C:\\Users\\Admin\\Desktop\\filesize-sum-out_doc_index_export.txt'
    # out_2 = 'C:\\Users\\Admin\\Desktop\\filesize-sum-out_docket.txt'
    # # out_3 = 'C:\\Users\\Admin\\Desktop\\filesize-sum-out_docs_index_w_date.txt'
    # file_aggregate(csv_f_1, out_1, 'DI_INDEX_di_folder_')
    # file_aggregate(csv_f_2, out_2, 'doc_filena')

    ## For staging the data to get the files copied and ready for Migration Mover
    # stage_data('C:\\Users\\Admin\\Desktop\\TRLA-StageFile-Docket.xlsx')
    stage_data_di('C:\\Users\\Admin\\Desktop\\TRLA-StageFile-docs index files.xlsx')

    # end_time = time.time()
    end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"start_time: {start_time} \t\t end_time: {end_time}")


if __name__ == "__main__":
    main()
