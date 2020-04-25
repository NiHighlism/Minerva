"""Register all namespaces and import API's from  controllers."""
from flask import Blueprint
from flask_restplus import Api

# from app.main.controller.article_controller import api as post_ns
from app.main.controller.auth_controller import api as auth_ns
from app.main.controller.comment_controller import api as comment_ns
from app.main.controller.movie_controller import api as movie_ns
from app.main.controller.post_controller import api as post_ns
from app.main.controller.user_controller import api as user_ns

blueprint = Blueprint('api', __name__)

api = Api(blueprint,
          title='Flask-RESTPlus common backend for Minerva',
          version='1.0',
          description='a boilerplate for flask restplus web service'
          )

api.add_namespace(auth_ns, path='/auth')
api.add_namespace(movie_ns, path='/movie')
api.add_namespace(user_ns, path='/user')
api.add_namespace(post_ns, path='/post')
api.add_namespace(comment_ns, path='/comment')
