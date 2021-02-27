from config.base_datos import bd
from sqlalchemy.orm import relationship
#from sqlalchemy import types


class SedeModel(bd.Model):
    __tablename__ = "t_sede"
    sedeId = bd.Column(name="sede_id", type_=bd.Integer,
                       primary_key=True, autoincrement=True, unique=True)
    sedeUbicacion = bd.Column(name="sede_ubicacion", type_=bd.String(45))
    #Con el tipo de dato DECIMAL se pueden indicar el total de números y el total de decimales.
    #https://docs.sqlalchemy.org/en/13/core/type_basics.html?highlight=datatypes#sql-standard-and-multiple-vendor-types
    sedeLatitud = bd.Column(name="sede_latitud", type_=bd.DECIMAL(9,7), nullable=False)
    sedeLongitud = bd.Column(name="sede_longitud", type_=bd.DECIMAL(9,7), nullable=False)

    libros = relationship('SedeLibroModel', backref='LibroSede', lazy=True)


    def __init__(self, ubicacion, latitud, longitud):
        self.sedeUbicacion = ubicacion
        self.sedeLatitud = latitud
        self.sedeLongitud = longitud

    def save(self):
        bd.session.add(self)
        bd.session.commit()
    
    def json(self):
        return{
            'sede_id': self.sedeId,
            'sede_ubicacion':self.sedeUbicacion,
            'sede_latitud':str(self.sedeLatitud),
            'sede_longitud':str(self.sedeLongitud)
        }

    
