from flask_restx import Namespace, Resource
from flask import Flask, render_template, url_for, request, session, redirect, flash
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

@auth_api.route('/kakaoStart', methods=['GET', 'POST'])
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

@auth_api.route('/oauth', methods=['GET', 'POST'])
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
        '''
        user = db.find({'userId': user_id})
    
        if user is None: 
            db.insertOne({
                'userId': user_id,
                'connectedAt': connected_at
            })
        
        session["userId"] = user_id
        '''
        #return escape(session["userId"])
    

@auth_api.route('/register', methods=['GET', 'POST'])
class Register(Resource):
    def post(self): 
        #nickname = request.form['name']
        nickname = request.args.get('nickname')
        id = request.args.get('id')
        #gender = request.form['gender']
        #age_range = request.form['age_range']
        #code = str(request.form['code'])
        try: 
            user = users.find({'id': id})
            if user is None: 
                try: 
                    #user.insert_one({'id': id, 'nickname': nickname, 'gender': gender, 'age_range': age_range})
                    user.insert_one({'id': id, 'nickname': nickname})
                    return "success"
                    #session['username'] = nickname
                except Exception as e:
                    return e
            else: 
                #session['username'] = nickname
                return '이미 있는 사용자'
        except Exception as e:
            return e
        

    
    


'''
@app.route('/oauth/logout')
def kakao_logout():
    code = str(request.form['code'])

    url = 'https://kapi.kakao.com/v1/user/logout?client_id=4c682d5d0c62b5c4a5d3e66d9c2c87e0'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': "KakaoAK " + '7029bc1203cf9469db6b8521023b8aa0',
    }
'''















'''
@login_api.route('/login', methods = ['POST', 'GET'])
class Login(Resource):
    def post(self):
        # Code to handle user authentication
        if request.method == 'POST':
            user_id = request.form.get("id")
            user_found = users.find_one({'id': user_id})

            #signup_user = user.find_one({'id': request.form['id']})
        
        if user_found:
            #message = 'Successful Login'
            success = True
            return success
        pass

@login_api.route('/logout')
class Logout(Resource):
    def post(self):
        # Code to handle user logout
        pass
'''
