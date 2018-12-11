# coding: utf-8
from flask import (
    Blueprint,
    render_template,
    current_app,
    request
    )
from like.models import Post, Topic, Comment, User
from flask_login import login_required, current_user
from sqlalchemy.sql.expression import func
from like.exts import db
from like.utils import Restful


front_bp = Blueprint('front', __name__)


@front_bp.route('/')
def index():
    page = request.args.get('page')
    per_page = current_app.config['POSTS_PER_PAGE']
    pagination = Post.query.order_by(Post.create_time.desc()).paginate(page, per_page)
    posts = pagination.items

    hot_topics = Topic.query.join(Topic.posts).group_by(Topic.id).order_by(func.count(Post.id)).limit(5)
    # hot_posts = Post.query.join(Post.liked_users).group_by(Post.id).order_by(func.count(User.id)).limit(5)
    return render_template('front/index.html', hot_topics=hot_topics)


@front_bp.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.get(post_id)
    return render_template('front/post.html', post=post)


@front_bp.route('/topic/<int:topic_id>')
def topic(topic_id):
    topic = Topic.query.get(topic_id)
    return render_template('front/topic.html', topic=topic)


@front_bp.route('/action/<string:type>/<string:action>')
def act(type, action):
    q_map = {
        'topic': {'like': 'followed_topics'},
        'post': {
            'like': 'liked_posts',
            'collect': 'collected_posts'
        },
        'comment': {'liked': 'liked_comments'}
    }

    model_map = {'topic': Topic, 'post': Post, 'comment': Comment}

    if current_user.is_authenticated:
        id = request.args.get('id', type=int)
        item = model_map[type].query.get(id)
        q = getattr(current_user, q_map[type][action])
        if item in q:
            q.remove(item)
            db.session.commit()
            return Restful.success('取消成功')
        else:
            q.append(item)
            db.session.commit()
            return Restful.success('关注成功')
    else:
        return Restful.unauth_error()


# @front_bp.route('/topic/like')
# def like_topic():
#     if current_user.is_authenticated:
#         topic_id = request.args.get('id', type=int)
#         topic = Topic.query.get(topic_id)
#         if topic in current_user.followed_topics:
#             current_user.followed_topics.remove(topic)
#             db.session.commit()
#             return Restful.success('取消成功')
#         else:
#             current_user.followed_topics.append(topic)
#             db.session.commit()
#             return Restful.success('关注成功')
#     else:
#         return Restful.unauth_error()
#
#
# @front_bp.route('/comment/like')
# def like_comment():
#     if current_user.is_authenticated:
#         comment_id = request.args.get('id', type=int)
#         comment = Comment.query.get(comment_id)
#         if comment in current_user.liked_comments:
#             current_user.liked_comments.remove(comment)
#             db.session.commit()
#             return Restful.success('取消成功')
#         else:
#             current_user.liked_comments.append(comment)
#             db.session.commit()
#             return Restful.success('点赞成功')
#     else:
#         return Restful.unauth_error()
#
#
# @front_bp.route('/post/like')
# def like_post():
#     if current_user.is_authenticated:
#         post_id = request.args.get('id', type=int)
#         post = Post.query.get(post_id)
#         if post in current_user.liked_posts:
#             current_user.liked_posts.remove(post)
#             db.session.commit()
#             return Restful.success('取消成功')
#         else:
#             current_user.liked_posts.append(post)
#             db.session.commit()
#             return Restful.success('点赞成功')
#     else:
#         return Restful.unauth_error()
#
# 
# @front_bp.route('/post/collect')
# def collect_post():
#     if current_user.is_authenticated:
#         post_id = request.args.get('id', type=int)
#         post = Post.query.get(post_id)
#         if post in current_user.collected_posts:
#             current_user.collected_posts.remove(post)
#             db.session.commit()
#             return Restful.success('取消成功')
#         else:
#             current_user.collected_posts.append(post)
#             db.session.commit()
#             return Restful.success('收藏成功')
#     else:
#         return Restful.unauth_error()
