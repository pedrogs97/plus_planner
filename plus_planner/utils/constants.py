"""
Project constants
"""
# Account

MANAGER = 1
DOCTOR = 2
ASSISTANT = 3
NURSE = 4

STR_MANAGER = "Manager"
STR_DOCTOR = "Doctor"
STR_ASSISTANT = "Assistant"
STR_NURSE = "Nurse"


ROLES = [
    MANAGER,
    DOCTOR,
    ASSISTANT,
    NURSE,
]


ADMINISTRATIVE_ROLES = [ASSISTANT, MANAGER]

NORMAL_ROLES = [DOCTOR, NURSE]

# Schedule

SCHEDULED = 1
CONFIRMED = 2
CANCELED = 3
FINISHED = 4

STR_SCHEDULED = "Scheduled"
STR_CONFIRMED = "Confirmed"
STR_CANCELED = "Canceled"
STR_FINISHED = "Finished"

# Clinical
MALE = 1
FAMALE = 2
OTHER = 3

STR_MALE = "Male"
STR_FAMALE = "Famale"
STR_OTHER = "other"
