# 14 Jun 19  3.4-15 Fixed typo in QMPoolIdle function name
# 03 Jun 19  3.4-15 Set() was attempting to return a value.
# 22 Jun 18  3.4-13 GetArg() was returning None for a null string.
# 04 Apr 17  3.4-11 Added QMSystem().
# 03 Apr 17  3.4-11 Added QMTrans() and QMRTrans().

"""
QMClient wrapper for Python 3.5

Jointly developed by Ladybridge Systems and George R Smith.

Use:
  "import QMClient as qm" to import this module into your application.
  Then, all QMClient function  names are accessed as "qm.Name" where
  the leading "QM" of the documented library function name is replaced
  by 'qm.'
  For example, QMRead becomes qm.Read

  On Linux, the QMSYSCLI or QMSYS environment variable must be set to
  point to the QMSYS account directory.

  The status codes returned by some functions are:
     SV_OK         0   Action successful
     SV_ON_ERROR   1   Action took ON ERROR clause
     SV_ELSE       2   Action took ELSE clause
     SV_ERROR      3   Action failed. Error text available
     SV_LOCKED     4   Action took LOCKED claus
     SV_PROMPT     5   Server requesting input

  For more details of the functions, see the QM Reference Guide. The
  function names in the comment bars below are the names as they
  appear in the documentation.
"""

import os
import platform
import ctypes as ct
import copy
import sys
from ctypes.util import find_library

# __qm_lib is needed by all functions defined here and must persist.

__qm_lib = None


# ======================================================================
# __LoadQMCliLib() - Internal function to load QMClient library
# ======================================================================
def __LoadQMCliLib():
    """
    Called from all functions that might be the first use of QMClient.

    On Linux, the QMSYSCLI or QMSYS environment variable must be set to point
    to the QMSYS account directory.
    """

    global __qm_lib

    if __qm_lib is None:
        if platform.system() == 'Linux':
            qmsys = os.getenv("QMSYS")
            libpath = qmsys + "/bin/qmclilib.so"
            __qm_lib = ct.cdll.LoadLibrary(libpath)
        else:
            __qm_lib = ct.cdll.LoadLibrary(find_library("qmclilib"))


# ======================================================================
# __QMFree() - Internal function to release dynamically allocated memory
# ======================================================================
def __QMFree(s):
    """
    This function releases memory returned by other functions.
    """

    __LoadQMCliLib()
    __qm_lib.QMFree(ct.c_void_p(s))


# ======================================================================
# QMCall()
# ======================================================================
def Call(subr, argct, arg1=None, arg2=None, arg3=None, arg4=None,
         arg5=None, arg6=None, arg7=None, arg8=None, arg9=None,
         arg10=None, arg11=None, arg12=None, arg13=None, arg14=None,
         arg15=None, arg16=None, arg17=None, arg18=None, arg19=None,
         arg20=None):
    """
    The Call() function calls a catalogued subroutine on the
    server. It is analogous to the QMBasic CALL statement.

    subr is the name of the subroutine to be called.

    argct is the number of arguments following.

    arg1, arg2, ... is a list of arguments to be passed
    to the subroutine.

    The Call() function calls the named catalogued subroutine
    on the server system. This subroutine may take up to
    20 arguments. QMClient does not provide a method to call
    subroutines with a greater number of arguments.

    Example:
        sub_name = 'TEST.QMCLIENT' Cataloged subroutine on QM
        arg_count = 2
        arg_01 = 'arg_01 from remote'
        arg_02 = 'arg_02 from remote'
        qm.Call(sub_name, arg_count, arg_01, arg_02)

    Also See:
        GetArg(n)
    """

    func = __qm_lib.QMCallxW
    func.argtypes = [ct.c_wchar_p, ct.c_short,
                     ct.c_wchar_p, ct.c_wchar_p, ct.c_wchar_p, ct.c_wchar_p,
                     ct.c_wchar_p, ct.c_wchar_p, ct.c_wchar_p, ct.c_wchar_p,
                     ct.c_wchar_p, ct.c_wchar_p, ct.c_wchar_p, ct.c_wchar_p,
                     ct.c_wchar_p, ct.c_wchar_p, ct.c_wchar_p, ct.c_wchar_p,
                     ct.c_wchar_p, ct.c_wchar_p, ct.c_wchar_p, ct.c_wchar_p]
    func(subr, argct, arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8, arg9,
         arg10, arg11, arg12, arg13, arg14, arg15, arg16, arg17, arg18, arg19,
         arg20)


# ======================================================================
# QMChange()
# ======================================================================
def Change(in_str, old, new, occ=0, start=1):
    """
    The Change() function replaces occurrences of one substring
    with another in a string. It is analogous to the QMBasic
    CHANGE() function.

    This function is evaluated on the client system and
    does not require a server connection to be open.

    in_str is the string to be processed.
    old    is the substring to be replaced.
    new    is the replacement substring.

    occ    is the number of occurrences of old to be replaced.
           If omitted or specified as less than one, all occurrences
           are replaced.

    start  is the occurrence number from one of the first
           occurrence of old to be replaced. If omitted or less than
           one, replacement commences at the first occurrence of old.

    Example:
        X = qm.Change("ABRACADABRA", "A", "a", 3, 2)
    """

    __LoadQMCliLib()
    func = __qm_lib.QMChangeW
    func.argtypes = [ct.c_wchar_p, ct.c_wchar_p, ct.c_wchar_p, ct.c_int, ct.c_int]
    func.restype = ct.c_void_p
    s = func(in_str, old, new, occ, start)
    out_str = ct.wstring_at(s)
    __QMFree(s)
    return out_str


# ======================================================================
# QMChecksum()
# ======================================================================
def Checksum(in_str):
    """
    The Checksum() function returns a checksum value for supplied data.

    It is analogous to the QMBasic CHECKSUM() function.
    This function is evaluated on the client system and
    does not require a server connection to be open.
    """

    __LoadQMCliLib()
    func = __qm_lib.QMChecksumW
    func.argtypes = [ct.c_wchar_p]
    return func(in_str)


# ======================================================================
# QMClearFile()
# ======================================================================
def ClearFile(fno):
    """
    The ClearFile() function deletes all content from a file.

    It is analogous to the QMBasic CLEARFILE statement.
    fno is the file number returned by a previous qm.Open call.
    """

    func = __qm_lib.QMClearFile
    func.argtypes = [ct.c_int]
    func(fno)


# ======================================================================
# QMClearSelect()
# ======================================================================
def ClearSelect(listno):
    """
    The ClearSelect() function clears the specified select list.

    No error occurs if the list was not active.
    Applications that use select list 0 (the default select list)
    and could leave unprocessed items in the list should always
    clear it to avoid unwanted effects on later server processing.
    """

    func = __qm_lib.QMClearSelect
    func.argtypes = [ct.c_int]
    func(listno)


