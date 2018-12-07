import os
from datetime import datetime
from datetime import timedelta
from pydicom.dataset import Dataset
from pynetdicom3 import (
    AE,
    StoragePresentationContexts,
    PYNETDICOM_IMPLEMENTATION_UID,
    PYNETDICOM_IMPLEMENTATION_VERSION
)

import pyodbc
import time
import multiprocessing

# Initialise the Application Entity and specify the listen port
ae = AE(ae_title=b'ANONYMIZE', port=11113)
ae.supported_contexts = StoragePresentationContexts
ae.maximum_associations = 30
ae.NumberOfActiveAssociations = 30
config_AE = ('test')
cnxn = pyodbc.connect(r'Driver={SQL Server};Server=CPSQL1;Database=Valid8;Trusted_Connection=yes;')
cursor = cnxn.cursor()
cursor.execute("SELECT * FROM dbo.DSTools_Anony_Config with(nolock)")
rows = cursor.fetchall()
for row in rows:
    print(str(row).replace(' ',''))
cnxn.close()
config_AE = str(row.dest_AE.replace(' ',''))
config_port = row.dest_PORT
config_ip = str(row.dest_IP.replace(' ',''))
send_to_dir = str(row.send_to_dir.replace(' ',''))
config_path = str(row.send_to_dir_path.replace(' ',''))


def on_c_store(ds, context, info):

    # Add the DICOM File Meta Information

    meta = Dataset()
    meta.MediaStorageSOPClassUID = ds.SOPClassUID
    meta.MediaStorageSOPInstanceUID = ds.SOPInstanceUID
    meta.ImplementationClassUID = PYNETDICOM_IMPLEMENTATION_UID
    meta.ImplementationVersionName = PYNETDICOM_IMPLEMENTATION_VERSION
    meta.TransferSyntaxUID = context.transfer_syntax

    ae.add_requested_context(meta.MediaStorageSOPClassUID)
    # Add the file meta to the dataset
    ds.file_meta = meta

    # Set the transfer syntax attributes of the dataset
    ds.is_little_endian = context.transfer_syntax.is_little_endian
    ds.is_implicit_VR = context.transfer_syntax.is_implicit_VR

    # Save the dataset using the SOP Instance UID as the filename
    # ds.save_as(ds.SOPInstanceUID, write_like_original=False)

    data_elements = ['PatientID',
                     'PatientBirthDate'
                     ]
    for de in data_elements:
        print(ds.data_element(de))

    cnxn = pyodbc.connect(r'Driver={SQL Server};Server=CPSQL1;Database=Valid8;Trusted_Connection=yes;')
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

    studyUID_path = ds.StudyInstanceUID
    seriesUID_path = ds.SeriesInstanceUID
    os.path.isdir(config_path)

    if 'True' in send_to_dir:

            def check_path_save():
                if os.path.isdir(config_path+'/'+studyUID_path+'/'+seriesUID_path):
                    ds.save_as(config_path+'/'+studyUID_path+'/'+seriesUID_path+'/'+ds.SOPInstanceUID+'.dcm')
                    return True

            def make_path():
                if check_path_save() != True:
                    try:
                        os.mkdir(config_path+'/'+studyUID_path)
                        return True
                    except FileExistsError:
                        os.mkdir(config_path+'/'+studyUID_path+'/'+seriesUID_path)

            def make_path2():
                if make_path() == True:
                    os.mkdir(config_path+'/'+studyUID_path+'/'+seriesUID_path)

            if check_path_save() != True:
                make_path()
                make_path2()

            check_path_save()

    elif 'False' in send_to_dir:

                assoc = ae.associate(config_ip, config_port)
                assoc.maximum_associations = 30
                assoc.NumberOfActiveAssociations = 30
                if assoc.is_established:
                    if ds.SOPClassUID != "1.2.840.10008.5.1.4.1.1.7" and ds.SOPClassUID != "1.2.840.10008.5.1.4.1.1.88.67'" and ds.SOPClassUID != "1.2.840.10008.5.1.4.1.1.11.1":
                        status = assoc.send_c_store(ds)
                    else:
                        assoc.release()

                assoc.release()
                time.sleep(1)
                ae.remove_requested_context(meta.MediaStorageSOPClassUID)
                    # Return a 'Success' status
    return 0x0000





ae.on_c_store = on_c_store

# Start listening for incoming association requests
ae.start()


if __name__ == '__main__':
    service = multiprocessing.Process(name='on_c_store', target=on_c_store)
    worker_1 = multiprocessing.Process(name='Worker1', target=on_c_store)
    worker_2 = multiprocessing.Process(name='Worker2', target=on_c_store)

    worker_1.start()
    worker_2.start()
    service.start()








