import os
from datetime import datetime
from flask import render_template,session,redirect,url_for,flash,abort,request,current_app
from flask_login import login_required,login_user,logout_user,current_user
from werkzeug.security import generate_password_hash,check_password_hash

from . import main
from .forms import RegisterForm,LoginForm,EditProfileForm,ChangePasswordForm,ChangeAvatarForm,PostForm,CommentForm
from .. import db
from ..models import User,Post,Comment

@main.route('/',methods=['GET','POST'])
def index():
	#用户登陆后才显示post form
	if current_user.is_authenticated:
		form = PostForm()
		if form.validate_on_submit():
			#picture = request.files['picture']
			if 'picture' in request.files:
				####BUG#####:bad request
				picture = request.files['picture']
				picture_filename = picture.filename
				folder = current_app.config['UPLOAD_PICTURE_FOLDER']
				allowed_extensions = ['png','jpg','gif','jpeg','JPG']
				#无后缀检测
				flag = False
				if len(picture_filename.rsplit('.',1)) == 1:
					flag = False
				else:
					upload_picture_extension = picture_filename.rsplit('.',1)[1]
					flag = '.' in picture_filename and upload_picture_extension in allowed_extensions
				if not flag:
					flash(u'图片格式只允许jpg/jpeg/png/gif！')
					return redirect(url_for('main.index'))
				#设置保存名字为account_timeNOW.xxx
				time = datetime.now().strftime('%y%m%d%H%M%S')
				save_picture_name = current_user.account+'_'+time+'.'+upload_picture_extension
				picture.save('{}{}'.format(folder,save_picture_name))
				post = Post(body=form.text.data,author_id=current_user.id,picture=save_picture_name)
				db.session.add(post)
				db.session.commit()
			else:
				post = Post(body=form.text.data,author_id=current_user.id)
				db.session.add(post)
				db.session.commit()
			flash(u'分享成功!')
			return redirect(url_for('main.index'))
		#查询全部post，【 分页 】显示
		page = request.args.get('page',1,type=int)	#默认渲染第一页
		pagination = Post.query.order_by(Post.timestamp.desc()).paginate(
			page,per_page=current_app.config['POSTS_PER_PAGE'],error_out=False)
		posts = pagination.items
		#posts = Post.query.order_by(Post.timestamp.desc()).all()
		#动态url刷新图片cahce
		time = datetime.now().strftime('%y%m%d%H%M%S')
		return render_template('index.html',post_form=form,posts=posts,pagination=pagination,
			dynamic_url=time)

	return render_template('index.html')

@main.route('/register',methods=['GET','POST'])
def register():
	form = RegisterForm()
	if form.validate_on_submit():
		#计算加盐密码散列值
		password_hash = generate_password_hash(form.password.data)
		user = User(account=form.account.data,password=password_hash)
		db.session.add(user)
		db.session.commit()
		flash(u'注册成功')
		return redirect(url_for('.index'))
	return render_template('register.html',register_form=form)

