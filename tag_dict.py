""" Dictionary for all of the values one can select to build rules on.  Its called in Build_Rules view in Views.py"""

# Each dict entry is Tag : (VR, VM, Name, Retired, Keyword)
DicomDictionary = [
    'Modality',
    'StudyDescription',
    'SeriesDescription',
    'Called AE',
    'InstitutionName',
    'AccessionNumber',
    'PatientID',
    'OtherPatientIDs',
    'SliceThickness'
]

#temp = []
#dictlist = []

#for key, value in DicomDictionary.items():
#    temp = [key, value]
#    dictlist.append(temp)


