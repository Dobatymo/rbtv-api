from enum import IntEnum
from typing import Optional, TypedDict

from ...shared.token import token
from ..user.UserPublic import UserExternalAuthProviderType


class authSuccessResponse(TypedDict):
    token: token
    refreshToken: token


class authRequestTokenResponse(TypedDict):
    token: token


class authVerifyRefreshTokenResponse(TypedDict):
    refreshToken: token


class authVerifyToken(TypedDict):
    token: token


class authProvider(TypedDict):
    name: str
    publicName: str
    available: bool
    type: UserExternalAuthProviderType
    sortPrio: int


class UserExternalAuthVerifyResult(IntEnum):
    FAIL = 0
    SUCCESS = 1
    SETUP_REQUIRED = 2
    FAIL_BLOCKED = 3
    FAIL_OTHER = 4
    SECONDFACTOR_REQ = 5
    ATTACHED = 6
    FAIL_ATTACHED_OTHER_ACC = 7
    FAIL_PROVIDER_ERROR = 8
    FAIL_NEED_REAUTH = 9


class UserExternalAuthVerifyFailNeedReauthResponse(TypedDict):
    result: UserExternalAuthVerifyResult
    url: str


class UserExternalAuthVerifyFailProviderErrorResponse(TypedDict, total=False):
    result: UserExternalAuthVerifyResult
    reason: str
    description: Optional[str]
    url: Optional[str]


class UserExternalAuthVerifyFailResponse(TypedDict):
    result: UserExternalAuthVerifyResult


class UserExternalAuthVerifySuccessResponse(TypedDict):
    result: UserExternalAuthVerifyResult
    navigationTarget: Optional[str]
    token: Optional[token]
    refreshToken: Optional[token]


class UserExternalAuthVerifySetupRequiredResponse(TypedDict):
    result: UserExternalAuthVerifyResult
    displayName: Optional[str]
    email: Optional[str]


class UserExternalAuthVerifyAttachedResponse(TypedDict):
    result: UserExternalAuthVerifyResult
    navigationTarget: Optional[str]


class UserExternalAuthRegistrationSuccessResponse(TypedDict):
    navigationTarget: Optional[str]
    token: Optional[token]
    refreshToken: Optional[token]
