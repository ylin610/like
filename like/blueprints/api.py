# coding: utf-8
from flask import (
    Blueprint,
    render_template,
    current_app,
    request
    )
from like.models import Post, Topic, Comment, User
from sqlalchemy.sql.expression import func


api_bp = Blueprint('api', __name__, url_prefix='/api/v1')

@api_bp.route('/post')
def get_post():
    topic = request.args.get('topic_id', type=int)
    page = request.args.get('page', 1, type=int)
    num = request.args.get('num', current_app.config['POSTS_PER_PAGE'], type=int)
    query_obj = Post.query
    if topic:
        query_obj = query_obj.filter_by(topic_id=topic)
    posts = query_obj.order_by(Post.create_time.desc()).paginate(page, num).items
    return render_template('api/post.html', posts=posts)
