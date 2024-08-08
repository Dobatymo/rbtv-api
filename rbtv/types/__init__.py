from enum import Enum, IntEnum, IntFlag
from typing import Dict, List, Literal, Optional, TypedDict, Union

Date = str

from .shared.image import Image
from .shared.raffle import IRaffleTeaser

# shared/bohneportrait.ts


class bohnePortrait(TypedDict):
    mgmtid: int
    name: str
    role: Literal["onair", "offair", "external"]
    episodeCount: int
    images: List[Image]


class ImageType(IntEnum):
    OAUTHAPPTHUMB = 0
    CONTENT = 1
    BLOG_TITLEIMAGE = 2
    BLOG_THUMBNAIL = 3
    BLOG_PROMO = 4
    MEDIA_PROMO = 5
    CDKEY_DOWNLOADTHUMB = 6
    SIMPLESHOP_PRODUCT = 7
    RAFFLE_PRIZE_IMAGE = 8
    BOHNE_PORTRAIT = 9
    RBTVEVENT_TEAMICON = 10
    DIGITALGOODIE_THUMB = 11
    MAIL = 12
    LAST = 13


class ImageTypeResolution(TypedDict):
    name: str
    width: int
    height: int


class ImageTypeDefinition(TypedDict):
    maxFileSize: int
    minWidth: int
    maxWidth: int
    minHeight: int
    maxHeight: int
    resolutions: List[ImageTypeResolution]
    uploadAllowed: bool
    requiredPermission: str
    browsable: bool
    uploadMaxPending: int


# shared/link.ts


class link(TypedDict, total=False):
    type: str
    target: str
    label: Optional[str]


# shared/media.ts

tMediaType = Literal["live", "premiere", "rerun"]

# shared/notification.ts


class NotificationType(IntEnum):
    NT_REGIE = 0
    NT_HIGHLIGHT = 1
    NT_EPISODE_NEW = 2
    NT_BOHNE_NEW_EPISODE = 3
    NT_BOHNE_NEW_SHOW = 4
    NT_SHOW_LIVE = 5
    NT_BOHNE_LIVE = 6
    NT_BLOGPOST = 7
    NT_BOHNE_NEW_BLOGPOST = 8
    NT_RAFFLE_WININFO = 9
    NT_RAFFLE_SHIPPEDINFO = 10
    NT_NEW_DIGITAL_GOODIE = 11
    NT_NEW_CLAIMABLE_GOODIE = 12
    NT_NUM = 13


class WebPushNotificationPayload__Data(TypedDict, total=False):
    type: NotificationType
    sub: str
    id: int
    url: Optional[str]


class WebPushNotificationAction(TypedDict):
    action: str
    title: str
    icon: str


class WebPushNotification(TypedDict, total=False):
    title: str
    actions: Optional[List[WebPushNotificationAction]]
    badge: Optional[str]
    body: Optional[str]
    data: Optional[WebPushNotificationPayload__Data]
    dir: Optional[Literal["auto", "ltr", "rtr"]]
    icon: Optional[str]
    image: Optional[str]
    lang: Optional[str]
    renotify: Optional[bool]
    requireInteraction: Optional[bool]
    silent: Optional[bool]
    tag: Optional[str]
    timestamp: Optional[int]
    vibrate: Optional[List[int]]
    urlparts: Optional[List[str]]


# shared/rbtvevent.ts


class RBTVEventTeamJoinStrategy(IntEnum):
    DISABLED = 0
    JOINABLE = 1
    AUTOASSIGN_ODD = 2
    AUTOASSIGN_EVEN = 3


class IRBTVEventTeam(TypedDict, total=False):
    id: int
    name: str
    description: Optional[str]
    color: str
    icon: Union[List[Image], str]
    joinStrategy: RBTVEventTeamJoinStrategy
    eventSlug: Optional[str]
    internalSlug: Optional[str]


class IRBTVEvent(TypedDict, total=False):
    slug: str
    name: str
    descriptionHTML: str
    descriptionMD: Optional[str]
    active: bool
    teams: Optional[List[IRBTVEventTeam]]
    cmspage: Optional[str]
    subLinks: Optional[List[link]]


