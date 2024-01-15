#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.exc import IntegrityError
from datetime import datetime

# Flask application setup
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy and Flask-Migrate
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Model definitions
class Hero(db.Model):
    __tablename__ = 'heroes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    super_name = db.Column(db.String(100), nullable=False)
    hero_powers = db.relationship('HeroPower', backref='hero')

class Power(db.Model):
    __tablename__ = 'powers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    power_heroes = db.relationship('HeroPower', backref='power')

class HeroPower(db.Model):
    __tablename__ = 'hero_powers'
    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.String(50), nullable=False)
    hero_id = db.Column(db.Integer, db.ForeignKey('heroes.id'), nullable=False)
    power_id = db.Column(db.Integer, db.ForeignKey('powers.id'), nullable=False)

    def validate_strength(self, strength):
        if strength not in ['Strong', 'Weak', 'Average']:
            raise ValueError("Invalid strength value")
        return strength

# API routes
@app.route('/heroes', methods=['GET'])
def get_heroes():
    heroes = Hero.query.all()
    return jsonify([{'id': hero.id, 'name': hero.name, 'super_name': hero.super_name} for hero in heroes])

@app.route('/heroes/<int:hero_id>', methods=['GET'])
def get_hero(hero_id):
    hero = Hero.query.get(hero_id)
    if not hero:
        return jsonify({"error": "Hero not found"}), 404

    powers = [{'id': hp.power.id, 'name': hp.power.name, 'description': hp.power.description} for hp in hero.hero_powers]
    return jsonify({'id': hero.id, 'name': hero.name, 'super_name': hero.super_name, 'powers': powers})

@app.route('/powers', methods=['GET'])
def get_powers():
    powers = Power.query.all()
    return jsonify([{'id': power.id, 'name': power.name, 'description': power.description} for power in powers])

@app.route('/powers/<int:power_id>', methods=['GET'])
def get_power(power_id):
    power = Power.query.get(power_id)
    if not power:
        return jsonify({"error": "Power not found"}), 404
    return jsonify({'id': power.id, 'name': power.name, 'description': power.description})

@app.route('/powers/<int:power_id>', methods=['PATCH'])
def update_power(power_id):
    power = Power.query.get(power_id)
    if not power:
        return jsonify({"error": "Power not found"}), 404

    data = request.get_json()
    description = data.get("description", "")

    if len(description) < 20:
        return jsonify({"errors": ["Description must be at least 20 characters long"]}), 400

    power.description = description
    db.session.commit()
    return jsonify({'id': power.id, 'name': power.name, 'description': power.description})

@app.route('/hero_powers', methods=['POST'])
def create_hero_power():
    data = request.get_json()
    strength = data.get("strength")
    power_id = data.get("power_id")
    hero_id = data.get("hero_id")

    if strength not in ['Strong', 'Weak', 'Average']:
        return jsonify({"errors": ["Invalid strength"]}), 400

    try:
        hero_power = HeroPower(strength=strength, hero_id=hero_id, power_id=power_id)
        db.session.add(hero_power)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"errors": ["Invalid hero or power ID"]}), 400

    hero = Hero.query.get(hero_id)
    powers = [{'id': hp.power.id, 'name': hp.power.name, 'description': hp.power.description} for hp in hero.hero_powers]
    return jsonify({'id': hero.id, 'name': hero.name, 'super_name': hero.super_name, 'powers': powers})

@app.route('/')
def home():
    return 'Welcome to the Superhero API'

if __name__ == '__main__':
    app.run(port=5555, debug=True)
