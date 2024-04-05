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
        plants_dict = [plant.to_dict() for plant in Plant.query.all()]
        return make_response(plants_dict, 200)
    
    def post(self):
        new_plant = Plant(name=request.get_json('name'), image=request.get_json('image'), price=request.get_json('price'))
        db.session.add(new_plant)
        db.session.commit()

        plant_dict = new_plant.to_dict()
        response = make_response(plant_dict, 201)
        return response
# Take note on why you use the get_json() method, this allows our front end to work with our back end to pass the data in the correct format so it could be processed correctly. This is used in place of the .json.get('') variation. THIS IS IMPORTANT!

    
api.add_resource(Plants, '/plants')

class PlantByID(Resource):
    def get(self, id):
        plant_id = db.session.get(Plant, id)
        plant_dict = plant_id.to_dict()

        response = make_response(plant_dict, 200)
        return response
        
api.add_resource(PlantByID, '/plants/<int:id>')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