class IRBTVEventTeamStatsTeam(TypedDict):
    id: int
    activeUsers: int
    totalUsers: int


IRBTVEventTeamStats = Dict[int, IRBTVEventTeamStatsTeam]

# shared/stream.ts


class streamCountChannelInfo(TypedDict):
    name: str
    url: str
    count: int


class streamCount(TypedDict, total=False):
    youtube: int
    twitch: int
    total: int
    external: Optional[List[streamCountChannelInfo]]


class streamInfoShow(TypedDict):
    title: str
    topic: str
    game: str
    type: tMediaType
    showId: int
    timeStart: Date
    timeEnd: Date
    progress: int
    viewers: streamCount
    links: List[link]


# shared/subscription.ts


class SubscriptionType(IntEnum):
    ST_BOHNE = 0
    ST_SHOW = 1
    ST_HIGHLIGHT = 2
    ST_REGIE = 3
    ST_BLOG = 4
    ST_SEASON = 5
    ST_NUM = 6


class AheadOfLiveNotifyTime(IntFlag):
    NONE = 0
    MINUTE_5 = 0x1
    MINUTE_15 = 0x2
    MINUTE_30 = 0x4
    HOUR_1 = 0x8
    HOUR_3 = 0x10
    HOUR_6 = 0x20
    HOUR_12 = 0x40
    HOUR_24 = 0x80
    ALL = 0xFF


AheadOfLiveNotifyIndex2Time = Literal[5, 15, 30, 60, 180, 360, 720, 1440]
AheadOfLiveNotifyTimeConfig = List[bool]


class SubscriptionFlags(TypedDict, total=False):
    notifyEmail: bool
    notifyBrowser: bool
    notifyWhatsapp: Optional[bool]


class SubscriptionFilterSettings(TypedDict, total=False):
    isBlacklist: bool
    newEpisode: Optional[bool]
    newShow: Optional[bool]
    newBlogPost: Optional[bool]
    aheadOfLive: bool
    aheadOfLiveTimes: Optional[AheadOfLiveNotifyTimeConfig]


class SubscriptionFilter(TypedDict):
    type: SubscriptionType
    id: int


class Subscription(TypedDict, total=False):
    type: SubscriptionType
    id: int
    name: Optional[str]
    flags: Optional[SubscriptionFlags]
    filterSettings: Optional[SubscriptionFilterSettings]
    filter: Optional[List[SubscriptionFilter]]


from .shared.supporter import *

# shared/terms.ts


class TermsErrorData(TypedDict):
    needsSignPrivacyPolicy: bool
    needsSignTerms: bool


class ITermsVersion(TypedDict):
    terms: Date
    privacyPolicy: Date


from .response.auth.AuthPublic import authProvider
from .shared.token import *

# response/blog/BlogPublic.ts


class blogCategory(TypedDict):
    id: str
    visibleName: str
    color: str


class blogResponse(TypedDict, total=False):
    id: int
    title: str
    subtitle: str
    contentMK: Optional[str]
    contentHTML: Optional[str]
    isDisabled: bool
    publishDate: Date
    createDate: Date
    lastChangeDate: Date
    authors: Union[List[bohnePortrait], List[int]]
    titleImage: Union[List[Image], str]
    thumbImage: Union[List[Image], str]
    links: List[link]
    isVisibleInPromo: bool
    promoImage: Union[List[Image], str]
    ciIsVisible: Optional[bool]
    ciSubtitle: Optional[str]
    isSponsored: bool
    category: Union[blogCategory, str, None]
    raffles: Union[List[IRaffleTeaser], List[int], None]


class blogPreviewResponse(TypedDict):
    id: int
    title: str
    subtitle: str
    publishDate: Date
    authors: List[bohnePortrait]
    thumbImage: List[Image]
    promoImage: List[Image]
    isSponsored: bool
    category: Optional[blogCategory]


class blogPostCreatedResponse(TypedDict):
    id: int


