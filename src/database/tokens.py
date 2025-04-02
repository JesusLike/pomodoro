from dataclasses import dataclass
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.models.auth import DbAccessToken

@dataclass
class TokensRepository():
    session: Session

    def get_tokens(self, user_id: int) -> list[DbAccessToken]:
        query = select(DbAccessToken).where(DbAccessToken.user_id == user_id)
        return self.session.execute(query).scalars().all()

    def create_token(self, props: dict[str, any]) -> DbAccessToken:
        db_token = DbAccessToken(**props)
        self.session.add(db_token)
        self.session.commit()
        return db_token
