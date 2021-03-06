import pyodbc
import Views
from registry_stuff import get_connect_string as re
conn_string = re()
print('Connection String : ', str(conn_string))


def add_device(Device_Name, IP, Port, AE, Max_Threads):
    """This adds the device to the DB.  It is called in the Views.py file by Devices.add_device"""
    cnxn = pyodbc.connect(conn_string)
    cursor = cnxn.cursor()
    cursor.execute('INSERT INTO [VALID8].[dbo].[DSTools_Devices] (Device_Name, IP, Port, AE, Max_Threads) '
                   'VALUES (?, ?, ?, ?, ?)', Device_Name, IP, Port, AE, Max_Threads)
    cnxn.commit()
    cnxn.close()


def get_list():
    """Grabs the devices from the DB. Uses return to pass the list of strings to _build_Tree in the Views.py file"""
    _list = ()
    cnxn = pyodbc.connect(conn_string)
    cursor = cnxn.cursor()
    cursor.execute('SELECT ID, Device_name, IP, PORT, AE, MAX_THREADS '
                   'FROM [VALID8].[dbo].[DSTools_Devices]with(nolock)')
    rows = cursor.fetchall()
    result = []
    for row in rows:
        ids = str(row[0])
        name = row[1]
        ip = row[2]
        port = str(row[3])
        ae = row[4]
        threads = str(row[5])
        _list = (ids, name, ip, port, ae, threads)
        result.append(_list)
    cnxn.close()
    return result


def remove_device(row_id):
    """Passed row_id from Views.py get_item func. It then passes the row_id number to the SQL query to remove the
        device when that button is clicked."""
    cnxn = pyodbc.connect(conn_string)
    cursor = cnxn.cursor()
    cursor.execute('DELETE FROM [VALID8].[dbo].[DSTools_Devices] WHERE ID = ?', row_id)
    cnxn.commit()
    cnxn.close()


def anony_config():
    """Gets the config from the  Anony_config table in the DB."""
    cnxn = pyodbc.connect(conn_string)
    cursor = cnxn.cursor()
    cursor.execute('SELECT local_AE, local_PORT, local_MAX_threads '
                   'FROM [VALID8].[dbo].[DSTools_Config]')
    rows = cursor.fetchall()
    cnxn.close()
    for row in rows:
        print(str(row).replace(' ', ''))
    config_local_AE = str(row.local_AE.replace(' ', ''))
    config_local_port = row.local_PORT
    config_threads = row.local_MAX_threads
    anon_list = [config_local_AE, config_threads, config_local_port]
    return anon_list


def update_anony_config(local_AE, local_PORT,
                        local_MAX_threads):
    """ Updates the anony config DB. Called in the Views.py Class Anonymize."""
    cnxn = pyodbc.connect(conn_string)
    cursor = cnxn.cursor()
    cursor.execute('UPDATE [VALID8].[dbo].[DSTools_Config] '
                   'SET local_AE=?, local_PORT=?, local_MAX_threads=? WHERE ID = ?', local_AE, local_PORT,
                   local_MAX_threads, 1)
    cnxn.commit()
    cnxn.close()


def get_rules():
    """ Queries the DSTools_Rules DB for the active rules"""
    _list = ()
    cnxn = pyodbc.connect(conn_string)
    cursor = cnxn.cursor()
    cursor.execute('SELECT ID, _Source, _Rule, _Destination, Active, Anony '
                   'FROM [VALID8].[dbo].[DSTools_Rules]with(nolock);')
    rows = cursor.fetchall()
    result = []
    print(rows)
    for row in rows:
        ids = row[0]
        _source = row[1]
        _rule = str(row[2])
        _destination = row[3]
        active = str(row[4])
        anony = str(row[5])
        _list = (ids, _source, _rule, _destination, active, anony)
        result.append(_list)
    cnxn.close()
    return result


def remove_rule(row_id):
    """Passed row_id from Views.py remove_rule func. It then passes the row_id number to the SQL query to remove the
        device when the button is clicked."""
    cnxn = pyodbc.connect(conn_string)
    cursor = cnxn.cursor()
    cursor.execute('DELETE FROM [VALID8].[dbo].[DSTools_Rules] WHERE ID = ?', row_id)
    cnxn.commit()
    cnxn.close()


def activate_rule(row_id):
    """Activates rule by changing the True/False in the DB table.  Called in Views.py by class Rules"""
    cnxn = pyodbc.connect(conn_string)
    cursor = cnxn.cursor()
    cursor.execute('UPDATE [VALID8].[dbo].[DSTools_Rules] '
                   'SET Active = ? WHERE ID = ?', 'True', row_id)
    cnxn.commit()
    cnxn.close()


def deactivate_rule(row_id):
    """Same as, Activates rule by changing the True/False in the DB table, but opposite.
    Called in Views.py by class Rules"""
    cnxn = pyodbc.connect(conn_string)
    cursor = cnxn.cursor()
    cursor.execute('UPDATE [VALID8].[dbo].[DSTools_Rules] '
                   'SET Active = ? WHERE ID = ?', 'False', row_id)
    cnxn.commit()
    cnxn.close()


def add_rules(source, rule, destination, active, anony):
    """ Adds the rules to the rules DB.  Called in Views.py by the add_rules button"""
    cnxn = pyodbc.connect(conn_string)
    cursor = cnxn.cursor()
    cursor.execute('INSERT INTO [VALID8].[dbo].[DSTools_Rules] (_Source, _Rule, _Destination, Active, Anony) '
                   'VALUES (?, ?, ?, ?, ?)', source, rule, destination, active, anony)
    cnxn.commit()
    cnxn.close()


def get_dest_ip(receiveip):
    _list = ()
    print('ReceiveIp in SQL', receiveip)
    cnxn = pyodbc.connect(conn_string)
    cursor = cnxn.cursor()
    cursor.execute('SELECT _Destination FROM [VALID8].[dbo].[DSTools_Rules] with(nolock) Where _Source = ?', receiveip)
    rows = cursor.fetchall()
    result = []
    print(rows)
    for row in rows:
        port = row[0]
        _list = port
        result.append(_list)
    cnxn.close()
    print('This is the result from SQL', result)
    return result


def get_active_rules(receiveip):
    """ Queries the DSTools_Rules DB for the active rules"""
    _list = ()
    cnxn = pyodbc.connect(conn_string)
    cursor = cnxn.cursor()
    cursor.execute('SELECT ID, _Source, _Rule, _Destination, Active, Anony '
                   'FROM [VALID8].[dbo].[DSTools_Rules] with(nolock) where Active = ? and _source = ?', 'True', receiveip)
    rows = cursor.fetchall()
    result = []
    print(rows)
    for row in rows:
        ids = row[0]
        _source = row[1]
        _rule = str(row[2])
        _destination = row[3]
        active = str(row[4])
        anony = str(row[5])
        _list = (ids, _source, _rule, _destination, active, anony)
        result.append(_list)
    cnxn.close()
    return result
