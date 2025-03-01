import os
import secrets
from PIL import Image
from flask import url_for
from flask_mail import Message
from flask_fp import mail
from flask import current_app
import boto3

def save_picture(form_picture):
	random_hex = secrets.token_hex(8)
	_, f_ext = os.path.splitext(form_picture.filename)
	picture_fn = random_hex + f_ext
	picture_path = os.path.join(current_app.root_path, 'static/profile_picture', picture_fn)
	
	output_size = (125,125)
	i = Image.open(form_picture)
	i.thumbnail(output_size)

	i.save(picture_path)

	return picture_fn

def save_picture_posted(form_picture):
	random_hex = secrets.token_hex(8)
	_, f_ext = os.path.splitext(form_picture.filename)
	picture_fn = random_hex + f_ext
	picture_path = os.path.join(current_app.root_path, 'static/posted_picture', picture_fn)
	
	

	i = Image.open(form_picture)

	i.save(picture_path)

	client = boto3.client('rekognition')

	with open(picture_path, 'rb') as image: response = client.detect_labels(Image={'Bytes': image.read()})
	
	return picture_fn, response['Labels']


def send_reset_email(user):
	token = user.get_reset_token()
	msg = Message('Password Reset Request', sender = 'bemisaalx3@gmail.com', recipients = [user.email])
	msg.body = f''' To reset your password, visit the following link:
{url_for('users.reset_token', token=token, _external=True)}

If you did not make this request, ignore this email and no changes will be made.
'''
	mail.send(msg)