# -- coding: utf-8 --



#获取脚本文件的当前路径
import sys,os,sqlite3
def cur_file_dir():

     #获取脚本路径

     path = sys.path[0]

     #判断为脚本文件还是py2exe编译后的文件，如果是脚本文件，则返回的是脚本的目录，如果是py2exe编译后的文件，则返回的是编译后的文件路径

     if os.path.isdir(path):

         return path

     elif os.path.isfile(path):

         return os.path.dirname(path)

#打印结果

#打印结果
print cur_file_dir() +"\\test.db"
conn = sqlite3.connect(cur_file_dir() +"\\test.db")


	   
	   

cursor = conn.execute("SELECT id, name, address, salary  from COMPANY")
for row in cursor:
   print "ID = ", row[0]
   print "NAME = ", row[1]
   print "ADDRESS = ", row[2]
   print "SALARY = ", row[3], "\n"

print "Operation done successfully";
	   
conn.close()