# ======================================================================
# QMClose()
# ======================================================================
def Close(fno):
    """
    The Close() function closes a file. It is analogous to the
    QMBasic CLOSE statement.

    fno is the file number returned by a previous Open() call.

    Example:
      qm.Close(fno)
    """

    func = __qm_lib.QMClose
    func.argtypes = [ct.c_int]
    func(fno)


# ======================================================================
# QMConnect()
# ======================================================================
def Connect(host, port, username, password, account):
    """
    The Connect() function connects to a QM server.

    Example:
        host = IP address (IPV4 or IPV6 form) or server name
        port = Normally 4243 or -1 (which defaults to 4243)
        username = "aaa"
        password = "bbb"
        account = "ccc"

        connect_result = qm.Connect(host, port, username,
                                    password, account)
        connect_result = 1 Connection successful
    """

    __LoadQMCliLib()
    func = __qm_lib.QMConnectW
    func.argtypes = [ct.c_wchar_p, ct.c_int, ct.c_wchar_p, ct.c_wchar_p, ct.c_wchar_p]
    return func(host, port, username, password, account)


# ======================================================================
# QMConnected()
# ======================================================================
def Connected():
    """
    The Connected() function can be used by an application
    to determine whether a client session is open.
    Example:
        connected_result = qm.Connected()
        connected_result = 1 client session is open.
    """

    __LoadQMCliLib()
    return __qm_lib.QMConnected()


# ======================================================================
# QMConnectionType()
# ======================================================================
def ConnectionType(n):
    """
    The ConnectionType() function sets parameters that affect the
    behaviour of QMClient. The argument is an additive value of
    options to be enabled.
    """

    __LoadQMCliLib()
    func = __qm_lib.QMConnectionType
    func.argtypes = [ct.c_int]
    func(n)


# ======================================================================
# QMConnectLocal()
# ======================================================================
def ConnectLocal(account):
    """
    The ConnectLocal() function establishes a QMClient session on the
    local system. The return value is 1 for success, 0 for failure.
    """

    __LoadQMCliLib()
    func = __qm_lib.QMConnectLocalW
    func.argtypes = [ct.c_wchar_p]
    return func(account)


# ======================================================================
# QMConnectPool()
# ======================================================================
def ConnectPool(host, port, username, password, account, pool):
    """
    The ConnectPool() function is identical to qm.Connect except
    that the QM process becomes part of a connection pool.
    """

    __LoadQMCliLib()
    func = __qm_lib.QMConnectPoolW
    func.argtypes = [ct.c_wchar_p, ct.c_int, ct.c_wchar_p, ct.c_wchar_p, ct.c_wchar_p, ct.c_wchar_p]
    return func(host, port, username, password, account, pool)


# ======================================================================
# QMCreateObject()
# ======================================================================
def CreateObject(subr, argct, arg1=None, arg2=None, arg3=None, arg4=None,
                 arg5=None, arg6=None, arg7=None, arg8=None,
                 arg9=None, arg10=None, arg11=None, arg12=None,
                 arg13=None, arg14=None, arg15=None, arg16=None,
                 arg17=None, arg18=None, arg19=None, arg20=None):
    """
    The CreateObject() function instantiates an object based on
    the QMBasic class module catalogued as subr.
    Up to 20 arguments may be supplied. These will be passed into
    the optional CREATE.OBJECT subroutine.
    """

    func = __qm_lib.QMCreateObjectW
    func.argtypes = [ct.c_wchar_p, ct.c_short,
                     ct.c_wchar_p, ct.c_wchar_p, ct.c_wchar_p, ct.c_wchar_p,
                     ct.c_wchar_p, ct.c_wchar_p, ct.c_wchar_p, ct.c_wchar_p,
                     ct.c_wchar_p, ct.c_wchar_p, ct.c_wchar_p, ct.c_wchar_p,
                     ct.c_wchar_p, ct.c_wchar_p, ct.c_wchar_p, ct.c_wchar_p,
                     ct.c_wchar_p, ct.c_wchar_p, ct.c_wchar_p, ct.c_wchar_p]
    objno = func(subr, argct, arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8, arg9,
                 arg10, arg11, arg12, arg13, arg14, arg15, arg16, arg17,
                 arg18, arg19, arg20)
    return objno


# ======================================================================
# QMDcount()
# ======================================================================
def Dcount(s, delim):
    """
    The Dcount() function counts delimited items in a string.

    It is analogous to the QMBasic DCOUNT() function.

    s     is the string to scan
    delim is the delimiter separating the items to be counted.

    The Dcount() function is usually used to count fields,
    values or subvalues in a dynamic array but can be used
    to count elements in any string that is separated by
    any substring.

    This function is evaluated on the client system and does
    not require a server connection to be open.
    """

    __LoadQMCliLib()
    func = __qm_lib.QMDcountW
    func.argtypes = [ct.c_wchar_p, ct.c_wchar_p]
    return func(s, delim)


# ======================================================================
# QMDel()
# ======================================================================
def Del(in_str, f, v, sv):
    """
    The Del() function deletes a field, value or subvalue
    from a dynamic array.

    This function is evaluated on the client system and
    does not require a server connection to be open.

    It is analogous to the QMBasic DELETE() function.

    in_str is the dynamic array to be processed

    f      is the number of the field to be deleted.
           If less than 1, 1 is assumed

    v      is the number of the value to be deleted.
           If less than 1, the entire field is deleted.

    sv     is the number of the subvalue to be deleted.
           If less than 1, the entire value is deleted.

    The function returns the modified dynamic array.

    Example:
        rec = qm.Del(rec, 2, 1, 0)
    """

    __LoadQMCliLib()
    func = __qm_lib.QMDelW
    func.argtypes = [ct.c_wchar_p, ct.c_int, ct.c_int, ct.c_int]
    func.restype = ct.c_void_p
    s = func(in_str, f, v, sv)
    out_str = ct.wstring_at(s)
    __QMFree(s)
    return out_str


# ======================================================================
# QMDelete()
# ======================================================================
def Delete(fno, id):
    """
    The Delete() function deletes a record from a file.
    It is analogous to the QMBasic DELETE statement

    fno is the file number returned by a previous qm.Open call.

    id is the id of the record to be deleted.

    Applications should always obtain an update lock for a
    record before deleting it. The lock is released by this function.
    """

    func = __qm_lib.QMDeleteW
    func.argtypes = [ct.c_int, ct.c_wchar_p]
    func(fno, id)


# ======================================================================
# QMDeleteu()
# ======================================================================
def Deleteu(fno, id):
    """
    The Deleteu() function deletes a record from a file.
    It is analogous to the QMBasic DELETEU statement

    fno is the file number returned by a previous qm.Open call.

    id is the id of the record to be deleted.

    Applications should always obtain an update lock for a record
    before deleting it. The lock is not released by this function.
    """

    func = __qm_lib.QMDeleteuW
    func.argtypes = [ct.c_int, ct.c_wchar_p]
    func(fno, id)


