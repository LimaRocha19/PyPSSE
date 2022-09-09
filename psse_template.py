# Importing PSSE module from PSSE installation folder
# DO NOT MODIFY this -- you must have Python 3.9 32 bits installed !!!
import sys
sys.path.insert(1, 'C:\\Program Files (x86)\\PTI\\PSSE34\\PSSPY39')

# Importing PSSE python modules
import psse34
import psspy

# Some pre-defined functions to support the script
def fnsl_error_check(ierr):
    options = {
        0: 'FNSL activity performed successfully.',
        1: 'Invalid OPTIONS value.',
        2: 'Generators are converted.',
        3: 'Buses in island(s) without a swing bus; use activity TREE.',
        4: 'Bus type code and series element status inconsistencies.',
        5: 'Prerequisite requirements for API are not met.'
    }
    status = {
        'status': False,
        'message': 'Error message not recognized, you are probably performing other activity then FNSL.'
    }
    if ierr > 5 or ierr < 0:
        return status
    else:
        status['message'] = options[ierr]
        if ierr == 0:
            status['status'] = True
    return status

def pout_error_check(ierr):
    options = {
        0: 'POUT activity performed successfully.',
        1: 'Invalid SID value or subsystem SID is not defined.',
        2: 'Invalid ALL value.',
        3: 'Prerequisite requirements for API are not met.'
    }
    status = {
        'status': False,
        'message': 'Error message not recognized, you are probably performing other activity then POUT.'
    }
    if ierr > 3 or ierr < 0:
        return status
    else:
        status['message'] = options[ierr]
        if ierr == 0:
            status['status'] = True
    return status

# Input here the desired files (backslash must be doubled -> \\)
root = 'C:\\Users\\brislim\\Downloads\\PSSE Training\\Power Flow 1\\'
raw = root + '*.raw'
sav = root + 'EXER4-1.sav'
sld = root + 'EXER2-3.sld'

# Initializing PSSE 34 and loading case
psspy.psseinit()
psspy.case(sav)

'''
Calling FNSL with options:
    ( OPTIONS )(            Description          )(        Value 1       )(        Value 2       )(        Value 3       )(        Value 4       )(        Value 5       )
    OPTIONS(1) Tap adjustment flag                0 (disable)             1 (stepping)            2 (direct)              N/A                     N/A
    OPTIONS(2) Area interchange adjustment flag   0 (disable)             1 (tie line)            2 (tie line and loads)  N/A                     N/A
    OPTIONS(3) Phase shift adjustment flag        0 (disable)             1 (enable)              N/A                     N/A                     N/A
    OPTIONS(4) DC tap adjustment flag             0 (disable)             1 (enable)              N/A                     N/A                     N/A
    OPTIONS(5) Switched shunt adjustment flag     0 (disable)             1 (enable)              2 (continuous)          N/A                     N/A
    OPTIONS(6) Flat start flag                    0 (disable)             1 (flat start)          2 (flat - magnitudes)   3 (flat - angles)       4 (flat - both)
    OPTIONS(7) VAr limit flag                     0 (immediatly)          > 0 (iteration n)       -1 (ignore)             N/A                     N/A
    OPTIONS(8) Non-divergent solution flag        0 (disable)             1 (enable)              N/A                     N/A                     N/A
'''

options = [
     1,     # OPTIONS(1)
     0,     # OPTIONS(2)
     0,     # OPTIONS(3)
     1,     # OPTIONS(4)
     1,     # OPTIONS(5)
     0,     # OPTIONS(6)
    99,     # OPTIONS(7)
     0      # OPTIONS(8)
]
ierr = psspy.fnsl(options)
status = fnsl_error_check(ierr)
print(status)
if not status['status']:
    exit()

'''
Calling POUT with INPUTS (* default):
    ( INPUTS )(            Description          )(        Value 1       )(        Value 2       )(        Value 3       )(        Value 4       )(        Value 5       )
    SID       Valid subsystem identifier         0 *                     Any valid SID           Any valid SID           Any valid SID           Any valid SID
    ALL       All buses or specified subsystem   0 (only buses in SID)   1 (all buses)           N/A                     N/A                     N/A
'''
with open('pout.txt', 'w') as output:
    sys.stdout = output
    inputs = [
        0,     # SID
        1      # ALL
        ]
    ierr = psspy.pout(inputs[0], inputs[1])
    status = pout_error_check(ierr)
    print(status)
    if not status['status']:
        exit()
