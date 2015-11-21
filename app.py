# app.py
import datetime

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
db = SQLAlchemy(app)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Unicode(255))
    content = db.Column(db.UnicodeText)
    author = db.Column(db.Unicode(255))
    published_at = db.Column(db.DateTime, default=datetime.datetime.now)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.UnicodeText)
    author = db.Column(db.Unicode(255))
    article_id = db.Column(db.Integer)
    published_at = db.Column(db.DateTime, default=datetime.datetime.now)


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
    if request.method == 'GET':
        return render_template('write.html')
    title = request.form.get('title', '')
    content = request.form.get('content', '')
    author = request.form.get('author', '')

    article = Article(title=title, content=content, author=author)
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
    article = Article.query.filter_by(id=article_id).first()
    if article is None:
        return redirect(url_for('/'))
    comment = Comment(article_id=article_id, content=request.form['content'], author=request.form['author'])
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


if __name__ == '__main__':
    app.run(debug=True)
