from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, String, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.song import Song
    from app.models.user import User

# Tabla intermedia de la relación muchos a muchos Playlist <-> Song.
# La clave primaria compuesta impide repetir una canción en la misma playlist.
playlist_songs = Table(
    "playlist_songs",
    Base.metadata,
    Column("playlist_id", ForeignKey("playlists.id", ondelete="CASCADE"), primary_key=True),
    Column("song_id", ForeignKey("songs.id", ondelete="CASCADE"), primary_key=True),
)


class Playlist(Base):
    __tablename__ = "playlists"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)

    owner: Mapped["User"] = relationship(back_populates="playlists")
    # selectin carga las canciones en una sola consulta adicional (evita N+1).
    songs: Mapped[list["Song"]] = relationship(secondary=playlist_songs, lazy="selectin")
