from flask import Flask,request,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS, cross_origin
import os

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLDATABASE_ENV')
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///prueba.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

#Creacion de Tabla Categorias
class Categorias(db.Model):
    cat_id = db.Column(db.Integer,primary_key=True)
    cat_nom = db.Column(db.String(100))
    cat_desp = db.Column(db.String(100))

    def __init__(self,cat_nom,cat_desp):
        self.cat_nom = cat_nom
        self.cat_desp = cat_desp

with app.app_context():
    db.create_all()

#Esquema Categorias
class CategoriaSchema(ma.Schema):
    class Meta:
        fields = ('cat_id', 'cat_nom', 'cat_desp')

#Una sola Respuesta
categoria_schema = CategoriaSchema()

#Cuando sean muchas respuestas
categorias_schema = CategoriaSchema(many=True)

#GET
@app.route('/categorias',methods=['GET'])
@cross_origin()
def get_categorias():
    all_categorias = Categorias.query.all()
    result = categorias_schema.dump(all_categorias)
    return jsonify(result)

#GET X ID
@app.route('/categoria/<id>',methods=['GET'])
@cross_origin()
def get_categoria_x_id(id):
    una_categoria = Categorias.query.get(id)
    return categoria_schema.jsonify(una_categoria)

#POST
@app.route('/categoria',methods=['POST'])
@cross_origin()
def insert_categoria():
    data = request.get_json(force=True)
    cat_nom = data['cat_nom']
    cat_desp = data['cat_desp']

    nuevo_registro = Categorias(cat_nom,cat_desp)
    db.session.add(nuevo_registro)
    db.session.commit()
    return categoria_schema.jsonify(nuevo_registro)

#PUT
@app.route('/categoria/<id>',methods=['PUT'])
@cross_origin()
def update_categoria(id):
    act_categoria = Categorias.query.get(id)
    data = request.get_json(force=True)
    cat_nom = data['cat_nom']
    cat_desp = data['cat_desp']

    act_categoria.cat_nom = cat_nom
    act_categoria.cat_desp = cat_desp

    db.session.commit()
    return categoria_schema.jsonify(act_categoria)

#DELETE
@app.route('/categoria/<id>',methods=['DELETE'])
@cross_origin()
def delete_categoria(id):
    del_categoria = Categorias.query.get(id)
    db.session.delete(del_categoria)
    db.session.commit()
    return categoria_schema.jsonify(del_categoria)

#Mensaje de Bienvenida
@app.route('/',methods=['GET'])
@cross_origin()
def index():
    return jsonify({'Mensaje':'Bienvenido'})

if __name__ == "__main__":
    app.run(debug=True)


