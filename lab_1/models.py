from sqlalchemy import Text, String
from .database import Base
from sqlalchemy.orm import Mapped, mapped_column


class Synonym(Base):
    __tablename__ = 'synonym'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    core_word: Mapped[str] = mapped_column(Text, nullable=False)
    synonym: Mapped[str] = mapped_column(Text, nullable=False)


class Request(Base):
    __tablename__ = 'questions_and_answers'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    request: Mapped[str] = mapped_column('question', Text, nullable=False)
    answer: Mapped[str] = mapped_column(Text, nullable=False)


class Word(Base):
    __tablename__ = 'words'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    word: Mapped[str] = mapped_column(String(100))
    connected_word: Mapped[str] = mapped_column(String(100))


class ServiceWord(Base):
    __tablename__ = 'service_words'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    word: Mapped[str] = mapped_column(Text)


class Senses(Base):
    __tablename__ = 'senses'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(Text)
    lemma: Mapped[str] = mapped_column(Text)
