"""for user related operations"""

import datetime
from logging import getLogger

import requests
from flask import current_app
from flask_login import current_user
from sqlalchemy.orm.exc import NoResultFound

from app.main import db
from app.main.models.comments import Comment
from app.main.models.movies import Movie
from app.main.models.posts import Post
from app.main.models.reactions import Reaction
from app.main.models.users import User

LOG = getLogger(__name__)


class PostService:
    @staticmethod
    def get_post_by_id(post_id):
        try:
            post = Post.query.filter_by(id=post_id).first()
            author_id = post.author_id
            author = User.query.filter_by(id=author_id).first()

            try:
                post.author_name = (author.first_name + " " + author.last_name)
            except BaseException:
                post.author_name = "Anonymous Bat"

            post.author_username = author.username

            post.numComments = len(post.comments.all())
            print(post.numComments)

            return post, 200

        except BaseException:
            LOG.error("Couldn't fetch post with ID {}".format(
                post_id), exc_info=True)
            response_object = {
                'status': 'fail',
                'message': 'Could not fetch post. Try later'
            }

            return response_object, 500

    @staticmethod
    def get_post_by_query(query, page=1):
        page = int(page)
        try:
            if query is not None:
                es = current_app.elasticsearch
                results_per_page = int(current_app.config['RESULTS_PER_PAGE'])
                res, totalResults = Post.search(query, page, results_per_page)
                res_objects = res.all()

                post_results = [post for post in res_objects]

                for post in post_results:
                    author_id = post.author_id
                    author = User.query.filter_by(id=author_id).first()

                    post.author_name = author.first_name + " " + author.last_name
                    post.author_username = author.username
                    post.numComments = len(post.comments.all())

                return post_results, 200

            else:
                res_objects = Post.query.all()

                post_results = [post for post in res_objects]

                for post in post_results:
                    author_id = post.author_id
                    author = User.query.filter_by(id=author_id).first()

                    post.author_name = author.first_name + " " + author.last_name
                    post.author_username = author.username
                    post.numComments = len(post.comments.all())

                totalResults = len(post_results)

                results_per_page = int(current_app.config['RESULTS_PER_PAGE'])

                totalPages = int(totalResults) / int(results_per_page)

                s = (page - 1) * results_per_page
                e = s + results_per_page
                return post_results[s:e], 200

        except BaseException:
            LOG.error("Couldn't fetch posts with query {}".format(
                query), exc_info=True)
            response_object = {
                'status': 'fail',
                'message': 'Could not fetch posts. Try later'
            }

            return response_object, 500

    @staticmethod
    def create_new_post(post_data):
        try:
            current_user_id = current_user.id
            post_title = post_data.get('title')
            post_body = post_data.get('body')
            post_movie = post_data.get('post_movie')
            tags = post_data.get('tags')

            post = Post.query.filter_by(title=post_title).first()
            if post is not None:
                response_object = {
                    'status': 'invalid',
                    'message': 'Post Already Exists',
                }

                LOG.info(
                    'Post already present in database. Redirect to Main Page')
                return response_object, 401

            post = Post(current_user_id, post_movie,
                        post_title, post_body, tags)
            response_object = {
                'status': 'success',
                'message': 'Post added successfully'
            }
            post.numComments = len(post.comments.all())
            return post, 200

        except BaseException:
            LOG.error("Couldn't create post with data {}".format(
                post_data), exc_info=True)
            response_object = {
                'status': 'fail',
                'message': 'Could not create post. Try later'
            }

            return response_object, 500

    @staticmethod
    def update_post(post_data, post_id):
        try:
            post = Post.query.filter_by(id=post_id).first()
            if post is None:
                LOG.error("Post does not exist", exc_info=True)
                response_object = {
                    'status': 'fail',
                    'message': 'Post does not exist'
                }
                return response_object, 400

            if current_user.id != post.author_id:
                LOG.error("User does not have permission to update post. ")
                response_object = {
                    'status': 'fail',
                    'message': 'User does not have edit rights'
                }
                return response_object, 403

            for key in post_data:
                post.update_col(key, post_data[key])

            post.update_col('last_edit_time', datetime.datetime.now())

            author_id = post.author_id
            author = User.query.filter_by(id=author_id).first()

            post.author_name = author.first_name + " " + author.last_name
            post.author_username = author.username
            post.numComments = len(post.comments.all())

            return post, 200

        except BaseException:
            LOG.error("Couldn't update post with data {}".format(
                post_data), exc_info=True)
            response_object = {
                'status': 'fail',
                'message': 'Could not update post. Try later'
            }

            return response_object, 500

    @staticmethod
    def delete_post(data):
        try:
            post_id = data.get('post_id')
            post = Post.query.filter_by(id=post_id).first()
            if post is None:
                LOG.error("Post does not exist", exc_info=True)
                response_object = {
                    'status': 'fail',
                    'message': 'Post does not exist'
                }
                return response_object, 400

            if current_user.id != post.author_id:
                LOG.error("User does not have permission to delete post. ")
                response_object = {
                    'status': 'fail',
                    'message': 'User does not have delete rights'
                }
                return response_object, 403

            post.delete_post(post_id)
            response_object = {
                'status': 'success',
                'message': 'deleted successfully'
            }

            return response_object, 200

        except BaseException:
            LOG.error("Couldn't delete post with data {}".format(
                data), exc_info=True)
            response_object = {
                'status': 'fail',
                'message': 'Could not delete post. Try later'
            }

            return response_object, 500

    @staticmethod
    def upvote_post(post_id):
        try:
            post = Post.query.filter_by(id=post_id).first()
            user = current_user.id

            present_reacts = post.reaction_list.all()

            for react in present_reacts:
                if react.user_id == user and react.value == 1:
                    response_object = {
                        'status': 'weird',
                        'message': 'already react kiya'
                    }
                    return response_object, 400

            post.upvote(user)

            reaction_list = {
                'upvotes': post.upvotes,
                'downvotes': post.downvotes,
                'score': post.upvotes - post.downvotes
            }
            return reaction_list, 200

        except BaseException:
            LOG.error("Couldn't upvote post with data {}".format(
                post_id), exc_info=True)
            response_object = {
                'status': 'fail',
                'message': 'Could not upvote post. Try later'
            }
            return response_object, 500

    @staticmethod
    def downvote_post(post_id):
        try:
            post = Post.query.filter_by(id=post_id).first()
            user = current_user.id

            present_reacts = post.reaction_list.all()

            for react in present_reacts:
                if react.user_id == user and react.value == -1:
                    response_object = {
                        'status': 'weird',
                        'message': 'already react kiya'
                    }
                    return response_object, 400

            post.downvote(user)
            reaction_list = {
                'upvotes': post.upvotes,
                'downvotes': post.downvotes,
                'score': post.upvotes - post.downvotes
            }
            return reaction_list, 200

        except BaseException:
            LOG.error("Couldn't upvote post with data {}".format(
                post_id), exc_info=True)
            response_object = {
                'status': 'fail',
                'message': 'Could not upvote post. Try later'
            }

            return response_object, 500

    @staticmethod
    def fetch_all_comments(post_id):
        try:
            post = Post.query.filter_by(id=post_id).first()

            comment_list = post.comments.all()
            for comment in comment_list:
                author_id = comment.author_id
                author = User.query.filter_by(id=author_id).first()
                comment.author_username = author.username
            return comment_list, 200

        except BaseException:
            LOG.error("Couldn't fetch comments for post with data {}".format(
                post_id), exc_info=True)
            response_object = {
                'status': 'fail',
                'message': 'Try later'
            }

            return response_object, 500

    @staticmethod
    def fetch_reaction_info(id):
        try:
            res = Post.query.filter_by(id=id).first()

            reaction_list = {
                'upvotes': res.upvotes,
                'downvotes': res.downvotes,
                'score': res.upvotes - res.downvotes
            }

            return reaction_list, 200

        except BaseException:
            LOG.error("Couldn't fetch data for {}".format(id), exc_info=True)
            response_object = {
                'status': 'fail',
                'message': 'Could not fetch data. Try later'
            }

            return response_object, 500

    @staticmethod
    def get_movie_by_post(id):
        try:
            post = Post.query.filter_by(id=id).first()
            imdb_ID = post.imdb_ID

            movie = Movie.query.filter_by(imdb_ID=imdb_ID).first()
            return movie, 200

        except BaseException:
            LOG.error("Couldn't fetch data for {}".format(id), exc_info=True)
            response_object = {
                'status': 'fail',
                'message': 'Could not fetch data. Try later'
            }

            return response_object, 500
