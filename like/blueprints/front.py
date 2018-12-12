# coding: utf-8
from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    abort,
    current_app,
    request
    )
from like.models import Post, Topic, Comment, User
from like.forms import NewPostForm, NewTopicForm
from flask_login import login_required, current_user
from sqlalchemy.sql.expression import func
from like.exts import db
from like.utils import Restful


front_bp = Blueprint('front', __name__)


@front_bp.context_processor
def make_context():
    hot_topics = Topic.query.join(Topic.posts).group_by(Topic.id) \
        .order_by(func.count(Post.id).desc()).limit(5)
    return {'hot_topics': hot_topics}


@front_bp.route('/')
def index():
    return render_template('front/index.html', stream='post', title='首页')


@front_bp.route('/discovery')
def discovery():
    return render_template('front/index.html', stream='discovery', title='发现')


@front_bp.route('/topic/<int:topic_id>')
def topic(topic_id):
    topic = Topic.query.get(topic_id)
    return render_template('front/topic.html', topic=topic)


@front_bp.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.get(post_id)
    return render_template('front/post.html', post=post)


@front_bp.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    if current_user.has_permission('PUBLISH'):
        form = NewPostForm()
        if form.validate_on_submit():
            content = form.content.data
            topic_id = form.topic.data
            topic = Topic.query.get(topic_id)
            post = Post(content=content,
                        topic=topic,
                        creator=current_user)
            db.session.add(post)
            db.session.commit()
            return redirect(url_for('user.index', user_id=current_user.id))
        topic_id = request.args.get('topic', 1)
        return render_template('front/new_post.html', form=form, topic_id=topic_id)
    abort(401)


@front_bp.route('/topic/new', methods=['GET', 'POST'])
@login_required
def new_topic():
    if current_user.has_permission('PUBLISH'):
        form = NewTopicForm()
        if form.validate_on_submit():
            name = form.name.data
            topic = Topic(name=name, creator=current_user)
            db.session.add(topic)
            db.session.commit()
            return redirect(url_for('user.index', user_id=current_user.id))
        return render_template('front/new_post.html', form=form)
    abort(401)


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
