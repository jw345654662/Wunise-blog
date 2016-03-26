# -- coding: utf-8 --
import sys  
reload(sys)  
sys.setdefaultencoding('utf8')  

from flask import Flask,render_template,request,make_response,redirect,url_for
import time
from werkzeug.contrib.fixers import ProxyFix


def time_now(): 
	now = int(time.time())  #这是时间戳
	timeArray = time.localtime(now)
	return time.strftime("%Y-%m-%d %H:%M:%S", timeArray)

app = Flask(__name__)

@app.errorhandler(404)
def page_not_found(e):
    return "404", 404


@app.errorhandler(500)
def internal_server_error(e):
    return "500", 500


@app.route('/')
def index():
	import sqlite3,config,base64
	conn = sqlite3.connect(config.path)
	cursor = conn.execute("SELECT TITLE, TIME, CLASS,ID,MAKEDOWN_TEXT from BLOG order by id desc")
	cursor2 = conn.execute("SELECT DISTINCT CLASS from BLOG")
	tuple0 = []
	tuple2 = []

	for row in cursor:
		tuple0.append([base64.b64decode(row[0]),row[1],base64.b64decode(row[2]),row[3],base64.b64decode(row[4])])
	for row2 in cursor2:
		tuple2.append([base64.b64decode(row2[0])])
	
	return render_template('index.html',cursor = tuple0,cursor2 = tuple2,blog_name=config.blog_name)
 



@app.route('/login', methods=['POST','GET'])
def login():
	import config 
	loginStatus = False
	errorMessage = False
	
	if request.cookies.get('login') == 'true':
		return redirect(url_for('dashboard'))

	if request.method == 'POST':
		if request.form['Username'] == config.username and request.form['Password'] == config.password:
			resp = make_response( redirect(url_for('dashboard')) )  
			resp.set_cookie("login", 'true')  
			return resp
		else:
			errorMessage = True
			

		
	return render_template('login.html',errorMessage=errorMessage);
	
	
@app.route('/dashboard')
def dashboard():
	import config,sqlite3,base64
	if request.cookies.get('login') == 'true':
		conn = sqlite3.connect(config.path)
		cursor = conn.execute("SELECT TITLE, TIME, CLASS,ID  from BLOG")
		tuple0 = []

		for row in cursor:
			tuple0.append([base64.b64decode(row[0]),row[1],base64.b64decode(row[2]),row[3]])
		
		return render_template('dashboard.html',blog_name=config.blog_name,cursor = tuple0);
	
	return "cuowu",500
	
@app.route('/write',methods=['POST','GET'])
def write():
	import config,sqlite3,markdown2,base64
	if request.method == 'POST':
		if request.form['tit'] != "" and request.form['classification'] != "" and request.form['text'] != "":
			text1 = base64.b64encode(request.form['tit']);
			text2 = base64.b64encode(request.form['classification']);
			text3 = base64.b64encode(request.form['text']);
			text4 = base64.b64encode(markdown2.markdown(request.form['text']));
			conn = sqlite3.connect(config.path);
			sql = "INSERT INTO BLOG (TITLE,TIME,CLASS,TEXT_,MAKEDOWN_TEXT) VALUES ('" +  text1 + "','" + time_now() + "','"  + text2 + "','" + text3 + "','"+ text4 + "')";
			conn.execute(sql);
			conn.commit();
			conn.close();
			return render_template('bianji.html',blog_name=config.blog_name,success = "True");
			
		else:
			return render_template('bianji.html',blog_name=config.blog_name,success = "False");
	
	if request.cookies.get('login') == 'true':
		return render_template('bianji.html',blog_name=config.blog_name,success= "First");
	else:
		return "cuowu",500
		

		
@app.route('/delete/<id>')
def delete(id):
	import config,sqlite3
	conn = sqlite3.connect(config.path)
	conn.execute("DELETE from BLOG where ID=" + id + ";")
	conn.commit()
	conn.close()
		
	return render_template('delete.html',blog_name=config.blog_name,flag = True);
	
	
@app.route('/<fenlei>/<id>')
def wenzhang(fenlei,id):
	import config,sqlite3,base64
	conn = sqlite3.connect(config.path)
	cursor = conn.execute("SELECT TITLE, TIME,MAKEDOWN_TEXT,ID  from BLOG where ID=" +id +";")
	cursor2 = conn.execute("SELECT DISTINCT CLASS  from BLOG")
	tuple0 = []
	tuple2 = []

	for row in cursor:
		tuple0.append([base64.b64decode(row[0]),row[1],base64.b64decode(row[2]),row[3]])
	for row2 in cursor2:
		tuple2.append([base64.b64decode(row2[0])])
		
	return render_template('wenzhang.html',blog_name=config.blog_name,cursor = tuple0,cursor2 = tuple2,url=config.url);
		

@app.route('/<fenlei>/')
def fenlei(fenlei):
	import config,sqlite3,base64
	conn = sqlite3.connect(config.path)
	cursor = conn.execute("SELECT  DISTINCT CLASS  from BLOG")
	cursor2 = conn.execute("SELECT TITLE,ID from BLOG where CLASS='" +  base64.b64encode(fenlei) +"';")
	tuple0 = []
	tuple2 = []

	for row in cursor:
		tuple0.append([base64.b64decode(row[0])])
	for row2 in cursor2:
		tuple2.append([base64.b64decode(row2[0]),row2[1]])
	return render_template('fenlei.html',blog_name=config.blog_name,cursor=tuple0,cursor2=tuple2);

app.wsgi_app = ProxyFix(app.wsgi_app)
if __name__ == "__main__":
	app.run(debug=True)
