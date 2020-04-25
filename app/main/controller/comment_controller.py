from logging import getLogger

from flask import Blueprint, abort, current_app, request
from flask_login import current_user, login_required
from flask_restplus import Api, Resource
from sqlalchemy import desc

from app.main.models.comments import Comment
from app.main.models.users import User
from app.main.service.comment_service import CommentService
from app.main.util.dto import CommentDto, PostDto

LOG = getLogger(__name__)

api = CommentDto.api
comment = CommentDto.comment
commentInfo = CommentDto.commentInfo

reactionInfo = PostDto.reactionInfo
postInfo = PostDto.postInfo


@api.route("/<id>")
class CommentFetch(Resource):
    @api.marshal_with(commentInfo)
    def get(self, id):
        """
        Fetches the comment given by the id.
        """

        comment_id = int(id)
        resp = CommentService.get_comment_by_id(comment_id)
        if resp[1] != 200:
            abort(403, resp)

        else:
            return resp


@api.route('/create/<post_id>')
class CreateNewPost(Resource):
    @login_required
    @api.marshal_with(commentInfo)
    @api.expect(comment)
    def post(self, post_id):
        """
        Create New Comment. Takes body as payload. Login is required.
        """
        new_comment_data = request.json
        resp = CommentService.create_new_comment(new_comment_data, post_id)

        if resp[1] != 200:
            abort(403, resp)

        else:
            return resp


@api.route('/<id>/update')
class UpdatePost(Resource):
    @login_required
    @api.marshal_with(commentInfo)
    @api.expect(comment)
    def post(self, id):
        """
        Update comment with given ID. User needs to be authenticated properly.
        """
        data = request.json
        resp = CommentService.update_comment(data, id)

        if resp[1] != 200:
            abort(403, resp)

        else:
            return resp


@api.route('/<id>/delete')
class DeleteComment(Resource):
    @login_required
    @api.doc(params={'id': 'Comment ID'})
    def delete(self, id):
        """
        Delete comment with given ID. User needs to be authenticated
        """
        resp = CommentService.delete_comment({'comment_id': id})

        if resp[1] != 200:
            abort(403, resp)

        else:
            return resp


@api.route('/<id>/upvote')
class UpvoteComment(Resource):
    @login_required
    @api.marshal_with(reactionInfo)
    @api.doc(params={'id': 'Comment ID'})
    def post(self, id):
        resp = CommentService.upvote_comment(id)
        if resp[1] != 200:
            abort(403, resp)

        else:
            return resp


@api.route('/<id>/downvote')
class DownvoteComment(Resource):
    @login_required
    @api.marshal_with(reactionInfo)
    @api.doc(params={'id': 'Comment ID'})
    def post(self, id):
        resp = CommentService.downvote_comment(id)
        if resp[1] != 200:
            abort(403, resp)

        else:
            return resp


@api.route('/<id>/parent')
class fetchParentComment(Resource):
    @api.marshal_with(postInfo)
    def get(self, id):
        resp = CommentService.get_parent_post(id)

        if resp[1] != 200:
            abort(403, resp)

        else:
            return resp


@api.route('/<id>/reactions')
class fetchReactionInfo(Resource):
    @api.marshal_with(reactionInfo)
    def get(self, id):
        resp = CommentService.fetch_reaction_info(id)
        if resp[1] != 200:
            abort(403, resp)

        else:
            return resp
