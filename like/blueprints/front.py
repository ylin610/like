# coding: utf-8
from flask import (
    Blueprint,
    render_template,
    current_app,
    request
    )
from like.models import Post, Topic, Comment, User
from sqlalchemy.sql.expression import func


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
