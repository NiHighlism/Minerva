"""for user related operations"""

import datetime
from logging import getLogger

from flask_login import current_user

from app.main import db
from app.main.models.movies import Movie
from app.main.models.users import User
from app.main.models.posts import Post

LOG = getLogger(__name__)


class UserService:

    @staticmethod
    def get_by_username(username):
        try:
            user = User.query.filter_by(username=username).first()
            if user is None:
                LOG.info('User with username: {} does not exit'.format(username))
                response_object = {
                    'status': 'Invalid',
                    'message': 'User does not exist'
                }
                return response_object, 400
            
            create_date = user.creation_time
            create_date = datetime.datetime.strftime(create_date, "%d %B")
            user.create_date = create_date
            return user, 200

        except Exception as e:
            LOG.error('Failed to fetch details for username :{}'.format(
                username), exc_info=True)
            response_object = {
                'status': 'fail',
                'message': 'Try again',
            }
            return response_object, 500

    @staticmethod
    def update_user_info(update_dict):
        LOG.info('update_dict for user {}: {}'.format(
            current_user.username, update_dict))
        try:
            user = User.query.filter_by(id=current_user.id).first()
            if user is None:
                LOG.info(
                    'User with id: {} does not exit'.format(
                        current_user.id))
                response_object = {
                    'status': 'Invalid',
                    'message': 'User does not exist'
                }
                return response_object, 300

            for key in update_dict:
                user.update_col(key, update_dict[key])

            response_object = {
                'status': 'Success',
                'message': 'Details updated Successfully'
            }
            return response_object, 200

        except Exception:
            LOG.error('Failed to update details for id :{}'.format(
                current_user.id), exc_info=True)
            response_object = {
                'status': 'fail',
                'message': 'Try again',
            }
            return response_object, 500


    @staticmethod
    def add_to_seen_list(data):
        try:
            imdb_ID = data.get('imdb_ID_list')
            title = data.get("movie_list")

            if imdb_ID is None or imdb_ID == "":
                res, totalResults = Movie.search(title, 1, 5)
                res_objects = res.all()

                movie = Movie.query.filter_by(imdb_ID=res_objects[0].imdb_ID).first()
                user = User.query.filter_by(id=current_user.id).first()
                
                if len(user.seen_list_titles) == 0:
                    print("Khali Hai")
                    movie_list = []
                    imdb_ID_list = []    

                else:
                    movie_list = user.seen_list_titles['movie_list']
                    imdb_ID_list = user.seen_list_IDs['imdb_ID_list']

                
                if movie.imdb_ID not in imdb_ID_list:
                    movie_list.append(movie.title)
                    imdb_ID_list.append(movie.imdb_ID)

                    res = {
                        'movie_list' : movie_list,
                        'imdb_ID_list' : imdb_ID_list
                    }

                    print("RES")
                    print(res)

        
                    setattr(user, 'seen_list_IDs', {'imdb_ID_list' : imdb_ID_list})
                    db.session.commit()
                    setattr(user, 'seen_list_titles', {'movie_list' : movie_list})
                    db.session.commit()
                    setattr(user, 'seen_list_IDs', {'imdb_ID_list' : imdb_ID_list})
                    db.session.commit()

            
            else:
                user = User.query.filter_by(id=current_user.id).first()
                movie = Movie.query.filter_by(imdb_ID=imdb_ID).first()
        
                if len(user.seen_list_titles) == 0:
                    print("Khali Hai")
                    movie_list = []
                    imdb_ID_list = []    

                else:
                    movie_list = user.seen_list_titles['movie_list']
                    imdb_ID_list = user.seen_list_IDs['imdb_ID_list']
                
                print(movie_list)
                print(imdb_ID_list)

                if movie.imdb_ID not in imdb_ID_list:
                    movie_list.append(movie.title)
                    imdb_ID_list.append(movie.imdb_ID)

                    res = {
                        'movie_list' : movie_list,
                        'imdb_ID_list' : imdb_ID_list
                    }

                    print("RES")
                    print(res)

        
                    setattr(user, 'seen_list_IDs', {'imdb_ID_list' : imdb_ID_list})
                    db.session.commit()
                    setattr(user, 'seen_list_titles', {'movie_list' : movie_list})
                    db.session.commit()
                    setattr(user, 'seen_list_IDs', {'imdb_ID_list' : imdb_ID_list})
                    db.session.commit()

                
            user = User.query.filter_by(id=current_user.id).first()

            movie_list = user.seen_list_titles
            return movie_list, 200
        
        except Exception:
            LOG.error("Movie couldn't be added to List.", exc_info=True)
            response_object = {
                'status': 'fail',
                'message': 'Try again later. '
            }

            return response_object, 500

    

    @staticmethod
    def add_to_bucket_list(data):
        try:
            imdb_ID = data.get('imdb_ID_list')
            title = data.get("movie_list")

            if imdb_ID is None or imdb_ID == "":
                res, totalResults = Movie.search(title, 1, 5)
                res_objects = res.all()

                movie = Movie.query.filter_by(imdb_ID=res_objects[0].imdb_ID).first()
                user = User.query.filter_by(id=current_user.id).first()
                
                if len(user.bucket_list_titles) == 0:
                    print("Khali Hai")
                    movie_list = []
                    imdb_ID_list = []    

                else:
                    movie_list = user.bucket_list_titles['movie_list']
                    imdb_ID_list = user.bucket_list_IDs['imdb_ID_list']

                
                if movie.imdb_ID not in imdb_ID_list:
                    movie_list.append(movie.title)
                    imdb_ID_list.append(movie.imdb_ID)

                    res = {
                        'movie_list' : movie_list,
                        'imdb_ID_list' : imdb_ID_list
                    }

                    print("RES")
                    print(res)

        
                    setattr(user, 'bucket_list_IDs', {'imdb_ID_list' : imdb_ID_list})
                    db.session.commit()
                    setattr(user, 'bucket_list_titles', {'movie_list' : movie_list})
                    db.session.commit()
                    setattr(user, 'bucket_list_IDs', {'imdb_ID_list' : imdb_ID_list})
                    db.session.commit()

            
            else:
                user = User.query.filter_by(id=current_user.id).first()
                movie = Movie.query.filter_by(imdb_ID=imdb_ID).first()
        
                if len(user.bucket_list_titles) == 0:
                    print("Khali Hai")
                    movie_list = []
                    imdb_ID_list = []    

                else:
                    movie_list = user.bucket_list_titles['movie_list']
                    imdb_ID_list = user.bucket_list_IDs['imdb_ID_list']
                
                print(movie_list)
                print(imdb_ID_list)

                if movie.imdb_ID not in imdb_ID_list:
                    movie_list.append(movie.title)
                    imdb_ID_list.append(movie.imdb_ID)

                    res = {
                        'movie_list' : movie_list,
                        'imdb_ID_list' : imdb_ID_list
                    }

                    print("RES")
                    print(res)

        
                    setattr(user, 'bucket_list_IDs', {'imdb_ID_list' : imdb_ID_list})
                    db.session.commit()
                    setattr(user, 'bucket_list_titles', {'movie_list' : movie_list})
                    db.session.commit()
                    setattr(user, 'bucket_list_IDs', {'imdb_ID_list' : imdb_ID_list})
                    db.session.commit()

                
            user = User.query.filter_by(id=current_user.id).first()

            movie_list = user.bucket_list_titles
            return movie_list, 200
        
        except Exception:
            LOG.error("Movie couldn't be added to List.", exc_info=True)
            response_object = {
                'status': 'fail',
                'message': 'Try again later. '
            }

            return response_object, 500

    @staticmethod
    def add_to_recommend_list(data):
        try:
            imdb_ID = data.get('imdb_ID_list')
            title = data.get("movie_list")

            if imdb_ID is None or imdb_ID == "":
                res, totalResults = Movie.search(title, 1, 5)
                res_objects = res.all()

                movie = Movie.query.filter_by(imdb_ID=res_objects[0].imdb_ID).first()
                user = User.query.filter_by(id=current_user.id).first()
                
                if len(user.recommend_list_titles) == 0:
                    print("Khali Hai")
                    movie_list = []
                    imdb_ID_list = []    

                else:
                    movie_list = user.recommend_list_titles['movie_list']
                    imdb_ID_list = user.recommend_list_IDs['imdb_ID_list']

                
                if movie.imdb_ID not in imdb_ID_list:
                    movie_list.append(movie.title)
                    imdb_ID_list.append(movie.imdb_ID)

                    res = {
                        'movie_list' : movie_list,
                        'imdb_ID_list' : imdb_ID_list
                    }

                    print("RES")
                    print(res)

        
                    setattr(user, 'recommend_list_IDs', {'imdb_ID_list' : imdb_ID_list})
                    db.session.commit()
                    setattr(user, 'recommend_list_titles', {'movie_list' : movie_list})
                    db.session.commit()
                    setattr(user, 'recommend_list_IDs', {'imdb_ID_list' : imdb_ID_list})
                    db.session.commit()

            
            else:
                user = User.query.filter_by(id=current_user.id).first()
                movie = Movie.query.filter_by(imdb_ID=imdb_ID).first()
        
                if len(user.recommend_list_titles) == 0:
                    print("Khali Hai")
                    movie_list = []
                    imdb_ID_list = []    

                else:
                    movie_list = user.recommend_list_titles['movie_list']
                    imdb_ID_list = user.recommend_list_IDs['imdb_ID_list']
                
                print(movie_list)
                print(imdb_ID_list)

                if movie.imdb_ID not in imdb_ID_list:
                    movie_list.append(movie.title)
                    imdb_ID_list.append(movie.imdb_ID)

                    res = {
                        'movie_list' : movie_list,
                        'imdb_ID_list' : imdb_ID_list
                    }

                    print("RES")
                    print(res)

        
                    setattr(user, 'recommend_list_IDs', {'imdb_ID_list' : imdb_ID_list})
                    db.session.commit()
                    setattr(user, 'recommend_list_titles', {'movie_list' : movie_list})
                    db.session.commit()
                    setattr(user, 'recommend_list_IDs', {'imdb_ID_list' : imdb_ID_list})
                    db.session.commit()

                

            movie_list = user.recommend_list_titles
            id_list = user.recommend_list_IDs
            resp = {
                "movie_list" : movie_list,
                "imdb_ID_list" : id_list
            }
            return resp, 200
        
        except Exception:
            LOG.error("Movie couldn't be added to List.", exc_info=True)
            response_object = {
                'status': 'fail',
                'message': 'Try again later. '
            }

            return response_object, 500


    @staticmethod
    def get_seen_list(username):
        try:
            user = User.query.filter_by(username=username).first()
            movie_list = user.seen_list_titles
            imdb_ID_list = user.seen_list_IDs

            resp = []
            for (movie, imdb_ID) in zip(movie_list['movie_list'], imdb_ID_list['imdb_ID_list']):
                x = {
                    "imdb_ID" : imdb_ID,
                    "movie" : movie
                }
                resp.append(x)
                
            return resp,  200
        
        except Exception:
            LOG.error("Couldn't be fetched", exc_info=True)
            response_object = {
                'status': 'fail',
                'message': 'Try again later. '
            }

            return response_object, 500

    @staticmethod
    def get_bucket_list(username):
        try:
            user = User.query.filter_by(username=username).first()
            movie_list = user.bucket_list_titles
            imdb_ID_list = user.bucket_list_IDs
            resp = []
            for (movie, imdb_ID) in zip(movie_list['movie_list'], imdb_ID_list['imdb_ID_list']):
                x = {
                    "imdb_ID" : imdb_ID,
                    "movie" : movie
                }
                resp.append(x)

            return resp,  200
        
        except Exception:
            LOG.error("Couldn't be fetched", exc_info=True)
            response_object = {
                'status': 'fail',
                'message': 'Try again later. '
            }

            return response_object, 500

    @staticmethod
    def get_recommend_list(username):
        try:
            user = User.query.filter_by(username=username).first()
            movie_list = user.recommend_list_titles
            imdb_ID_list = user.recommend_list_IDs

            resp = []
            for (movie, imdb_ID) in zip(movie_list['movie_list'], imdb_ID_list['imdb_ID_list']):
                x = {
                    "imdb_ID" : imdb_ID,
                    "movie" : movie
                }
                resp.append(x)
                
            return resp,  200
        
        except Exception:
            LOG.error("Couldn't be fetched", exc_info=True)
            response_object = {
                'status': 'fail',
                'message': 'Try again later. '
            }

            return response_object, 500

    @staticmethod
    def get_user_posts(username):
        try:
            user = User.query.filter_by(username=username).first()
            user_id = user.id

            posts = Post.query.filter_by(author_id=user_id).all()
            return posts, 200


        except:
            LOG.error("Couldn't be fetched", exc_info=True)
            response_object = {
                'status': 'fail',
                'message': 'Try again later. '
            }

            return response_object, 500


