import os
from datetime import datetime
from datetime import timedelta
import pyodbc
from registry_stuff import get_connect_string as re
conn_string = re()
print('Connection String : ', str(conn_string))


def anony(ds):
    cnxn = pyodbc.connect(conn_string)
    cursor = cnxn.cursor()
    cursor.execute("SELECT * FROM dbo.RADAI with(nolock) Where Accession = ?", ds.AccessionNumber)
    rows = cursor.fetchall()
    for row in rows:
        print(str(row).replace(' ', ''))
    cnxn.close()

    def person_names_callback(ds, data_element):
        if data_element.VR == "PN":
            data_element.value = "anonymous"
    ds.walk(person_names_callback)

    def curves_callback(ds, data_element):
        if data_element.tag.group & 0xFF00 == 0x5000:
            del ds[data_element.tag]
    ds.walk(curves_callback)

    if 'OtherPatientIDs' in ds:
        delattr(ds, 'OtherPatientIDs')

    if 'OtherPatientIDsSequence' in ds:
        del ds.OtherPatientIDsSequence

    def validate(date_text):
        try:
            if date_text == datetime.strptime(date_text, '%Y%m%d'):
                raise ValueError
            return "True1"
        except ValueError:
            return False
        try:
            if date_text == datetime.strptime(date_text, "%Y%m%d%H%M%S.%f"):
                raise ValueError
            return "True2"
        except ValueError:
            return False

        try:
            if date_text == datetime.strptime(date_text, "%Y%m%d%H%M%S"):
                raise ValueError
            return "True3"
        except ValueError:
            return False

# code to adjust all date in dcm file
    def all_date_time_adjust(ds, data_element):
        if data_element.VR == "DT" or data_element.VR == "DA":
            if validate(str(data_element.value)) == "True1":
                data_element.value = datetime.strptime(data_element.value, "%Y%m%d")
                data_element.value = data_element.value - timedelta(days=224)
            if validate(str(data_element.value)) == "True2":
                data_element.value = datetime.strptime(data_element.value, "%Y%m%d%H%M%S.%f")
                data_element.value = data_element.value - timedelta(days=224)
            if validate(str(data_element.value)) == "True3":
                data_element.value = datetime.strptime(data_element.value, "%Y%m%d%H%M%S.%f")
                data_element.value = data_element.value - timedelta(days=224)

    ds.walk(all_date_time_adjust)
    ds.remove_private_tags()

# anonymizing random DICOM Tags that have a conflicting VR
    try:
        ds.PatientID = row.Patient_Id
    except:
        ds.PatientID = "didnotwork"
    try:
        ds.AccessionNumber = row.Result_Id
    except:
        ds.AccessionNumber = "didnotwork"

    ds.InstitutionName = "Anonymous"
    ds.InstitutionAddress = "Anonymous"
    ds.PatientAddress = "Anonymous"
    ds.PatientPhoneNumber = "Anonymous"
    ds.PatientsMothersBirthName = "Anonymous"
    ds.StationName = "Anonymous"
    ds.PatientTelephoneNumbers = "Anonymous"
    ds.IssuerOfPatientID = "Anonymous"
    return ds



