# coding: utf-8
from flask import (
    Blueprint,
    render_template,
    jsonify,
    current_app,
    request
    )
from like.models import Post, Topic, Comment, User, Discussion, Statement
from flask_login import login_required, current_user
from flask_socketio import emit, join_room
from sqlalchemy.sql.expression import func
from like.exts import db, socketio
from like.utils import Restful


disc_bp = Blueprint('disc', __name__, url_prefix='/discussion')


@disc_bp.route('/<int:disc_id>')
@login_required
def disc_room(disc_id):
    disc = Discussion.query.get(disc_id)
    return render_template('disc/room.html', disc=disc)


@socketio.on('join')
def join(data):
    print('recv join message')
    disc_id = data['disc_id']
    room = f'disc-{disc_id}'
    join_room(room)
    emit('join', data['user_id'], room=room)


@socketio.on('new message')
def new_message(data):
    print('recv new message')
    content = data['content']
    disc_id = data['disc_id']
    disc = Discussion.query.get(int(disc_id))
    user = User.query.get(int(data['user_id']))
    stat = Statement(content=content, creator=user, discussion=disc)
    db.session.add(stat)
    db.session.commit()
    room = f'disc-{disc_id}'
    html = render_template('disc/message.html', stat=stat)
    emit('new message', {'html':html}, room=room)

