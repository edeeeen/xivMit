#################################################################
#       Parameter classes for FastAPI functions                 #
#################################################################

# Input values for getTemplates()
# Is just shorthand neams for encounters
class encounterNames(str, Enum):
    m1s = "M1S"
    m2s = "M2S"
    m3s = "M3S"
    m4s = "M4S"
    m5s = "M5S"
    m6s = "M6S"
    m7s = "M7S"
    m8s = "M8S"