@main.route('/login',methods=['GET','POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(account=form.account.data).first()
		#密码散列值检查
		if check_password_hash(user.password,form.password.data):
			flash(u'登陆成功')
			#加载用户
			login_user(user,form.remember_me.data)

			return redirect(url_for('.index'))
		else:
			flash(u'密码错误!')
	return render_template('login.html',login_form=form)

@main.route('/profile/<account>')
@login_required
def profile(account):
	user = User.query.filter_by(account=account).first()
	if user is None:
		abort(404)
	#查询全部post，列在主页
	posts = user.posts.order_by(Post.timestamp.desc()).all()
	#传递一个动态str，为img src做动态后缀，使浏览器更新头像
	time = datetime.now().strftime('%y%m%d%H%M%S')
	return render_template('profile.html',user=user,posts=posts,dynamic_url=time)

@main.route('/edit_profile',methods=['GET','POST'])
@login_required
def edit_profile():
	form = EditProfileForm()
	if form.validate_on_submit():
		#检查submit时有无更改资料
		#有bug，待处理
		#if str(form.email.data) == str(current_user.email) & str(form.address.data) == str(current_user.address) & str(form.phone.data) == str(current_user.phone) & str(form.domain.data) == str(current_user.domain):
		#	flash(u'个人资料没变化！')
		#	return redirect(url_for('.edit_profile'))

		user = User.query.filter_by(account=current_user.account).first()
		user.email = form.email.data
		user.address = form.address.data
		user.phone = form.phone.data
		user.domain = form.domain.data
		db.session.add(user)
		db.session.commit()
		flash(u'修改个人资料成功！')
		return redirect(url_for('main.profile',account=current_user.account))

	#预加载资料
	#必须写在validate_on_submit()下面才不会干扰submit按钮
	form.email.data = current_user.email
	form.address.data = current_user.address
	form.phone.data = current_user.phone
	form.domain.data = current_user.domain

	return render_template('edit_profile.html',edit_profile_form=form)

@main.route('/change_password',methods=['GET','POST'])
@login_required
def change_password():
	form = ChangePasswordForm()
	if form.validate_on_submit():
		user = User.query.filter_by(account=current_user.account).first()
		password_hash = generate_password_hash(form.password.data)
		user.password = password_hash
		db.session.add(user)
		db.session.commit()
		flash(u'修改密码成功！')
		return redirect(url_for('.index'))

	return render_template('change_password.html',change_password_form=form)

@main.route('/change_avatar',methods=['GET','POST'])
@login_required
def change_avatar():
	form = ChangeAvatarForm()
	if form.validate_on_submit():
		#加载‘avatar’文件
		avatar = request.files['avatar']
		#获取'avatar'文件名
		avatar_filename = avatar.filename
		#从config.py获取存放路径
		folder = current_app.config['UPLOAD_AVATAR_FOLDER']
		#限制上传文件的格式
		allowed_extensions = ['png','jpg','gif','jpeg']
		#检测文件无后缀名的情况
		flag = False
		if len(avatar_filename.rsplit('.',1)) == 1:
			flag = False
		else:
			upload_avatar_extension = avatar_filename.rsplit('.',1)[1]
			flag = '.' in avatar_filename and upload_avatar_extension in allowed_extensions
		if not flag:
			flash(u'头像格式只允许jpg/jpeg/png/gif！')
			return redirect(url_for('main.change_avatar'))
		#设置保存名字为account.xxx
		save_avatar_name = current_user.account+'.'+upload_avatar_extension
		#更新数据库
		user = User.query.filter_by(account=current_user.account).first()
		#先删除原头像（避免格式不同重复存储）
		if user.avatar and os.path.exists(os.getcwd() + '/app/static/avatar/' + user.avatar):
			os.remove(os.getcwd() + '/app/static/avatar/'+user.avatar)
		user.avatar = save_avatar_name
		db.session.add(user)
		db.session.commit()

		#######保存图片的函数！！！
		avatar.save('{}{}'.format(folder,save_avatar_name))
		flash(u'头像已更新！')
		return redirect(url_for('main.profile',account=current_user.account))

	return render_template('change_avatar.html',change_avatar_form=form)

@main.route('/view_picture/<picture>')
@login_required
def view_picture(picture):
	return render_template('view_picture.html',picture=picture)

@main.route('/delete_post/<post_id>')
@login_required
def delete_post(post_id):
	post = Post.query.filter_by(id=post_id).first()
	if post:
		#删除post的图片
		if post.picture and os.path.exists(os.getcwd() + '/app/static/picture/' + post.picture):
			os.remove(os.getcwd() + '/app/static/picture/'+post.picture)
		#删除评论,delete()只能1个1个del
		comments = Comment.query.filter_by(post_id=post.id).all()
		for c in comments:
			db.session.delete(c)
		#删除post
		db.session.delete(post)
		db.session.commit()
		flash(u'删除成功！')
		return redirect(url_for('main.index'))
	
	abort(403)

@main.route('/post_comment/<int:id>',methods=['GET','POST'])
@login_required
def post_comment(id):
	post = Post.query.get_or_404(id)
	form = CommentForm()
	if form.validate_on_submit():
		comment = Comment(body=form.body.data,post=post,
							author=current_user._get_current_object())
		db.session.add(comment)
		db.session.commit()
		flash(u'评论成功！')
		return redirect(url_for('main.post_comment',id=post.id,page=-1))
	page = request.args.get('page',1,type=int)
	if page == -1:
		page = (post.comments.count() - 1) / current_app.config['COMMENTS_PER_PAGE'] + 1
	pagination = post.comments.order_by(Comment.timestamp.asc()).paginate(
		page,per_page=current_app.config['COMMENTS_PER_PAGE'],error_out=False)
	comments = pagination.items
	time = datetime.now().strftime('%y%m%d%H%M%S')
	return render_template('post_comment.html',posts=[post],form=form,
		comments=comments,pagination=pagination,dynamic_url=time)

@main.route('/delete_comment/<comment_id>')
@login_required
def delete_comment(comment_id):
	comment = Comment.query.filter_by(id=comment_id).first()
	if comment:
		#保存该comment所在的post的id，用来传给url
		post_id = comment.post.id
		#删除comment
		db.session.delete(comment)
		db.session.commit()
		return redirect(url_for('main.post_comment',id=post_id))

@main.route('/logout')
@login_required
def logout():
	#flask-login: 登出用户函数
	logout_user()
	flash(u'注销成功！')
	return render_template('index.html')