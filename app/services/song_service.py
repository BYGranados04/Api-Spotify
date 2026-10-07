"""Lógica de negocio de canciones."""

from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.song import Song
from app.schemas.song import SongCreate


def create_song(db: Session, data: SongCreate) -> Song:
    song = Song(**data.model_dump())
    db.add(song)
    db.commit()
    db.refresh(song)
    return song


def list_songs(db: Session) -> Sequence[Song]:
    return db.scalars(select(Song).order_by(Song.id)).all()


def get_song(db: Session, song_id: int) -> Song | None:
    return db.get(Song, song_id)
