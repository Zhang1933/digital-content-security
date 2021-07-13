import os
from flask import Blueprint,render_template,request,flash,jsonify,redirect,url_for
from flask_login import login_required,  current_user
from werkzeug.utils import secure_filename
import json
from .models import Note
from . import db
# pylint: disable=no-member

views=Blueprint('views',__name__)
UPLOAD_FOLDER = os.path.join('.','website','static')


ALLOWED_EXTENSIONS = {'png','bmp','tiff'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@views.route('/index')
@views.route('/',methods=['Get','POST'])
# @login_required # 必须要登陆才能进入此页面
def home():
    # 匿名用户登陆
    if current_user.is_anonymous== True:
        # print("###DEBUG###")
        # print(Note.query.all())
        # 按时间逆序
        return render_template('index.html',notes=Note.query.order_by(Note.date.desc()).all())
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
            new_note=Note(data=name,user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            note.save(os.path.join(UPLOAD_FOLDER,name))
            flash('Note added!',category='True')
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
    return jsonify({})
