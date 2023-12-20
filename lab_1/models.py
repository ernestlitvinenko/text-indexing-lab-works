from sqlalchemy import Text
from .database import Base
from sqlalchemy.orm import Mapped, mapped_column


class Synonym(Base):
    __tablename__ = 'synonym'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    core_word: Mapped[str] = mapped_column(Text, nullable=False)
    synonym: Mapped[str] = mapped_column(Text, nullable=False)


class Request(Base):
    __tablename__ = 'request'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    request: Mapped[str] = mapped_column(Text, nullable=False)
    answer: Mapped[str] = mapped_column(Text, nullable=False)

