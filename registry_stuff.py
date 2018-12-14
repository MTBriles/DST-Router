from winreg import *


def get_connect_string():
    print(r"*** Reading from SOFTWARE\DSTools ***")
    aReg = ConnectRegistry(None, HKEY_LOCAL_MACHINE)

    try:
        aKey = OpenKey(aReg, r"SOFTWARE\DSTools")
    except:
        aKey = CreateKey(aReg, r"SOFTWARE\DSTools")
    CloseKey(aKey)
    for i in range(1024):
        try:
            n, v, t = EnumValue(aKey, i)
            print(i, n, v, t)
        except EnvironmentError:
            print("You have", i, " tasks starting at logon...")
            break

    print(r"*** Writing to SOFTWARE\DSTools ***")
    aKey = OpenKey(aReg, r"SOFTWARE\DSTools", 0, KEY_ALL_ACCESS)
    try:
        reg_conn_str = str(QueryValueEx(aKey, 'conn_string'))
    except:
        try:
            SetValueEx(aKey, "conn_string", 0, REG_SZ,
                   'Driver={SQL Server};Server=CPSQL1;Database=Valid8;Trusted_Connection=yes;')
        except EnvironmentError:
            print("Encountered problems writing into the Registry...")
    print(reg_conn_str)
    reg_conn_str = reg_conn_str.replace("', 1)", "").replace("('", "")

    CloseKey(aKey)

    CloseKey(aReg)
    return reg_conn_str