# ======================================================================
# QMDestroyObject()
# ======================================================================
def DestroyObject(objno):
    """
    The DestroyObject() function destroys an object previously
    instatiated with qm.CreateObject()
    """

    func = __qm_lib.QMDestroyObject
    func.argtypes = [ct.c_int]
    func(objno)


# ======================================================================
# QMDisconnect()
# ======================================================================
def Disconnect():
    """
    The Disconnect() function disconnects the current QMClient session.
    """

    __LoadQMCliLib()
    __qm_lib.QMDisconnect()


# ======================================================================
# QMDisconnectAll()
# ======================================================================
def DisconnectAll():
    """
    The DisconnectAll() function disconnects all QMClient sessions.
    """

    __LoadQMCliLib()
    __qm_lib.QMDisconnectAll()


# ======================================================================
# QMDynArrayToList()
# ======================================================================
def DynArrayToList(dyn):
    """
    Converts attributes, multi-values, and sub-values
    to a Python list.
    """

    a_list = []
    AM = chr(254)
    VM = chr(253)
    SVM = chr(252)

    nbr_attributes = Dcount(dyn, AM)

    for attr_count in range(1, nbr_attributes + 1):
        attribute = Extract(dyn, attr_count, 0, 0)
        nbr_multi_values = Dcount(attribute, VM)

        if nbr_multi_values == 1:
            a_list.append(attribute)
        else:
            b_list = []
            for mv_count in range(1, nbr_multi_values + 1):
                multi_value = Extract(dyn, attr_count, mv_count, 0)
                nbr_sub_values = Dcount(multi_value, SVM)

                if nbr_sub_values == 1:
                    b_list.append(multi_value)
                else:
                    c_list = []
                    for sub_value_count in range(1, nbr_sub_values + 1):
                        sub_value = Extract(dyn, attr_count, mv_count, sub_value_count)
                        c_list.append(sub_value)
                    b_list.append(c_list)

            a_list.append(b_list)

    return a_list


# ======================================================================
# QMEndCommand()
# ======================================================================
def EndCommand():
    """
    The EndCommand() function allows a QMClient application to
    terminate execution of a command started with qm.Execute() that
    is asking for data input.
    """

    __qm_lib.QMEndCommand


# ======================================================================
# QMEnterPackage()
# ======================================================================
def EnterPackage(name):
    """
    The EnterPackage() function attempts to enter a licensed
    software package.
    """

    func = __qm_lib.QMEnterPackageW
    func.argtypes = [ct.c_wchar_p]
    return func(name)


# ======================================================================
# QMError()
# ======================================================================
def Error():
    """
    The Error() function returns extended error message text.

    Some API functions set extended error text and return
    an error code of SV_ERROR when an error condition occurs.
    The qm.Error function can be used to retrieve this text.
    """

    func = __qm_lib.QMErrorW
    func.restype = ct.c_void_p
    s = func()
    return ct.wstring_at(s)


# ======================================================================
# QMEvalConv()
# ======================================================================
def EvalConv(fno, name, data, id):
    """
    The EvalConv() function evaluates a dictionary data defining
    item, applying any conversion code specified in the dictionary.

    fno   is the file number reurn from use of qm.Open() to open
          the dictionary portion of the file.

    name  is the name of the dictionary item to be evaluated.

    data  is the record data to be used in evaluating the item.

    id    is the record id to be used in evaluating the item.
    """

    func = __qm_lib.QMEvalConvW
    func.argtypes = [ct.c_int, ct.c_wchar_p, ct.c_wchar_p, ct.c_wchar_p]
    func.restype = ct.c_void_p
    s = func(fno, name, data, id)
    out_str = ct.wstring_at(s)
    __QMFree(s)
    return out_str


# ======================================================================
# QMEvaluate()
# ======================================================================
def Evaluate(fno, name, data, id):
    """
    The Evaluate() function evaluates a dictionary data defining item,
    without applying any conversion code specified in the dictionary.

    fno   is the file number reurn from use of qm.Open() to open
          the dictionary portion of the file.

    name  is the name of the dictionary item to be evaluated.

    data  is the record data to be used in evaluating the item.

    id    is the record id to be used in evaluating the item.
    """

    func = __qm_lib.QMEvaluateW
    func.argtypes = [ct.c_int, ct.c_wchar_p, ct.c_wchar_p, ct.c_wchar_p]
    func.restype = ct.c_void_p
    s = func(fno, name, data, id)
    out_str = ct.wstring_at(s)
    __QMFree(s)
    return out_str


# ======================================================================
# QMExecute()
# ======================================================================
def Execute(command):
    """
    The Execute() function executes the specified command on the
    server.

    The function returns two items, for example,
       data, err = qm.Execute("LIST VOC FIRST 5")
    where
       data is the output from the command as a field mark delimited
            string in which each field corresponds to a line of output.

       err  is  SV_OK (0)      if the command executed completely
                SV_PROMPT (5)  if the command is waiting for data input
    """

    func = __qm_lib.QMExecuteW
    func.argtypes = [ct.c_wchar_p, ct.c_void_p]
    func.restype = ct.c_void_p
    err = ct.c_int()
    s = func(command, ct.byref(err))
    out_str = ct.wstring_at(s)
    __QMFree(s)
    return out_str, err.value


# ======================================================================
# QMExitPackage()
# ======================================================================
def ExitPackage(name):
    """
    The ExitPackage() function exits from a licensed software package.
    """

    func = __qm_lib.QMExitPackageW
    func.argtypes = [ct.c_wchar_p]
    func(name)


# ======================================================================
# QMExtract()
# ======================================================================
def Extract(in_str, f, v, sv):
    """
    The Extract() function extracts a field, value or subvalue
    from a dynamic array.

    It is analogous to the QMBasic field extraction operator
    or the EXTRACT() function.

    This function is evaluated on the client system and
    does not require a server connection to be open.

    in_str is the dynamic array to be processed

    f      is the number of the field to be extracted.
           If less than 1, 1 is assumed

    v      is the number of the value to be extracted.
           If less than 1, the entire field is extracted.

    sv     is the number of the subvalue to be extracted.
           If less than 1, the entire value is extracted.
    """

    __LoadQMCliLib()
    func = __qm_lib.QMExtractW
    func.argtypes = [ct.c_wchar_p, ct.c_int, ct.c_int, ct.c_int]
    func.restype = ct.c_void_p
    s = func(in_str, f, v, sv)
    out_str = ct.wstring_at(s)
    __QMFree(s)
    return out_str


