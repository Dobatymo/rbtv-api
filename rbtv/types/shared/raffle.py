from typing import TypedDict, List, Optional, Union, Any
from enum import IntEnum

from .image import Image
from .supporter import SupporterLevel

Date = str

class RaffleParticipationState(IntEnum):
	NOT_SET = 0
	ENABLED = 1
	DISABLED = 2

class RaffleTransactionLogAction(IntEnum):
	CREATE = 0
	MODIFY = 1
	DICEBEGIN = 2
	DICEEND = 3
	NOTIFY_WINNER = 4
	SEND_PRIZEINFO_WINNER = 5
	PARTICIPATE = 6
	PARTICIPATE_GUEST = 7
	PARTICIPATE_GUEST_VALIDATE = 8
	PARTICIPATE_ADMIN_CHANGE_VALIDATION = 9
	WINNER_EDIT = 10

class IRaffleLogWinnerEditData_Info(TypedDict):
	num: int
	winningPos: int
	isPhyiscalPrize: bool
	digitalPrizeInfo: str
	trackingInformation: str
	prizeShipped: bool
	internalNote: str
	externalNote: str

class IRaffleLogWinnerEditData(TypedDict):
	num: int
	old: IRaffleLogWinnerEditData_Info
	new: IRaffleLogWinnerEditData_Info

class IRaffleLogParticipateAdminChangeValidation(TypedDict):
	id: int
	old: bool
	new: bool

class IRaffleLogParticipateData(TypedDict):
	supporterLevel: SupporterLevel
	id: int

class IRaffleLogParticipateGuestData(TypedDict):
	createAccount: bool
	id: int

class IRaffleLogParticipateGuestValidateData(TypedDict):
	id: int

class IRaffleLogNotifyWinnerData(TypedDict):
	num: int
	winningPos: int
	isLocalUser: bool
	userId: int
	email: str
	prizeTitle: str
	prizeImage: List[Image]

class IRaffleLogSendPrizeInfo(TypedDict):
	num: int
	winningPos: int
	isLocalUser: bool
	userId: int
	email: str
	prizeTitle: str
	prizeImage: List[Image]
	isPhyiscalPrize: bool
	digitalPrizeInfo: str
	trackingInformation: str
	addressVersion: int
	addressData: str
	prizeShipped: bool
	externalNote: str
	internalNote: str

class IRaffleLogCreateData(TypedDict):
	title: str
	descriptionMD: str
	cidescriptionMD: str
	prizeImage: List[Image]
	partnerLogo: List[Image]
	productLogo: List[Image]
	manufacturerLogo: List[Image]
	prizeDescription: str
	prizeTitle: str
	publishDate: Date
	startDate: Date
	endDate: Date
	autoDetermineWinner: bool
	participationState: RaffleParticipationState
	numWinners: int
	minimumSupporterLevel: SupporterLevel
	termsMD: str
	slug: str
	frontendTheme: str

class IRaffleLogModifyData(TypedDict):
	old: IRaffleLogCreateData
	new: IRaffleLogCreateData

class RaffleDiceMethod(IntEnum):
	NONE = 0
	SHUFFLE = 1
	PICK = 2

class IRaffleLogDiceEnd(TypedDict):
	type: RaffleDiceMethod
	winnerids: List[int] 



class IRaffle(TypedDict, total=False):
	id: int
	title: str
	groupTag: Optional[str]
	descriptionHTML: str
	descriptionMD: str
	cidescriptionHTML: Optional[str]
	cidescriptionMD: Optional[str]
	partnerLogo: Optional[List[Image]]
	manufacturerLogo: Optional[List[Image]]
	productLogo: Optional[List[Image]]
	priceImage: Union[List[Image], str]
	priceDescriptionHTML: Optional[str]
	priceDescriptionMD: str
	prizeTitle: str
	publishDate: Date
	startDate: Optional[Date]
	endDate: Optional[Date]
	participationAvailable: bool
	participationState: RaffleParticipationState
	autoDetermineWiner: bool
	numWinners: int
	minimumSupporterLevel: SupporterLevel
	frontendTheme: str
	slug: str
	termsHTML: str
	termsMD: str
	raffleWinner: Optional[List[str]]
	restrictToGroups: List[int]


class IRaffleTeaser(TypedDict, total=False):
	id: int
	slug: str
	title: str
	descriptionHTML: str
	startDate: Date
	endDate: Date
	participationAvailable: bool
	frontendTheme: str
	priceImage: List[Image]
	raffleWinner: Optional[List[str]]


class IRaffleShippingAddress(TypedDict, total=False):
	firstName: str
	lastName: str
	address: List[str]
	zip: str
	city: str
	state: str
	country: str
	email: str
	allowance: bool


class IRaffleUserParticipation(TypedDict):
	date: Date
	title: str
	slug: str
	priceTitle: str

class IRaffleUserWinEntry(TypedDict):
	winningPos: int
	date: Date
	title: str
	prizeTitle: str
	prizeImage: List[Image]
	digitalPriceInformation: Optional[str]
	prizeShipped: bool
	externalNote: Optional[str]
	trackingInformation: Optional[str]

class IRaffleParticipantsStats(TypedDict):
	registered: int
	guest: int
	pending: int
	total: int

class IRaffleAdminListEntry(TypedDict):
	id: int
	title: str
	groupTag: Optional[str]
	publishDate: Date
	isRunning: bool
	isFinished: bool
	hasPendingShipments: bool
	numParticipants: IRaffleParticipantsStats

class IRaffleAdminParticipationUserInfo(TypedDict):
	id: int
	displayName: str

class IRaffleAdminParticipationListEntry(TypedDict):
	id: int
	ip: str
	date: Date
	user: Optional[IRaffleAdminParticipationUserInfo]
	shippingAddress: Optional[IRaffleShippingAddress]
	email: str
	validated: bool

class IRaffleAdminWinnerListEntry(TypedDict):
	num: int
	winningPos: int
	date: Date
	isPhysicalPrize: bool
	digitalPrizeInformation: str
	prizeTitle: str
	userId: int
	shippingAddress: IRaffleShippingAddress
	email: str
	prizeShipped: bool
	internalNote: str
	externalNote: str
	trackingInformation: str
	prizeShippingNotificationSent: bool

class IRaffleParticipation(TypedDict):
	id: int
	date: Date
	ip: str
	userId: Optional[int]
	shippingAddress: Optional[IRaffleShippingAddress]
	email: str
	validated: bool

class IRaffleTransactionLogEntryUserInfo(TypedDict):
	id: int
	displayName: str

class IRaffleTransactionLogEntry(TypedDict):
	id: int
	date: Date
	ip: Optional[str]
	user: Optional[IRaffleTransactionLogEntryUserInfo]
	action: RaffleTransactionLogAction
	data: Any

