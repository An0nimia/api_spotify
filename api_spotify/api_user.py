from typing import Any

from base64 import b64encode

from requests import (
	Session,
	post as req_post
)

from .api import API

from .types import (
	Token_User, Track
)

from .exceptions import Invalid_Grant

from .decorators.login import check_refresh_token


class API_USER(API):
	API_AUTHORIZE_ENDPOINT = 'https://accounts.spotify.com/authorize'

	def __init__(self, client_id: str, client_secret: str) -> None:
		self.__client_id = client_id
		self.__client_secret = client_secret
		self.__session = Session()
		super().__init__(client_id, client_secret)


	def refresh_token(self) -> None:
		params = {
			'grant_type': 'refresh_token',
			'refresh_token': self.token_user.refresh_token
		}

		self.make_login(params)


	def make_login(self, params: dict[str, Any]):
		login = b64encode(
			f'{self.__client_id}:{self.__client_secret}'.encode()
		).decode()

		headers = {
			'Content-Type': 'application/x-www-form-urlencoded',
			'Authorization': f'Basic {login}'
		}

		self.logger.debug(f'Before request {headers} with params {params}')

		json_data: dict[str, Any] = req_post(
			self.API_ACCESS_TOKEN_ENDPOINT,
			data = params,
			headers = headers,
			timeout = 30
		).json()

		self.logger.debug(f'Response {json_data}')

		if json_data.get('error') == 'invalid_grant':
			raise Invalid_Grant(json_data['error_description'])

		if json_data.get('refresh_token') is None and json_data.get('access_token') is not None:
			self.logger.debug(f'No new refresh token still saving previous one {self.token_user.refresh_token}')
			json_data['refresh_token'] = self.token_user.refresh_token

		self.token_user = Token_User.model_validate(json_data)
		self.logger.debug(f'Saved token: {self.token_user}')
		self.__session.headers['Authorization'] = f'Bearer {self.token_user.access_token}'


	@check_refresh_token
	def make_req_user(self, method: str) -> dict[str, Any] | None:
		res = self.__session.get(f'{self.API_URL}{method}')
		self.logger.debug(f'Response; {res.text} of {res.url}')

		if res.status_code == 204:
			return None

		return res.json()


	def craft_authorization_link(self, scope: str, redirect_uri: str) -> str:
		params = {
			'response_type': 'code',
			'client_id': self.__client_id,
			'scope': scope,
			'redirect_uri': redirect_uri
		}

		url = f'{self.API_AUTHORIZE_ENDPOINT}?'

		for param, value in params.items():
			url += f'{param}={value}&'

		return url


	def exchange_authorization_code(self, code: str, redirect_uri: str) -> None:
		params = {
			'grant_type': 'authorization_code',
			'code': code,
			'redirect_uri': redirect_uri
		}

		self.make_login(params)


	def get_current_listening_track_JSON(self) -> dict[str, Any] | None:
		method = 'me/player/currently-playing'

		return self.make_req_user(method)


	def get_current_listening_track(self) -> Track | None:
		res = self.get_current_listening_track_JSON()

		if res is None:
			return None

		return Track.model_validate(res['item'])