# ======================================================================
# QMField()
# ======================================================================
def Field(in_str, delim, occurrence, count):
    """
    The Field() function extracts one or more components of a
    delimited string.

    It is analogous to the QMBasic FIELD() function.

    This function is evaluated on the client system and
    does not require a server connection to be open.

    in_str     is the string from which substrings are to be extracted.

    delim      is the single character delimiter separating components
               of the string.

    occurrence evaluates to the position of the substring to be extracted.

    count      evaluates to the number of substrings to be extracted. If
               omitted or less than one, one substring is extracted.

    Example:
        A = "1*2*3*4*5"
        S = FIELD(A, '*', 2, 3)
        This program fragment assigns the string '2*3*4'
        to variable S.
    """

    __LoadQMCliLib()
    func = __qm_lib.QMFieldW
    func.argtypes = [ct.c_wchar_p, ct.c_wchar_p, ct.c_int, ct.c_int]
    func.restype = ct.c_void_p
    s = func(in_str, delim, occurrence, count)
    out_str = ct.wstring_at(s)
    __QMFree(s)
    return out_str


# ======================================================================
# QMGet()
# ======================================================================
def Get(objno, name, argct, arg1=None, arg2=None, arg3=None, arg4=None,
        arg5=None, arg6=None, arg7=None, arg8=None, arg9=None, arg10=None,
        arg11=None, arg12=None, arg13=None, arg14=None, arg15=None,
        arg16=None, arg17=None, arg18=None, arg19=None, arg20=None):
    """
    The Get() function executes a public function or retrieves the
    value of a public variable in a QMBasic class module instance.

    objno  is the object number returned by an earlier CreateObject().

    name   is the name of the public item.

    argct  is the count of arguments (max 20).
    """

    func = __qm_lib.QMGetW
    func.argtypes = [ct.c_short, ct.c_wchar_p, ct.c_short,
                     ct.c_wchar_p, ct.c_wchar_p, ct.c_wchar_p, ct.c_wchar_p,
                     ct.c_wchar_p, ct.c_wchar_p, ct.c_wchar_p, ct.c_wchar_p,
                     ct.c_wchar_p, ct.c_wchar_p, ct.c_wchar_p, ct.c_wchar_p,
                     ct.c_wchar_p, ct.c_wchar_p, ct.c_wchar_p, ct.c_wchar_p,
                     ct.c_wchar_p, ct.c_wchar_p, ct.c_wchar_p, ct.c_wchar_p]
    func.restype = ct.c_void_p
    s = func(objno, name, argct, arg1, arg2, arg3, arg4, arg5, arg6, arg7,
             arg8, arg9, arg10, arg11, arg12, arg13, arg14, arg15, arg16,
             arg17, arg18, arg19, arg20)
    out_str = ct.wstring_at(s)
    __QMFree(s)
    return out_str


# ======================================================================
# QMGetArg()
# ======================================================================
def GetArg(n):
    """
    The GetArg(0 function retrieves the value of argument variables
    updated on the server by use of Call(), CreateObject(), Get()
    or Set().

    An argument may be retrieved multiple times. Use of GetArg()
    to retrieve an argument that was not modified will return the
    corresponding argument value as passed into subroutine/function.

    Argument data remains accessible until the next use of
    any of the functions named above.
    """

    func = __qm_lib.QMGetArgW
    func.argtypes = [ct.c_short]
    func.restype = ct.c_void_p
    s = func(n)
    if s is None: return ""
    out_str = ct.wstring_at(s)
    __QMFree(s)
    return out_str


# ======================================================================
# QMGetSession()
# ======================================================================
def GetSession():
    """
    A program can make simultaneous connections to multiple QM servers.
    The GetSession() function returns the session number associated
    with the currently active session.
    See also: SetSession()
    """

    __LoadQMCliLib
    func = __qm_lib.QMGetSession
    return func()


# ======================================================================
# QMGetVar()
# ======================================================================
def GetVar(name):
    """
    The GetVar() function returns the value of an @-variable
    from the server.

    Example:
        SelectedCount = QMGetVar('@SELECTED')
    """

    func = __qm_lib.QMGetVarW
    func.argtypes = [ct.c_wchar_p]
    func.restype = ct.c_void_p
    s = func(name)
    out_str = ct.wstring_at(s)
    __QMFree(s)
    return out_str


# ======================================================================
# QMIConv()
# ======================================================================
def IConv(in_str, code):
    """
    The IConv() function applies an input conversion code to a string.
    It is analogous to the QMBasic ICONV() function.

    Because the interpretation of some conversion codes is dependent on
    information known only to the server, the evaluation is performed
    on the server system.
    """

    func = __qm_lib.QMIConvW
    func.argtypes = [ct.c_wchar_p, ct.c_wchar_p]
    func.restype = ct.c_void_p
    s = func(in_str, code)
    out_str = ct.wstring_at(s)
    __QMFree(s)
    return out_str


# ======================================================================
# QMIConvs()
# ======================================================================
def IConvs(in_str, code):
    """
    The IConvs() function applies an input conversion code to each
    element of a dynamic array, returning a similary structured result.
    It is analogous to the QMBasic ICONVS() function.

    Because the interpretation of some conversion codes is dependent on
    information known only to the server, the evaluation is performed
    on the server system.
    """

    func = __qm_lib.QMIConvsW
    func.argtypes = [ct.c_wchar_p, ct.c_wchar_p]
    func.restype = ct.c_void_p
    s = func(in_str, code)
    out_str = ct.wstring_at(s)
    __QMFree(s)
    return out_str


# ======================================================================
# QMIndices()
# ======================================================================
def Indices(fno, name):
    """
    The Indices() function returns information about alternate key
    indices in the file referenced by fno. It is analogous to the
    QMBasic INDICES() function.

    If name is an empty string, a field mark delmited list of index
    names is returned.

    If name is not an empty string it specifies and index name and
    details of that index are returned.
    """

    func = __qm_lib.QMIndicesW
    func.argtypes = [ct.c_int, ct.c_wchar_p]
    func.restype = ct.c_void_p
    s = func(fno, name)
    out_str = ct.wstring_at(s)
    __QMFree(s)
    return out_str


# ======================================================================
# QMIns()
# ======================================================================
def Ins(in_str, f, v, sv, new_data):
    """
    The Ins() function inserts an item into a dynamic array, returning
    the modified dynamic array as its result.
    """

    __LoadQMCliLib()
    func = __qm_lib.QMInsW
    func.argtypes = [ct.c_wchar_p, ct.c_int, ct.c_int, ct.c_int, ct.c_wchar_p]
    func.restype = ct.c_void_p
    s = func(in_str, f, v, sv, new_data)
    out_str = ct.wstring_at(s)
    __QMFree(s)
    return out_str


# ======================================================================
# QMIsECS()
# ======================================================================
def IsECS():
    """
    The IsECS() function returns 1 if the server is running in ECS
    mode, 0 if it is not.
    """

    func = __qm_lib.QMIsECS
    return func()


