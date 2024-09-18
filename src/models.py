from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class Usuario(db.Model):
    __tablename__ = 'usuario'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    firstname = db.Column(db.String(20), nullable=False)
    lastname = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(50), nullable=False)
    favoritos = db.relationship('Favoritos', back_populates='usuario')

    def __repr__(self):
        return '<Usuario %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "email": self.email,
        }
   
 
class Favoritos(db.Model):
    __tablename__ = 'favoritos'
    id = db.Column(db.Integer, primary_key=True)
    personaje_id = db.Column(db.Integer, db.ForeignKey('personajes.id'), nullable=True)
    planeta_id = db.Column(db.Integer, db.ForeignKey('planetas.id'), nullable=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    vehiculo_id = db.Column(db.Integer, db.ForeignKey('vehiculos.id'), nullable=True)

    usuario = db.relationship('Usuario', back_populates='favoritos')
    personaje = db.relationship('Personajes', back_populates='favoritos')
    planeta = db.relationship('Planetas', back_populates='favoritos')
    vehiculo = db.relationship('Vehiculos', back_populates='favoritos')

    def serialize(self):
        return {
            "id": self.id,
            "personaje": self.personaje.serialize() if self.personaje else None,
            "planeta": self.planeta.serialize() if self.planeta else None,
            "vehiculo": self.vehiculo.serialize() if self.vehiculo else None,
            "usuario_id": self.usuario_id
        }

class Personajes(db.Model):
    __tablename__ = 'personajes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    especie = db.Column(db.String(50), nullable=True)  
    altura = db.Column(db.Float, nullable=True)        
    peso = db.Column(db.Float, nullable=True)         
    pelicula_origen = db.Column(db.String(100), nullable=True)  
    description = db.Column(db.String(250), nullable=True)

    favoritos = db.relationship('Favoritos', back_populates='personaje')

    def __repr__(self):
        return '<Personajes %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "especie": self.especie,
            "altura": self.altura,
            "peso": self.peso,
            "pelicula_origen": self.pelicula_origen,
            "description": self.description,
        }

class Planetas(db.Model):
    __tablename__ = 'planetas'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    climate = db.Column(db.String(50), nullable=True)
    population = db.Column(db.String(50), nullable=True)
    diametro = db.Column(db.Float, nullable=True)     
    gravedad = db.Column(db.String(50), nullable=True) 
    terreno = db.Column(db.String(50), nullable=True)  
    pelicula_origen = db.Column(db.String(100), nullable=True)

    favoritos = db.relationship('Favoritos', back_populates='planeta')

    def __repr__(self):
        return '<Planetas %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "climate": self.climate,
            "population": self.population,
            "diametro": self.diametro,
            "gravedad": self.gravedad,
            "terreno": self.terreno,
            "pelicula_origen": self.pelicula_origen,
        }

class Vehiculos(db.Model):
    __tablename__ = 'vehiculos'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    modelo = db.Column(db.String(50), nullable=True)   
    fabricante = db.Column(db.String(50), nullable=True)  
    longitud = db.Column(db.Float, nullable=True)       
    velocidad_maxima = db.Column(db.Float, nullable=True) 
    capacidad_pasajeros = db.Column(db.Integer, nullable=True)

    favoritos = db.relationship('Favoritos', back_populates='vehiculo')

    def __repr__(self):
        return '<Vehiculos %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "modelo": self.modelo,
            "fabricante": self.fabricante,
            "longitud": self.longitud,
            "velocidad_maxima": self.velocidad_maxima,
            "capacidad_pasajeros": self.capacidad_pasajeros,
        }