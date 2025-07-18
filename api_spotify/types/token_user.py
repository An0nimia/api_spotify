from datetime import datetime

from pydantic import (
	BaseModel, Field
)


class Token_User(BaseModel):
	access_token: str
	token_type: str
	scope: str
	expires_in: int
	refresh_token: str

	created_at: datetime = Field(
		default_factory = datetime.now,
		frozen = True
	)
