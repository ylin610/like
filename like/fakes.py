# coding: utf-8
from faker import Faker
from like.exts import db
from like.models import User, Topic, Post, Comment, Discussion, Statement
import random


fake = Faker()


def fake_users(count=30):
    admin = User(username='admin', email='admin@test.com', bio=fake.sentence())
    admin.password = '1234'
    admin.set_role('ADMIN')
    db.session.add(admin)
    for _ in range(count):
        user = User(username=fake.name(),
                    email=fake.email(),
                    bio=fake.sentence()
                    )
        user.password = '1234'
        user.set_role('USER')
        db.session.add(user)
    db.session.commit()


def fake_topics(count=20):
    users = User.query.all()
    for _ in range(count):
        topic = Topic(name=fake.word(),
                      description=''.join(fake.sentences()),
                      )
        topic.creator = random.choice(users)
        topic.followers = random.sample(users, k=random.randint(1, len(users)))
        db.session.add(topic)
    db.session.commit()


def fake_posts(count=150):
    users = User.query.all()
    topics = Topic.query.all()
    for _ in range(count):
        post = Post(content=''.join(fake.sentences(nb=random.randint(1, 8))),
                    topic=random.choice(topics),
                    creator=random.choice(users),
                    create_time=fake.date_time_this_year(),
                    collectors=random.sample(users, k=random.randint(1, len(users))),
                    liked_users=random.sample(users, k=random.randint(1, len(users)))
                    )
        db.session.add(post)
    db.session.commit()


def fake_comments(count=500):
    users = User.query.all()
    posts = Post.query.all()
    for _ in range(count):
        comment = Comment(content=''.join(fake.sentences(nb=random.randint(1, 3))),
                          creator=random.choice(users),
                          post=random.choice(posts),
                          liked_users=random.sample(users, k=random.randint(1,20))
                          )
        comment.create_time = fake.date_time_this_year(after_now=comment.create_time)
        db.session.add(comment)
    db.session.commit()


def fake_discussion(count=40):
    users = User.query.all()
    for _ in range(count):
        disc = Discussion(name=fake.sentence(),
                          creator=random.choice(users),
                          create_time=fake.date_time_this_year(),
                          participants=random.sample(users, k=random.randint(1, 10))
                          )
        disc.start_time = fake.date_time_this_year(after_now=disc.create_time)
        for __ in range(random.randint(40, 100)):
            stat = Statement(content=fake.sentence(),
                             creator=random.choice(disc.participants),
                             create_time=fake.date_time_this_year(after_now=disc.start_time)
                             )
            stat.discussion = disc
        db.session.add(disc)
    db.session.commit()
