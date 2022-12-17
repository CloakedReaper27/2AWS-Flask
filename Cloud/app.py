from ast import JoinedStr
from cgi import test
from cgitb import reset
from http.client import BAD_REQUEST
from multiprocessing.resource_sharer import stop
from flask import Flask,render_template, request ,redirect,Response,flash, url_for
import os
from flask_mysqldb import MySQL
from memcache import *
from S3 import *
from time import *
from apscheduler.schedulers.background import BackgroundScheduler
import datetime
from EC2 import *

# import re
name = ['','','','','','']
name1 = ['','','','','','']
name2 = ['','','','','','']
name3 = ['','','','','','']
name4 = ['','','','','','']
workers = ['','','','','','']
hit = {0 :0}
miss = {0 :0}
requests= {0 :0}
arrow = [1]
arrow[0] = 0
#---------------------------------
# Changes = {0:'' ,1:'' ,2:'' ,3:'' ,4:''}
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.secret_key = 'dont tell anyone'
#app.run(debug=True, use_reloader=False)
scheduler = BackgroundScheduler()
scheduler.start()

mysql = MySQL(app)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'website'

def interval_task():
    with app.app_context():
        ct = datetime.datetime.now()
        cursor = mysql.connection.cursor()
        cursor.execute(''' INSERT INTO db_cache_statistic VALUES(%s,%s,%s,%s,%s,%s)''',(len(memory_cache),requests[0],Total_Size(),miss[0],hit[0],ct))
        mysql.connection.commit()
        cursor.close()

def ThirtyMins():
    with app.app_context():
        

        if (arrow[0] == 0):
            name[0] = len(memory_cache)
            name[1] = requests[0]
            name[2] = Total_Size()/100000
            name[3] = miss[0]
            name[4] = hit[0]
            name[5] = Max[0]

        elif (arrow[0] == 1):
            name1[0] = len(memory_cache)
            name1[1] = requests[0]
            name1[2] = Total_Size()/100000
            name1[3] = miss[0]
            name1[4] = hit[0]
            name1[5] = Max[0]

        elif (arrow[0] == 2):
            name2[0] = len(memory_cache)
            name2[1] = requests[0]
            name2[2] = Total_Size()/100000
            name2[3] = miss[0]
            name2[4] = hit[0]
            name2[5] = Max[0]

        elif (arrow[0] == 3):
            name3[0] = len(memory_cache)
            name3[1] = requests[0]
            name3[2] = Total_Size()/100000
            name3[3] = miss[0]
            name3[4] = hit[0]
            name3[5] = Max[0]

        elif (arrow[0] == 4):
            name4[0] = len(memory_cache)
            name4[1] = requests[0]
            name4[2] = Total_Size()/100000
            name4[3] = miss[0]
            name4[4] = hit[0]
            name4[5] = Max[0]

        elif (arrow[0] >= 5):
            for e in name:
                name[e]=name1[e]
                name1[e]=name2[e]
                name1[e]=name2[e]
                name2[e]=name3[e]
                name3[e]=name4[e]
                
            name4[0] = len(memory_cache)
            name4[1] = requests[0]
            name4[2] = Total_Size()/100000
            name4[3] = miss[0]
            name4[4] = hit[0]
            name4[5] = Max[0]
        
        arrow[0] = arrow[0] + 1
        print("ticked!")
#==================================
#Displays Current active instances and thier IDs


@app.before_first_request
def before_first_request():
    scheduler.add_job(func=interval_task, trigger="interval", seconds=5)
    scheduler.add_job(func=ThirtyMins, trigger="interval", seconds=10)

    cursor = mysql.connection.cursor()
    cursor.execute(''' Select Mem_size from db_cache''')
    rows = cursor.fetchone()
    max_Default[0] = rows[0]*1000000

    cursor.execute(''' Select Algorithm_Chosen from db_cache''')
    rows = cursor.fetchone()
    Algo_Default[0] = rows[0]

    mysql.connection.commit()
    cursor.close()

    

#---------------------------------------
@app.route("/")
def home():

    return render_template('upload.html')

#=======================================
# App manager Page

