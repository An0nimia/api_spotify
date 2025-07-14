from __future__ import annotations

from datetime import datetime

from collections.abc import Callable

from functools import update_wrapper

from typing import (
	Any, TYPE_CHECKING
)


if TYPE_CHECKING:
	from ..api import API
	from ..api_user import API_USER


def check_login(
	func: Callable[
		..., dict[str, Any]
	]
):
	def inner(self: API, *args: ...) -> dict[str, Any]:
		self.logger.debug('Check if expired')
		c_time = datetime.now()

		if (c_time - self.token.created_at).seconds >= self.token.expires_in:
			self.refresh()

		return func(self, *args)

	update_wrapper(inner, func)

	return inner



def check_refresh_token(
	func: Callable[
		..., dict[str, Any] | None
	]
):
	def inner(self: API_USER, *args: ...) -> dict[str, Any] | None:
		self.logger.debug('Check if expired')
		c_time = datetime.now()

		if (c_time - self.token_user.created_at).seconds >= self.token_user.expires_in:
			self.refresh_token()

		return func(self, *args)

	update_wrapper(inner, func)

	return inner