# response/bohne/BohnePublic.ts


class bohneResponse(TypedDict, total=False):
    mgmtid: int
    nickname: Optional[str]
    firstname: str
    lastname: str
    contentMK: Optional[str]
    contentHTML: Optional[str]
    portraitImage: Union[List[Image], str]
    public: bool
    listed: Optional[bool]
    showreelURL: Optional[str]
    links: List[link]
    role: str
    episodeCount: Optional[int]
    sortPrio: Optional[int]
    isSubscribed: Optional[bool]
    userid: Optional[int]


# response/channel/ChannelPublic.ts


ServiceType = Literal["twitch", "youtube"]
ChannelGroupType = Literal["main", "talent", "guest"]


class Channel(TypedDict, total=False):
    mgmtId: int
    channelGroupId: int
    name: str
    title: str
    url: str
    serviceType: ServiceType
    platformId: str
    platformIcon: str
    platformThumbnail: str
    ytToken: Optional[str]
    ytLiveChatId: Union[List[Image], str]
    twitchChannel: Union[List[Image], str]
    currentGame: Union[List[Image], str]
    currentlyLive: bool
    viewers: int


ChannelGroupIcon = Dict[str, str]


class ChannelGroup(TypedDict, total=False):
    mgmtId: int
    type: ChannelGroupType
    name: str
    description: Union[List[Image], str]
    channelGroupIcon: List[Image]
    channels: Optional[List[Channel]]
    bohnen: Optional[List[bohnePortrait]]
    currentlyInMainContext: bool
    priority: int


class ChannelGroupStream(TypedDict):
    channelGroup: ChannelGroup
    streamInfoShow: streamInfoShow


ChannelGroupInfo = List[ChannelGroupStream]

# response/cms/CMSPublic.ts


class cmsPageResponse(TypedDict, total=False):
    id: str
    title: str
    contentMK: Union[List[Image], str]
    contentHTML: Union[List[Image], str]
    isPublic: Optional[bool]
    createDate: Optional[Date]
    lastChangeDate: Date


class cmsRouteResponse(TypedDict, total=False):
    route: str
    page: str
    isWildcard: bool
    isActive: Optional[bool]


# response/frontend/FrontendPublic.ts


class websocketParameters(TypedDict):
    url: str
    path: str


class frontendInitResponse(TypedDict, total=False):
    routes: List[cmsRouteResponse]
    authProviders: List[authProvider]
    websocket: websocketParameters
    channelGroupInfo: ChannelGroupInfo
    recaptchaSiteKey: str
    pageTheme: str
    randomYoutubeApiKey: str
    frontendVersion: int
    vapidPublicKey: Union[List[Image], str]
    applePushId: Union[List[Image], str]


# response/generic/RedirectResponse.ts


class genericRedirectResponse(TypedDict):
    destUrl: str


# response/media/MediaPublic.ts


class mediaShowPodcastInfo(TypedDict):
    feedUrl: Optional[str]  # /rocketbeans/rbtv-apidoc/issues/5
    soundcloudId: Optional[str]  # /rocketbeans/rbtv-apidoc/issues/5
    itunesUrl: Optional[str]  # /rocketbeans/rbtv-apidoc/issues/5
    spotifyUrl: Optional[str]  # /rocketbeans/rbtv-apidoc/issues/5
    podigeeUrl: Optional[str]  # /rocketbeans/rbtv-apidoc/issues/5


class mediaSeasonResponse(TypedDict, total=False):
    id: int
    showId: int
    name: Union[List[Image], str]
    numeric: int
    thumbnail: List[Image]
    podcastId: int


class mediaEpisodePreview(TypedDict, total=False):
    id: int
    title: str
    showId: int
    showName: str
    thumbnail: List[Image]
    hosts: List[int]
    distributionPublishingDate: Date
    firstBroadcastdate: Optional[Date]  # /rocketbeans/rbtv-apidoc/issues/5
    duration: int
    isAvailable: Optional[bool]


