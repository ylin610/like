# coding: utf-8
from .base import BaseTestCase
from like.exts import db
from like.models import User, Permission, Role, Topic, Post, Comment, Discussion, Statement


class DatabaseTestCase(BaseTestCase):

    def setUp(self):
        super().setUp()
        admin = User(username='admin', email='test@test.com')
        admin.set_role('ADMIN')
        topic = Topic(name='test_topic')
        topic.creator = admin
        discussion = Discussion(name='test_discussion', creator=admin)
        self.admin = admin
        self.topic = topic
        self.discussion = discussion

        self.users = []
        self.posts = []
        self.comments = []
        self.stats = []
        for i in range(3):
            user = User(username=f'user<{i}>', email=f'user<{i}>@test.com')
            user.set_role('USER')
            post = Post(content=f'test_post_content<{i}>.')
            post.creator = user
            post.topic = topic
            comment = Comment(content=f'comment<{i}>', creator=admin)
            comment.post = post
            discussion.participants.append(user)
            stat = Statement(content=f'test_statement<{i}>', creator=user,discussion=discussion)
            self.users.append(user)
            self.posts.append(post)
            self.comments.append(comment)
            self.stats.append(stat)
            db.session.add(user)

        db.session.add(admin)
        db.session.commit()

    def test_existence(self):
        self.assertEqual(1, len(User.query.filter_by(username='admin').all()))
        self.assertEqual(4, len(User.query.all()))
        self.assertEqual(1, len(Topic.query.all()))
        self.assertEqual(1, len(Discussion.query.all()))
        self.assertEqual(3, len(Post.query.all()))
        self.assertEqual(3, len(Comment.query.all()))
        self.assertEqual(3, len(Statement.query.all()))

    def test_admin(self):
        self.assertEqual('ADMIN', self.admin.role.name)
        self.assertTrue(self.admin.has_permission('ADMIN'))
        self.assertRaises(ValueError, self.admin.set_role, 'ADMIN')

    def test_topic(self):
        self.assertEqual(self.topic.creator, self.admin)
        self.assertEqual(self.posts, self.topic.posts)

    def test_post(self):
        self.assertIn(self.comments[0], self.posts[0].comments)

    def test_discussion(self):
        self.assertEqual(self.discussion.creator, self.admin)
        self.assertEqual(self.stats, self.discussion.statements)
        self.assertIn(self.users[0], self.discussion.participants)
