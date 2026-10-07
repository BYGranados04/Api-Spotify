"""Punto de entrada de Musicflow API."""

from fastapi import FastAPI

from app.routers import auth, playlists, songs, users

app = FastAPI(
    title="Musicflow API",
    description="API REST análoga a Spotify: usuarios, canciones y playlists con autenticación JWT.",
    version="0.1.0",
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(songs.router)
app.include_router(playlists.router)