class videoToken(TypedDict, total=False):  # /rocketbeans/rbtv-apidoc/issues/5
    id: int
    mediaEpisodeId: int
    token: str
    type: Literal["youtube", "twitch", "cloudflare"]
    length: int


class mediaEpisode(TypedDict, total=False):
    id: int
    showId: int
    showName: str
    seasonId: Optional[int]  # /rocketbeans/rbtv-apidoc/issues/5
    episode: Optional[int]  # /rocketbeans/rbtv-apidoc/issues/5
    title: str
    description: str
    thumbnail: List[Image]
    links: List[link]
    hosts: List[int]
    tokens: List[videoToken]
    distributionPublishingDate: Date
    firstBroadcastdate: Optional[Date]  # /rocketbeans/rbtv-apidoc/issues/5
    duration: int
    prev: Optional[mediaEpisodePreview]
    next: Optional[mediaEpisodePreview]
    isAvailable: bool


class mediaEpisodeProgress(TypedDict):
    lastSeenPart: int
    total: int
    progress: List[int]


class mediaEpisodeCombinedResponse(TypedDict, total=False):
    bohnen: Dict[int, bohnePortrait]
    episodes: List[mediaEpisode]
    progress: Optional[Dict[int, mediaEpisodeProgress]]


class mediaShowResponse(TypedDict, total=False):
    id: int
    title: str
    description: str
    genre: str
    duration: int
    isExternal: bool
    isTruePodcast: bool
    thumbnail: List[Image]
    backgroundImage: Optional[List[Image]]
    slideshowImages: List[List[Image]]
    links: List[link]
    hosts: Optional[List[bohnePortrait]]
    seasons: List[mediaSeasonResponse]
    hasUnsortedEpisodes: bool
    lastEpisode: mediaEpisodeCombinedResponse
    podcast: mediaShowPodcastInfo
    statusPublicNote: Optional[str]  # /rocketbeans/rbtv-apidoc/issues/5
    isSubscribed: Optional[bool]


class mediaShowPreviewResponse(TypedDict, total=False):
    id: int
    title: str
    genre: Optional[str]  # bad docs
    isExternal: bool
    isTruePodcast: bool
    thumbnail: List[Image]
    hasPodcast: bool
    isSubscribed: Optional[bool]


class mediaShowPreviewMiniResponse(TypedDict):
    id: int
    title: str
    thumbnail: List[Image]


class mediaEpisodePreviewCombinedResponse(TypedDict, total=False):
    bohnen: Dict[int, bohnePortrait]
    episodes: List[mediaEpisodePreview]
    progress: Optional[Dict[int, mediaEpisodeProgress]]


class mediaPromoBoxContent(TypedDict, total=False):
    id: int
    set: int
    date: Date
    visibleUntil: Optional[Date]
    image: Union[List[Image], str]
    title: str
    subtitle: str
    link: str
    type: tMediaType


class mediaCurrentPromoBoxResponse(TypedDict):
    content: List[mediaPromoBoxContent]


class CloudflareToken(TypedDict):
    signedToken: str
    validUntil: Date


# response/mediacenter/MediacenterPublic.ts


class IMediacenterImage(TypedDict, total=False):
    id: str
    alt: Optional[str]
    caption: Optional[str]
    type: ImageType
    tags: Optional[List[str]]
    image: List[Image]


# response/oauth/OAuthPublic.ts


class OAuthScopeSeverity(IntEnum):
    DONTCARE = 0
    WARN = 1
    CRITICAL = 2


class OAuthApp(TypedDict, total=False):
    id: Union[List[Image], str]
    public: bool
    name: str
    description: str
    redirectURLs: List[str]
    icon: Union[List[Image], str, None]
    terms: str
    scopes: List[str]
    ownerid: Optional[int]


class OAuthAppPreview(TypedDict):
    id: str
    name: str
    description: str
    public: bool


class OAuthScope(TypedDict, total=False):
    name: str
    publicName: str
    description: str
    severity: OAuthScopeSeverity
    special: bool
    permissions: Optional[List[str]]


