from flask import Flask, request, jsonify, Response
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from bson import json_util
from bson.objectid import ObjectId

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb+srv://admin:admin123@cluster0.32pgj.mongodb.net/covid19?retryWrites=true&w=majority"
mongo = PyMongo(app)

# Define la ruta de users con el metodo POST para registrar un nuevo usuario
@app.route("/users", methods=["POST"])
def create_user():
    username = request.json["username"]
    password = request.json["password"]
    email = request.json["email"]
    if username and password and email:
        generated_password = generate_password_hash(password)
        id = mongo.db.users.insert_one({
            "username": username,
            "password": generated_password,
            "email": email
        })
        response = {
            "id": str(id),
            "username": username,
            "password": generated_password,
            "email": email
        }
        return response
    else:
        return not_found()

    return {"message": "User created successfully"}   

# Define la ruta de users con el metodo GET para obtener todos los usuarios
@app.route("/users", methods=["GET"])
def get_users():
    users = mongo.db.users.find()
    response = json_util.dumps(users)
    return Response(response, mimetype="application/json")

# Define la ruta de users con el metodo GET para obtener un usuario por id
@app.route("/users/<id>", methods=["GET"])
def get_user(id):
    user = mongo.db.users.find_one({"_id": ObjectId(id)})
    response = json_util.dumps(user)
    return Response(response, mimetype="application/json")

# Define la ruta de users con el metodo DELETE para eliminar un usuario por id
@app.route("/users/<id>/d", methods=["DELETE"])
def delete_user(id):
    mongo.db.users.delete_one({"_id": ObjectId(id)})
    return {"message": "User " + id + " deleted successfully"}

# Define la ruta de users con el metodo PUT para actualizar un usuario por id
@app.route("/users/<id>", methods=["PUT"])
def update_user(id):
    username = request.json["username"]
    password = request.json["password"]
    email = request.json["email"]
    if username and password and email:
        generated_password = generate_password_hash(password)
        mongo.db.users.update_one({"_id": ObjectId(id)}, {
            "$set": {
                "username": username,
                "password": generated_password,
                "email": email
            }
        })
        return {"message": "User " + id + " updated successfully"}
    else:
        return not_found()

# Define a function to return a 404 error
@app.errorhandler(404)
def not_found(error=None):
    response = jsonify({
        "message": "Resource Not found: " + request.url,
        "status": 404
    })
    response.status_code = 404
    return response


if __name__ == '__main__':
    app.run(debug=True)