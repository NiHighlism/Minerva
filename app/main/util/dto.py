# Data Transfer Object- Responsible for carrying data between processes
from flask import current_app
from flask_restplus import Namespace, fields, reqparse
from werkzeug.datastructures import FileStorage


class AuthDto:
    api = Namespace('auth', description='Authentication Related operations')
    user_auth = api.model('auth_details', {
        'username': fields.String(required=True, description='Login Username'),
        'password': fields.String(required=True, description='Login Password'),
        'remember': fields.String(description='Stay Logged In')
    })

    login_info = api.model('login_info', {
        'id': fields.Integer(required=True, description="ID of the user."),
        'username': fields.String(required=True, description="username of the user."),
        'access_token': fields.String(),
        'refresh_token': fields.String()
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
    favourites = api.model('favourites', {
        'movie': fields.String(description="Favourite Movie", default=""),
        'actor': fields.String(description="Favourite Actor", default=""),
        'genre': fields.String(description="Favourite genre", default="")
    })

    user = api.model('user', {
        'first_name': fields.String(required=False),
        'last_name': fields.String(required=False),
        'username': fields.String(required=True, description='user username'),
        'password': fields.String(required=True, description='user password'),
        'email': fields.String(required=True, description='user email address'),
    })

    userInfo = api.model('userInfo', {
        'id': fields.Integer(required=True),
        'username': fields.String(required=True, description='user username'),
        'first_name': fields.String(description='first name', default=""),
        'last_name': fields.String(description="last name", default=""),
        'dob': fields.DateTime(dt_format='rfc822', description="date of birth"),
        'email': fields.String(required=True, description='user email address'),
        'fb_handle': fields.String(description="facebook handle"),
        'instagram_handle': fields.String(description="medium handle"),
        'twitter_handle': fields.String(description="twitter handle"),
        'favourites': fields.Nested(favourites),
        'bio': fields.String(description="biography"),
        'occupation': fields.String(description="occupation"),
        'last_login': fields.DateTime(dt_format='rfc822', description="last login time")
    })

    updateInfo = api.model('userInfo', {
        'username': fields.String(required=True, description='user username'),
        'first_name': fields.String(description='first name', default=""),
        'last_name': fields.String(description="last name", default=""),
        'fb_handle': fields.String(description="facebook handle"),
        'instagram_handle': fields.String(description="medium handle"),
        'twitter_handle': fields.String(description="twitter handle"),
        'favourites': fields.Nested(favourites),
        'bio': fields.String(description="biography"),
        'occupation': fields.String(description="occupation")
    })


class MovieDto:
    api = Namespace('movie', description='movie related operations')

    genre = api.model('genre', {'genreList': fields.List(fields.String)})
    director = api.model(
        'director', {'directorList': fields.List(fields.String)})
    writer = api.model('writer', {'writerList': fields.List(fields.String)})
    actors = api.model('actors', {'actorsList': fields.List(fields.String)})
    language = api.model(
        'language', {'languageList': fields.List(fields.String)})
    country = api.model('country', {'countryList': fields.List(fields.String)})

    movie = api.model('movie', {
        'total_pages': fields.Integer(description="Number of pages of results", default=1),
        'imdb_ID': fields.String(required=True, description="ID of the given movie on IMDB"),
        'title': fields.String(required=True, description="Title of the movie"),
        'year': fields.Integer(required=True, description="Release Year of the movie"),
        'runtime': fields.String(description="Runtime in minutes"),
        'release_date': fields.String(description="Release date"),
        'plot': fields.String(description="Plotline of the movie"),
        'genre': fields.Nested(genre),
        'director': fields.Nested(director),
        'writer': fields.Nested(writer),
        'actors': fields.Nested(actors),
        'language': fields.Nested(language),
        'country': fields.Nested(country),
        'awards': fields.String(default="N/A", description="Awards won or nominated"),
        'imdb_rating': fields.String(default="N/A", description="IMDB Rating of movie"),
        'rotten_tomatoes': fields.String(default="N/A", description="Rotten Tomatoes score of movie"),
        'metascore': fields.String(default="N/A", description="Metacritic score of Movie"),
        'poster_url': fields.String(description="URL of poster from IMDB"),
        'box_office': fields.String(description="Box office collection in dollars")
    })


class PostDto:
    api = Namespace('post', description='post related operations')
    
    tags = api.model('tags', {'tagList': fields.List(fields.String)})
    post = api.model('post', {
        'title': fields.String(description="Post title", required=True),
        'body': fields.String(description="Content of the post"),
        'post_movie': fields.String(description="Movie the post is related to"),
        'tags' : fields.Nested(tags)
    })

    postInfo = api.model('postInfo', {
        'id': fields.Integer(description="ID of post"),
        'title': fields.String(description="Title of post"),
        'body': fields.String(description="Post content body"),
        'upvotes': fields.Integer(description="Upvotes to a Post"),
        'post_movie': fields.String(description="Movie the post is related to"),
        'downvotes': fields.Integer(description="Downvotes to a Post"),
        'author_id': fields.Integer(description="ID of author of post"),
        'author_name' : fields.String(),
        'author_username' : fields.String(),
        'last_edit_time': fields.DateTime(description="Last edit timestamp of post")
    })

    reactionInfo = api.model('reactionInfo', {
        'upvotes': fields.Integer(description="Total number of upvotes"),
        'downvotes': fields.Integer(description="Total number of downvotes"),
        'score': fields.Integer(description="upvotes - downvotes")
    })


class CommentDto:
    api = Namespace('comment', description="Comment related operations")

    comment = api.model('comment', {
        'body': fields.String(description="Body of the comment")
    })

    commentInfo = api.model('commentInfo', {
        'id': fields.Integer(description="ID of post"),
        'body': fields.String(description="Post content body"),
        'upvotes': fields.Integer(description="Upvotes to a Post"),
        'downvotes': fields.Integer(description="Downvotes to a Post"),
        'author_id': fields.Integer(description="ID of author of post"),
        'parent_post_id': fields.Integer(description="ID of parent post"),
        'last_edit_time': fields.DateTime(description="Last edit timestamp of post")
    })
