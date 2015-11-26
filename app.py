# app.py
import datetime
import hashlib

from flask import Flask, render_template, request, redirect, url_for, session, g, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SECRET_KEY'] = 'sdflkjsdfsdfsdf'
db = SQLAlchemy(app)


class User(db.Model):
    username = db.Column(db.Unicode(255), primary_key=True)
    password = db.Column(db.Unicode(255))
    nickname = db.Column(db.Unicode(20), unique=True)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Unicode(255))
    content = db.Column(db.UnicodeText)
    author_username = db.Column(db.Unicode(255), db.ForeignKey('user.username'))
    published_at = db.Column(db.DateTime, default=datetime.datetime.now)

    author = db.relationship('User', backref='articles')


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.UnicodeText)
    author_username = db.Column(db.Unicode(255), db.ForeignKey('user.username'))
    article_id = db.Column(db.Integer)
    published_at = db.Column(db.DateTime, default=datetime.datetime.now)

    author = db.relationship('User', backref='comments')


@app.route('/')
def index():
    articles = Article.query.all()
    return render_template('index.html', articles=articles)


@app.route('/<int:article_id>')
def read(article_id):
    article = Article.query.filter_by(id=article_id).first()
    if article is None:
        return redirect(url_for('index'))

    comments = Comment.query.filter_by(article_id=article_id).all()
    comments_count = Comment.query.filter_by(article_id=article_id).count()
    return render_template('read.html', article=article, comments=comments, comments_count=comments_count)


@app.route('/write', methods=['GET', 'POST'])
def write():
    if g.user is None:
        flash('글을 작성하시려면 로그인하셔야 합니다.')
        return redirect(url_for('login'))

    if request.method == 'GET':
        return render_template('write.html')

    title = request.form.get('title', '')
    content = request.form.get('content', '')

    article = Article(author=g.user, title=title, content=content)
    db.session.add(article)
    db.session.commit()

    return redirect(url_for('read', article_id=article.id))


@app.route('/modify/<int:article_id>', methods=['GET', 'POST'])
def modify(article_id):
    article = Article.query.filter_by(id=article_id).first()
    if article is None:
        return redirect('/')

    if request.method == 'GET':
        return render_template('modify.html', article=article)

    article.title = request.form.get('title')
    article.content = request.form.get('content')
    article.author = request.form.get('author')
    db.session.commit()

    return redirect(url_for('read', article_id=article_id))


@app.route('/delete/<int:article_id>')
def delete(article_id):
    article = Article.query.filter_by(id=article_id).first()
    if article is None:
        return redirect(url_for('/'))

    db.session.delete(article)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/<int:article_id>/comment', methods=['POST'])
def write_comment(article_id):
    if g.user is None:
        flash('댓글 작성하시려면 로그인하셔야 합니다.')
        return redirect('login')

    article = Article.query.filter_by(id=article_id).first()

    if article is None:
        return redirect(url_for('/'))

    comment = Comment(article_id=article_id, content=request.form['content'], author=g.user)
    db.session.add(comment)
    db.session.commit()

    return redirect(url_for('read', article_id=article_id))


@app.route('/comment/delete/<int:comment_id>')
def delete_comment(comment_id):
    comment = Comment.query.filter_by(id=comment_id).first()

    if comment is None:
        return redirect(url_for('index'))

    db.session.delete(comment)
    db.session.commit()
    return redirect(url_for('read', article_id=comment.article_id))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    username = request.form['username']
    password = request.form['password']
    hashed_password = hashlib.sha1(password.encode('utf-8')).hexdigest()
    nickname = request.form['nickname']

    user = User(username=username, password=hashed_password, nickname=nickname)

    db.session.add(user)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        flash('중복된 아이디나 닉네임입니다.')
        return redirect(url_for('register'))

    session['logined_username'] = username

    return redirect(url_for('index'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    username = request.form['username']
    password = request.form['password']
    hashed_password = hashlib.sha1(password.encode('utf-8')).hexdigest()

    user = User.query.filter_by(username=username, password=hashed_password).first()

    if user is None:
        flash('유효하지 않은 계정입니다. 회원 가입 후 이용하세요.')
        return redirect(url_for('login'))
    session['logined_username'] = username

    return redirect(url_for('index'))


@app.route('/logout')
def logout():
    try:
        del session['logined_username']
    except:
        pass
    return redirect(url_for('index'))


@app.before_request
def set_user():
    try:
        g.user = User.query.filter_by(username=session['logined_username']).first()
    except:
        g.user = None


@app.context_processor
def inject_user():
    return dict(user=g.user)

if __name__ == '__main__':
    app.run(debug=True)
