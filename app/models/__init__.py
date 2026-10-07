"""Importa todos los modelos para que SQLAlchemy y Alembic los registren."""

from app.models.playlist import Playlist, playlist_songs
from app.models.song import Song
from app.models.user import User

__all__ = ["Playlist", "Song", "User", "playlist_songs"]
