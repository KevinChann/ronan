from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,PasswordField,BooleanField,FileField,TextAreaField
from wtforms.validators import Required,Length,EqualTo,Email,Regexp,URL
from wtforms import ValidationError
from ..models import User

#注册表单
class RegisterForm(FlaskForm):
	account = StringField(u'账号：',validators=[Required(),Length(min=8,max=16,message=u'请输入8至16位数'),
		Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,u'账号只能包含英文、数字、点和下划线,并且以字母开头！')])
	password = PasswordField(u'密码：',validators=[Required(),Length(min=8,max=16,message=u'请输入8至16位数'),
		EqualTo('password_confirm',message=u'两次密码不一致'),
		Regexp('[A-Za-z0-9_.]*$', 0,u'密码只能包含英文,数字,点和下划线！')])
	password_confirm = PasswordField(u'验证密码：',validators=[Required(),Length(min=8,max=16,message=u'请输入8至16位数')])
	accept_protocol = BooleanField(u'接受协议（待完成）')
	submit = SubmitField(u'注册')

	#以'validata_'+'字段'为函数名的自定义验证函数，和其他炎症函数一起执行
	#规定格式函数名，自动执行，检验account选项
	#验证account唯一性
	def validate_account(self,field):
		if User.query.filter_by(account=field.data).first():
			raise ValidationError(u'这个账号已经被注册了!')
		#阻止用户注册'__default__'这个名字，因为【默认头像】预占用了
		if field.data == '__default__':
			raise ValidationError(u'这个账号已经被注册了!')

#登陆表单
class LoginForm(FlaskForm):
	account = StringField(u'账号：',validators=[Required(),Length(min=8,max=16,message=u'请输入8至16位数')])
	password = PasswordField(u'密码：',validators=[Required(),Length(min=8,max=16,message=u'请输入8至16位数')])
	remember_me = BooleanField(u'记住我')
	submit = SubmitField(u'登陆')

	def validate_account(self,field):
		if not User.query.filter_by(account=field.data).first():
			raise ValidationError(u'账号不存在！')

#修改个人资料表单
class EditProfileForm(FlaskForm):
	email = StringField(u'邮箱：',validators=[Length(min=0,max=64,message=u'太长了！'),Email(message=u'邮箱格式错误！')])
	address = StringField(u'地址：',validators=[Length(min=0,max=64,message=u'太长了！')])
	phone = StringField(u'电话：',validators=[Length(min=0,max=16,message=u'太长了！'),
		Regexp('[0-9]*$', 0,u'电话只能包含数字！')])
	domain = StringField(u'个人网址：',validators=[Length(min=0,max=64,message=u'太长了！')])
	submit = SubmitField(u'保存')

#修改密码表单
class ChangePasswordForm(FlaskForm):
	password = PasswordField(u'修改密码：',validators=[Required(),Length(min=8,max=16,message=u'请输入8至16位数'),
		EqualTo('password_confirm',message=u'两次密码不一致'),
		Regexp('[A-Za-z0-9_.]*$', 0,u'密码只能包含英文,数字,点和下划线！')])
	password_confirm = PasswordField(u'验证修改密码：',validators=[Required(),Length(min=8,max=16,message=u'请输入8至16位数')])
	submit = SubmitField(u'保存')

#上传头像表单
class ChangeAvatarForm(FlaskForm):
	avatar = FileField(u'头像：',validators=[Required()])
	submit = SubmitField(u'上传')

#Post表单
class PostForm(FlaskForm):
	text = TextAreaField(u'说点什么呢～',validators=[Length(min=1,max=200,message=u'长度：1-200')])
	picture = FileField(u'分享图片～')
	submit = SubmitField(u'提交')

#评论表单
class CommentForm(FlaskForm):
	body = StringField('',validators=[Length(min=1,max=35,message=u'长度：1-35')])
	submit = SubmitField(u'提交')







