from enum import StrEnum


class CallDirection(StrEnum):
    INBOUND = "inbound"
    OUTBOUND = "outbound"


class CallType(StrEnum):
    MISSED = "missed"
    ANSWERED = "answered"
    VOICEMAIL = "voicemail"
