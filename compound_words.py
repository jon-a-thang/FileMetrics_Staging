"""
    Filename:
        compound_words.py

    Description:
        This program if for the purpose of having a temp-test environment for quick and easy tests or other functions to run.
    
    Author:
        Jonathan Jang
        
"""

import os, re, csv, time, math
import pandas as pd


def temp_func(param1, param2):
    """
        temp func description
    
    :param param1:
    :return:
    """
    out_list, temp_str = [], ""
    for each_key in range(0, len(param1)):
        for each_i in range(0, len(param1)):
            if param1[each_i] != param1[each_key]:
                temp_str = param1[each_key] + param1[each_i]
                if temp_str in param1 and temp_str not in out_list:
                    out_list.append(temp_str)
                    temp_str = ""
        for each_i in range(0, len(param1)):
            next_val = each_i + 1
            if next_val == len(param1):
                next_val = 0
            temp_str = param1[each_key] + param1[each_i] + param1[next_val]
            if temp_str in param1 and temp_str not in out_list:
                out_list.append(temp_str)
                temp_str = ""

    return out_list


# def temp_func2(param1):
#     out_list, temp_str = [], ""
#     for each_key in range(0, len(param1)):
#         # temp_str += param1[each_key]
#         out_list.extend(temp_func3(param1, each_key, out_list))
#     return out_list

# def temp_func3(param1, each_key, out_list):
#     temp_str = ""
#     for i in range(0, len(param1)):
#         temp_str += param1[each_key]
#         for each_i in range(0, len(param1)):
#             next_val = each_i + i
#             if next_val == len(param1):
#                 next_val = 0
#             if next_val > len(param1):
#                 next_val = next_val - len(param1)
#             temp_str += param1[each_i] + param1[next_val]
#             if temp_str in param1 and temp_str not in out_list:
#                 out_list.append(temp_str)
#                 temp_str = ""
#     return out_list


def main():
    """
        Main function of the python project
    """
    list_a = ["none", "fishcake", "fish", "cake", "cakes", "fishcakes", "for", "ever", "more", "mores", "forevermore", "forevermores", "nonetheless", "the", "less", "thenewstrawberry", "new", "straw", "berry"]
    print(temp_func(list_a, len(list_a)))
    # print("\n")
    # print(temp_func2(list_a))


if __name__ == "__main__":
    main()
