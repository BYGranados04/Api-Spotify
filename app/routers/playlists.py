from fastapi import APIRouter, HTTPException, status

from app.dependencies import CurrentUser, DbSession
from app.schemas.playlist import PlaylistCreate, PlaylistRead
from app.services import playlist_service, song_service

router = APIRouter(prefix="/playlists", tags=["Playlists"])


@router.post("", response_model=PlaylistRead, status_code=status.HTTP_201_CREATED)
def create_playlist(data: PlaylistCreate, db: DbSession, current_user: CurrentUser):
    return playlist_service.create_playlist(db, current_user.id, data)


@router.get("", response_model=list[PlaylistRead])
def list_my_playlists(db: DbSession, current_user: CurrentUser):
    return playlist_service.list_user_playlists(db, current_user.id)


@router.post("/{playlist_id}/songs/{song_id}", response_model=PlaylistRead)
def add_song_to_playlist(playlist_id: int, song_id: int, db: DbSession, current_user: CurrentUser):
    # Una playlist ajena responde 404 para no revelar que existe.
    playlist = playlist_service.get_user_playlist(db, playlist_id, current_user.id)
    if playlist is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Playlist no encontrada")
    song = song_service.get_song(db, song_id)
    if song is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Canción no encontrada")
    if not playlist_service.add_song(db, playlist, song):
        raise HTTPException(status.HTTP_409_CONFLICT, detail="La canción ya está en la playlist")
    return playlist
