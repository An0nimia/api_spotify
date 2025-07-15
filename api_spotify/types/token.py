from datetime import datetime

from pydantic import (
	BaseModel, Field
)


class Token(BaseModel):
	access_token: str
	token_type: str
	expires_in: int

	created_at: datetime = Field(
		default_factory = datetime.now,
		frozen = True
	)
