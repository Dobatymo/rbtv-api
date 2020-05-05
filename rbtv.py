import logging
from urllib.parse import urlencode, urlunsplit
from functools import lru_cache
from datetime import datetime, timedelta

import requests

def name_of_season(season, tpl="Season {}"):
	try:
		return season["name"]
	except KeyError:
		return tpl.format(season["numeric"])

def oauth_required(scope=None):

	def decorator(func):
		def inner(*args, **kwargs):
			raise RuntimeError("Oauth required, but not implemented yet")

		return inner

	return decorator

class API(object):

	netloc = "api.rocketbeans.tv"

	def __init__(self, timeout=60, scheme="https"):
		self.timeout = timeout
		self.scheme = scheme

	@lru_cache(maxsize=128)
	def _request(self, path, **params):

		query = urlencode(params)
		parts = (self.scheme, self.netloc, path, query, "")
		url = urlunsplit(parts)

		logging.debug("GET %s", url)
		r = requests.get(url, timeout=self.timeout)
		r.raise_for_status()
		return r.json()

	def _patch_request(self, path, body):
		parts = (self.scheme, self.netloc, path, "", "")
		url = urlunsplit(parts)

		logging.debug("PATCH %s", url)
		r = requests.patch(url, json=body, timeout=self.timeout)
		r.raise_for_status()
		res = r.json()

		assert res["success"]
		return res["data"]

	def _request_paged(self, path, limit, flat=True, **params):

		offset = 0
		total = limit

		while offset < total:
			res = self._request(path, offset=offset, limit=limit, **params)
			total = res["pagination"]["total"]
			assert res["success"]

			if flat:
				for item in res["data"]:
					yield item
			else:
				yield res["data"]

			offset += limit

	def _request_single(self, path, **params):
		res = self._request(path, **params)
		assert res["success"]
		return res["data"]

	# Blog

	def get_blog_posts(self):
		# type: () -> dict

		""" Returns all blog posts for the given pagination parameters.
		"""

		for blog in self._request_paged("/v1/blog/all", 50, True):
			yield blog

	def get_blog_posts_preview(self):
		# type: () -> dict

		""" Returns all blog posts.
		"""

		for blog in self._request_paged("/v1/blog/preview/all", 50, True):
			yield blog

	def get_blog_post(self, blogpost_id):
		# type: (int, ) -> dict

		""" Returns a single blog post.
		"""

		return self._request_single("/v1/blog/{}".format(blogpost_id))

	def get_blog_post_preview(self, blogpost_id):
		# type: (int, ) -> dict

		return self._request_single("/v1/blog/preview/{}".format(blogpost_id))

	# Bohne

	def get_bohnen_portraits(self):
		# type: () -> dict

		""" Returns reduced information about all team members.
		"""

		return self._request_single("/v1/bohne/portrait/all")

	def get_bohne(self, mgmtid):
		# type: (int, ) -> dict

		""" Returns information about a single team member.
		"""

		return self._request_single("/v1/bohne/{}".format(mgmtid))

	def get_bohne_portrait(self, mgmtid):
		# type: (int, ) -> dict

		""" Returns reduced information about a given team member.
		"""

		return self._request_single("/v1/bohne/portrait/{}".format(mgmtid))

	# CMS

	def get_cms_routes(self):
		# type: () -> dict

		""" Returns all CMS routes (frontend paths which are connected to CMS pages).
		"""

		return self._request_single("/v1/cms/route/all")

	def get_cms_page(self, cms_id):
		# type: (int, ) -> dict

		""" Returns the given CMS page.
		"""

		return self._request_single("/v1/cms/{}".format(cms_id))

	# Frontend

	def get_frontend_init_info(self):
		# type: () -> dict

		""" Returns necessary information for frontend initialization,
			such as current stream details, cms routes etc.
		"""

		return self._request_single("/v1/frontend/init")

	# Mediathek Episode

	def get_episodes_by_bohne(self, bohne_id, order="ASC"):
		# type: (int, str) -> Iterator[dict]

		""" Returns information about all episodes for the given Bohne.
		"""

		assert order in ("ASC", "DESC")
		for ep in self._request_paged("/v1/media/episode/bybohne/{}".format(bohne_id), 50, False, order=order):
			yield ep

	def get_episode(self, episode_id):
		# type: (int, ) -> dict

		""" Returns information about a single episode.
		"""

		return self._request_single("/v1/media/episode/{}".format(episode_id))

	def get_episodes_by_season(self, season_id, order="ASC"):
		# type: (int, str) -> Iterator[dict]

		""" Returns information about all episodes of a given season.
		"""

		assert order in ("ASC", "DESC")
		for ep in self._request_paged("/v1/media/episode/byseason/{}".format(season_id), 50, False, order=order):
			yield ep

	def get_episodes_by_show(self, show_id, order="ASC"):
		# type: (int, str) -> Iterator[dict]

		""" Returns information about all episodes for the given show.
		"""

		assert order in ("ASC", "DESC")
		for ep in self._request_paged("/v1/media/episode/byshow/{}".format(show_id), 50, False, order=order):
			yield ep

	def get_newest_episodes_preview(self, order="ASC"):
		# type: (str, ) -> Iterator[dict]

		assert order in ("ASC", "DESC")
		for ep in self._request_paged("/v1/media/episode/preview/newest", 50, False, order=order):
			yield ep

	@oauth_required()
	def get_abobox_content_for_self(self):
		# type: (int, str) -> Iterator[dict]

		""" Returns all episodes from subscribed shows and bohnen for the authorised user.
		"""

		for ep in self._request_paged("/v1/media/abobox/self", 50, False, order=order):
			yield ep

	def get_unsorted_episodes_by_show(self, show_id, order="ASC"):
		# type: (int, str) -> Iterator[dict]

		""" Returns reduced information about all episodes of a given season.
		"""

		assert order in ("ASC", "DESC")
		for ep in self._request_paged("/v1/media/episode/byshow/unsorted/{}".format(show_id), 50, False, order=order):
			yield ep

	def get_episodes_by_bohne_preview(self, bohne_id, order="ASC"):
		# type: (int, str) -> dict

		""" Returns reduced information about all episodes for the given Bohne.
		"""

		assert order in ("ASC", "DESC")
		return self._request_single("/v1/media/episode/bybohne/preview/{}".format(bohne_id))

	def get_episode_preview(self, episode_id):
		# type: (int, ) -> dict

		""" Returns reduced information about a single episode.
		"""

		return self._request_single("/v1/media/episode/preview/{}".format(episode_id))

	def get_episodes_by_season_preview(self, season_id, order="ASC"):
		# type: (int, str) -> Iterator[dict]

		""" Returns reduced information about all episodes of a given season.
		"""

		assert order in ("ASC", "DESC")
		for ep in self._request_paged("/v1/media/episode/byseason/preview/{}".format(season_id), 50, False, order=order):
			yield ep

	def get_episodes_by_show_preview(self, show_id, order="ASC"):
		# type: (int, str) -> Iterator[dict]

		""" Returns reduced information about all episodes for the given show.
		"""

		assert order in ("ASC", "DESC")
		for ep in self._request_paged("/v1/media/episode/byshow/preview/{}".format(show_id), 50, False, order=order):
			yield ep

	def get_unsorted_episodes_by_show_preview(self, show_id, order="ASC"):
		# type: (int, str) -> Iterator[dict]

		""" Returns reduced information about all unsorted (no season set)
			episodes for the given show.
		"""

		assert order in ("ASC", "DESC")
		for ep in self._request_paged("/v1/media/episode/byshow/unsorted/preview/{}".format(show_id), 50, False, order=order):
			yield ep

	# Mediathek Show

	def get_shows(self, sortby="LastEpisode", only=None):
		# type: (str, Optional[str]) -> Iterator[dict]

		assert sortby in ("LastEpisode", )
		assert only in (None, "podcast")
		for show in self._request_paged("/v1/media/show/all", 50, sortby=sortby, only=only):
			yield show

	def get_show(self, show_id):
		# type: (int, ) -> dict

		""" Returns information about the given show.
		"""

		return self._request_single("/v1/media/show/{}".format(show_id))

	def get_shows_preview(self, sortby="LastEpisode", only=None):
		# type: (str, Optional[str]) -> Iterator[dict]

		""" Returns paginated, reduced information about all shows.
		"""

		assert sortby in ("LastEpisode", )
		assert only in (None, "podcast")
		for show in self._request_paged("/v1/media/show/preview/all", 50, sortby=sortby, only=only):
			yield show

	def get_show_preview(self, show_id):
		# type: (int, ) -> dict

		""" Returns reduced information about the given show.
		"""

		return self._request_single("/v1/media/show/preview/{}".format(show_id))

	def get_shows_mini(self, sortby="LastEpisode", only=None):
		# type: (str, Optional[str]) -> Iterator[dict]

		""" Returns minimal information about all shows.
		"""

		assert sortby in ("LastEpisode", )
		assert only in (None, "podcast")
		return self._request_single("/v1/media/show/preview/mini/all", sortby=sortby, only=only)

	# Event

	def get_current_event(self):
		# type: () -> dict

		""" Returns Information about the current active RBTV Event.
		"""

		return self._request_single("/v1/rbtvevent/active")

	def get_current_event_team(self, team_id):
		# type: () -> dict

		""" Returns RBTV Event Team Information, restricted to active Events.
		"""

		return self._request_single("/v1/rbtvevent/team/{id}".format(id=team_id))

	@oauth_required("user.rbtvevent.read")
	def get_current_event_joined_team(self, event_id):
		# type: () -> dict

		""" Gets the joined Team for the given RBTV Event
			(which must be active in order to request these information).
		"""

		return self._request_single("/v1/rbtvevent/{slug}/team".format(slug=event_id))

	@oauth_required("user.rbtvevent.manage")
	def current_event_join_team(self, event_id, team_id):
		# type: (int, int) -> dict

		""" Joins the given Team for the given Event (the event must be active).
		"""

		return self._request_single("/v1/rbtvevent/{slug}/team/{id}/join".format(slug=event_id, id=team_id)) # POST

	# Schedule

	def get_schedule(self, startDay, endDay):
		# type: (datetime, datetime) -> List[dict]

		""" Returns the program schedule. Each day starts with the first schedule item of type 'live' or 'premiere'.
			Most of the time this will be "MoinMoin" at 10:30 CEST,
			except on weekends or when there are 'live'/'premiere' items at 0:00 CEST.
		"""

		assert endDay - startDay <= timedelta(days=14)
		return self._request_single("/v1/schedule/normalized", startDay=startDay.timestamp(), endDay=endDay.timestamp())

	# Shop

	def get_products(self): # fixme: currently not working
		# type: () -> dict

		""" Returns information about all shop products.
		"""

		#return self._request_paged("/v1/simpleshop/product/all", 50)
		return self._request_single("/v1/simpleshop/product/all")

	# StreamCount

	def get_viewer_count(self):
		# type: () -> dict

		""" Returns information about the current viewers.
			Contains separate numbers for Youtube, Twitch, and combined.
		"""

		return self._request_single("/v1/streamcount")

	# Subscription

	@oauth_required("user.subscriptions.manage")
	def subcribe(self, type_id, entity_id):
		# type: (int, int) -> dict

		return self._request_single("/v1/subscription/{type}/{id}".format(type=type_id, id=entity_id)) # POST

	@oauth_required("user.subscriptions.manage")
	def unsubscribe(self, type_id, entity_id):
		# type: (int, int) -> dict

		return self._request_single("/v1/subscription/{type}/{id}".format(type=type_id, id=entity_id)) # DELETE

	@oauth_required("user.subscriptions.read")
	def get_subscriptions(self):
		# type: () -> dict

		""" Returns all subscriptions for the current user.
		"""

		return self._request_single("/v1/subscription/mysubscriptions")

	@oauth_required("user.subscriptions.read")
	def get_subscription(self, type_id, entity_id):
		# type: (int, int) -> dict

		""" Returns notification settings for the given subscription.
		"""

		return self._request_single("/v1/subscription/{type}/{id}".format(type=type_id, id=entity_id)) # GET

	@oauth_required("user.subscriptions.manage")
	def modify_subscription(self, type_id, entity_id, subscribed=None, flags=None):
		# type: () -> dict

		""" Returns subscriptionResponse, requires subscriptionResponse in body.
		"""

		subscriptionResponse = {
			"type": type_id,
			"id": entity_id,
			"subscribed": subscribed,
			"flags": flags,
		}

		return self._patch_request("/v1/subscription/{type}/{id}".format(type=type_id, id=entity_id), subscriptionResponse)

	@oauth_required("user.subscriptions.manage")
	def modify_subscription_defaults(self, type_id, flags=None):
		# type: () -> dict

		""" Returns default notification flags for the given type.
			Requires subscriptionDefaultResponse in body.
		"""

		subscriptionDefaultResponse = {
			"type": type_id,
			"flags": flags,
		}

		return self._patch_request("/v1/subscription/mydefault/{type}".format(type=type_id), subscriptionDefaultResponse)

	# User

	@oauth_required("user.info")
	def get_user_info(self):

		""" Returns information about the current user,
			amount of Information depends on requested Scopes.
		"""

		return self._request_single("/v1/user/self")

