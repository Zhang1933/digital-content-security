import io
import os
import numpy as np
from flask import Blueprint,render_template,request,flash,jsonify,redirect,url_for, abort
from flask_login import login_required,  current_user
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash
import json
from .models import Note,User
from . import db
from flask_paginate import Pagination
import requests
import base64
import rsa
from PIL import Image
# pylint: disable=no-member

views=Blueprint('views',__name__)
UPLOAD_FOLDER = os.path.join('.','website','static')


ALLOWED_EXTENSIONS = {'png','bmp','tiff','jpeg','jpg'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@views.route('/index/')
@views.route('/',methods=['Get','POST'])
# @login_required # 必须要登陆才能进入此页面
def home():
    # 匿名用户登陆
    ROWS_PER_PAGE = 5
    page = int(request.args.get('page', 1)) 
    per_page = int(request.args.get('per_page', 5))

    if current_user.is_anonymous== True:
        # print("###DEBUG###")
        # print(Note.query.all())
        # 按时间逆序
        paginate=Note.query.order_by(Note.date.desc()).paginate(page,per_page,error_out=False)
        return render_template('index.html',paginate=paginate,notes=paginate.items)
    # 上传图片
    if request.method== 'POST':
        if 'file' not in request.files:
            flash('No file part',category='error')
            return redirect(request.url)
        note=request.files['file']
        if  note.filename=="" :
            print(note.filename)
            flash('You submit nothing.',category='error')
        elif allowed_file(note.filename):
            # 创建上传图片到服务器,创建图片路径
            # print ("###"+os.getcwd())
            cnt=db.session.query(Note).count()
            name=str(cnt)+secure_filename(note.filename)
            new_note=Note(data=name,user_id=current_user.id,user_name=current_user.first_name)
            db.session.add(new_note)
            db.session.commit()
            note.save(os.path.join(UPLOAD_FOLDER,name))
            flash('Note added!',category='True')
        else :
            flash('UPLOAD_Failed',category='error')
    return render_template("home.html",user=current_user)

@views.route('/delete-note',methods=['POST'])
def delete_note():
    note=json.loads(request.data)
    noteId= note['noteId']
    note=Note.query.get(noteId)
    if note:
        if note.user_id==current_user.id:
            db.session.delete(note)
            db.session.commit()
            os.remove(os.path.join(UPLOAD_FOLDER,note.data))
    return jsonify({})

@views.route('/like-note',methods=['POST'])
def like_note():
    note=json.loads(request.data)
    noteId=note['noteId']
    note=Note.query.get(noteId)
    if note:
        note.liked+=1
        db.session.commit()
    return jsonify({})

@views.route('/upload',methods=['POST'])
def upload_note():
    if not request.json or 'image' not in request.json:
        abort(400)
    if 'email' not in request.json or 'encryppass' not in request.json :
        abort(400)

    email=request.json['email']
    encryppass=request.json['encryppass']
    user=User.query.filter_by(email=email).first()
    priv_key=rsa.PrivateKey(int(user.n),int(user.e),int(user.d),int(user.p),int(user.q))

    tmp=base64.b64decode(encryppass.encode('utf-8'))
    password=rsa.decrypt(tmp,priv_key).decode('utf-8')
    if not check_password_hash(user.password,password):
        abort(400)
    im_b64=request.json['image']
    img_bytes=base64.b64decode(im_b64.encode('utf-8'))
    try :
        img=Image.open(io.BytesIO(img_bytes))
    except IOError:
        abort(400)
    cnt=db.session.query(Note).count()
    name=str(cnt)+user.first_name+"."+img.format

    new_note=Note(data=name,user_id=user.id,user_name=user.first_name)
    img.save(os.path.join(UPLOAD_FOLDER,name))
    db.session.add(new_note)
    db.session.commit()
    return {'status':'200'}
