import os
import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status, Form
from typing import Annotated
from keycloak import KeycloakOpenID

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

KEYCLOAK_URL = "http://keycloak:8080/"
KEYCLOAK_CLIENT_ID = "test"
KEYCLOAK_REALM = "myRealm"
KEYCLOAK_CLIENT_SECRET = "zXkxCT1zhllUO1t6KqPC8qREQKklFNMM"

user_token = ""
keycloak_openid = KeycloakOpenID(server_url=KEYCLOAK_URL,
                                  client_id=KEYCLOAK_CLIENT_ID,
                                  realm_name=KEYCLOAK_REALM,
                                  client_secret_key=KEYCLOAK_CLIENT_SECRET)

###########
#Prometheus
from prometheus_fastapi_instrumentator import Instrumentator
Instrumentator().instrument(app).expose(app)

@app.post("/login")
async def login(username: str = Form(...), password: str = Form(...)):
    try:
        # Получение токена
        token = keycloak_openid.token(grant_type=["password"],
                                      username=username,
                                      password=password)
        global user_token
        user_token = token
        return token
    except Exception as e:
        print(e)  # Логирование для диагностики
        raise HTTPException(status_code=400, detail="Не удалось получить токен")

def user_got_role():
    global user_token
    token = user_token
    try:
        userinfo = keycloak_openid.userinfo(token["access_token"])
        token_info = keycloak_openid.introspect(token["access_token"])
        if "myRole" not in token_info["realm_access"]["roles"]:
            raise HTTPException(status_code=403, detail="Access denied")
        return token_info
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token or access denied")

@app.get("/health", status_code=status.HTTP_200_OK)
async def service_alive():
    if (user_got_role()):
        return {'message': 'service alive'}
    else:
        return "Wrong JWT Token"


@app.get("/get_movies")
async def get_movies(db: db_dependency):
    if (user_got_role()):
        try:
            result = db.query(MovieDB).limit(100).all()
            return result
        except Exception as e:
            return "Cant access database!"
    else:
        return "Wrong JWT Token"

@app.get("/get_movie_by_id")
async def get_movie_by_id(movie_id: int, db: db_dependency):
    if (user_got_role()):
        try:
            result = db.query(MovieDB).filter(MovieDB.id == movie_id).first()
            return result
        except Exception as e:
            raise HTTPException(status_code=404, detail="Movie not found")
        return result
    else:
        return "Wrong JWT Token"

@app.post("/add_movie")
async def add_movie(movie: Movie, db: db_dependency):
    if (user_got_role()):
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
    else:
        return "Wrong JWT Token"

@app.delete("/delete_movie")
async def delete_movie(movie_id: int, db: db_dependency):
    if (user_got_role()):
        try:
            movie_db = db.query(MovieDB).filter(MovieDB.id == movie_id).first()
            db.delete(movie_db)
            db.commit()
            return "Success"
        except Exception as e:
            return "Cant find movie"
    else:
        return "Wrong JWT Token"

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv('PORT', 80)))
