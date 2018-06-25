# -*- coding: utf-8 -*-

from flask import Flask, jsonify, url_for, redirect, request
from flask_pymongo import PyMongo
from flask_restful import Api, Resource

app = Flask(__name__)
app.config["MONGO_DBNAME"] = "contatos_db"
mongo = PyMongo(app, config_prefix='MONGO')
APP_URL = "http://127.0.0.1:5000"


class Contatos(Resource):
    def get(self, cpf=None, nome=None, telefone=None):
        data = []
        if cpf:
            contato = mongo.db.contatos.find_one({"cpf": cpf}, {"_id": 0})
            if contato:
                return jsonify({"status": "ok", "data": contato})
            else:
                return {"response": "nenhum contato encontrado para {}".format(cpf)}

        elif nome:
            contato = mongo.db.contatos.find_one({"nome": nome}, {"_id": 0})
            if contato:
                return jsonify({"status": "ok", "data": contato})
            else:
                return jsonify({"response": "nenhum contato encontrado para {}".format(nome)})

        elif telefone:
            contato = mongo.db.contatos.find_one({"telefone": telefone}, {"_id": 0})
            if contato:
                return jsonify({"status": "ok", "data": contato})
            else:
                return jsonify({"response": "nenhum contato encontrado para {}".format(telefone)})

    def post(self):
        data = request.get_json()
        if not data:
            data = {"response": "error"}
            return jsonify(data)
        else:
            cpf = data.get('cpf')
            if cpf:
                if mongo.db.contatos.find_one({"cpf": cpf}):
                    return jsonify({"response": "contato ja existe"})
                else:
                    mongo.db.contatos.insert(data)
            else:
                return jsonify({"response": "cpf do contato faltando"})
        
        return jsonify({"response": "contato adicionado"})

    def put(self, cpf):
        data = request.get_json()
        mongo.db.contatos.update({'cpf': cpf}, {'$set': data})
        return jsonify({"response": "contato atualizado"})

    def delete(self, cpf):
        mongo.db.contatos.remove({'cpf': cpf})
        return jsonify({"response": "contato removido"})


class Index(Resource):
    def get(self):
        return jsonify({"response": "api de contatos"})


api = Api(app)
api.add_resource(Index, "/", endpoint="index")
api.add_resource(Contatos, "/api", endpoint="contatos")
api.add_resource(Contatos, "/api/<string:cpf>", endpoint="cpf")
api.add_resource(Contatos, "/api/nome/<string:nome>", endpoint="nome")
api.add_resource(Contatos, "/api/telefone/<string:telefone>", endpoint="telefone")

if __name__ == "__main__":
    app.run(debug=True)