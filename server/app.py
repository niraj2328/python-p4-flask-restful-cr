#!/usr/bin/env python3

from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Newsletter

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///newsletters.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json_encoder = jsonify.JSONEncoder

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class Home(Resource):
    def get(self):
        response_dict = {"message": "Welcome to the Newsletter RESTful API"}
        return response_dict, 200

api.add_resource(Home, '/')

class Newsletters(Resource):
    def get(self):
        response_dict_list = [n.to_dict() for n in Newsletter.query.all()]
        return response_dict_list, 200

    def post(self):
        new_record = Newsletter(title=request.form['title'], body=request.form['body'])
        db.session.add(new_record)
        db.session.commit()
        response_dict = new_record.to_dict()
        return response_dict, 201

api.add_resource(Newsletters, '/newsletters')

class NewsletterByID(Resource):
    def get(self, id):
        newsletter = Newsletter.query.filter_by(id=id).first_or_404()
        response_dict = newsletter.to_dict()
        return response_dict, 200

api.add_resource(NewsletterByID, '/newsletters/<int:id>')

if __name__ == '__main__':
    app.run(port=5555)
