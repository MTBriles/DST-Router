from pydicom.dataset import Dataset
from pynetdicom3 import (
    AE,
    StoragePresentationContexts,
    PYNETDICOM_IMPLEMENTATION_UID,
    PYNETDICOM_IMPLEMENTATION_VERSION
)

import multiprocessing
from SQL import anony_config, get_list

# Initialise the Application Entity and specify the listen port
anon_list = anony_config()
print('LocaL AE: ', anon_list[5])
print('MAX_threads : ', anon_list[6])
print('local_PORT: ', anon_list[7])
config_local_AE = anon_list[5]
config_MAX_threads = anon_list[6]
config_local_PORT = int(anon_list[7])

ae = AE(ae_title=config_local_AE, port=int(config_local_PORT))
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
    print('Called AE is: ', AE.ae_title)
    called_ae = str(AE.ae_title)
    print(called_ae)
    dest_dev_list = get_list()
    print(dest_dev_list[3])
    print('Slot 0', dest_dev_list[3][0])
    print('Slot 1', dest_dev_list[3][1])
    print('Slot 2', dest_dev_list[3][2])
    print('Slot 3', dest_dev_list[3][3])
    print('Slot 4', dest_dev_list[3][4])
    print('Slot 4', dest_dev_list[3][5])

    config_dest_IP = dest_dev_list[3][2]
    config_dest_PORT = int(dest_dev_list[3][3])
    config_dest_MAX_Threads = int(dest_dev_list[3][5])
    print('dest_PORT: ', config_dest_PORT)
    #print(ds)

    assoc = ae.associate(config_dest_IP, config_dest_PORT)
    assoc.maximum_associations = config_dest_MAX_Threads
    assoc.NumberOfActiveAssociations = config_dest_MAX_Threads
    if assoc.is_established:
        status = assoc.send_c_store(ds)
        print(status)

    assoc.release()
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
