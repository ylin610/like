# coding: utf-8
from flask import (
    Blueprint,
    render_template,
    current_app,
    request
    )
from like.models import Post, Topic, Comment, User
from sqlalchemy.sql.expression import func
from like.utils import Restful
from datetime import datetime, timedelta
from itertools import chain


api_bp = Blueprint('api', __name__, url_prefix='/api/v1')

@api_bp.route('/post')
def get_post():
    topic = request.args.get('topic_id', type=int)
    user = request.args.get('user_id', type=int)
    page = request.args.get('page', 1, type=int)
    num = request.args.get('num', current_app.config['POSTS_PER_PAGE'], type=int)
    query_obj = Post.query
    if topic:
        query_obj = query_obj.filter_by(topic_id=topic)
    if user:
        query_obj = query_obj.filter_by(creator_id=user)
    query = query_obj.order_by(Post.create_time.desc()).paginate(page, num)
    html = render_template('api/post.html', posts=query.items)
    res = {'html': html, 'has_next': query.has_next}
    return Restful.success(data=res)


@api_bp.route('/comment')
def get_comment():
    post = request.args.get('post_id', type=int)
    page = request.args.get('page', 1, type=int)
    num = request.args.get('num', current_app.config['COMMENTS_PER_PAGE'], type=int)
    query = Comment.query.filter_by(post_id=post) \
        .order_by(Comment.create_time.desc()).paginate(page, num)
    html = render_template('api/comment.html', comments=query.items)
    res = {'html': html, 'has_next': query.has_next}
    return Restful.success(data=res)


@api_bp.route('/discovery')
def discover():
    page = request.args.get('page', 1, type=int)
    num = request.args.get('num', current_app.config['COMMENTS_PER_PAGE'], type=int)
    date = datetime.now() - timedelta(days=7)
    query = Post.query.join(Post.liked_users).filter(Post.create_time > date) \
        .group_by(Post.id).order_by(func.count(User.id).desc()).paginate(page, num)
    html = render_template('api/post.html', posts=query.items)
    res = {'html': html, 'has_next': query.has_next}
    return Restful.success(data=res)


# @api_bp.route('/trend')
# def trend():
#     user = request.args.get('user_id', type=int)
#     page = request.args.get('page', 1, type=int)
#     num = request.args.get('num', current_app.config['COMMENTS_PER_PAGE'], type=int)
#     start = num * (page - 1)
#     end = start + num
#     posts = Post.query.filter_by(creator_id=user).all()
#     comments = Comment.query.filter_by(creator_id=user).all()
#     trend = sorted(chain(posts, comments), key=lambda x: x.create_time)
#     html = render_template('api/trend.html', trends=trend[start:end])
#     res = {'html': html, 'has_next': len(trend) > end}
#     return Restful.success(data=res)
