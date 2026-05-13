from enum import StrEnum


class DirectionCall(StrEnum):
    INBOUND = "inbound"
    OUTBOUND = "outbound"


class CallType(StrEnum):
    MISSED = "missed"
    ANSWERED = "answered"
    VOICEMAIL = "voicemail"
