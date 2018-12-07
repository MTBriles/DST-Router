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

cnxn = pyodbc.connect(r'Driver={SQL Server};Server=CPSQL1;Database=Valid8;Trusted_Connection=yes;')
cursor = cnxn.cursor()
cursor.execute("SELECT * FROM dbo.DSTools_Router_Config with(nolock)")
rows = cursor.fetchall()
for row in rows:
    print(str(row).replace(' ', ''))
cnxn.close()
config_local_AE = str(row.local_AE.replace(' ', ''))
config_local_PORT = row.local_PORT
config_MAX_threads = row.local_MAX_Threads
config_dest_IP = '10.232.200.22'
config_dest_PORT = 11112
config_dest_MAX_Threads = 30


ae = AE(ae_title=config_local_AE, port=config_local_PORT)
ae.supported_contexts = StoragePresentationContexts
ae.maximum_associations = config_MAX_threads
ae.NumberOfActiveAssociations = config_MAX_threads


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

    assoc = ae.associate(config_dest_IP, config_dest_PORT)
    assoc.maximum_associations = config_dest_MAX_Threads
    assoc.NumberOfActiveAssociations = config_dest_MAX_Threads
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
    