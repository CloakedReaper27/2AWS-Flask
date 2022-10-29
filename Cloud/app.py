from ast import JoinedStr
from cgi import test
from cgitb import reset
from http.client import BAD_REQUEST
from multiprocessing.resource_sharer import stop
from flask import Flask,render_template, request ,redirect,Response,flash, url_for
import os
from flask_mysqldb import MySQL
from memcache import *
from time import *
from apscheduler.schedulers.background import BackgroundScheduler
import datetime
# import re

hit = {0 :0}
miss = {0 :0}
requests= {0 :0}
#---------------------------------
Changes = {0:0 ,1:0 ,2:0 ,3:0 ,4:0}


app = Flask(__name__)
app.secret_key = 'dont tell anyone'
#app.run(debug=True, use_reloader=False)
scheduler = BackgroundScheduler()
scheduler.start()

mysql = MySQL(app)
app.config['MYSQL_HOST'] = '3.89.251.158'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'localhost'

def interval_task():
    with app.app_context():
        ct = datetime.datetime.now()
        cursor = mysql.connection.cursor()
        cursor.execute(''' INSERT INTO db_cache_statistic VALUES(%s,%s,%s,%s,%s,%s)''',(len(memory_cache),requests[0],Total_Size(),miss[0],hit[0],ct))
        mysql.connection.commit()
        cursor.close()

def delay_Mins():
    
    with app.app_context():
        # Changes[0] = len(memory_cache)
        # Changes[1] = sys.getsizeof(memory_cache)
        # Changes[2] = requests[0]

        cursor = mysql.connection.cursor()
        cursor.execute(''' Select AVG(No_of_items) AS average from db_cache_statistic ''')
        rows = cursor.fetchall()
        for i in rows:
            Changes[0] = i[0]

        
        cursor.execute(''' Select AVG(TotalSize_of_items) AS average from db_cache_statistic ''')
        rows = cursor.fetchall()
        for i in rows:
            Changes[1] = i[0]

        
        cursor.execute(''' Select AVG(No_of_requests ) AS average from db_cache_statistic ''')
        rows = cursor.fetchall()
        for i in rows:
            Changes[2] = i[0]

        
        cursor.execute(''' Select AVG(Miss_rate) AS average from db_cache_statistic ''')
        rows = cursor.fetchall()
        for i in rows:
            Changes[3] = i[0]

        cursor.execute(''' Select AVG(Hit_rate) AS average from db_cache_statistic ''')
        rows = cursor.fetchall()
        for i in rows:
            Changes[4] = i[0]
            
@app.before_first_request
def before_first_request():
    scheduler.add_job(func=interval_task, trigger="interval", seconds=5)
    scheduler.add_job(func=delay_Mins, trigger="interval", minutes=10)

    cursor = mysql.connection.cursor()
    cursor.execute(''' Select Mem_size from db_cache''')
    rows = cursor.fetchone()
    max_Default[0] = rows[0]*1000000

    cursor.execute(''' Select Algorithm_Chosen from db_cache''')
    rows = cursor.fetchone()
    Algo_Default[0] = rows[0]


#---------------------------------------
@app.route("/")
def home():

    return render_template('index.html')
@app.route("/editmem",methods=["GET", "POST"])
def edit():
        if request.method == 'GET':
                
            return render_template('editmem.html')   
            
        elif request.method == 'POST':

            try:
                if request.form['clear'] == 'clear':
                    x = 0
            except:
                if request.form['submit'] == 'submit':

                    range = request.form['range']
                        
                    if request.form['mem'] == 'Random':
                        x = 0
                            
                    elif request.form['mem'] == 'Least':
                        x = 1
                           
                    max_Default[0] = int(range)*1000000
                    Algo_Default[0] = x
                    
                    cursor = mysql.connection.cursor()
                    cursor.execute(''' UPDATE db_cache SET Algorithm_Chosen = (%s), Mem_size= (%s)  ''',(x,int(range)))
                    mysql.connection.commit()
                    cursor.close()
                    
                    print(max_Default)
                return render_template('editmem.html')
                    
            memory_cache.clear()
            print("Cache cleared!")
            
            
        return render_template('editmem.html')

@app.route("/memcache")
def memcache():

    no = Changes[0]
    size = Changes[1]
    request = Changes[2]
    misses = Changes[3]
    hits = Changes[4]
    
    return render_template('memcache.html', no=no,hits=hits,misses=misses,size=size,request=request)


app.config['IMAGE_UPLOADS'] = "static/images"

path = 0

@app.route("/keys",methods=["GET"])
def viewall():
        if request.method == 'GET':
            
            cur = mysql.connection.cursor() 
            cur.execute('''SELECT `image_key` FROM `images` ''')
            keys = cur.fetchall()
            
        return render_template("keys.html",status=200,keys = keys)
        

@app.route("/item",methods=["GET","POST"])
def search():
    if request.method == 'GET':

        return render_template("item.html")

    if request.method == 'POST':
            key = request.form['key']
            
            if key in memory_cache:
                start_time = time()
                
                path = memory_cache[key]

                LRUs[key] = LRUs[key] + 1.0

                end_time = time()
                
                print((end_time - start_time)*1000000,'ms')
                
                hit[0] = hit[0] + 1
                requests[0] = requests[0] + 1

                zed = 0

            else:
                start_time = time()
                cur = mysql.connection.cursor()
                cur.execute('''SELECT `image_path` FROM `images` WHERE `image_key` = %s''', (key,))
                path = cur.fetchone()
                try:
                    path = ''.join(path)
                except TypeError:
                    invaild = 'Invaild key'
                    return render_template("item.html",Invaild=invaild)
                end_time = time()
                print((end_time - start_time)*1000,'ms')
                LRUs[key] = 1
                miss[0] = miss[0] + 1
                requests[0] = requests[0] + 1
                mem_cache(key,path)
                zed = 1
            
    if zed == 1:
            return render_template("item.html",path=path, CurrentKey=key)
    elif zed == 0:
            return render_template("item.html",img_data=path, CurrentKey=key)
    

@app.route('/display/<filename>')
def display_image(filename):
        
	#print('display_image filename: ' + filename)

	return redirect(url_for('static', filename='images/' + filename))



@app.route("/upload-image",methods=["GET","POST"])

def upload_image():
    if request.method == 'GET':
        return render_template("upload.html")
    
    if request.method == "POST":
        if request.files:
            image = request.files["image"]
            image.save(os.path.join(app.config['IMAGE_UPLOADS'],image.filename ))
            #print(os.path.join(app.config['IMAGE_UPLOADS'],image.filename))

            name = request.form['name']

            cursor = mysql.connection.cursor()
            cursor.execute('''SELECT `image_path` FROM `images` WHERE `image_key` = %s''', (name,))
            path = cursor.fetchone()
            
            try:
                path = ''.join(path)  #Checks if key is already available

            except TypeError:
                cursor = mysql.connection.cursor()
                cursor.execute(''' INSERT INTO images VALUES(%s,%s)''',(name,image.filename))
                mysql.connection.commit()
                cursor.close()

            cursor = mysql.connection.cursor()
            cursor.execute(''' UPDATE images SET image_path = %s WHERE image_key = %s''',(image.filename,name))
            mysql.connection.commit()
            cursor.close()
            if name in memory_cache:
                mem_cache(name,image.filename)
            return redirect(request.url)
            
    

    return render_template("upload.html")



@app.errorhandler(500)
def server_error(e):
    app.logger.error("server error")
    flash("error ! already exists")
    return redirect(request.url)


if __name__ == "__main__":
    app.run(debug=True)


