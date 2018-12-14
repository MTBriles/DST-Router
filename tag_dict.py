""" Dictionary for all of the values one can select to build rules on.  Its called in Build_Rules view in Views.py"""

# Each dict entry is Tag : (VR, VM, Name, Retired, Keyword)
DicomDictionary = {
    '0x00080030': 'Study Time',
    '0x00080031': 'Series Time'

}

temp = []
dictlist = []

for key, value in DicomDictionary.items():
    temp = [key, value]
    dictlist.append(temp)


