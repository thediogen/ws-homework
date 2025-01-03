from sqlalchemy import String, select
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base
from app.database import Session_DP
from app.utils.generate_token import generate_token


class User(Base):
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    email: Mapped[str] = mapped_column(String(128), unique=True)
    password: Mapped[str] = mapped_column()
    session_token: Mapped[int] = mapped_column(unique=True)

    @classmethod
    async def get(cls, session: Session_DP, email: str):
        stmt = select(User).where(User.email == email)
        query = await session.execute(stmt)
        user = query.scalars().all()

        return user
    
    @classmethod
    async def get_by_token(cls, session: Session_DP, token: str):
        stmt = select(User).where(User.session_token == token)
        query = await session.execute(stmt)
        user = query.scalars().all()

        return user
    
    @classmethod
    async def create(cls, session: Session_DP, form_data):
        new_user = cls(
            name=form_data.username,
            email=form_data.email,
            password=form_data.password,
            session_token=generate_token()
        )
        session.add(new_user)
        await session.commit()

        return new_user