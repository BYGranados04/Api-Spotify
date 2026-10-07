"""Lógica de negocio de playlists."""

from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.playlist import Playlist
from app.models.song import Song
from app.schemas.playlist import PlaylistCreate


def create_playlist(db: Session, owner_id: int, data: PlaylistCreate) -> Playlist:
    playlist = Playlist(name=data.name, owner_id=owner_id)
    db.add(playlist)
    db.commit()
    db.refresh(playlist)
    return playlist


def list_user_playlists(db: Session, owner_id: int) -> Sequence[Playlist]:
    return db.scalars(
        select(Playlist).where(Playlist.owner_id == owner_id).order_by(Playlist.id)
    ).all()


def get_user_playlist(db: Session, playlist_id: int, owner_id: int) -> Playlist | None:
    """Devuelve la playlist solo si pertenece al usuario indicado."""
    playlist = db.get(Playlist, playlist_id)
    if playlist is None or playlist.owner_id != owner_id:
        return None
    return playlist


def add_song(db: Session, playlist: Playlist, song: Song) -> bool:
    """Agrega la canción. Devuelve False si ya estaba en la playlist."""
    if song in playlist.songs:
        return False
    playlist.songs.append(song)
    db.commit()
    db.refresh(playlist)
    return True
