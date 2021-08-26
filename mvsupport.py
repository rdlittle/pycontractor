"""
A collection of standard multi-value functions that are not present
in the qmclient.py module.  Although these functions were created
for use with OpenQM, they are generic enough to be used with any 
multi-value database.

Defines constant multi-value data markers:
    AM / FM: char(253)
    VM     : char(252)
    SV/SVM : char(251)
    TM     : char(250)
"""
import os
import re

FM = '\xfe'
AM = '\xfe'
VM = '\xfd'
SV = '\xfc'
TM = '\xfb'
SVM = '\xfc'


def mv_readnext(list_name):
    """
    Provides a 'readnext' function to simulate a pick-style readnext
    """
    for attr in list_name:
        yield list_name[attr]

def mv_to_list(dyn_array):
    """
    Converts a dynamic array to a python list
    """
    return dyn_array.split(sep=AM)

def mv_raise(dynarray):
    """
    Provides multi-value raise functionality.
    If the dynamic array being passed in is already raised to the attribute 
    mark level, the dynamic array is just returned unchanged.
    """
    if AM in dynarray:
        return dynarray
    dynarray = re.sub(VM,AM,dynarray)
    dynarray = re.sub(SVM,VM,dynarray)
    dynarray = re.sub(TM,SVM,dynarray)
    return dynarray

def mv_lower(dynarray):
    """
    Provides multi-value lower functionality.
    If the dynamic array being passed in is already lowered to the text 
    mark level, the dynamic array is just returned unchanged.
    """
    if TM in dynarray:
        return dynarray
    dynarray = re.sub(SVM,TM,dynarray)
    dynarray = re.sub(VM,SVM,dynarray)
    dynarray = re.sub(AM,VM,dynarray)
    return dynarray