class OAuthAuthResponseType(IntEnum):
    REDIRECT = (0,)
    ERROR = (1,)
    AUTHORIZATION = 2


class OAuthAuthResponse(TypedDict):
    type: OAuthAuthResponseType


class OAuthAuthRedirectResponse(OAuthAuthResponse):
    destination: str


class OAuthAuthErrorResponse(OAuthAuthResponse):
    code: int
    message: str


class OAuthAuthAppInfo(TypedDict):
    name: str
    description: str
    icon: List[Image]
    terms: str


class OAuthAuthScopeInfo(TypedDict):
    publicName: str
    description: str
    severity: OAuthScopeSeverity


class OAuthAuthAuthorizationReason(IntEnum):
    NOAUTH = 0
    TERMS_CHANGED = 1
    SCOPES_CHANGED = 2


class OAuthAuthAuthorizationResponse(OAuthAuthResponse):
    reason: OAuthAuthAuthorizationReason
    app: OAuthAuthAppInfo
    scopes: List[OAuthAuthScopeInfo]


class OAuthAuthorizationListItem(TypedDict):
    id: int
    date: Date
    app: OAuthAuthAppInfo
    scopes: List[OAuthAuthScopeInfo]


class OAuthPendingVerificationRequestItem(TypedDict):
    date: Date
    userId: int
    displayName: str
    numApps: int


class OAuthPendingVerificationRequestRejectRequest(TypedDict):
    reason: str


class OAuthPendingVerificationRequestAcknowledgeRequest(TypedDict):
    pass


# response/playlist/PlaylistPublic.ts


class PlaylistType(Enum):
    CUSTOM = "custom"
    ABO_BOX = "abobox"
    WATCH_LATER = "watchlater"
    WATCH_HISTORY = "watchhistory"
    FILTER = "filter"


class InsertItemAt(Enum):
    FRONT = "front"
    BACK = "back"


class SortType(Enum):
    MANUAL = "manual"
    EPISODE_ASC = "episodeASC"
    EPISODE_DSC = "episodeDSC"
    RELEASE_ASC = "releaseASC"
    RELEASE_DSC = "releaseDSC"
    ADDED_ASC = "addedASC"
    ADDED_DSC = "addedDSC"


class Playlist(TypedDict, total=False):
    id: Optional[int]
    uuid: str
    name: str
    description: Optional[str]
    thumbnailMediaId: Optional[int]
    thumbnail: Optional[List[Image]]
    icon: Optional[str]
    createDate: Date
    lastUpdated: Date
    isPublic: bool
    ownerName: str
    insertItemAt: InsertItemAt
    sortType: SortType
    systemGenerated: bool
    playlistType: PlaylistType
    editPlaylist: bool
    editPlaylistItem: bool
    deletePlaylistItem: bool
    mediaEpisodeIncluded: Optional[bool]
    muteNotifications: bool


class PlaylistItem(TypedDict, total=False):
    id: Optional[int]
    order: int
    addedDate: Date
    mediaEpisode: mediaEpisodePreview
    progress: Optional[mediaEpisodeProgress]


class _Pagination(TypedDict):
    limit: int
    offset: int
    total: int


class CombinedPlaylistResponse(TypedDict, total=False):
    found: Optional[bool]
    playlist: Playlist
    playlistItems: List[PlaylistItem]
    pagination: _Pagination


class CreatePlaylistRequest(TypedDict, total=False):
    name: str
    description: Optional[str]
    thumbnailMediaId: Optional[int]
    mediaEpisodeId: Optional[int]
    isPublic: bool
    insertItemAt: InsertItemAt
    sortType: SortType
    systemGenerated: bool
    editPlaylist: Optional[bool]
    editPlaylistItem: Optional[bool]
    deletePlaylistItem: Optional[bool]
    muteNotifications: bool


class GetPlaylistRequest(TypedDict):
    pass


class SortPlaylistsBy(Enum):
    NAME_ASC = "nameASC"
    NAME_DESC = "nameDESC"
    CREATED_DATE_ASC = "createDateASC"
    CREATED_DATE_DESC = "createDateDESC"
    LAST_UPDATED_ASC = "lastUpdatedASC"
    LAST_UPDATED_DESC = "lastUpdatedDESC"