# ======================================================================
# QMLocate()
# ======================================================================
def Locate(item, dyn, f, v, sv, order):
    """
    The Locate() function searches a dynamic array for an element that
    contains a specified string. It is analogous to the QMBasic LOCATE
    statement.

    The function returns two items; a value indicating whether the item
    was found and the position at which it was found or could be inserted.

    Example:
    found, pos = qm.Locate(item, dyn, f, v, s, "")
    """

    __LoadQMCliLib()
    func = __qm_lib.QMLocateW
    func.argtypes = [ct.c_wchar_p, ct.c_wchar_p, ct.c_int, ct.c_int, ct.c_int,
                     ct.c_void_p, ct.c_wchar_p]
    func.restype = ct.c_int
    pos = ct.c_int()
    found = func(item, dyn, f, v, sv, ct.byref(pos), order)
    return found, pos.value


# ======================================================================
# QMLogto()
# ======================================================================
def Logto(account):
    """
    The Logto() function switches to a different account on the server.
    It is analogous to the QM LOGTO command.

    The function returns 1 if successful, 0 otherwise.
    """

    func = __qm_lib.QMLogtoW
    func.argtypes = [ct.c_wchar_p]
    func.restype = ct.c_int
    return func(account)


# ======================================================================
# QMMarkMapping()
# ======================================================================
def MarkMapping(fno, state):
    """
    The MarkMapping() function allows an application to control whether
    directory file read operations should transform newlines to field
    marks (or the inverse translation on write).
    """

    func = __qm_lib.QMMarkMapping
    func.argtypes = [ct.c_int, ct.c_int]
    func(fno, state)


# ======================================================================
# QMMatch()
# ======================================================================
def Match(in_str, pattern):
    """
    The Match() function matches a string against a pattern, returning 1
    if it matches, 0 if it does not.
    """
    __LoadQMCliLib()
    func = __qm_lib.QMMatchW
    func.argtypes = [ct.c_wchar_p, ct.c_wchar_p]
    return func(in_str, pattern)


# ======================================================================
# QMMatchfield()
# ======================================================================
def Matchfield(in_str, pattern, component):
    """
    The Match() function matches a string against a pattern and returns
    the portion of the string that matches a specified pattern element.
    """

    __LoadQMCliLib()
    func = __qm_lib.QMMatchfieldW
    func.argtypes = [ct.c_wchar_p, ct.c_wchar_p, ct.c_int]
    func.restype = ct.c_void_p
    s = func(in_str, pattern, component)
    out_str = ct.wstring_at(s)
    __QMFree(s)
    return out_str


# ======================================================================
# QMNextPartial()
# ======================================================================
def NextPartial(listno):
    """
    The NextPartial() function returns the next part of a select list
    created using SelectPartial().
    """

    func = __qm_lib.QMNextPartialW
    func.argtypes = [ct.c_wchar_p]
    func.restype = ct.c_void_p
    s = func(listno)
    out_str = ct.wstring_at(s)
    __QMFree(s)
    return out_str


# ======================================================================
# QMOConv()
# ======================================================================
def OConv(in_str, code):
    """
    The qm.OConv() function applies an output conversion code to a string.
    It is analogous to the QMBasic OCONV() function.

    Because the interpretation of some conversion codes is dependent on
    information known only to the server, the evaluation is performed
    on the server system.
    """

    func = __qm_lib.QMOConvW
    func.argtypes = [ct.c_wchar_p, ct.c_wchar_p]
    func.restype = ct.c_void_p
    s = func(in_str, code)
    out_str = ct.wstring_at(s)
    __QMFree(s)
    return out_str


# ======================================================================
# QMOConvs()
# ======================================================================
def OConvs(in_str, code):
    """
    The qm.OConvs() function applies an output conversion code to each
    element of a dynamic array, returning a similary strutured result.
    It is analogous to the QMBasic OCONVS() function.

    Because the interpretation of some conversion codes is dependent on
    information known only to the server, the evaluation is performed
    on the server system.
    """

    func = __qm_lib.QMOConvsW
    func.argtypes = [ct.c_wchar_p, ct.c_wchar_p]
    func.restype = ct.c_void_p
    s = func(in_str, code)
    out_str = ct.wstring_at(s)
    __QMFree(s)
    return out_str


# ======================================================================
# QMOpen()
# ======================================================================
def Open(filename):
    """
    The Open() function opens a QM database file. The returned
    integer value is the file number which must be used in all
    subsequent operations against this file. If the file cannot
    be opened, the function returns zero.
    Example:
        file_name = 'Clients'
        file_number = qm.Open(file_name)
    """

    func = __qm_lib.QMOpenW
    func.argtypes = [ct.c_wchar_p]
    return func(filename)


# ======================================================================
# QMOpenSeq()
# ======================================================================
def OpenSeq(filename, id, modes):
    """
    The OpenSeq() function opens an item in a directory file for
    sequential (line by line) processing. It is analogous to the
    QMBasic OPENSEQ statement.
    The function returns the file number to be used in other sequential
    file operations.
    """

    func = __qm_lib.QMOpenSeqW
    func.argtypes = [ct.c_wchar_p, ct.c_wchar_p, ct.c_int]
    return func(filename, id, modes)


# ======================================================================
# QMPoolIdle
# ======================================================================
def PoolIdle():
    """
    The PoolIdle() function puts the server process into an idle state
    if it was established by use of ConnectPool(). Subsequent use of
    ConnectPool() with the same details will re-awaken the process.
    """

    __qm_lib.QMPoolIdle()


# ======================================================================
# QMRead()
# ======================================================================
def Read(fno, id):
    """
    The Read() function reads a record without locking. It is
    analogous to the QMBasic READ statement.

    The Read() function requests the server to return the record
    with key Id from the file opened as fno (File Number).

    The funtion returns two values as in this example:
       data, err = qm.Read(fno, id)
    where
       data is the record as a dynamic array
       err  is non-zero if an error occurred. The Status() function can
            be used to find further details of the error.
    """

    func = __qm_lib.QMReadW
    func.argtypes = [ct.c_int, ct.c_wchar_p, ct.c_void_p]
    func.restype = ct.c_void_p
    err = ct.c_int()
    s = func(fno, id, ct.byref(err))
    rec = ct.wstring_at(s)
    __QMFree(s)
    return rec, err.value


# ======================================================================
# QMReadBlk()
# ======================================================================
def ReadBlk(fno, len):
    """
    The ReadBlk() function reads a specified number of bytes from a
    file opened with OpenSeq().

    The funtion returns two values as in this example:
       data, err = qm.ReadBlk(fno, 100)
    where
       data is the data
       err  is non-zero if an error occurred. The Status() function can
            be used to find further details of the error.
    """

    func = __qm_lib.QMReadBlkW
    func.argtypes = [ct.c_int, ct.c_int]
    func.restype = ct.c_void_p
    err = ct.c_int()
    s = func(fno, len, ct.byref(err))
    rec = ct.wstring_at(s)
    __QMFree(s)
    return rec, err.value


