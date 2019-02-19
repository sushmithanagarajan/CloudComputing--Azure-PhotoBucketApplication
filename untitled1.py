

import  pymysql.cursors
import glob
import os
import time
import datetime
from PIL import Image
import cStringIO
import pymysql
from azure.storage.blob import PublicAccess
from flask import Flask
from azure.storage.blob import BlockBlobService
from azure.storage.blob import ContentSettings
from flask import render_template
from flask import request


hostname = ''
username = 'e'
password = ''
database = 'q'
myConnection = pymysql.connect( host=hostname, user=username, passwd=password, db=database, cursorclass=pymysql.cursors.DictCursor, local_infile=True)

print 'DB connected'

block_blob_service = BlockBlobService(account_name='', account_key='')
print ('Blob connected')

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
print(APP_ROOT)

app = Flask(__name__)

@app.route('/')
def main():
    print "Welcome to the PhotoSharing Application"
    return render_template('Welcome.html')

@app.route('/Upload',methods=['get','post'])
def Upload():
    global author_name
    author_name = request.form['username']
    print author_name
    return render_template('Upload.html' , value = author_name)

@app.route('/uploadImage',methods=['get','post'])
def upload1():
    f = request.files['upload_files']
    file_name = f.filename
    print (file_name)
    titlename = request.form['file']
    print (titlename)
    newfile = "C:/Users/Sushmitha Nagarajan/Desktop/pictures/" + file_name
    print newfile
    app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024
    Timedetails = time.strftime("%a, %d %b %Y %H:%M:%S")
    print Timedetails
    block_blob_service.create_blob_from_path('containerone',file_name,newfile,content_settings=ContentSettings(content_type='image/png'))
    imgUrl = 'https://cs2ffbaxb13.blob.core.windows/' + file_name
    rating = '0'
    avgrating = '0'
    peoplecount = '0'
    insertQuery = "insert into PhotoUpload9 values ('" + newfile + "','" + imgUrl +"','" + Timedetails +"','" + titlename +"','" + author_name +"','" + rating +"','" + avgrating +"')"
    print insertQuery
    cur = myConnection.cursor()
    cur.execute(insertQuery)
    myConnection.commit()
    cur.close()
    return insertQuery

@app.route('/DisplayImage',methods=['get','post'])
def view():
    query = "select * from PhotoUpload9"
    cur = myConnection.cursor()
    cur.execute(query)
    res = cur.fetchall()
    myConnection.commit()
    cur.close()
    return render_template('Display.html', img=res)

@app.route('/post_field',methods=['get','post'])
def need_input():
    for key, value in request.form.items():
        print("key: {0}, value: {1}".format(key, value))
    global peoplecount
    updateQuery = "update PhotoUpload9 set rating ='" + key + "'where Timedetails ='" + value + "'"
    cur = myConnection.cursor()
    cur.execute(updateQuery)
    myConnection.commit()
    cur.close()
    print updateQuery





if __name__ == '__main__':
    app.run(debug=True)

