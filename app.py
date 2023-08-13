from flask import Flask, render_template, request
from flask_restx import Api, Resource, fields, Namespace
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import db_config 
from templates.auth import auth_api
from templates.board import board_api
from templates.real_estate import real_estate_api
from templates.agents import agents_api
from templates.home_safety_rating import home_safety_rating_api 
from templates.register_user import register_user_api
from templates.survey import survey_api

app = Flask(__name__)
api = Api(
    app,
    version='0.1',
    title="Homey API",
    description="Homey API Server!",
    terms_url="/",
    contact="seungjaelim@kaist.ac.kr",
    license="MIT"
)
api.add_namespace(auth_api)
api.add_namespace(board_api)
api.add_namespace(real_estate_api)
api.add_namespace(agents_api)
api.add_namespace(home_safety_rating_api)
api.add_namespace(register_user_api)
api.add_namespace(survey_api)

if __name__ == "__main__":
    # Send a ping to confirm a successful connection
    try:
        # client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)
    app.run(debug=True, host='0.0.0.0', port=5000)
