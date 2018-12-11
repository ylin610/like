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


@front_bp.route('/comment/like')
def like_comment():
    if current_user.is_authenticated:
        comment_id = request.args.get('comment_id', type=int)
        comment = Comment.query.get(comment_id)
        if comment in current_user.liked_comments:
            current_user.liked_comments.remove(comment)
            db.session.commit()
            return Restful.success('取消成功')
        else:
            current_user.liked_comments.append(comment)
            db.session.commit()
            return Restful.success('点赞成功')
    else:
        return Restful.unauth_error()


@front_bp.route('/post/like')
def like_post():
    if current_user.is_authenticated:
        post_id = request.args.get('post_id', type=int)
        post = Post.query.get(post_id)
        if post in current_user.liked_posts:
            current_user.liked_posts.remove(post)
            db.session.commit()
            return Restful.success('取消成功')
        else:
            current_user.liked_posts.append(post)
            db.session.commit()
            return Restful.success('点赞成功')
    else:
        return Restful.unauth_error()


@front_bp.route('/post/collect')
def collect_post():
    if current_user.is_authenticated:
        post_id = request.args.get('post_id', type=int)
        post = Post.query.get(post_id)
        if post in current_user.collected_posts:
            current_user.collected_posts.remove(post)
            db.session.commit()
            return Restful.success('取消成功')
        else:
            current_user.collected_posts.append(post)
            db.session.commit()
            return Restful.success('点赞成功')
    else:
        return Restful.unauth_error()