class GetAllPlaylistsRequest(TypedDict, total=False):
    includeGenerated: Optional[bool]
    includeReadOnly: Optional[bool]
    includesEpisode: Optional[int]
    orderBy: Optional[SortPlaylistsBy]


class GetPlaylistItemsRequest(TypedDict, total=False):
    sortType: Optional[SortType]


class UpdatePlaylistRequest(TypedDict, total=False):
    name: Optional[str]
    description: Optional[str]
    thumbnailMediaId: Optional[int]
    isPublic: Optional[bool]
    insertItemAt: Optional[InsertItemAt]
    sortType: Optional[SortType]
    readOnly: Optional[bool]
    muteNotifications: Optional[bool]
    editPlaylist: Optional[bool]
    editPlaylistItem: Optional[bool]
    deletePlaylistItem: Optional[bool]


class AddPlaylistItemsRequest(TypedDict, total=False):
    afterItemId: Optional[int]
    mediaEpisodes: List[int]


class MovePlaylistItemsRequest(TypedDict, total=False):
    afterItemId: int
    playlistItemIds: List[int]
    offset: Optional[int]
    limit: Optional[int]


class RemoveAllPlaylistItemsRequest(TypedDict):
    pass


class RemovePlaylistItemsRequest(TypedDict, total=False):
    playlistItemIds: List[int]
    mediaEpisodeIds: List[int]
    offset: Optional[int]
    limit: Optional[int]


class DeletePlaylistRequest(TypedDict):
    pass


# response/schedule/SchedulePublic.ts


class scheduleItem(TypedDict, total=False):
    id: int
    title: str
    topic: str
    game: str
    showId: int
    episodeId: int
    episodeImage: str
    episodeImages: List[Image]
    bohnen: List[bohnePortrait]
    timeStart: Date
    timeEnd: Date
    publishingDate: Optional[Date]
    duration: int
    durationClass: int
    streamExclusive: bool
    isSubscribed: Optional[bool]
    type: tMediaType
    links: List[link]
    channelGroups: List[ChannelGroup]
    openEnd: bool


class schedule(TypedDict):
    date: Date
    elements: List[scheduleItem]


class ChannelGroupSchedule(TypedDict):
    channelGroup: ChannelGroup
    schedule: List[schedule]


class GetChannelGroupScheduleRequest(TypedDict):
    startDay: int
    endDay: int
    filterChannelGroups: List[str]


class UploadScheduleEntry(TypedDict, total=False):
    id: int
    uploadDate: Date
    publishingDate: Optional[Date]
    title: str
    topic: Optional[str]
    showId: int
    showTitle: str
    showThumbnail: List[Image]


class UploadSchedule(TypedDict):
    date: Date
    elements: List[UploadScheduleEntry]


# response/search/SearchPublic.ts


class searchResultEpisode(TypedDict):
    id: int
    title: str
    showName: str
    thumbnail: List[Image]
    distibutionPublishingDate: Date
    firstBroadcastdate: Date


class searchResultShow(TypedDict):
    id: int
    title: str
    thumbnail: List[Image]


class searchResultBlog(TypedDict):
    id: int
    title: str
    thumbnail: List[Image]
    publishDate: Date


class searchResultSeason(TypedDict, total=False):
    id: int
    name: Optional[str]
    numeric: int
    showId: int
    showTitle: str
    thumbnail: List[Image]


class searchResultResonse(TypedDict):
    shows: List[searchResultShow]
    episodes: List[searchResultEpisode]
    blog: List[searchResultBlog]


filterSearchResultBlog = blogPreviewResponse
filterSearchResultEpisode = mediaEpisodePreviewCombinedResponse
filterSearchResultShow = mediaShowPreviewResponse
filterSearchResultSeason = searchResultSeason
filterSearchResultData = Union[
    List[filterSearchResultBlog],
    filterSearchResultEpisode,
    List[filterSearchResultShow],
    List[filterSearchResultSeason],
]


