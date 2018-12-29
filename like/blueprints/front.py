# coding: utf-8
from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    abort,
    request
)
from like.models import Post, Topic, User, follow as follow_model
from like.forms import NewPostForm, NewTopicForm
from flask_login import login_required, current_user
from like.exts import db
from sqlalchemy.sql.expression import func, and_


front_bp = Blueprint('front', __name__)


SEARCH_RESULT_NUM = 8


@front_bp.context_processor
def make_context():
    possible_know = None
    if current_user.is_authenticated:
        possible_know = [
            (num, User.query.get(user_id)) for num, user_id in get_possible_know(current_user.id)
        ]
    return {'possible_know': possible_know}


def get_possible_know(user_id, num=6):
    """Get a number of users that the specific user may know.

    :param user_id: The id of the specific user.
    :param num: The number of result to get.
    :return: A list of tuples, each tuple contains the count of same followed and
        the id of result user.
    """
    _ed = follow_model.c.followed_id
    _er = follow_model.c.follower_id
    count = func.count(_ed)
    followed_id = db.session.query(_ed).filter(_er == user_id).subquery()

    possible_know = db.session.query(count, _er) \
        .filter(and_(~_er.in_(followed_id), _er != user_id)) \
        .filter(_ed.in_(followed_id)) \
        .group_by(_er) \
        .order_by(count.desc()).all()
    return possible_know[0:num]


@front_bp.route('/')
def index():
    return render_template('front/index.html',
                           stream='post',
                           title='首页')


@front_bp.route('/search', methods=['GET', 'POST'])
def search():
    query = request.form.get('query', '')
    users = User.query.whooshee_search(query).limit(SEARCH_RESULT_NUM).all()
    posts = Post.query.whooshee_search(query).limit(SEARCH_RESULT_NUM).all()
    return render_template('front/search.html', users=users, posts=posts)


@front_bp.route('/follow')
def follow():
    return render_template('front/index.html', stream='follow', title='关注')


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
        return render_template('front/new_topic.html', form=form)
    abort(401)
