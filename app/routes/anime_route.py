from flask import Blueprint
from app.controllers import anime_controller

bp = Blueprint("anime", __name__, url_prefix="/animes")

bp.post("")(anime_controller.create_anime);
bp.get("")(anime_controller.read_animes);
bp.get("/<int:id>")(anime_controller.read_anime_by_id);
bp.patch("/<int:id>")(anime_controller.update_anime_by_id);
bp.delete("/<int:id>")(anime_controller.delete_anime_by_id);
