from fastapi import APIRouter
from fastapi import Depends,Path,Query
from fastapi.responses import JSONResponse
from typing import List
from config.database import Session
from models.movie import Movie as MovieModel
from fastapi.encoders import jsonable_encoder
from middlewares.jwt_bearer import JWTBearer
from services.movie import MovieService
from schemas.movie import Movie

movie_router=APIRouter()

# movies = [
#     {
#         'id': 1,
#         'title': 'Avatar',
#         'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
#         'year': '2009',
#         'rating': 7.8,
#         'category': 'Acción'    
#     } ,
#         {
#         'id': 2,
#         'title': 'Avatar',
#         'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
#         'year': '2009',
#         'rating': 7.8,
#         'category': 'Comedia'    
#     } 
# ]

@movie_router.get('/movies',tags=['movies'],response_model=List[Movie],status_code=200,dependencies=[Depends(JWTBearer())])
def get_movies()->List[Movie]:
    db=Session()
    result=MovieService(db).get_movies()
    return JSONResponse(status_code=200,content=jsonable_encoder(result))

@movie_router.get('/movies/{id}',tags=['movies'],response_model=Movie)
def get_movie(id:int =Path(ge=1,le=2000))->Movie:
    db=Session()
    result=MovieService(db).get_movie(id)
    if not result:
        return JSONResponse(status_code=404,content={'message':'No encontrado'})
    # for item in movies:
    #     if item["id"]==id:
    #         return JSONResponse(content=item)
    return JSONResponse(status_code=200,content=jsonable_encoder(result))

@movie_router.get('/movies/',tags=['movies'],response_model=List[Movie])
def get_movie_by_category(category:str=Query(min_length=5,max_length=15))->List[Movie]:
    # movies_by_category=[]
    # for item in movies:
    #     if item["category"]==category:
    #         movies_by_category.append(item)
    # return movies_by_category
    db=Session()
    result=MovieService(db).get_movie_by_category(category)
    if not result:
        return JSONResponse(status_code=404,content={'message':'No encontrados'})
    # data =[item for item in movies if item['category']==category]
    return  JSONResponse(status_code=200,content=jsonable_encoder(result))

@movie_router.post('/movies',tags=['movies'],response_model=dict,status_code=201)
# def create_movie(id:int=Body(),title:str=Body(),overview:str=Body(),year:str=Body(),rating:float=Body(),category:str=Body()):
def create_movie(movie:Movie)->dict:
    # movies.append({
    #     'id': id,
    #     'title': title,
    #     'overview': overview,
    #     'year': year,
    #     'rating': rating,
    #     'category': category    
    # })
    db=Session()
    MovieService(db).create_movie(movie)
    # movies.append(movie)
    return JSONResponse(status_code=201,content={"message":"Se ha registrado la película"})

@movie_router.put('/movies/{id}',tags=['movies'],response_model=dict,status_code=200)
# def update_movie(id:int,title:str=Body(),overview:str=Body(),year:str=Body(),rating:float=Body(),category:str=Body()):
def update_movie(id:int,movie:Movie)->dict:
    db=Session()
    result=MovieService(db).get_movie(id)
    if not result:
        return JSONResponse(status_code=404,content={'message':'No encontrado'})
    
    MovieService(db).update_movie(id,movie)
    # for item in movies: 
    #     if item['id']==id:
    #         item['title']= movie.title
    #         item['overview']=movie.overview
    #         item['year']=movie.year
    #         item['rating']=movie.rating
    #         item['category']=movie.category 
    return JSONResponse(status_code=200,content={"message":"Se ha modificado la película"})
#     for item in movies: 
#         if item['id']==id:
#             item['title']= title
#             item['overview']=overview
#             item['year']=year
#             item['rating']=rating
#             item['category']=category    
    




@movie_router.delete('/movies/{id}',tags=['movies'],response_model=dict,status_code=200)
def delete_movie(id:int)->dict:
    db=Session()
    result:MovieModel=db.query(MovieModel).filter(MovieModel.id==id).first()
    if not result:
        return JSONResponse(status_code=404,content={'message':'No encontrado'})
    MovieService(db).delete_movie(id)
    # for item in movies: 
    #     if item['id']==id:
    #        movies.remove(item)    
    return JSONResponse(status_code=200,content={"message":"Se ha eliminado la película"})