# ======================================================================
# QMReadl()
# ======================================================================
def Readl(fno, id, wait):
    """
    The Readl() function reads a record, applying a read lock. It is
    analogous to the QMBasic READL statement.

    The Readl() function requests the server to return the record
    with key Id from the file opened as fno (File Number).

    The funtion returns two values as in this example:
       data, err = qm.Readl(fno, id)
    where
       data is the record as a dynamic array
       err  is non-zero if an error occurred. The Status() function can
            be used to find further details of the error.
    """

    func = __qm_lib.QMReadlW
    func.argtypes = [ct.c_int, ct.c_wchar_p, ct.c_int, ct.c_void_p]
    func.restype = ct.c_void_p
    err = ct.c_int()
    s = func(fno, id, wait, ct.byref(err))
    rec = ct.wstring_at(s)
    __QMFree(s)
    return rec, err


# ======================================================================
# QMReadList()
# ======================================================================
def ReadList(listno):
    """
    The ReadList() function reads a select list into a dynamic
    array in the client application. It is analogous to the
    QMBasic READLIST statement.

    If successful, the function returns the list of records as a field
    mark delimited dynamic array. An empty string is returned if the
    list is empty.
    """

    func = __qm_lib.QMReadListW
    func.argtypes = [ct.c_int]
    func.restype = ct.c_void_p
    s = func(listno)
    if s is None: return ""
    rec = ct.wstring_at(s)
    __QMFree(s)
    return rec


# ======================================================================
# QMReadNext()
# ======================================================================
def ReadNext(listno):
    """
    The ReadNext() function retrieves next entry from a select list.
    It is analogous to the QMBasic READNEXT statement. An empty
    string is returned when the list is exhausted.
    """

    func = __qm_lib.QMReadNextW
    func.argtypes = [ct.c_int]
    func.restype = ct.c_void_p
    s = func(listno)
    if s is None: return ""
    rec = ct.wstring_at(s)
    __QMFree(s)
    return rec


# ======================================================================
# QMReadSeq()
# ======================================================================
def ReadSeq(fno):
    """
    The ReadSeq() function reads the next line from a file opened for
    sequential processing by use of OpenSeq().

    The funtion returns two values as in this example:
       data, err = qm.ReadSeq(fno)
    where
       data is the text read from the file
       err  is non-zero if an error occurred. The Status() function can
            be used to find further details of the error.
    """

    func = __qm_lib.QMReadSeqW
    func.argtypes = [ct.c_int, ct.c_void_p]
    func.restype = ct.c_void_p
    err = ct.c_int()
    s = func(fno, ct.byref(err))
    rec = ct.wstring_at(s)
    __QMFree(s)
    return rec, err.value


# ======================================================================
# QMReadu()
# ======================================================================
def Readu(fno, id, wait):
    """
    The Readu() function reads a record, applying an update lock. It is
    analogous to the QMBasic READU statement.

    The Readu() function requests the server to return the record
    with key Id from the file opened as fno (File Number).

    The funtion returns two values as in this example:
       data, err = qm.Read(fno, id)
    where
       data is the record as a dynamic array
       err  is non-zero if an error occurred. The Status() function can
            be used to find further details of the error.
    """

    func = __qm_lib.QMReaduW
    func.argtypes = [ct.c_int, ct.c_wchar_p, ct.c_int, ct.c_void_p]
    func.restype = ct.c_void_p
    err = ct.c_int()
    s = func(fno, id, wait, ct.byref(err))
    rec = ct.wstring_at(s)
    __QMFree(s)
    return rec, err.value

# ======================================================================
# QMRecordlock()
# ======================================================================
def Recordlock(fno, id, update, wait):
    """
    The Recordlock() function locks a record. It is analogous
    to the QMBasic RECORDLOCKL and RECORDLOCKU statements.

    fno     is the file number returned by a previous Open() call.

    id      is the id of the record to be locked.

    update  is a Boolean value specifying the type of lock to be
            obtained:
               1 i.e. True   Update lock
               0 i.e. False  Shareable read lock

    wait    is a Boolean value indicating the action to be taken if
            the record is currently locked by another user:
               1 i.e. True  Wait for the record to become available
               0 i.e False  Return an error code of SV_LOCKED
    """

    func = __qm_lib.QMRecordlockW
    func.argtypes = [ct.c_int, ct.c_wchar_p, ct.c_int, ct.c_int]
    func(fno, id, update, wait)


# ======================================================================
# QMRecordlocked()
# ======================================================================
def Recordlocked(fno, id):
    """
    The Recordlocked() function queries the lock on a record.
    It is analogous to the QMBasic RECORDLOCKED() function.

    fno  is the file number returned by a previous qm.Open call.

    id   is the id of the locked record.

    The returned value is:
        -3     Another user holds a file lock
        -2     Another user holds an update lock
        -1     Another user holds a read lock
         0     The record is not locked
         1     This user holds a read lock
         2     This user holds an update lock
         3     This user holds a file lock
    """

    func = __qm_lib.QMRecordlockedW
    func.argtypes = [ct.c_int, ct.c_wchar_p]
    return func(fno, id)


# ======================================================================
# QMRelease()
# ======================================================================
def Release(fno, id):
    """
    The QMRelease() function releases a record lock. It is analogous to
    the QMBasic RELEASE statement.

    fno  is the file number returned by a previous qm.Open call.
         If zero, all locks are released.

    id   is the id of the record to be unlocked.
         If given as a null string, all locks in the file identified
         by fno are released.
    """

    func = __qm_lib.QMReleaseW
    func.argtypes = [ct.c_int, ct.c_wchar_p]
    func(fno, id)


# ======================================================================
# QMReplace()
# ======================================================================
def Replace(in_str, f, v, sv, new_data):
    """
    The Replace() function replaces the content of a field,
    value or subvalue in a dynamic array. It is analogous
    to the QMBasic REPLACE() function.

    Replace() is executed locally, not on the server.

    in_str   is the dynamic array to be processed

    f        is the number of the field to be replaced. If zero,
             1 is assumed. If negative, a new field is appended to
             the dynamic array.

    v        is the number of the value to be replaced. If zero,
             the entire field is inserted. If negative, a new value
             is appended to the specified field.

    sv       is the number of the subvalue to be replaced. If zero,
             the entire value is inserted. If negative, a new subvalue
             is appended to the specified value.

    new_data is the new data to form the new dynamic array element.

    The Replace() function returns a new dynamic array with
    the specified field, value or subvalue replaced.

    Example:
        last_name = 'Jones'
        first_name = 'Al'
        street = '824 Wisky Rd'
        city = 'Greenville'
        state = 'SC'

        data = ""
        data = qm.Replace(data, 1, 0, 0, last_name)
        data = qm.Replace(data, 2, 0, 0, first_name)
        data = qm.Replace(data, 3, 0, 0, street)
        data = qm.Replace(data, 4, 0, 0, city)
        data = qm.Replace(data, 5, 0, 0, state)
    """

    __LoadQMCliLib()
    func = __qm_lib.QMReplaceW
    func.argtypes = [ct.c_wchar_p, ct.c_int, ct.c_int, ct.c_int, ct.c_wchar_p]
    func.restype = ct.c_void_p
    s = func(in_str, f, v, sv, new_data)
    out_str = ct.wstring_at(s)
    __QMFree(s)
    return out_str


