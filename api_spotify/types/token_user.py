from datetime import datetime

from pydantic import (
	BaseModel, computed_field
)


class Token_User(BaseModel):
	access_token: str
	token_type: str
	scope: str
	expires_in: int
	refresh_token: str


	@computed_field
	@property
	def created_at(self) -> datetime:
		return datetime.now()
