# coding: utf-8
from flask import (
    Blueprint,
    render_template,
    request
    )
from like.models import Discussion, Statement
from flask_login import login_required, current_user
from flask_socketio import emit, join_room
from like.exts import db, socketio
from like.utils import Restful


disc_bp = Blueprint('disc', __name__, url_prefix='/discussion')


@disc_bp.route('/')
@login_required
def index():
    return render_template('disc/index.html', user=current_user)


@disc_bp.route('/<int:disc_id>')
@login_required
def disc_room(disc_id):
    disc = Discussion.query.get(disc_id)
    return render_template('disc/room.html', disc=disc)


@disc_bp.route('/join')
@login_required
def join_disc():
    disc_id = request.args.get('disc_id', type=int)
    disc = Discussion.query.get(disc_id)
    disc.participants.append(current_user)
    db.session.add(disc)
    db.session.commit()
    return Restful.success()


@socketio.on('join')
def join(data):
    disc_id = data['disc_id']
    room = f'disc-{disc_id}'
    join_room(room)
    emit('join', room=room)


@socketio.on('new message')
def new_message(data):
    content = data['content']
    disc_id = data['disc_id']
    disc = Discussion.query.get(int(disc_id))
    if current_user in disc.participants:
        stat = Statement(content=content, creator=current_user, discussion=disc)
        db.session.add(stat)
        db.session.commit()
        room = f'disc-{disc_id}'
        html = render_template('disc/message.html', stat=stat)
        emit('new message', {'html': html}, room=room)
