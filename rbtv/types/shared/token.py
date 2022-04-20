from enum import IntEnum
from typing import TypedDict

Date = str


class userAuthTokenType(IntEnum):
    TOKEN_NORMAL = 0
    TOKEN_REFRESH = 1
    NUM = 2


class token(TypedDict):
    type: userAuthTokenType
    uid: int
    token: str
    validUntil: Date
