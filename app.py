from flask import Flask, request
from flask_restful import Api
from config.base_datos import bd
#from models.autor import AutorModel
from controllers.autor import AutoresController, AutorController
#from models.categoria import CategoriaModel
from controllers.categoria import CategoriaController
#from models.libro import LibroModel
from controllers.libro import LibrosController, LibroModel, RegistroLibroSedeController
#from models.sede import SedeModel
from controllers.sede import SedesController, LibroSedeController, SedeModel, LibroCategoriaSedeController
#from models.sedeLibro import SedeLibroModel
from flask_cors import CORS
#PARA LA DOCUMENTACION
from flask_swagger_ui import get_swaggerui_blueprint


SWAGGER_URL='' #Este variable se usa para indicar en que endpoint se encontrará la documentación
API_URL='/static/swagger.json' #Se usa para indicar en que parte del proyecto se encuentra el archivo de la documentación
swagger_blueprint = get_swaggerui_blueprint( #Blueprint sirve para hacer aplicaciones modulares
    SWAGGER_URL,
    API_URL,
    config={
        'app_name':"Libreria Flask - Swagger Documentation"
    }
)


app = Flask(__name__)
app.register_blueprint(swagger_blueprint)
# https://flask-sqlalchemy.palletsprojects.com/en/2.x/config/#connection-uri-format
#                                    formato://username:password@host:port/databasename
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:Mysql123*@localhost:3306/flasklibreria'
api = Api(app)
CORS(app) #PERMITIENDO TODOS LOS MÉTODOS, DOMINIOS Y HEADERS
# si tu servidor no tiene contraseña, ponlo asi:
# 'mysql://root:@localhost:3306/flasklibreria'
# para evitar el warning de la funcionalidad de sqlalchemy de track modification:
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# inicio la aplicacion proveyendo las credenciales indicadas en el app.config pero aun no se ha conectado a la bd
bd.init_app(app)
#Con drop all se eliminan todas las tablas MAPEADAS del proyecto
#bd.drop_all(app=app)
# recien se conecta a la bd, pero necesita el driver para poder conectarse
# para conectarnos a una base de datos en mysql deberemos instalar el driver: pip install mysqlclient
bd.create_all(app=app)

@app.route('/buscar')
def buscarLibro():
    
    print(request.args.get('palabra'))
    #De acuerdo a la palabra mandada que me de el resultado de la busqueda de todos los libros, si no hay ningun
    #libro con esa palabra o no se mandó la palabra indicar que la busqueda no tuvo efecto. Con un BAD REQUEST.
    palabra = request.args.get('palabra')
    if palabra:
        resultadoBusqueda=LibroModel.query.filter(LibroModel.libroNombre.like('%'+ palabra +'%')).all()
        if resultadoBusqueda:
            resultado = []
            for libro in resultadoBusqueda:
                resultado.append(libro.json())
            return {
                'success':True,
                'content': resultado,
                'message': None
            }

    return {
        'success':False,
        'content':None,
        'message': 'No se encontró nada para buscar o la búsqueda no tuvo éxito'
    }, 400

#RUTAS DE MI API RESTFUL
api.add_resource(AutoresController,'/autores')
api.add_resource(AutorController, '/autor/<int:id>')
api.add_resource(CategoriaController, '/categorias','/categoria')
api.add_resource(LibrosController, '/libro','/libros')
api.add_resource(SedesController, '/sedes','/sede')
api.add_resource(LibroSedeController,'/sedeLibros/<int:id_sede>')
api.add_resource(LibroCategoriaSedeController,'/busquedaLibroSedeCat')
api.add_resource(RegistroLibroSedeController,'/registrarSedesLibro')



if __name__ == '__main__':
    app.run(debug=True)
