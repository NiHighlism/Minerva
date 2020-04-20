# Data Transfer Object- Responsible for carrying data between processes
from flask import current_app
from flask_restplus import Namespace, fields, reqparse
from werkzeug.datastructures import FileStorage


class AuthDto:
    api = Namespace('auth', description='Authentication Related operations')
    user_auth = api.model('auth_details', {
        'email': fields.String(required=True, description='Login Email'),
        'password': fields.String(required=True, description='Login Password'),
        'remember': fields.String(description='Stay Logged In'),
    })

    login_info = api.model('login_info', {
        'id': fields.Integer(required=True, description="ID of the user."),
        'username': fields.String(required=True, description="username of the user.")
    })

    reset_email = api.model('email_details', {
        'email': fields.String(required=True, description='Login Email')
    })

    change_password = api.model('change_password', {
        'oldPassword': fields.String(required=True, format='password'),
        'newPassword': fields.String(required=True, format='password')
    })


class UserDto:
    api = Namespace('user', description='user related operations')
    user = api.model('user', {
        'username': fields.String(required=True, description='user username'),
        'password': fields.String(required=True, description='user password'),
        'email': fields.String(required=True, description='user email address'),
    })

    userInfo = api.model('userInfo', {
        'username': fields.String(required=True, description='user username'),
        'first_name': fields.String(description='first name', default=""),
        'last_name': fields.String(description="last name", default=""),
        'dob': fields.DateTime(dt_format='rfc822', description="date of birth"),
        'email': fields.String(required=True, description='user email address'),
        'fb_handle': fields.String(description="facebook handle"),
        'g_handle': fields.String(description="github handle"),
        'medium_handle': fields.String(description="medium handle"),
        'twitter_handle': fields.String(description="twitter handle"),
        'linkedin_handle': fields.String(description="linkedin handle"),
        'bio': fields.String(description="biography"),
        'occupation': fields.String(description="occupation"),
        'last_login': fields.DateTime(dt_format='rfc822', description="last login time")
    })

    payment = api.model('payment', {
        'username': fields.String(required=True,
                                  description='username of the payee'),
        'amount': fields.Float(required=True, descripton="Amount paid"),
        'api_response': fields.String(required=True,
                                      description="Response returned by vendor")
    })

class MovieDto:
    api = Namespace('movie', description='movie related operations')
    
    genre = api.model('genre', {'genreList' : fields.List(fields.String)})
    director = api.model('director', {'directorList' : fields.List(fields.String)})
    writer = api.model('writer',{'writerList' : fields.List(fields.String)})
    actors = api.model('actors', {'actorsList' : fields.List(fields.String)})
    language = api.model('language', {'languageList' : fields.List(fields.String)})
    country = api.model('country', {'countryList' : fields.List(fields.String)})

    movie = api.model('movie', {
        'imdb_ID' : fields.String(required=True, description="ID of the given movie on IMDB"),
        'title' : fields.String(required=True, description="Title of the movie"),
        'year' : fields.Integer(required=True, description="Release Year of the movie"),
        'runtime' : fields.String(description="Runtime in minutes"),
        'release_date' : fields.String(description="Release date"),
        'plot' : fields.String(description="Plotline of the movie"),
        'genre' : fields.Nested(genre),
        'director' : fields.Nested(director),
        'writer' : fields.Nested(writer),
        'actors' : fields.Nested(actors),
        'language' : fields.Nested(language),
        'country' : fields.Nested(country),
        'awards' : fields.String(default="N/A", description="Awards won or nominated"),
        'imdb_rating' : fields.String(default="N/A", description="IMDB Rating of movie"),
        'rotten_tomatoes' : fields.String(default="N/A", description="Rotten Tomatoes score of movie"),
        'metascore' : fields.String(default="N/A", description="Metacritic score of Movie"),
        'poster_url': fields.String(description="URL of poster from IMDB"),
        'box_office' : fields.String(description="Box office collection in dollars")
    })
