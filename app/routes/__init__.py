from flask import Flask

from app.routes.anime_route import bp as bp_anime

def init_app(app: Flask):

    app.register_blueprint(bp_anime)