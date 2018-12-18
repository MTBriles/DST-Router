""" Dictionary for all of the values one can select to build rules on.  Its called in Build_Rules view in Views.py"""

# Each dict entry is Tag : (VR, VM, Name, Retired, Keyword)
DicomDictionary = {
    '0x00080060': 'Modality',
    '0x00081030': 'StudyDescription',
    '0x0008103E': 'SeriesDescription',
    'No Tag': 'Called AE',
    '0x00080080': 'InstitutionName',
    '0x00080050': 'AccessionNumber',
    '0x00100020': 'PatientID',
    '0x00101000': 'OtherPatientIDs',
    '0x00180050': 'SliceThickness'
}

temp = []
dictlist = []

for key, value in DicomDictionary.items():
    temp = [key, value]
    dictlist.append(temp)


