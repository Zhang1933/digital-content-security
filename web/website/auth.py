from flask import Blueprint, render_template,request,flash,redirect, url_for
from .models import User
from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

auth=Blueprint('auth',__name__)

@auth.route('/sign-up',methods=['Get','POST'])
def sign_up():
    # pylint: disable=no-member
    if request.method == 'POST':
        email=request.form.get('email')
        first_name=request.form.get('firstName')
        password1=request.form.get('password1')
        password2=request.form.get('password2')

        user=User.query.filter_by(email=email).first()
        if user :
            flash('Email already exists',category='error')
        elif len(email)<4:
            flash('Email must be greater than 4 characters.',category='error')
        elif len(first_name)<2:
            flash('firstName must be greater than 2 characters.',category='error')
        elif password1 != password2 :
            flash('Passwords don\'t match.',category='error')
        elif len(password1) <3 :
            flash('Passwords must be at least 7 characters.',category='error')
        else :
            # 检查完毕 创建账户
            new_user=User(email=email,first_name=first_name,password=generate_password_hash(password1,'sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash('Account created!',category='success')
            login_user(user,remember=True)
            return  redirect(url_for('views.home'))
    return render_template("sign_up.html",user=current_user)

@auth.route('/logout')
@login_required # 没有登陆不能进入此页面
def logout():
    # 登出
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/login',methods=['Get','POST'])
def login():
    if request.method =='POST':
        email=request.form.get('email')
        password=request.form.get('password')
        
        user=User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password,password):
                # 检查完毕 成功登陆
                flash('Logged in successfully!',category='success')
                # 记住登陆
                login_user(user,remember=True)
                return redirect(url_for('views.home'))
            else :
                flash('Incorrct password,try again.',category='error')
        else :
            flash('Email does not exist.',category='error')
    return render_template("login.html",user=current_user)
