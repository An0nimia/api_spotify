from pprint import pp

from unittest import TestCase

from api_spotify import API
from api_spotify.utils import magic_link


class Test_Types_Serialization(TestCase):
	__API = API(
		client_id = 'c6b23f1e91f84b6a9361de16aba0ae17',
		client_secret = '237e355acaa24636abc79f1a089e6204'
	)


	def test_refresh(self):
		print(self.__API.token.created_at)
		print(self.__API.refresh())
		print(self.__API.token.created_at)


	def test_get_track(self):
		assert self.__API.get_track('11dFghVXANMlKmJXsNCbNl').external_ids.isrc == 'USUM71703861'


	def test_get_album(self):
		res = self.__API.get_album('6G0POeSml1dY0l8SuvhY6s')
		assert len(res.tracks.get_next().items) == 6


	def test_get_album2(self):
		res = self.__API.get_album('7ySJCA3nVG00JT35rOiCNT')
		print(res.external_ids.upc, 'ciao')

		for track in res.tracks.items:
			print(track.name)

		is_next = res.tracks.get_next()

		while is_next:
			for track in is_next.items:
				print(track.name)

			is_next = is_next.get_next()

		print(res.genres, res.tracks.items[0].duration)


	def test_get_next_and_prev(self):
		res = self.__API.get_album('7ySJCA3nVG00JT35rOiCNT')
		n = res.tracks.get_next()

		assert res.tracks == n.get_previous()


	def test_get_album_tracks(self):
		res = self.__API.get_album_tracks('7ySJCA3nVG00JT35rOiCNT')

		for track in res.items:
			print(track.name)


	def test_new_releases(self):
		res = self.__API.get_new_releases()

		for track in res.albums.items:
			print(track.name)


	def test_get_playlist(self):
		res = self.__API.get_playlist('37i9dQZF1DZ06evO4gTUOY')

		assert res.id == '37i9dQZF1DZ06evO4gTUOY'


	def test_magic_link(self):
		assert magic_link('https://open.spotify.com/album/7L64BsqhmNImNoCyei2e0x?si=MjB0eb9vSQ6HJv0lXx9HrQ')[1] == '7L64BsqhmNImNoCyei2e0x'


	def test_get_artist(self):
		assert self.__API.get_artist('0TnOYISbd1XYRBk9myaseg').name == 'Pitbull'
