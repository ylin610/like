# coding: utf-8
from flask import (
    Blueprint,
    render_template,
    current_app,
    request
    )
from like.models import Post, Topic, Comment, User, follow as follow_model, user_topic
from sqlalchemy.sql.expression import func, or_
from like.utils import Restful, Memcached
from datetime import datetime, timedelta
from like.exts import db
from flask_login import current_user


DISCOVER_POSTS_IN_DAYS = 7
HOT_TOPICS_CACHED_MINUTES = 5


api_bp = Blueprint('api', __name__, url_prefix='/api/v1')


@api_bp.route('/post')
def get_post():
    topic_id = request.args.get('topic_id', type=int)
    user_id = request.args.get('user_id', type=int)
    page = request.args.get('page', 1, type=int)
    num = request.args.get('num', current_app.config['POSTS_PER_PAGE'], type=int)

    query_obj = Post.query
    if topic_id:
        query_obj = query_obj.filter_by(topic_id=topic_id)
    if user_id:
        query_obj = query_obj.filter_by(creator_id=user_id)
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


@api_bp.route('/follow')
def follow():
    page = request.args.get('page', 1, type=int)
    num = request.args.get('num', current_app.config['COMMENTS_PER_PAGE'], type=int)
    followed_user_ids = db.session.query(follow_model.c.followed_id) \
                                  .filter(follow_model.c.follower_id == current_user.id) \
                                  .subquery()
    followed_topic_ids = db.session.query(user_topic.c.topic_id) \
                                  .filter(user_topic.c.user_id == current_user.id) \
                                  .subquery()
    query = Post.query.filter(
        or_(Post.creator_id.in_(followed_user_ids), Post.topic_id.in_(followed_topic_ids))
    ).order_by(Post.create_time.desc()).paginate(page, num)

    html = render_template('api/post.html', posts=query.items)
    res = {'html': html, 'has_next': query.has_next}
    return Restful.success(data=res)


@api_bp.route('/discovery')
def discover():
    page = request.args.get('page', 1, type=int)
    num = request.args.get('num', current_app.config['COMMENTS_PER_PAGE'], type=int)

    date = datetime.now() - timedelta(days=DISCOVER_POSTS_IN_DAYS)
    query = Post.query.join(Post.liked_users)\
                      .filter(Post.create_time > date) \
                      .group_by(Post.id)\
                      .order_by(func.count(User.id).desc()).paginate(page, num)

    html = render_template('api/post.html', posts=query.items)
    res = {'html': html, 'has_next': query.has_next}
    return Restful.success(data=res)


@api_bp.route('/collection')
def collection():
    user_id = request.args.get('user_id', type=int)
    page = request.args.get('page', 1, type=int)
    num = request.args.get('num', current_app.config['COMMENTS_PER_PAGE'], type=int)

    query = Post.query.join(Post.collected_users)\
                      .filter(User.id == user_id) \
                      .order_by(Post.create_time.desc()).paginate(page, num)

    html = render_template('api/post.html', posts=query.items)
    res = {'html': html, 'has_next': query.has_next}
    return Restful.success(data=res)


@api_bp.route('/reply_input')
def get_reply_input():
    comment_id = request.args.get('comment_id', type=int)
    comment = Comment.query.get(comment_id)

    html = render_template('api/reply.html', comment=comment)
    return Restful.success(data=html)


@api_bp.route('/hot_topics')
def get_hot_topics():
    cached_topics = Memcached.get('hot_topics')
    if not cached_topics:
        hot_topics = Topic.query.join(Topic.posts)\
                                .group_by(Topic.id) \
                                .order_by(func.count(Post.id).desc())\
                                .limit(5)
        cached_topics = render_template('api/hot_topics.html', hot_topics=hot_topics)
        Memcached.set('hot_topics', cached_topics, 60*HOT_TOPICS_CACHED_MINUTES)
    return cached_topics
