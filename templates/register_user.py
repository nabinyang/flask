# from flask_restx import Namespace, Resource
# from flask import Flask, render_template, url_for, request, session, redirect, flash
# from pymongo.mongo_client import MongoClient
# from flask_bcrypt import Bcrypt
# import config 

# register_user_api = Namespace(
#     name='register users',
# )

# USER_NAME = config.MONGODB_USERNAME
# PASSWORD = config.MONGODB_PASSWORD

# client = MongoClient(f'mongodb://{USER_NAME}:{PASSWORD}@43.202.53.29', 27017, tlsInsecure= True)
# db = client.homey
# users = db.user

# @register_user_api.route('/register', methods = ['POST', 'GET'])
# class Login(Resource):
#     def post(self):
#         # Code to handle user authentication
#         if request.method == 'POST':
#             userName = request.form.get("name")
#             authCode = request.form.get("authCode")
#             #user_email = request.form.get("email")
#             #user_name = request.form.get('name')
#             user_found = users.find_one({'authCode': authCode})

#             #signup_user = user.find_one({'id': request.form['id']})
        
#         if user_found:
#             #message = 'Successful Login'
#             #existId = True
#             return "This user already exists."
#         else:
#             user_input = {'username': userName, 'authCode': authCode}
#             users.insert_one(user_input)
#             return "success"
#         #pass