class filterContentType(IntEnum):
    VIDEO = 1
    SHOW = 2
    SEASON = 3
    BLOG = 4


class filterSearchResultPaginationData(TypedDict):
    offset: int
    limit: int
    total: int


class filterSearchResult(TypedDict):
    paginationData: Dict[int, filterSearchResultPaginationData]
    data: Dict[int, filterSearchResultData]
    resultId: str


# response/simpleshop/SimpleShopPublic.ts


class simpleShopItem(TypedDict, total=False):
    id: int
    name: str
    description: str
    price: str
    vat: str
    link: str
    image: Union[List[Image], str]
    sortPrio: Optional[int]
    ciVisible: Optional[bool]
    ciDescription: Optional[str]
    pageVisible: Optional[bool]


# response/subscription/SubscriptionPublic.ts


class subscriptionResponse(TypedDict, total=False):
    type: SubscriptionType
    id: int
    subscribed: bool
    flags: Optional[SubscriptionFlags]


class subscriptionBohneData(TypedDict):
    id: int
    name: str
    flags: SubscriptionFlags


class subscriptionShowData(TypedDict):
    id: int
    title: str
    flags: SubscriptionFlags


class subscriptionBlogData(TypedDict):
    id: int
    name: str
    flags: SubscriptionFlags


class subscriptionListResponse(TypedDict):
    bohnen: List[subscriptionBohneData]
    shows: List[subscriptionShowData]
    blog: List[subscriptionBlogData]


class subscriptionDefaultResponse(TypedDict):
    type: SubscriptionType
    flags: SubscriptionFlags


class subscriptionData(TypedDict):
    type: SubscriptionType
    id: int
    name: str
    flags: SubscriptionFlags
    isDefault: bool


subscriptionListV2Response = List[subscriptionData]

# response/tags/TagsPublic.ts


class TagState(IntEnum):
    CREATED = 0
    APPROVED = 1
    BLOCKED = 2


class Vote(IntEnum):
    UP = 1
    NO = 0
    DOWN = -1


class Tag(TypedDict, total=False):
    id: int
    name: str
    state: TagState
    score: Optional[int]
    pinned: Optional[bool]
    voted: Optional[Vote]
    hidden: Optional[bool]


class SingleTagResponse(TypedDict):
    tag: Tag


class MultipleTagsResponse(TypedDict):
    tags: List[Tag]


class CreateTagRequest(TypedDict, total=False):
    name: str
    mediaId: Optional[int]


class CreateTagResponse(SingleTagResponse):
    pass


class GetTagsRequest(TypedDict, total=False):
    name: Optional[str]
    mediaId: Optional[int]


class GetTagsResponse(MultipleTagsResponse):
    pass


class GetAllTagsRequest(TypedDict):
    pass


class GetAllTagsResponse(MultipleTagsResponse):
    pass


class UpdateTagRequest(TypedDict):
    name: str
    state: TagState


class UpdateTagResponse(SingleTagResponse):
    pass


class VoteTagRequest(TypedDict):
    mediaId: int
    vote: Vote


class VoteTagResponse(TypedDict):
    pass


class PinTagRequest(TypedDict):
    mediaId: int


class PinTagResponse(TypedDict):
    pass


class UnpinTagRequest(TypedDict):
    mediaId: int


class UnpinTagResponse(TypedDict):
    pass


class AddTagRequest(TypedDict):
    mediaId: int


class AddTagResponse(TypedDict):
    pass


class RemoveTagRequest(TypedDict):
    mediaId: int


class RemoveTagResponse(TypedDict):
    pass


class HideTagRequest(TypedDict):
    mediaId: int


class HideTagResponse(TypedDict):
    pass


class UnhideTagRequest(TypedDict):
    mediaId: int


class UnhideTagResponse(TypedDict):
    pass


class DeleteTagRequest(TypedDict):
    pass


class DeleteTagResponse(SingleTagResponse):
    pass


from .response.user.UserPublic import *
