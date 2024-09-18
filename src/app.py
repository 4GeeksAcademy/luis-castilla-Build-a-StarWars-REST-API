import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, Personajes, Planetas, Favoritos, Usuario

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

@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/people', methods=['GET'])
def get_all_people():
    try:
        people = Personajes.query.all()
        people_list = [personaje.serialize() for personaje in people]
        return jsonify(people_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/people/<int:people_id>', methods=['GET'])
def get_personaje(people_id):
    try:
        personaje = Personajes.query.get(people_id)
        if not personaje:
            return jsonify({"msg": "Personaje no encontrado"}), 404
        return jsonify(personaje.serialize()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/planets', methods=['GET'])
def get_all_planets():
    try:
        planets = Planetas.query.all()
        planet_list = [planeta.serialize() for planeta in planets]
        return jsonify(planet_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    try:
        planeta = Planetas.query.get(planet_id)
        if not planeta:
            return jsonify({"msg": "Planeta no encontrado"}), 404
        return jsonify(planeta.serialize()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/users', methods=['GET'])
def get_all_users():
    users = Usuario.query.all()
    result = [user.serialize() for user in users]
    return jsonify(result), 200

@app.route('/users/<int:user_id>/favorites', methods=['GET'])
def get_user_favorites(user_id):
    user = Usuario.query.get(user_id)
    if not user:
        return jsonify({"msg": "Usuario no encontrado"}), 404

    favorites = Favoritos.query.filter_by(usuario_id=user_id).all()
    result = [fav.serialize() for fav in favorites]
    return jsonify(result), 200

@app.route('/users/<int:user_id>/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(user_id, planet_id):
    user = Usuario.query.get(user_id)
    if not user:
        return jsonify({"msg": "Usuario no encontrado"}), 404

    planet = Planetas.query.get(planet_id)
    if not planet:
        return jsonify({"msg": "Planeta no encontrado"}), 404

    favorite_exists = Favoritos.query.filter_by(usuario_id=user_id, planeta_id=planet_id).first()
    if favorite_exists:
        return jsonify({"msg": "Este planeta ya está en tus favoritos"}), 400

    new_favorite = Favoritos(usuario_id=user_id, planeta_id=planet_id)
    db.session.add(new_favorite)
    db.session.commit()
    return jsonify({"msg": "Planeta añadido a favoritos"}), 200

@app.route('/users/<int:user_id>/favorite/people/<int:people_id>', methods=['POST'])
def add_favorite_people(user_id, people_id):
    user = Usuario.query.get(user_id)
    if not user:
        return jsonify({"msg": "Usuario no encontrado"}), 404

    person = Personajes.query.get(people_id)
    if not person:
        return jsonify({"msg": "Personaje no encontrado"}), 404
    
    favorite_exists = Favoritos.query.filter_by(usuario_id=user_id, personaje_id=people_id).first()
    if favorite_exists:
        return jsonify({"msg": "Este personaje ya está en tus favoritos"}), 400

    new_favorite = Favoritos(usuario_id=user_id, personaje_id=people_id)
    db.session.add(new_favorite)
    db.session.commit()
    return jsonify({"msg": "Personaje añadido a favoritos"}), 200

@app.route('/users/<int:user_id>/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(user_id, planet_id):
    user = Usuario.query.get(user_id)
    if not user:
        return jsonify({"msg": "Usuario no encontrado"}), 404

    favorite = Favoritos.query.filter_by(usuario_id=user_id, planeta_id=planet_id).first()
    if not favorite:
        return jsonify({"msg": "Favorito no encontrado"}), 404

    db.session.delete(favorite)
    db.session.commit()
    return jsonify({"msg": "Planeta eliminado de favoritos"}), 200

@app.route('/users/<int:user_id>/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_favorite_people(user_id, people_id):
    user = Usuario.query.get(user_id)
    if not user:
        return jsonify({"msg": "Usuario no encontrado"}), 404

    favorite = Favoritos.query.filter_by(usuario_id=user_id, personaje_id=people_id).first()
    if not favorite:
        return jsonify({"msg": "Favorito no encontrado"}), 404

    db.session.delete(favorite)
    db.session.commit()
    return jsonify({"msg": "Personaje eliminado de favoritos"}), 200

if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
