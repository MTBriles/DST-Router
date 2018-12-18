from pydicom.dataset import Dataset
from pynetdicom3 import (
    AE,
    StoragePresentationContexts,
    PYNETDICOM_IMPLEMENTATION_UID,
    PYNETDICOM_IMPLEMENTATION_VERSION
)

from pynetdicom3.sop_class import VerificationSOPClass
from Anonymize import anony
import multiprocessing
from SQL import anony_config, get_list, get_active_rules

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
    return 0x0000


def operand_equal(ds, active_rule_tag, dicom_tag_value):
    print('Activve rule tag in equals to: ', active_rule_tag)

    return dicom_tag_value


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


def get_dicom_tag_value(ds, rule_list3, active_rule_tag):
    if active_rule_tag == 'Modality':
        print('Active Modality Rule value =', ds.Modality)
        dicom_tag_value = ds.Modality
    elif active_rule_tag == 'InstitutionName':
        print('trying to get Institution Name')
        dicom_tag_value = ds.InstitutionName
        print('Active Institution Rule value =', ds.InstitutionName)
    elif active_rule_tag == 'SliceThickness':
        dicom_tag_value = ds.SliceThickness
        print('Active Slice Thickness Rule value =', ds.SliceThickness)
    elif active_rule_tag == 'StudyDescription':
        dicom_tag_value = ds.StudyDescription
        print('Active Study Description Rule value =', ds.StudyDescription)
    elif active_rule_tag == 'SeriesDescription':
        dicom_tag_value = ds.SeriesDescription
        print('Active Study Description Rule value =', ds.SeriesDescription)
    return dicom_tag_value


def check_rule_logic(dicom_tag_value, active_rule_var, active_rule_oper):
    print('Logic', dicom_tag_value, ' ', active_rule_oper, ' ', active_rule_var)
    print('Do logic')
    if active_rule_oper == '=':
        if dicom_tag_value == active_rule_var:
            return True
        else:
            return False
    elif active_rule_oper == '!=':
        if dicom_tag_value != active_rule_var:
            return True
        else:
            return False
    elif active_rule_oper == 'Contains':
        if active_rule_var.find(dicom_tag_value):
            return True
        else:
            return False
    elif active_rule_oper == 'Not Contains':
        if not active_rule_var.find(dicom_tag_value):
            return True
        else:
            return False
    elif active_rule_oper == '<>':
        if int(dicom_tag_value) != int(active_rule_var):
            return True
        else:
            return True
    elif active_rule_oper == '>':
        if int(dicom_tag_value) > int(active_rule_var):
            return True
        else:
            return True
    elif active_rule_oper == '<':
        if int(dicom_tag_value) < int(active_rule_var):
            return True
        else:
            return True
    elif active_rule_oper == '>=':
        if int(dicom_tag_value) >= int(active_rule_var):
            return True
        else:
            return True
    elif active_rule_oper == '<=':
        if int(dicom_tag_value) <= int(active_rule_var):
            return True
        else:
            return True


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
    print('Get Device List from SQL')
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
            result = str(get_active_rules(receiveip))
            restr = str(''.join(result))
            rule_list = restr.split(",")
            rule_list1 = rule_list[1].replace("'", "").replace(" ", "")
            print('Rule list 1 Receiving IP  :', rule_list1)
            rule_list2 = rule_list[2].replace("'", "").replace(" ", "")
            print('Rule list 2  DIcom tag:', rule_list2)
            rule_list3 = rule_list[3].replace("'", "").replace(" ", "")
            print('Rule list 3  Operand:', rule_list3)
            rule_list4 = rule_list[4].replace("'", "").replace(" ", "")
            print('Rule list 4 :', rule_list4)
            rule_list5 = rule_list[5].replace("'", "").replace(" ", "")
            print('Rule list 5 : Desztination IP', rule_list5)
            rule_list6 = rule_list[6].replace("'", "").replace(" ", "")
            print('Rule list 6 :', rule_list6)
            rule_list7 = rule_list[7].replace(")", "").replace(" ", "").replace("]", "").replace("'", "")
            print('Rule list 7 :', rule_list7)
            if rule_list7 == 'True':
                print('Running Anonymizer script')
                anony(ds)
            _dest_ip = rule_list5
            _dest_port = 2222
            print('Destination IP Final : ', _dest_ip)
            for list in dest_dev_list:
                print(list[2].replace("'", "").replace(" ", ""))
                if rule_list5 == list[2].replace("'", "").replace(" ", ""):
                    print('Setting destination Port', int(list[3]))
                    list_dest_port = int(list[3])
                    _dest_port == int(list_dest_port)
                else:
                    print('could not get destination port')
            _dest_port = list_dest_port
            print('Destination PORT Final : ', _dest_port)
            print('Destination PORt Final LIST', list_dest_port)
            try:
                _dest_port == int(list_dest_port)
            except:
                print('could not set port')

            config_dest_IP = _dest_ip
            config_dest_PORT = _dest_port
            config_dest_MAX_Threads = int(dest_dev_list[2][5])
            print('Destination Port', config_dest_PORT)
            print('Destination IP', config_dest_IP)
            print('Destination Max Threads', config_dest_MAX_Threads)

            active_rule_var = rule_list4
            active_rule_oper = rule_list3
            active_rule_tag = rule_list2
            active_rule_tag = active_rule_tag.replace("'", "").replace(" ", "")
            active_rule_var = active_rule_var.replace("'", "").replace(" ", "")

            print('Rule Operand', active_rule_oper)
            print('Rule Tag', active_rule_tag)
            print('Rule Var', active_rule_var)
            print('Dataset tag Modality', ds.Modality)

            dicom_tag_value = get_dicom_tag_value(ds, rule_list3, active_rule_tag)
            dicom_tag_value = dicom_tag_value.replace(" ", "")

            print('DICOM tag Value after def:', dicom_tag_value)

            print('Dicom Active Rule varable : ', active_rule_var)

            check_rule = check_rule_logic(dicom_tag_value, active_rule_var, active_rule_oper)

            print('Just checked rule logic and it is : ', check_rule)
            if check_rule:
                print('Creating Association')
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
                # Return a 'Success' status
                return 0x0000

            else:
                print('No Active Rule')
                return 0x0000

    ae.remove_requested_context(meta.MediaStorageSOPClassUID)


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
