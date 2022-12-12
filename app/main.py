from fastapi import FastAPI, Depends
from . import schemas, models
from .database import engine, SessionLocal
from sqlalchemy.orm import Session
from . import Funciones
from typing import Union


app = FastAPI(title='Sismos', description='En esta APi podras encontrar información acerca de eventos sísmicos y tsunamis ocurridos en Chile, Japón y Estados Unidos. Adicionalmente, permite hacer consultas de los volcanes en dichos paises.\n Para filtrar por país se deberá escribir el nombre del país de la siguiente manera: Chile, Japón, USA')
models.Base.metadata.create_all(bind = engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@app.get('/',tags=['Sismos'])
def inicio(db: Session = Depends(get_db)):
    return {'Hola':'Bienvenido a la API de EARTH DATA, por favor dirigite a la página: '}

@app.get('/sismos/all',tags=['Sismos'], description='Petición para obtener todos los registros de sismos.')
def sismos_todos(db: Session = Depends(get_db)):
    sismos_todos = Funciones.obtener_sismos(db)
    return sismos_todos

# Obtener los registros de sismos filtrando por características.
@app.get('/sismos/',tags=['Sismos'], description='Petición para obtener los registros  de sismos filtrados según sus características.')
def sismos_filtrados(max_depth: Union[float, None] = 800, min_depth: Union[float, None] = 0, min_mag: Union[float, None] = 0, max_mag: Union[float, None] = 9.9,
         min_lat: Union[float, None] = -90, max_lat: Union[float, None] = 90, min_long: Union[float, None] = -180, max_long:Union[float, None] = 180,
         min_anio: Union[float, None] = 2000, max_anio:Union[float, None] = 2022, pais : Union[str, None] = 'Japón',
         db: Session = Depends(get_db)):
    pais_valor = Funciones.pais(pais)
    sismos = db.query(models.Sismos).filter(models.Sismos.depth >= min_depth).filter(models.Sismos.depth <= max_depth).\
            filter(models.Sismos.mag <= max_mag).filter(models.Sismos.mag >= min_mag).\
                filter(models.Sismos.lat <= max_lat).filter(models.Sismos.lat >= min_lat).\
                    filter(models.Sismos.lng <= max_long).filter(models.Sismos.lng >= min_long).\
                        filter(models.Sismos.year <= max_anio).filter(models.Sismos.year >= min_anio).\
                            filter(models.Sismos.idpais == pais_valor).limit(100).all()
    return sismos


# Sismo mas fuerte para el año deseado en el pais de interes.
@app.get('/sismos/evento_maximo', tags=['Sismos'], description='Petición que retorna el sismo mas fuerte para el año deseado en el pais de interes.')
def sismo_maximo(pais_i : str,anio: int, db: Session = Depends(get_db)):
    pais_valor = Funciones.pais(pais_i)
    max_sismo = db.query(models.Sismos).select_from(models.Sismos).join(models.Pais, models.Sismos.idpais == models.Pais.idpais,).\
        filter(models.Pais.idpais == pais_valor).filter(models.Sismos.year == anio).order_by(models.Sismos.mag.desc()).limit(1).all()
    return max_sismo
    

# # TSUNAMIS

# Obtener todos los registros de tsunamis
@app.get('/tsunamis/all',tags=['Tsunamis'], description='Petición para obtener todos los registros de tsunamis.')
def tsunamis_todos(db: Session = Depends(get_db)):
    tsunamis = db.query(models.Tsunamis).all()
    return tsunamis

# Obtener los registros de intento filtrando por características.
@app.get('/tsunamis/',tags=['Tsunamis'], description='Petición para obtener los registros  de tsunamis filtrados según sus características.')
def tsunamis_filtrados(altura_olas_max: Union[float, None] = 100, altura_olas_min: Union[float, None] = 0, max_depth: Union[float, None] = 800, min_depth: Union[float, None] = 0, min_mag: Union[float, None] = 0, max_mag: Union[float, None] = 9.9,
         min_lat: Union[float, None] = -90, max_lat: Union[float, None] = 90, min_long: Union[float, None] = -180, max_long:Union[float, None] = 180,
         min_anio: Union[float, None] = 2000, max_anio:Union[float, None] = 2022,
         db: Session = Depends(get_db)):
    tsunamis = db.query(models.Tsunamis).filter(models.Tsunamis.lat <= max_lat).filter(models.Tsunamis.lat >= min_lat).\
        filter(models.Tsunamis.lng <= max_long).filter(models.Tsunamis.lng >= min_long).\
            filter(models.Tsunamis.altura_oleaje <= altura_olas_max).filter(models.Tsunamis.altura_oleaje >= altura_olas_min).\
                filter(models.Tsunamis.depth >= min_depth).filter(models.Tsunamis.depth <= max_depth).\
                    filter(models.Tsunamis.mag <= max_mag).filter(models.Tsunamis.mag >= min_mag).\
                        filter(models.Tsunamis.year <= max_anio).filter(models.Tsunamis.year >= min_anio).limit(100).all()
    return tsunamis

# Top 5 Tsunami mas fuertes para el año deseado en el pais de interes
@app.get('/Tsunamis/eventos_maximos', tags=['Tsunamis'], description='Petición para obtener los 5 tsunamis con mayor elevación de marea filtrados según pais y año.')
def tsunamis_maximos(pais_i: str, anio: int, db: Session = Depends(get_db)):
    pais_valor = Funciones.pais(pais_i)
    tsunami_maximo = db.query(models.Tsunamis).select_from(models.Tsunamis).join(models.Pais, models.Tsunamis.idpais == models.Pais.idpais).\
        filter(models.Tsunamis.year == anio).filter(models.Pais.idpais == pais_valor).order_by(models.Tsunamis.altura_oleaje.desc()).limit(5).all()
    return tsunami_maximo

# VOLCANES

# Obtener todos los registros de volcanes.
@app.get('/volcanes/all', tags=['Volcanes'], description='Petición para obtener los volcanes de los paises de interes')
def volcanes_todos(db: Session = Depends(get_db)):
    volcanes_todos = db.query(models.Volcanes).all()
    return volcanes_todos

# Obtener todos los registros de volcanes segun el pais.
@app.get('/volcanes/', tags=['Volcanes'], description='Petición para obterner los volcanes filtrados por pais.')
def volcanes_filtrados(pais_i: str,db: Session = Depends(get_db)):
    pais_valor = Funciones.pais(pais_i)
    volcanes_filtrados = db.query(models.Volcanes).select_from(models.Volcanes).join(models.Pais, models.Volcanes.idpais == models.Pais.idpais).\
        filter(models.Pais.idpais == pais_valor).all()
    return volcanes_filtrados
        


# Crear registros
# @app.post('/intento',tags=['Intento'], description='Crear registros')
# def create(request: schemas.Intento, db: Session = Depends(get_db)):
#     new_intento = models.Intento(mag=request.mag, depth=request.depth, peligro = request.peligro)
#     db.add(new_intento)
#     db.commit()
#     db.refresh(new_intento)
#     return new_intento