from psycopg2.errors import UniqueViolation
from app.models.anime_model import Anime
from flask import jsonify, request
from http import HTTPStatus


def create_anime():
    data = request.get_json()

    if len(Anime.available_keys(data.keys())) != 0:
        return jsonify({"available_keys": Anime.valid_keys, "wrong_keys_sended": Anime.available_keys(data.keys())}), HTTPStatus.UNPROCESSABLE_ENTITY

    serie =  Anime(**data)    

    try:    
        inserted_anime = serie.create_anime()

    except UniqueViolation:
        return {"msg": "Anime aready exist in list"}, HTTPStatus.CONFLICT

    inserted_anime = Anime.serealiaze_anime(inserted_anime)

    return inserted_anime, HTTPStatus.CREATED


def read_animes():
    
    animes = Anime.read_all_animes()

    animes = Anime.serealiaze_anime(animes)

    return jsonify(animes), HTTPStatus.OK


def read_anime_by_id(id):
    
    anime = Anime.read_by_id(id)

    if not anime:
        return jsonify({}), HTTPStatus.NOT_FOUND

    anime = Anime.serealiaze_anime(anime)

    return jsonify(anime), HTTPStatus.OK


def update_anime_by_id(id):
    data = request.get_json()

    if len(Anime.available_keys(data.keys())) != 0:
        return jsonify({"available_keys": Anime.valid_keys, "wrong_keys_sended": Anime.available_keys(data.keys())}), HTTPStatus.UNPROCESSABLE_ENTITY

    try:
        update_anime = Anime.update_by_id(id, data)
    
    except UniqueViolation:
        return {"msg": "Anime aready exist in list"}, HTTPStatus.CONFLICT

    if not update_anime:
        return {"msg": "Not found"}, HTTPStatus.NOT_FOUND
        
    update_anime = Anime.serealiaze_anime(update_anime)

    return jsonify(update_anime), HTTPStatus.OK


def delete_anime_by_id(id):

    anime = Anime.delete_by_id(id)

    if not anime:
        return jsonify({"msg": "Not foud"}), HTTPStatus.NOT_FOUND   

    anime = Anime.serealiaze_anime(anime)    

    return jsonify(anime), HTTPStatus.NO_CONTENT  