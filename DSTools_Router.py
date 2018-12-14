from pydicom.dataset import Dataset
from pynetdicom3 import (
    AE,
    StoragePresentationContexts,
    PYNETDICOM_IMPLEMENTATION_UID,
    PYNETDICOM_IMPLEMENTATION_VERSION
)

from pydicom.uid import (
    ExplicitVRLittleEndian, ImplicitVRLittleEndian, ExplicitVRBigEndian)

from pynetdicom3.sop_class import VerificationSOPClass
import multiprocessing
from SQL import anony_config, get_list, get_rules, get_dest_ip
#import logging

#LOGGER = logging.getLogger('pynetdicom3')
#LOGGER.setLevel(logging.DEBUG)

# Initialise the Application Entity and specify the listen port
anon_list = anony_config()
print('LocaL AE: ', anon_list[0])
print('MAX_threads : ', anon_list[1])
print('local_PORT: ', anon_list[2])
config_local_AE = anon_list[0]
config_MAX_threads = anon_list[1]
config_local_PORT = int(anon_list[2])

ae = AE(ae_title=config_local_AE, port=int(config_local_PORT))
ae.supported_contexts = StoragePresentationContexts
ae.maximum_associations = config_MAX_threads
ae.NumberOfActiveAssociations = config_MAX_threads

ae.add_supported_context(VerificationSOPClass)


def on_c_echo(context, info):
    """Respond to a C-ECHO service request.

    Parameters
    ----------
    context : namedtuple
        The presentation context that the verification request was sent under.
    info : dict
        Information about the association and verification request.

    Returns
    -------
    status : int or pydicom.dataset.Dataset
        The status returned to the peer AE in the C-ECHO response. Must be
        a valid C-ECHO status value for the applicable Service Class as
        either an ``int`` or a ``Dataset`` object containing (at a
        minimum) a (0000,0900) *Status* element.
    """
    return 0x0000


def getsendingae(ds, context, info):
    temp = []
    dictList = []
    for key, value in info.items():
        temp = [key, value]
        dictList.append(temp)
    templist = list(info.values())
    testing = str(templist[0])
    newtesting = testing.split(':')
    newtesting1 = str(newtesting[1])
    newtesting2 = newtesting1.replace("b'", "")
    newtesting3 = newtesting2.replace("', 'called_aet'", "")
    receiveing_ae = newtesting3.replace("}", "")
    return receiveing_ae


def getsendingip(ds, context, info):
    temp = []
    dictList = []
    for key, value in info.items():
        temp = [key, value]
        dictList.append(temp)
    templist = list(info.values())
    testing = str(templist[0])
    newtesting = testing.split(':')
    newtesting1 = str(newtesting[4])
    newtesting2 = newtesting1.replace("'", "")
    receiveing_ip = newtesting2.replace("}", "")
    receiveing_ip = receiveing_ip.strip(" ")
    return receiveing_ip


def on_c_store(ds, context, info):
    receiveip = getsendingip(ds, context, info)
    receiveae = getsendingae(ds, context, info)
    print('on c store receiving IP :', receiveip)
    print('on c store receiving AE :', receiveae)
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

    dest_dev_list = get_list()
    print('Slot 0', dest_dev_list[2][0])
    print('Slot 1', dest_dev_list[2][1])
    print('Slot 2', dest_dev_list[2][2])
    print('Slot 3', dest_dev_list[2][3])
    print('Slot 4', dest_dev_list[2][4])
    print('Slot 5', dest_dev_list[2][5])

    for list in dest_dev_list:
        rule_ip = list[2]
        rule_ip = rule_ip.strip(" ")
        if receiveip == rule_ip:
            print('matching ip', rule_ip)
            result = str(get_rules())
            restr = str(''.join(result))
            list = restr.split(",")
            dest_id = list[13]
            print('Trouble Shooting')
            _dest_ip_port = str(get_dest_ip(dest_id))
            _dest_ip_port1 = str(''.join(_dest_ip_port))
            new_list = _dest_ip_port1.split(",")
            rule_dest_ip = new_list[0]
            rule_dest_port = new_list[1]
            rule_dest_ip = rule_dest_ip.replace(" ", "")
            rule_dest_ip = rule_dest_ip.replace("'", "")
            rule_dest_ip = rule_dest_ip.replace("[", "")
            rule_dest_ip = rule_dest_ip.replace("(", "")
            rule_dest_port = rule_dest_port.replace(" ", "")
            rule_dest_port = rule_dest_port.replace(")", "")
            rule_dest_port = rule_dest_port.replace("]", "")

            print(rule_dest_ip)
            print(rule_dest_port)
            config_dest_IP = rule_dest_ip
            config_dest_PORT = int(rule_dest_port)
            config_dest_MAX_Threads = int(dest_dev_list[2][5])
            active_rule_var = list[12]
            active_rule_oper = list[11]
            active_rule_tag = (list[10])
            active_rule_tag = active_rule_tag.replace("'", "")
            active_rule_tag = active_rule_tag.replace(" ", "")
            active_rule_var = active_rule_var.replace("'", "")
            active_rule_var = active_rule_var.replace(" ", "")
            print('Rule Operand', active_rule_oper)
            print('Rule Tag', active_rule_tag)
            print('Rule Var', active_rule_var)
            print(ds.Modality)
            dicom_tag_value = 'test'
            if active_rule_tag == 'modality':
                dicom_tag_value = ds.Modality
            print(active_rule_tag)
            print(active_rule_var)
            if dicom_tag_value == active_rule_var:
                print('testing')
                assoc = ae.associate(config_dest_IP, config_dest_PORT)
                assoc.maximum_associations = config_dest_MAX_Threads
                assoc.NumberOfActiveAssociations = config_dest_MAX_Threads
                # print(assoc)
                if assoc.is_established:
                    # Use the C-STORE service to send the dataset
                    # returns a pydicom Dataset
                    status = assoc.send_c_store(ds)

                    # Check the status of the storage request
                    if 'Status' in status:
                        # If the storage request succeeded this will be 0x0000
                        print('C-STORE request status: 0x{0:04x}'.format(status.Status))
                    else:
                        print('Connection timed out or invalid response from peer')

                    # Release the association
                    assoc.release()
                else:
                    print('Association rejected or aborted')
                ae.remove_requested_context(meta.MediaStorageSOPClassUID)
                # Return a 'Success' status
                return 0x0000

            else:
                print('No Active Rule')


ae.on_c_echo = on_c_echo
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
