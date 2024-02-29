import os
import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status
from typing import Annotated

from sqlalchemy.orm import Session

from database import database as database
from database.database import MovieDB

from model.movie import Movie

app = FastAPI()
database.Base.metadata.create_all(bind=database.engine)


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


@app.get("/health", status_code=status.HTTP_200_OK)
async def service_alive():
    return {'message': 'service alive'}


@app.get("/get_movies")
async def get_movies(db: db_dependency):
    try:
        result = db.query(MovieDB).limit(100).all()
        return result
    except Exception as e:
        return "Cant access database!"


@app.get("/get_movie_by_id")
async def get_movie_by_id(movie_id: int, db: db_dependency):
    try:
        result = db.query(MovieDB).filter(MovieDB.id == movie_id).first()
        return result
    except Exception as e:
        raise HTTPException(status_code=404, detail="Movie not found")
    return result


@app.post("/add_movie")
async def add_movie(movie: Movie, db: db_dependency):
    try:
        movie_db = MovieDB(
            id=movie.id,
            movie_name=movie.movie_name,
            creation_date=movie.creation_date,
            genre=movie.genre,
            director=movie.director
        )
        db.add(movie_db)
        db.commit()
        return movie_db
    except Exception as e:
        raise HTTPException(status_code=404, detail="Movie not found")


@app.delete("/delete_movie")
async def delete_movie(movie_id: int, db: db_dependency):
    try:
        movie_db = db.query(MovieDB).filter(MovieDB.id == movie_id).first()
        db.delete(movie_db)
        db.commit()
        return "Success"
    except Exception as e:
        return "Cant find movie"


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv('PORT', 80)))