# ======================================================================
# QMRespond()
# ======================================================================
def Respond(response):
    """
    The Respond() function provides a response to a command initiated
    with the Execute() function that is now waiting for data.

    The function returns two items, for example,
       data, err = qm.Respond("Y")
    where
       data is the output from the command as a field mark delimited
            string in which each field corresponds to a line of output.

       err  is  SV_OK (0)      if the command completed execution
                SV_PROMPT (5)  if the command is waiting for further
                               data input
    """

    func = __qm_lib.QMRespondW
    func.argtypes = [ct.c_wchar_p]
    func.restype = ct.c_void_p
    err = ct.c_int()
    s = func(response, ct.byref(err))
    out_str = ct.wstring_at(s)
    __QMFree(s)
    return out_str, err.value


# ======================================================================
# QMRevision()
# ======================================================================
def Revision():
    """
    The Revision() function returns the revision level of the
    client and server components.

    If successful, the function returns a field mark delimited
    dynamic array in which the first field is the client revision
    and the second field is the server revision.
    """

    func = __qm_lib.QMRevisionW
    func.restype = ct.c_void_p
    s = func()
    out_str = ct.wstring_at(s)
    __QMFree(s)
    return out_str


# ======================================================================
# QMRTrans()
# ======================================================================
def RTrans(listno):
    """
    The RTrans() function is analogous to the QMBasic RTRANS() function,
    fetching data from a specified file.
    """

    func = __qm_lib.QMRTransW
    func.argtypes = [ct.c_wchar_p, ct.c_wchar_p, ct.c_wchar_p, ct.c_wchar_p]
    func.restype = ct.c_void_p
    s = func(listno)
    if s is None: return ""
    rec = ct.wstring_at(s)
    __QMFree(s)
    return rec


# ======================================================================
# QMSeek()
# ======================================================================
def Seek(fno, offset, relto):
    """
    The Seek() function positions in a file opened for sequential
    processing using OpenSeq().

    fno     is the file number returned by OpenSeq()

    offset  is the byte offset required

    relto   identifies where offset is relative to.
            0 = start of file
            1 = current position
            2 = end of file
    """

    func = __qm_lib.QMSeek
    func.argtypes = [ct.c_int, ct.c_int, ct.c_int]
    func(fno, offset, relto)


# ======================================================================
# QMSelect()
# ======================================================================
def Select(fno, listno):
    """
    The Select() function generates a select list containing the
    ids of all records in a file. It is analogous to use of the
    QMBasic SELECT statement.
    """

    func = __qm_lib.QMSelect
    func.argtypes = [ct.c_int, ct.c_int]
    func(fno, listno)


# ======================================================================
# QMSelectIndex()
# ======================================================================
def SelectIndex(fno, index, value, listno):
    """
    The SelectIndex() function generates a select list from an
    alternate key index. It is analogous to use of the QMBasic
    SELECTINDEX statement.
    """

    func = __qm_lib.QMSelectIndexW
    func.argtypes = [ct.c_int, ct.c_wchar_p, ct.c_wchar_p, ct.c_int]
    func(fno, index, value, listno)


# ======================================================================
# QMSelectLeft()
# ======================================================================
def SelectLeft(fno, index, listno):
    """
    The SelectLeft() function moves one position left in an alternate
    key index, builds a select list of items with the associated
    indexed value and returns the indexed value as its result.
    """

    func = __qm_lib.QMSelectLeftW
    func.argtypes = [ct.c_int, ct.c_wchar_p, ct.c_int]
    s = func(fno, index, listno)
    out_str = ct.wstring_at(s)
    __QMFree(s)
    return out_str


# ======================================================================
# QMSelectPartial()
# ======================================================================
def SelectPartial(fno, listno):
    """
    The SelectPartial() function commences a select operation, creating
    a select list with the first batch of record keys. Once this list is
    exhausted, use of NextPartial will build a list of the next batch
    of record keys.
    """

    func = __qm_lib.QMSelectPartialW
    func.argtypes = [ct.c_int, ct.c_int]
    s = func(fno, listno)
    out_str = ct.wstring_at(s)
    __QMFree(s)
    return out_str


# ======================================================================
# QMSelectRight()
# ======================================================================
def SelectRight(fno, index, listno):
    """
    The SelectRight() function moves one position right in an alternate
    key index, builds a select list of items with the associated
    indexed value and returns the indexed value as its result.
    """

    func = __qm_lib.QMSelectRightW
    func.argtypes = [ct.c_int, ct.c_wchar_p, ct.c_int]
    s = func(fno, index, listno)
    out_str = ct.wstring_at(s)
    __QMFree(s)
    return out_str


# ======================================================================
# QMSet()
# ======================================================================
def Set(objno, name, argct, arg1=None, arg2=None, arg3=None, arg4=None,
        arg5=None, arg6=None, arg7=None, arg8=None, arg9=None, arg10=None,
        arg11=None, arg12=None, arg13=None, arg14=None, arg15=None,
        arg16=None, arg17=None, arg18=None, arg19=None, arg20=None):
    """
    The Set() function executes a public subroutine or updates the
    value of a public variable in a QMBasic class module instance.

    objno  is the object number returned by an earlier CreateObject().

    name   is the name of the public item.

    argct  is the count of arguments (max 20).
    """

    func = __qm_lib.QMSetW
    func.argtypes = [ct.c_short, ct.c_wchar_p, ct.c_short,
                     ct.c_wchar_p, ct.c_wchar_p, ct.c_wchar_p, ct.c_wchar_p,
                     ct.c_wchar_p, ct.c_wchar_p, ct.c_wchar_p, ct.c_wchar_p,
                     ct.c_wchar_p, ct.c_wchar_p, ct.c_wchar_p, ct.c_wchar_p,
                     ct.c_wchar_p, ct.c_wchar_p, ct.c_wchar_p, ct.c_wchar_p,
                     ct.c_wchar_p, ct.c_wchar_p, ct.c_wchar_p, ct.c_wchar_p]
    func(objno, name, argct, arg1, arg2, arg3, arg4, arg5, arg6, arg7,
         arg8, arg9, arg10, arg11, arg12, arg13, arg14, arg15, arg16,
         arg17, arg18, arg19, arg20)


# ======================================================================
# QMSetLeft()
# ======================================================================
def SetLeft(fno, index):
    """
    The SetLeft() function sets the scan position of an alternate
    key index to be at the leftmost record.
    """

    func = __qm_lib.QMSetLeftW
    func.argtypes = [ct.c_int, ct.c_wchar_p]
    func(fno, index)