@app.route("/Appmanager",methods=["GET", "POST"])
def edit():
        if request.method == 'GET': 

            return render_template('Appmanager.html',CurrentNum = Max[0], name = name
            , name1 = name1, name2 = name2, name3 = name3, name4 = name4,numofworkers = Max[0])   
            
        elif request.method == 'POST':

            try:
                if request.form['grow'] == 'grow':
 
                        create_EC2_Instance()

                        no = Max[0]
                        return render_template('Appmanager.html',CurrentNum = no)

            except:
                try:
                    if request.form['shrink'] == 'shrink':

                        terminate_EC2_Instance()

                        no = Max[0]
                        return render_template('Appmanager.html',CurrentNum = no)
                
                except:
                    try:
                        if request.form['clear'] == 'clear cache':
                            memory_cache.clear()
                            print("Cache cleared!")
                            
                    except:
                        try:
                            if request.form['clear2'] == 'clear images':

                                cursor = mysql.connection.cursor()
                                cursor.execute(''' DELETE FROM images ''')
                                mysql.connection.commit
                                print(cursor.rowcount, "record(s) deleted")
                                cursor.close()

                                print("Images cleared!")

                                delete_all_from_bucket ()
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
  
        return render_template('Appmanager.html',CurrentNum = Max[0])

#=============================

# Statictics Page

# @app.route("/memcache")
# def memcache():

#     no = Changes[0]
#     size = Changes[1]
#     request = Changes[2]
#     misses = Changes[3]
#     hits = Changes[4]
    
#     return render_template('memcache.html', no=no,hits=hits,misses=misses,size=size,request=request)


# app.config['IMAGE_UPLOADS'] = "static/images"

path =  0

#=============================

# List of Keys Page

@app.route("/keys",methods=["GET"])
def viewall():
        if request.method == 'GET':
            
            cur = mysql.connection.cursor() 
            cur.execute('''SELECT `image_key` FROM `images` ''')
            keys = cur.fetchall()
            
        return render_template("keys.html",status=200,keys = keys)
        
#=============================

# Get image Page

@app.route("/item",methods=["GET","POST"])
def search():
    if request.method == 'GET':

        return render_template("item.html")

    if request.method == 'POST':
            key = request.form['key']
            
            if key in memory_cache:
                # start_time = time()
                
                path = memory_cache[key]

                LRUs[key] = LRUs[key] + 1.0

                # end_time = time()
                
                # print((end_time - start_time)*1000000,'ms')
                
                hit[0] = hit[0] + 1
                requests[0] = requests[0] + 1

                zed = 0

            else:
                # start_time = time()
                cur = mysql.connection.cursor()
                cur.execute('''SELECT `image_path` FROM `images` WHERE `image_key` = %s''', (key,))
                path = cur.fetchone()
                
                try:
                    path = ''.join(path)
                except TypeError:
                    invaild = 'Invaild key'
                    return render_template("item.html",Invaild=invaild)

                path = download_file_from_bucket(path)
                
                # end_time = time()
                # print((end_time - start_time)*1000,'ms')
                LRUs[key] = 1
                miss[0] = miss[0] + 1
                requests[0] = requests[0] + 1
                mem_cache(key,path)
                zed = 0
            
    if zed == 1:
            return render_template("item.html",path=path, CurrentKey=key)
    elif zed == 0:
            return render_template("item.html",img_data=path, CurrentKey=key)

#=============================

# App Manager Page

# @app.route("/Appmanager", methods=["GET"])
# def AppManager():
#     if request.method == 'GET':
#         return render_template('Appmanager.html')

#=============================

@app.route('/display/<filename>')
def display_image(filename):
        
	#print('display_image filename: ' + filename)

	return redirect(url_for('static', filename='images/' + filename))

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#=============================

# Upload image Page

@app.route("/upload-image",methods=["GET","POST"])

def upload_image():
    if request.method == 'GET':
        return render_template("upload.html")
    
    if request.method == "POST":
        check = 0
        if request.files:
            image = request.files["image"]
            if image and allowed_file(image.filename):

                upload_to_aws(image, image.filename)


                # image.save(os.path.join(app.config['IMAGE_UPLOADS'],image.filename ))
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
                    flash("Image uploaded successfully.")
                    check = 1

                if (check != 1):
                    
                    delete_file_from_bucket(path)
                    cursor = mysql.connection.cursor()
                    cursor.execute(''' UPDATE images SET image_path = %s WHERE image_key = %s''',(image.filename,name))
                    mysql.connection.commit()
                    cursor.close()
                    flash("Image updated successfully.")
                    check = 0
                    if name in memory_cache:
                        
                        image = download_file_from_bucket(image.filename)
                        mem_cache(name,image)

                    
                    return redirect(request.url)

            else:
                flash("Please enter a vaild image.")
    

    return render_template("upload.html")



@app.errorhandler(500)
def server_error(e):
    app.logger.error("server error")
    flash("error ! already exists")
    return redirect(request.url)


if __name__ == "__main__":
    app.run(debug=True)


