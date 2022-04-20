from enum import IntEnum, IntFlag
from typing import Dict, Optional, TypedDict

Date = str


class SupporterPaymentProvider(IntEnum):
    PAYPAL = 0
    PAYPAL_OLD = 1
    BANKTRANSFER = 2
    MANUAL_POSTING = 3
    YOUTUBE_SUBSCRIPTION = 4


class SupporterLevel(IntEnum):
    NONE = 0
    SUPPORTER = 1
    CLUBMEMBER = 2
    TIER3 = 3


class ISupporterInfo(TypedDict):
    displayName: str
    subscriptionDate: Date
    level: SupporterLevel


class ISupporterBillingTransaction(TypedDict):
    id: int
    date: Date
    provider: SupporterPaymentProvider
    reference: str
    details: Optional[str]
    value: int


class SupporterSubscriptionTerminationReason(IntFlag):
    SST_NONE = 0
    SST_OPTION_A = 0x1
    SST_OPTION_B = 0x2
    SST_OPTION_C = 0x4
    SST_OPTION_D = 0x8
    SST_OPTION_E = 0x10
    SST_OPTION_F = 0x20
    SST_OWN_MESSAGE = 0x2000
    SST_HIDDEN = 0x4000
    SST_ALL = (
        SST_OPTION_A
        | SST_OPTION_B
        | SST_OPTION_C
        | SST_OPTION_D
        | SST_OPTION_E
        | SST_OPTION_F
        | SST_OWN_MESSAGE
        | SST_HIDDEN
    )
