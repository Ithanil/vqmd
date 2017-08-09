import warnings

# Warnings related to vqmd's XML parsing

def warn_mult_xml(xmlele):
    warnings.warn('More than one \'' + xmlele + '\' XML element provided. Overwriting previous information.')

def warn_miss_xml(missele, xmlele):
    warnings.warn('Trying to process \'' + xmlele + '\' XML element without previous \'' + missele + '\' xml element.')

def warn_wrong_xml(xmlele):
    if not xmlele == '_text':
        warnings.warn('XML element \'' + xmlele + '\' is unknown. Did nothing.')

def warn_data_type(dtype):
    warnings.warn('Data type \'' + dtype + '\' is unknown. Did nothing.')

def warn_data_mode(dmode):
    warnings.warn('Data mode \'' + dmode + '\' is unknown. Did nothing.')
