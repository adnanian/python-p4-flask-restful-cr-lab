#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = True

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class Plants(Resource):
    def get(self):
        plants = [plant.to_dict() for plant in Plant.query.all()]
        return make_response(plants, 200)
    
    def post(self):
        new_plant = Plant(
            name=request.get_json()["name"],
            image=request.get_json()["image"],
            price=request.get_json()["price"]
        )
        db.session.add(new_plant)
        db.session.commit()
        return make_response(new_plant.to_dict(), 201)

class PlantByID(Resource):
    def get(self, id):
        if plant := Plant.query.filter_by(id=id).first():
            return make_response(plant.to_dict(), 200)
        else:
            response_body = {
                "message": "This record does not exist in our database. Please try again."
            }
            return make_response(response_body, 404)
        
api.add_resource(Plants, '/plants')
api.add_resource(PlantByID, '/plants/<int:id>')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
