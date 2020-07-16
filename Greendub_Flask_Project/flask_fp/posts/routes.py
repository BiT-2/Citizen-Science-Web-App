from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from flask_login import current_user, login_required
from flask_fp import db
from flask_fp.models import Post, Image
from flask_fp.posts.forms import PostForm
from flask_fp.users.utils import save_picture_posted

posts = Blueprint('posts', __name__)

@posts.route("/post/new", methods = ['GET', 'POST'])
@login_required
def new_post():
	form = PostForm()
	if form.validate_on_submit():
		picture_file,response = save_picture_posted(form.picture.data)
		post = Post(title = form.title.data, content = form.content.data, author = current_user, image_post=picture_file)
		current_post_id = post.id
		db.session.add(post)
		for label in response:
			image_recg = Image(label = label['Name'], confidence = str(label['Confidence']), image_trans = post, post_id = post.id)
			db.session.add(image_recg)
		db.session.commit()
		
		flash('Post Created', 'success')
		return redirect(url_for('main.home'))
	return render_template('create_post.html', title = 'New Post', form = form, legend ='New Post')

@posts.route("/post/<int:post_id>")
def post(post_id):
	post = Post.query.get_or_404(post_id)
	image_trans = Image.query.filter_by(post_id = post_id).all()
	return render_template('post.html', title = post.title, post=post, image_trans = image_trans)

@posts.route("/post/<int:post_id>/update", methods = ['GET', 'POST'])
@login_required
def update_post(post_id):
	post = Post.query.get_or_404(post_id)
	if post.author != current_user:
		abort(403)
	form = PostForm()
	if form.validate_on_submit():
		post.title = form.title.data
		post.content = form.content.data
		picture_file = save_picture_posted(form.picture.data)
		post.image_post = picture_file
		db.session.commit()
		flash('Updated successfully', 'success')
		return redirect(url_for('posts.post', post_id=post.id))
	elif request.method == 'GET':
		form.title.data = post.title
		form.content.data = post.content
	return render_template('create_post.html', title = 'Update Post', form = form, legend = 'Update Post')


@posts.route("/post/<int:post_id>/dalete", methods = ['POST'])
@login_required
def delete_post(post_id):
	post = Post.query.get_or_404(post_id)
	if post.author != current_user:
		abort(403)
	db.session.delete(post)
	db.session.commit()
	flash('Post successfully deleted', 'success')
	return redirect(url_for('main.home'))
