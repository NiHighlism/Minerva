"""for user related operations"""

import datetime
from logging import getLogger

import requests
from flask import current_app
from flask_login import current_user
from sqlalchemy.orm.exc import NoResultFound

from app.main import db
from app.main.models.posts import Post
from app.main.models.reactions import Reaction
from app.main.models.comments import Comment

LOG = getLogger(__name__)


class CommentService:
    @staticmethod
    def get_comment_by_id(comment_id):
        try:
            comment = Comment.query.filter_by(id=comment_id).first()
            return comment, 200

        except BaseException:
            LOG.error("Couldn't fetch post with ID {}".format(post_id), exc_info=True)
            response_object = {
                'status' : 'fail',
                'message' : 'Could not fetch post. Try later'
            }            
            
            return response_object, 500


    @staticmethod
    def create_new_comment(data, post_id):
        try:
            current_user_id = current_user.id
            comment_body = data.get('body')

            post = Post.query.filter_by(id=post_id).first()
            if post is None:
                response_object = {
                    'status': 'invalid',
                    'message': 'Post does not Exists',
                }

                LOG.info(
                    'Post does not exist.')
                return response_object, 400
            
            comment_list = post.comments.all()
            
            for comment in comment_list:
                if comment.body == comment_body:
                    response_object = {
                        'status' : 'fail',
                        'message' : 'comment already exists'
                    }
                    return response_object, 400
            
            comment_id = post.add_comment(current_user_id, comment_body)
            comment = Comment.query.filter_by(id=comment_id).first()

            return comment, 200

        except BaseException:
            LOG.error("Couldn't create comment with data {}".format(data), exc_info=True)
            response_object = {
                'status' : 'fail',
                'message' : 'Could not create comment. Try later'
            }            
            
            return response_object, 500

    
    @staticmethod
    def update_comment(data, comment_id):
        try:
            comment = Comment.query.filter_by(id=comment_id).first()
            if comment is None:
                LOG.error("Comment does not exist", exc_info=True)
                response_object = {
                    'status' : 'fail',
                    'message' : 'Comment does not exist'
                }
                return response_object, 400
            
            if current_user.id != comment.author_id:
                LOG.error("User does not have permission to update comment.")
                response_object = {
                    'status' : 'fail',
                    'message' : 'User does not have edit rights'
                }
                return response_object, 403
            
            for key in data:
                comment.update_col(key, data[key])
            
            comment.update_col('last_edit_time', datetime.datetime.now())

            return comment, 200

        except:
            LOG.error("Couldn't update post with data {}".format(data), exc_info=True)
            response_object = {
                'status' : 'fail',
                'message' : 'Could not update post. Try later'
            }            
            
            return response_object, 500

    
    @staticmethod
    def delete_comment(data):
        try:
            comment_id = data.get('comment_id')
            comment = Comment.query.filter_by(id=comment_id).first()
            if comment is None:
                LOG.error("Comment does not exist", exc_info=True)
                response_object = {
                    'status' : 'fail',
                    'message' : 'Comment does not exist'
                }
                return response_object, 400
            
            if current_user.id != comment.author_id:
                LOG.error("User does not have permission to delete comment. ")
                response_object = {
                    'status' : 'fail',
                    'message' : 'User does not have delete rights'
                }
                return response_object, 403
            
            comment.delete_comment(comment_id)
            response_object = {
                'status' : 'success',
                'message' : 'deleted successfully'
            }

            return response_object, 200

        except:
            LOG.error("Couldn't delete post with data {}".format(data), exc_info=True)
            response_object = {
                'status' : 'fail',
                'message' : 'Could not delete post. Try later'
            }            
            
            return response_object, 500

    
    @staticmethod
    def upvote_comment(comment_id):
        try:
            comment = Comment.query.filter_by(id=comment_id).first()
            user = current_user.id

            present_reacts = comment.reaction_list.all()

            for react in present_reacts:
                if react.user_id == user and react.value == 1:
                    response_object = {
                        'status' : 'weird',
                        'message' : 'already react kiya'
                    }
                    return response_object, 400
    
            
            comment.upvote(user)
            
            reaction_list = {
                'upvotes' : comment.upvotes, 
                'downvotes' : comment.downvotes,
                'score' : comment.upvotes - comment.downvotes
            }
            return reaction_list, 200
        
        except:
            LOG.error("Couldn't upvote comment with data {}".format(comment_id), exc_info=True)
            response_object = {
                'status' : 'fail',
                'message' : 'Could not upvote comment. Try later'     
            }
            return response_object, 500
    
    @staticmethod
    def downvote_comment(comment_id):
        try:
            comment = Comment.query.filter_by(id=comment_id).first()
            user = current_user.id

            present_reacts = comment.reaction_list.all()
            
            for react in present_reacts:
                if react.user_id == user and react.value == -1:
                    response_object = {
                        'status' : 'weird',
                        'message' : 'already react kiya'
                    }
                    return response_object, 400
                

            comment.downvote(user)
            reaction_list = {
                'upvotes' : comment.upvotes, 
                'downvotes' : comment.downvotes,
                'score' : comment.upvotes - comment.downvotes
            }
            return reaction_list, 200
        
        except:
            LOG.error("Couldn't upvote comment with data {}".format(post_id), exc_info=True)
            response_object = {
                'status' : 'fail',
                'message' : 'Could not downvote comment. Try later'
            }            
            
            return response_object, 500

    
    @staticmethod
    def get_parent_post(comment_id):
        try:
            comment = Comment.query.filter_by(id=comment_id).first()
            parent_post_id = comment.parent_post_id

            post = Post.query.filter_by(id=parent_post_id).first()
            return post, 200
        except:
            LOG.error("Couldn't fetch parent of comment with data {}".format(comment_id), exc_info=True)
            response_object = {
                'status' : 'fail',
                'message' : 'Try later'
            }            
            
            return response_object, 500
