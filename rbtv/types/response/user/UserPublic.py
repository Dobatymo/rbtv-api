from typing import TypedDict, Dict, Optional, List
from enum import IntEnum

from ...shared.supporter import SupporterLevel
from ...shared.image import Image

Date = str

class UserAccountState(IntEnum):
    BLOCKED = -1
    ACTIVE = 0
    VALIDATION = 1
    OAUTH_PENDING = 2


class UserExternalAuthProviderType(IntEnum):
    AUTH_LOCAL = 0
    AUTH_GOOGLE = 1
    AUTH_TWITCH = 2
    AUTH_STEAM = 3
    AUTH_REDDIT = 4
    AUTH_DISCORD = 5
    AUTH_TWITTER = 6
    AUTH_FACEBOOK = 7
    # AUTH_RBTVHUB = 8
    # AUTH_RBTVHUBADMIN = 9
    AUTH_NUM = 8


class UserGoodiePoolItemAvailability(IntEnum):
    OUT_OF_STOCK = 0
    IN_STOCK = 1
    LOW_STOCK = 2
    ALREADY_CLAIMED = 3


class UserSecondFactorType(IntEnum):
    GTOTP = 0


permissionMap = Dict[str, bool]


class entityUserResponse(TypedDict, total=False):
    id: int
    displayName: str
    email: Optional[str]
    emailVerificationPending: Optional[bool]
    registrationDate: Optional[Date]
    noPasswordSet: Optional[bool]
    secondFactorEnabled: Optional[bool]
    supporterLevel: Optional[SupporterLevel]
    permissions: Optional[permissionMap]
    rbtvEventTeam: Optional[int]


class userRegistrationLocalRequest(TypedDict):
    displayName: str
    email: str
    password: str
    acceptTerms: bool
    acceptPrivacyPolicy: bool
    recaptcha: str


class userRegistrationSuccessReponse(TypedDict):
    uid: int
    displayName: str
    verificationNeeded: bool


class userRegistrationOAuthRequest(TypedDict):
    oauthToken: str
    displayName: str
    acceptTerms: bool
    acceptPrivacyPolicy: bool


class userChangePasswordRequest(TypedDict, total=False):
    currentPassword: Optional[str]
    newPassword: str


class userChangeEMailRequest(TypedDict):
    currentPassword: str
    newEMail: str


class userResetPasswordRequest(TypedDict):
    email: str


class userSetPasswordRequest(TypedDict):
    token: str
    newPassword: str


class userChangeDisplayNameRequest(TypedDict):
    displayname: str


class connectedAccount(TypedDict):
    type: UserExternalAuthProviderType
    displayName: str
    connectTime: Date
    isValid: bool


class userConnectedAccountsResponse(TypedDict):
    id: int
    linkedAccounts: List[connectedAccount]


class userRemoveConnectedAccountRequest(TypedDict):
    type: UserExternalAuthProviderType


class userSecondFactorBeginSetup(TypedDict):
    type: UserSecondFactorType
    secret: str
    url: str


class userSecondFactorSetup(TypedDict):
    recoveryCode: str


class UserDigitalGoodieType(IntEnum):
    SUPPORTER = (0,)
    CHEATCODE = 1
    GENERIC = 2
    NUM = 3


class UserDigitalGoodie(TypedDict, total=False):
    type: UserDigitalGoodieType
    title: str
    description: str
    key: str
    linkDate: Date
    thumbnail: Optional[List[Image]]
    expireDate: Optional[Date]


class UserGoodiePoolItem(TypedDict, total=False):
    id: int
    type: UserDigitalGoodieType
    title: str
    description: str
    status: UserGoodiePoolItemAvailability
    minimumSupporterLevel: SupporterLevel
    thumbnail: Optional[List[Image]]
    expireDate: Optional[Date]
    endDate: Optional[Date]