# ======================================================================
# QMSetRight()
# ======================================================================
def SetRight(fno, index):
    """
    The SetRight() function sets the scan position of an alternate
    key index to be after the rightmost record.
    """

    func = __qm_lib.QMSetRightW
    func.argtypes = [ct.c_int, ct.c_wchar_p]
    func(fno, index)


# ======================================================================
# QMSetSession()
# ======================================================================
def SetSession(session):
    """
    A program can make simultaneous connections to multiple QM servers.
    The qm.SetSession() function allows the client to select which
    session other QMClient functions will use.
    See also: qm.GetSession()
    """

    __LoadQMCliLib
    func = __qm_lib.QMSetSession
    func.argtypes = [ct.c_int]
    return func(session)


# ======================================================================
# QMStatus()
# ======================================================================
def Status():
    """
    The Status() function returns the value of the QMBasic STATUS()
    function for the last server function executed.
    """

    return __qm_lib.QMStatus()


# ======================================================================
# QMSystem()
# ======================================================================
def System(key):
    """
    The System() function returns information dependent on a supplied
    key value. The result is always returned as a string. It is analogous
    to the QMBasic SYSTEM() function.
    """

    func = __qm_lib.QMSystemW
    func.argtypes = [ct.c_int]
    func.restype = ct.c_void_p
    s = func(key)
    if s is None: return ""
    rec = ct.wstring_at(s)
    __QMFree(s)
    return rec


# ======================================================================
# QMTrans()
# ======================================================================
def Trans(listno):
    """
    The Trans() function is analogous to the QMBasic TRANS() function,
    fetching data from a specified file.
    """

    func = __qm_lib.QMTransW
    func.argtypes = [ct.c_wchar_p, ct.c_wchar_p, ct.c_wchar_p, ct.c_wchar_p]
    func.restype = ct.c_void_p
    s = func(listno)
    if s is None: return ""
    rec = ct.wstring_at(s)
    __QMFree(s)
    return rec


# ======================================================================
# QMTrapCallAbort()
# ======================================================================
def TrapCallAbort(mode):
    """
    The TrapCallAbort() function enables or disables client side
    trapping of aborts in actions performed on the server.
    """

    __LoadQMCliLib
    func = __qm_lib.QMTrapCallAbort
    func.argtypes = [ct.c_int]
    func(mode)


# ======================================================================
# QMTxn()
# ======================================================================
def Txn(mode):
    """
    The TXN() function performs transactional operations on the server.
    Values of the mode argument are:
      1   Start a transaction
      2   Commit a durable transaction
      3   Abort a transaction
      4   Commit a non-durable transaction
    """

    func = __qm_lib.QMTxn
    func.argtypes = [ct.c_int]
    func(mode)


# ======================================================================
# QMWeofSeq()
# ======================================================================
def WeofSeq(fno):
    """
    The WeofSeq() function truncates a sequential file at its
    current position.
    """

    func = __qm_lib.QMWeofSeq
    func.argtypes = [ct.c_int]
    func(fno)


# ======================================================================
# QMWrite()
# ======================================================================
def Write(fno, id, data):
    """
    The Write() function writes a record. This is analogous
    to the QMBasic WRITE statement.

    The arguments are:
      fno    The file number returned from an earlier use of QMOpen().
      id     The record id.
      data   The data to be written.

    If the record already exists, it is replaced. If the record does
    not already exist, it is added.

    An application should always obtain an update lock on a record
    before writing it. This function releases the lock.

    Example:
        id = '102'
        last_name = 'Jones'
        first_name = 'Al'
        street = '824 Wisky Rd'
        city = 'Greenville'
        state = 'SC'

        data = ""
        data = qm.Replace(data, 1, 0, 0, last_name)
        data = qm.Replace(data, 2, 0, 0, first_name)
        data = qm.Replace(data, 3, 0, 0, street)
        data = qm.Replace(data, 4, 0, 0, city)
        data = qm.Replace(data, 5, 0, 0, state)

        qm.Write(file_number, id, data)
    """

    func = __qm_lib.QMWriteW
    func.argtypes = [ct.c_int, ct.c_wchar_p, ct.c_wchar_p]
    func(fno, id, data)


# ======================================================================
# QMWriteBlk()
# ======================================================================
def WriteBlk(fno, data, len):
    """
    The WriteBlk() function writes data of a given length to a file
    opened for sequential processing.
    """

    func = __qm_lib.QMWriteBlk
    func.argtypes = [ct.c_int, ct.c_wchar_p, ct.c_int]
    func(fno, data, len)


# ======================================================================
# QMWriteSeq()
# ======================================================================
def WriteSeq(fno, data):
    """
    The WriteBlk() function writes a line of text to a file opened
    for sequential processing.
    """

    func = __qm_lib.QMWriteSeq
    func.argtypes = [ct.c_int, ct.c_wchar_p]
    func(fno, data)


# ======================================================================
# QMWriteSeqKey()
# ======================================================================
def WriteSeqKey(fno, data):
    """
    The WriteSeqKey() function writes a record using an automatically
    generated sequential record id. This is analogous to the QMBasic
    WRITE statement with the CREATING.SEQKEY option.

    The arguments are:
      fno    The file number returned from an earlier use of QMOpen().
      data   The data to be written.

    If the record already exists, it is replaced. If the record does
    not already exist, it is added.

    The function returns the record id generated for this write.
    """

    func = __qm_lib.QMWriteSeqKey
    func.argtypes = [ct.c_int, ct.c_wchar_p]
    s = func(fno, data)
    out_str = ct.wstring_at(s)
    __QMFree(s)
    return out_str


# ======================================================================
# QMWriteu()
# ======================================================================
def Writeu(fno, id, data):
    """
    The Writeu() function writes a record, keeping the record lock.
    This is analogous to the QMBasic WRITEU statement.

    The arguments are:
      fno    The file number returned from an earlier use of QMOpen().
      id     The record id.
      data   The data to be written.

    If the record already exists, it is replaced. If the record does
    not already exist, it is added.

    An application should always obtain an update lock on a record
    before writing it.

    Example:
        id = '102'
        last_name = 'Jones'
        first_name = 'Al'
        street = '824 Wisky Rd'
        city = 'Greenville'
        state = 'SC'

        data = ""
        data = qm.Replace(data, 1, 0, 0, last_name)
        data = qm.Replace(data, 2, 0, 0, first_name)
        data = qm.Replace(data, 3, 0, 0, street)
        data = qm.Replace(data, 4, 0, 0, city)
        data = qm.Replace(data, 5, 0, 0, state)

        qm.Writeu(file_number, id, data)
    """

    func = __qm_lib.QMWriteuW
    func.argtypes = [ct.c_int, ct.c_wchar_p, ct.c_wchar_p]
    func(fno, id, data)


if __name__ == '__main__':
    pass

