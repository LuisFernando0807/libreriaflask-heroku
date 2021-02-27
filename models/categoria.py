from config.base_datos import bd
from sqlalchemy.orm import relationship


class CategoriaModel(bd.Model):
    __tablename__ = "t_categoria"
    categoriaId = bd.Column(name="categoria_id", type_=bd.Integer,
                            primary_key=True, autoincrement=True, nullable=False, unique=True)
    categoriaDescripcion = bd.Column(
        name="categoria_descripcion", type_=bd.String(45), unique=True, nullable=False)

    #Esto no crea las relaciones simplemente sirve para al momento de hacer consultas con JOIN'S
    libros = relationship('LibroModel', backref='categoriaLibro', lazy=True)

    def json(self):
        return {
            'categoria_id': self.categoriaId,
            'categoria_descripcion': self.categoriaDescripcion
        }

    def __init__(self, nombre):
        self.categoriaDescripcion = nombre

    def save(self):
        bd.session.add(self)
        bd.session.commit()
