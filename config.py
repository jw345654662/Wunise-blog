# -- coding: utf-8 --

username = "123"
password = "123"

blog_name = u"王小智的个人Blog"

db_path = "blog.db"

url = "http://blog.wunise.com"

#评论框请访问多说获取 http://duoshuo.com/ 注意第二行的改动 其他部分与多说提供的代码一致
comment_box = '''
<!-- 多说评论框 start -->
	<div class="ds-thread" data-thread-key="{{ id }}" data-title="{{ title }}" data-url="{{ url }}/{{ title }}/{{ id }}"></div>
<!-- 多说评论框 end -->
<!-- 多说公共JS代码 start (一个网页只需插入一次) -->
<script type="text/javascript">
var duoshuoQuery = {short_name:"wangxiaozhi"};
	(function() {
		var ds = document.createElement('script');
		ds.type = 'text/javascript';ds.async = true;
		ds.src = (document.location.protocol == 'https:' ? 'https:' : 'http:') + '//static.duoshuo.com/embed.js';
		ds.charset = 'UTF-8';
		(document.getElementsByTagName('head')[0] 
		 || document.getElementsByTagName('body')[0]).appendChild(ds);
	})();
	</script>
<!-- 多说公共JS代码 end -->
'''
















import sys,os,sqlite3
import platform
def cur_file_dir():

     #获取脚本路径

     path = sys.path[0]

     #判断为脚本文件还是py2exe编译后的文件，如果是脚本文件，则返回的是脚本的目录，如果是py2exe编译后的文件，则返回的是编译后的文件路径

     if os.path.isdir(path):

         return path

     elif os.path.isfile(path):

         return os.path.dirname(path)


if platform.system() == "Windows":
	path = cur_file_dir() +"\\db\\blog.db"
	comment_box_path = cur_file_dir() + "\\templates\\comment.html"
else:
	path = cur_file_dir() +"/db/blog.db"
	comment_box_path = cur_file_dir() + "/templates/comment.html"





if __name__ == "__main__":
	if platform.system() == "Windows":
		conn = sqlite3.connect(path)
		
	else:
		conn = sqlite3.connect(path)
		
			
	conn.execute('''CREATE TABLE BLOG(
	   			ID 				INTEGER PRIMARY KEY AUTOINCREMENT,
				TITLE           TEXT    NOT NULL,
				TIME			TEXT	NOT NULL,
				CLASS           TEXT    NOT NULL,
				TEXT_        	TEXT	NOT NULL,
				MAKEDOWN_TEXT	TEXT	NUT NULL);''')
				
	conn.commit()
	conn.close()

	f=open(comment_box_path,'w') 
	f.write("{% macro output(url, id, title) -%}" + comment_box + "{%- endmacro %}")
	f.close()
				

