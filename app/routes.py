from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from flask_login import login_required, current_user
from .models import News, ForumThread, ForumPost, CollectionItem
from . import db

main = Blueprint('main', __name__)

@main.route('/set_lang/<lang>')
def set_lang(lang):
    if lang in ['es', 'en']:
        session['lang'] = lang
    return redirect(request.referrer or url_for('main.index'))

@main.route('/')
def index():
    news = News.query.order_by(News.created_at.desc()).limit(10).all()
    return render_template('index.html', news=news)

@main.route('/collection', methods=['GET', 'POST'])
@login_required
def collection():
    if request.method == 'POST':
        title = request.form.get('title')
        platform = request.form.get('platform')
        status = request.form.get('status')
        item = CollectionItem(user_id=current_user.id, game_title=title, platform=platform, status=status)
        db.session.add(item)
        db.session.commit()
        return redirect(url_for('main.collection'))
        
    items = CollectionItem.query.filter_by(user_id=current_user.id).all()
    return render_template('collection.html', items=items)

@main.route('/forum', methods=['GET', 'POST'])
def forum():
    if request.method == 'POST':
        if not current_user.is_authenticated:
            flash('Inicia sesión para crear un hilo.')
            return redirect(url_for('auth.login'))
        title = request.form.get('title')
        thread = ForumThread(title=title, author_id=current_user.id)
        db.session.add(thread)
        db.session.commit()
        return redirect(url_for('main.thread', thread_id=thread.id))
        
    threads = ForumThread.query.order_by(ForumThread.created_at.desc()).all()
    return render_template('forum.html', threads=threads)

@main.route('/thread/<int:thread_id>', methods=['GET', 'POST'])
def thread(thread_id):
    thread = ForumThread.query.get_or_404(thread_id)
    if request.method == 'POST':
        if not current_user.is_authenticated:
            flash('Inicia sesión para responder.')
            return redirect(url_for('auth.login'))
            
        content = request.form.get('content')
        post = ForumPost(content=content, thread_id=thread.id, author_id=current_user.id)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('main.thread', thread_id=thread.id))
        
    return render_template('thread.html', thread=thread)
