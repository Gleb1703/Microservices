import os
import uvicorn
from fastapi import FastAPI, status, Query
import requests
import random

app = FastAPI()


@app.get("/health", status_code=status.HTTP_200_OK)
async def service_alive():
    return {'message': 'service alive'}


@app.get("/")
async def root():
    r_id = random.randint(298, 10000)
    r = requests.get(f"https://kinopoiskapiunofficial.tech/api/v2.2/films/{r_id}", headers={'X-API-KEY': '700211e1-f970-499f-9957-6bca24e2adb1'})
    return r.json()


@app.get("/get_movie_by_id")
async def get_movie_by_id(q: list | None = Query()):
    film_list = []
    for id in q:
        r = requests.get(f"https://kinopoiskapiunofficial.tech/api/v2.2/films/{id}",
                         headers={'X-API-KEY': '700211e1-f970-499f-9957-6bca24e2adb1'})
        film_list.append(r.json())
    return film_list


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv('PORT', 80)))
