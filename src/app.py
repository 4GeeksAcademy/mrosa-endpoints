"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Character, Planet, Favorite
#from models import Person



app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code
@app.route('/wipeall', methods=['GET'])
def database_wipe():
    try:
        db.reflect()
        db.drop_all()
        db.session.commit()
    except Exception as e:
        return "mec", 500
    return "ok", 200

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/Character', methods=['GET'])
def handle_hello():
    characters = Character.query.all()
    characters = list(map(lambda x: x.serialize(), characters))
    response_body = {
        
        "characters": characters

    }

    return jsonify(response_body), 200


@app.route('/Character/<int:id>', methods=['GET'])
def get_single_character(id):
    character = Character.query.get(id)
    if character is None:
        raise APIException('Character not found', status_code=404)
    return jsonify(character.serialize()), 200

@app.route('/User', methods=['GET'])
def handle_user():
    users = User.query.all()
    users = list(map(lambda x: x.serialize(), users))
    response_body = {
        
        "users": users

    }

    return jsonify(response_body), 200
    

@app.route('/User/Favorites', methods=['GET'])
def handle_favorites():
    favorites = Favorite.query.all()
    favorites = list(map(lambda x: x.serialize(), favorites))
    response_body = {
        
        "favorites": favorites

    }

    return jsonify(response_body), 200


@app.route('/Planet', methods=['GET'])
def handle_planet():
    planets = Planet.query.all()
    planets = list(map(lambda x: x.serialize(), planets))
    response_body = {
        
        "planets": planets

    }

    return jsonify(response_body), 200

@app.route('/favorites', methods=['POST'])
def add_favorite():
    request_body = request.get_json()
    favorite = Favorite(user_id=request_body["user_id"], Planet_id=request_body["planet_id"], Character_id=request_body["character_id"])
    db.session.add(favorite)
    db.session.commit()
    return jsonify("Favorite added successfully"), 200

@app.route('/favorites/<int:id>', methods=['DELETE'])
def delete_favorite(id):
    favorite = Favorite.query.get(id)
    if favorite is None:
        raise APIException('Favorite not found', status_code=404)
    db.session.delete(favorite)
    db.session.commit()
    return jsonify("Favorite deleted successfully"), 200
 


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)