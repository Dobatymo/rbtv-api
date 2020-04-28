import logging
from urllib.parse import urlencode, urlunsplit
from functools import lru_cache

import requests

def name_of_season(season, tpl="Season {}"):
	try:
		return season["name"]
	except KeyError:
		return tpl.format(season["numeric"])

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

	#@auth
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

class RBTVAPI(API):

	def get_season(self, show_id, season_id):

		show = self.get_show(show_id)

		for season in show["seasons"]:
			if season["id"] == season_id:
				return season

		raise KeyError("Season id not found")
