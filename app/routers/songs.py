from fastapi import APIRouter, Depends, HTTPException, status

from app.dependencies import DbSession, get_current_user
from app.schemas.song import SongCreate, SongRead
from app.services import song_service

router = APIRouter(prefix="/songs", tags=["Canciones"])


@router.post(
    "",
    response_model=SongRead,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(get_current_user)],
)
def create_song(data: SongCreate, db: DbSession):
    return song_service.create_song(db, data)


@router.get("", response_model=list[SongRead])
def list_songs(db: DbSession):
    return song_service.list_songs(db)


@router.get("/{song_id}", response_model=SongRead)
def get_song(song_id: int, db: DbSession):
    song = song_service.get_song(db, song_id)
    if song is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Canción no encontrada")
    return song
