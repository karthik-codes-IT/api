from flask import Flask, json, jsonify,request

from flask_pymongo import PyMongo

from bson.json_util import dumps

from bson.objectid import ObjectId

app = Flask(__name__)

app.config['MONGO_URI'] = "mongodb://127.0.0.1:27017/User"

mongo = PyMongo(app)
 
@app.route('/add',methods=['POST'])
def add_user():
    _json = request.json
    _name = _json['name']
    _email = _json['email']

    if _name and _email and request.method == 'POST':

        id = mongo.db.user.insert({'name':_name,'email':_email})

        resp = jsonify("user added sucessfully")

        resp.status_code = 200

        return resp

    else:
        return not_found()

@app.route('/users')
def users():
    users = mongo.db.user.find()
    resp = dumps(users)
    return resp
@app.route('/user/<id>')
def user(id):
    user = mongo.db.user.find_one({'_id':ObjectId(id)})
    resp = dumps(user)
    return resp

@app.route('/delete/<id>', methods=['DELETE'])
def delete_user(id):
    mongo.db.user.delete_one({'_id':ObjectId(id)})
    resp = jsonify("user deleted successfully")

    resp.status_code = 200

    return resp

@app.route('/update/<id>', methods=['PUT'])
def update_user(id):
    _id = id
    _json = request.json
    _name = _json['name']
    _email = _json['email']

    if _name and _email and _id and request.method =='PUT':
        mongo.db.user.update_one({'_id':ObjectId(id['$oid']) if '$oid' in _id else ObjectId(_id)},{'$set':{'name':_name, 'email':_email}})

        resp = jsonify("user updated successfully")

        resp.status_code = 200
        
        return resp
    
    else:
        return not_found()

@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message':'Not Found' + request.url
    }
    resp = jsonify(message)

    resp.status_code =404

    return resp  
               

if __name__ == "__main__":
    app.run(debug=True)

