from logging import getLogger

from flask import Blueprint, abort, current_app, request
from flask_login import current_user, login_required
from flask_restplus import Api, Resource
from sqlalchemy import desc

from app.main.models.posts import Post
from app.main.models.users import User
from app.main.service.post_service import PostService
from app.main.util.dto import CommentDto, PostDto

LOG = getLogger(__name__)

api = PostDto.api
post = PostDto.post
postInfo = PostDto.postInfo
reactionInfo = PostDto.reactionInfo

comment_api = CommentDto.api
comment = CommentDto.comment
commentInfo = CommentDto.commentInfo

@api.route("/<id>")
class PostFetch(Resource):
    @api.marshal_with(postInfo)
    def get(self, id):
        """
        Fetches the post given by the id.
        """
        post_id = int(id)
        resp = PostService.get_post_by_id(post_id)
        if resp[1] != 200:
            abort(403, resp)
        
        else:
            return resp



@api.route("/getAll")
class PostFetchAll(Resource):
    @api.marshal_list_with(postInfo)
    @api.doc(params = {'q': 'Search query', 'page' : 'Page number for pagination'})
    def get(self):
        '''
        Get all Posts. If a query is given, fetch all posts that match query. 
        '''

        q = request.args.get("q")
        page = request.args.get("page") or 1
        resp = PostService.get_post_by_query(q, page)
        if resp[1] != 200:
            abort(403, resp)
        
        else:
            return resp


@api.route('/')
class CreateNewPost(Resource):
    @login_required
    @api.marshal_with(postInfo)
    @api.expect(post)
    def post(self):
        """
        Create New Post. Takes post title and post body as payload. 
        Login is required. 
        """
        new_post_data = request.json
        resp = PostService.create_new_post(new_post_data)
        
        if resp[1] != 200:
            abort(403, resp)
        
        else:
            return resp

@api.route('/update/<id>')
class UpdatePost(Resource):
    @login_required
    @api.marshal_with(postInfo)
    @api.expect(post)
    def post(self, id):
        """
        Update post with given ID. User needs to be authenticated properly. 
        """ 
        post_data = request.json
        resp = PostService.update_post(post_data, id)

        if resp[1] != 200:
            abort(403, resp)
        
        else:
            return resp


@api.route('/delete/<id>')
class DeletePost(Resource):
    @login_required
    @api.doc(params = {'id': 'Post ID'})

    def delete(self, id):
        """
        Delete post with given ID. User needs to be authenticated
        """
        resp = PostService.delete_post({'post_id' : id})
        if resp[1] != 200:
            abort(403, resp)
        
        else:
            return resp

@api.route('/<id>/upvote')
class UpvotePost(Resource):
    @login_required
    @api.marshal_with(reactionInfo)
    @api.doc(params = {'id' : 'Post ID'})

    def post(self, id):
        resp = PostService.upvote_post(id)
        if resp[1] != 200:
            abort(403, resp)
        
        else:
            return resp
        
@api.route('/<id>/downvote')
class DownvotePost(Resource):
    @login_required
    @api.marshal_with(reactionInfo)
    @api.doc(params = {'id' : 'Post ID'})

    def post(self, id):
        resp = PostService.downvote_post(id)
        if resp[1] != 200:
            abort(403, resp)
        
        else:
            return resp

@api.route('/<id>/comments')
class fetchAllComments(Resource):
    @api.marshal_list_with(commentInfo)
    def get(self, id):
        resp = PostService.fetch_all_comments(id)
        
        if resp[1] != 200:
            abort(403, resp)
        
        else:
            return resp
