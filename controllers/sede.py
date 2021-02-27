from flask_restful import Resource, reqparse
from models.sede import SedeModel

#GET ALL SEDE
#CREATE SEDE
#VINCULA UNA SEDE CON VARIOS LIBROS Y VICEVERSA (UN LIBRO CON VARIAS SEDES)

serializer = reqparse.RequestParser(bundle_errors=True)
serializer.add_argument(
    'sede_latitud',
    type=float,
    required=True,
    help='Falta la sede_latitud',
    dest='latitud' #Es como se va a llamar una vez que hemos usado el método parse_args()
)
serializer.add_argument(
    'sede_ubicacion',
    type=str,
    required=True,
    help='Falta la sede_ubicacion',
    dest='ubicacion' #Es como se va a llamar una vez que hemos usado el método parse_args()
)
serializer.add_argument(
    'sede_longitud',
    type=float,
    required=True,
    help='Falta la sede_longitud',
    dest='longitud' #Es como se va a llamar una vez que hemos usado el método parse_args()
)

class SedesController(Resource):
    def post(self):
        data = serializer.parse_args()
        print(data)
        #Los tipos de datos que no son ni numericos ni strings = decimal, fecha, no puede hacer la conversión automática
        nuevaSede=SedeModel(data['ubicacion'], data['latitud'], data['longitud'])
        nuevaSede.save()
        return {
            'success':True,
            'content':nuevaSede.json(),
            'message':'Se creó la sede exitosamente'
        }
    def get(self):
        sedes = SedeModel.query.all()
        resultado = []
        for sede in sedes:
            resultado.append(sede.json())
        return {
            'success':True,
            'content':resultado,
            'message': None
        }

#BUSQUEDA DE TODOS LOS LIBROS DE UNA SEDE
class LibroSedeController(Resource):
    def get(self, id_sede):
        #De acuerdo al id de la sede, devolver todos los libros que hay en esa sede
        sede = SedeModel.query.filter_by(sedeId=id_sede).first()
        sedeLibros = sede.libros #me retorna todas mis sedesLibros
        libros = []
        for sedeLibro in sedeLibros:
            libro = sedeLibro.libroSede.json()
            #Agregar el autor del libro
            libro['autor'] = sedeLibro.libroSede.autorLibro.json()
            libro['categoria'] = sedeLibro.libroSede.categoriaLibro.json()
            del libro['categoria']['categoria_id']
            del libro['autor_id']
            libros.append(libro)
            #libros.append(sedes.autorLibro.json())
            #print(sedeLibro.libroSede.json())
        resultado = sede.json()
        resultado['libros']=libros
        return{
            'success':True,
            'content':resultado
        }
       

#BUSQUEDA DE TODOS LOS LIBROS DE UNA SEDE SEGUN SU CATEGORIA
#CATEGORIA
#SEDE
#127.0.0.1:5000/buscarLibroCategoria?sede=1&categoria=2

class LibroCategoriaSedeController(Resource):
   def get(self):
        serializer.remove_argument('sede_latitud')
        serializer.remove_argument('sede_longitud')
        serializer.remove_argument('sede_ubicacion')
        serializer.add_argument(
           'categoria',
           type=int,
           required=True,
           help='Falta la categoria',
           location='args' #Args: Sirve para que me mande por el querystring(de forma dinámica).
        )
        serializer.add_argument(
            'sede',
            type=int,
            required=True,
            help='Falta la sede',
            location='args' 
        )
        data = serializer.parse_args()
        #Luego de mi sede ingresar a mi sede_libro -> [].., luego ingresar a mis libros 
        #y hacer el filtro según la categoria(data['categoria])
        sede = SedeModel.query.filter_by(sedeId=data['sede']).first()
        #print(sede.libros)
        libros=[]
        for sedelibro in sede.libros:
            #print(sedelibro.libroSede.categoria)
            if(sedelibro.libroSede.categoria == data['categoria']):
                libros.append(sedelibro.libroSede.json())
        return {
            'success':True,
            'content':libros
        }
    