class RBTVAPI(API):

	def get_season(self, show_id, season_id):

		show = self.get_show(show_id)

		for season in show["seasons"]:
			if season["id"] == season_id:
				return season

		raise KeyError("Season id not found")

	@staticmethod
	def _preprocess(name):
		# type: (str, ) -> str

		return name.replace(" ", "").lower() # make show name matching independent of whitespace and casing

	def show_name_to_id(self, show_name):
		# type: (str, ) -> int

		d = {self._preprocess(show["title"]): int(show["id"]) for show in self.get_shows_mini()}
		try:
			return d[self._preprocess(show_name)]
		except KeyError:
			raise ValueError("Could not find show {}".format(show_name))

	def bohne_name_to_id(self, bohne_name):
		# type: (str, ) -> int

		d = {self._preprocess(bohne["name"]): int(bohne["mgmtid"]) for bohne in self.get_bohnen_portraits()}
		try:
			return d[self._preprocess(bohne_name)]
		except KeyError:
			raise ValueError("Could not find bohne {}".format(bohne_name))

if __name__ == "__main__":
	from datetime import timezone
	from itertools import islice

	api = RBTVAPI()

	start = datetime.now(timezone.utc)
	end = datetime.now(timezone.utc) + timedelta(days=1)

	print("Blog posts:")
	for post in islice(api.get_blog_posts(), 10):
		print("id={} {}".format(post["id"], post["title"]))
	print("-"*20)

	print("Blog post id=100:", api.get_blog_post(100)["title"])

	print("Bohnen portraits:")
	for portrait in islice(api.get_bohnen_portraits(), 10):
		print("id={} {}".format(portrait["mgmtid"], portrait["name"], portrait["episodeCount"]))
	print("-"*20)

	print("Bohne id=33:", api.get_bohne(33)["firstname"])
	print("Bohne portrait id=33:", api.get_bohne_portrait(33)["name"])

	print("Episodes by bohne id=33:")
	for episode in api.get_episodes_by_bohne_preview(33)["episodes"]:
		print("id={} {}".format(episode["id"], episode["title"]))
	print("-"*20)

	print("Current event:", api.get_current_event())
	print("First show of the day:", api.get_schedule(start, end)[0]["elements"][0]["title"])
	print("Shop products:", api.get_products())
	print("Total viewers:", api.get_viewer_count()["total"])
