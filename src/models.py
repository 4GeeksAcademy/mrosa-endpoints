from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    favorites = db.relationship('Favorite', backref='user', lazy=True)

    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,

            # do not serialize the password, its a security breach
        }
    
class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=False, nullable=False)
    height = db.Column(db.String(120), unique=False, nullable=False)
    mass = db.Column(db.String(120), unique=False, nullable=False)
    hair_color = db.Column(db.String(120), unique=False, nullable=False)
    favorites = db.relationship('Favorite', backref='character', lazy=True)
                           
    def __repr__(self):
        return '<Character %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "height": self.height,
            "mass": self.mass,
            "hair_color": self.hair_color
           
        }
    
class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=False, nullable=False)
    rotation_period = db.Column(db.String(120), unique=False, nullable=False)
    orbital_period = db.Column(db.String(120), unique=False, nullable=False)
    diameter = db.Column(db.String(120), unique=False, nullable=False)
    climate = db.Column(db.String(120), unique=False, nullable=False)
    gravity = db.Column(db.String(120), unique=False, nullable=False)
    terrain = db.Column(db.String(120), unique=False, nullable=False)
    surface_water = db.Column(db.String(120), unique=False, nullable=False)
    population = db.Column(db.String(120), unique=False, nullable=False)
    favorites = db.relationship('Favorite', backref='planet', lazy=True)
                           
    def __repr__(self):
        return '<Planet %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "rotation_period": self.rotation_period,
            "orbital_period": self.orbital_period,
            "diameter": self.diameter,
            "climate": self.climate,
            "gravity": self.gravity,
            "terrain": self.terrain,
            "surface_water": self.surface_water,
            "population": self.population
           
        }
    
class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    Planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'), nullable=False)
    Character_id = db.Column(db.Integer, db.ForeignKey('character.id'), nullable=False)
    
    def __repr__(self):
        return '<Favorite %r>' % self.id



    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "Planet_id": self.Planet_id,
            "Character_id": self.Character_id
             }