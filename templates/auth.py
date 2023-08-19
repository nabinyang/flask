from flask_restx import Namespace, Resource
from flask import Flask, render_template, url_for, request, session, redirect, flash, jsonify
from pymongo.mongo_client import MongoClient
from flask_bcrypt import Bcrypt
from db_config import db
import requests
import json
#app.secret_key = "ghalghal2323"

auth_api = Namespace(
    name='login',
    description='Authentication API'
)

#USER_NAME = config.MONGODB_USERNAME
#PASSWORD = config.MONGODB_PASSWORD

#client = MongoClient(f'mongodb://{USER_NAME}:{PASSWORD}@43.202.53.29', 27017, tlsInsecure= True)
#db = client.homey
users = db.users
'''
@auth_api.route('/kakaoStart', methods=['GET'])
class Starting(Resource):
    def get(self):
        #url = https://kauth.kakao.com/oauth/authorize?client_id=4c682d5d0c62b5c4a5d3e66d9c2c87e0&redirect_uri=https://port-0-flask-ac2nll8rz1xn.sel3.cloudtype.app/oauth&response_type=code
        url = 'https://kauth.kakao.com/oauth/authorize'
        param = {
            'client_id': '4c682d5d0c62b5c4a5d3e66d9c2c87e0',
            'redirect_uri': 'https://port-0-flask-ac2nll8rz1xn.sel3.cloudtype.app/oauth',
            'response_type': 'code'
            }
        response = requests.request("GET", url, data= json.dumps(param))

@auth_api.route('/oauth', methods=['POST'])
class Oauth(Resource):
    def post(self):
        # 1.인가코드 가져오기
        code = str(request.args.get('code'))
        #return str(code)
    
        # 2. access_token 받기
        url = "https://kauth.kakao.com/oauth/token"
        payload = "grant_type=authorization_code&client_id=4c682d5d0c62b5c4a5d3e66d9c2c87e0&redirect_uri=http://127.0.0.1:5000/oauth&code=" + str(code) +"&client_secret=rQrh7WvzTYSYMRN2hx0PWARNVdwo7KPq" 
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8',
        }
    
        response = requests.request("POST", url, data= payload, headers= headers)
        #print(json.loads(response.text))
        access_token = json.loads(((response.text).encode('utf-8')))['access_token']
        #return access_token
        
        # 3. 앱과 연결 
        url = "https://kapi.kakao.com/v1/user/signup"
    
        headers.update({'Authorization': "Bearer " + str(access_token)})
        response= requests.request("POST", url, headers=headers)
        
        #return (response.text)
        
        # 4. 사용자 정보 가져오기
        url = "https://kapi.kakao.com/v2/user/me"
        response = requests.request("POST", url, headers = headers)
        json_response = json.loads(response.text)
        return json_response
        #return (json.loads(response.text))
        user_id = json_response["id"]
        connected_at = json_response["connected_at"]
        nickname = json_response['properties']['nickname']
        #print(str(user_id) + ", " + connected_at +", " + nickname)
        
        user = db.find({'userId': user_id})
    
        if user is None: 
            db.insertOne({
                'userId': user_id,
                'connectedAt': connected_at
            })
        
        session["userId"] = user_id
        
        #return escape(session["userId"])
    '''

@auth_api.route('/register', methods=['POST'])
class Register(Resource):
    def post(self): 
        params = request.get_json()
        id_ = params['id']
        nickname = params['nickname']
        email = params['email']
        gender = params['gender']
        ageRange = params['ageRange']
        print(id_)
        print(nickname)
        print(email)
        print(gender)
        print(ageRange)
        try: 
            user = users.find_one({'id': id_})
            #print(user)
            if user is None: 
                try: 
                    #users.insert_one({'id': id_, 'nickname': nickname})
                    users.insert_one({'id': id_, 'nickname': nickname, 'email': email, 'gender': gender, 'ageRange': ageRange})
                    #print('success1')
                    #return jsonify({'response': 'success1'})
                    return "success"
                
                except Exception as e:
                    print(e)
                    response = {'response': e}
                    #return jsonify(response)
                    return "오류"
            else: 
                #response = {'response': 'success2'}
                #print('success2')
                #return jsonify(response)
                return "success"
        except Exception as e:
            #response = {'response': e}
            #print(e)
            #return jsonify(response)
            return "오류"

    
    