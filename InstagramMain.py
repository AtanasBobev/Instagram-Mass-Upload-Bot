from instabot import Bot 
from skimage.io import imread_collection
from glob import glob
from win10toast import ToastNotifier
import random
import json
import os
import urllib.request
import time
import requests
import smtplib
import smtplib
from tkinter import *

num=0
window = Tk()
window.title("Photos Uploaded")
window.iconbitmap("Instagram/Instagram.ico")
lbl = Label(window, text=num, font=("Arial Bold", 100))
lbl.grid(column=0, row=0)
window.update()

def url_ok(url):
    r = requests.head(url)
    return r.status_code == 200

 
def sendMessage(Num):
    gmail_user = 'email'
    gmail_password = 'email_password'
    sent_from = gmail_user
    to = ['recipient_email']
    subject = 'Upload Count'
    body = "Upload Count"
    email_text = Num
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(sent_from, to, email_text)
        server.close()
    except:
        print("Could not send a push-notification!")

with open("Instagram/NumberOfImagesUploaded.txt", "r") as f:
   num = int(float(f.read()))

def ChangeNum(n):
    num=n
    with open("Instagram/NumberOfImagesUploaded.txt", "w") as f:
        f.write(str(int(n)))

links=[]
r=''
with open(os.path.abspath("Instagram/Data/links.txt"), 'r') as filehandle:
    for line in filehandle:
        currentPlace = line[:-1]
        links.append(currentPlace)
print("Started at: " +time.ctime()+" with a list of "+str(len(links))+" links.")
def GetImage():
    r = requests.get('https://source.unsplash.com/featured/3840x2160')
    while r.url == "https://images.unsplash.com/source-404?fit=crop&fm=jpg&h=800&q=60&w=1200":
        print("API requests are over capita! Waiting one hour. Continuing at "+str(time.ctime(time.time() + 3600)+"..."))
        time.sleep(3600)
        print("Trying again... "+time.ctime())
        r = requests.get('https://source.unsplash.com/featured/3840x2160')
    try:
        urllib.request.urlretrieve(str(r.url), os.path.abspath("Instagram/media")+"\\"+str(random.randrange(1,10000))+".jpg")
    except:
        print("API requests are over capita! Waiting in 10 hours. Continuing at "+str(time.ctime(time.time() + 36000)+"..."))
        time.sleep(36000)
        urllib.request.urlretrieve(str(r.url), os.path.abspath("Instagram/media")+"\\"+str(random.randrange(1,10000))+".jpg")
    while r.url in links:
        r = requests.get('https://source.unsplash.com/featured/3840x2160')
   
    links.append(r.url)
    with open(os.path.abspath("Instagram/Data/links.txt"), 'w') as filehandle:
        for listitem in links:
            filehandle.write('%s\n' % listitem)
GetImage()
print("Backup image loaded at: " +time.ctime())
toast = ToastNotifier()
col_dir =os.path.abspath("Instagram/media")+"\\"+("*.jpg")
col = glob(col_dir)
print(col_dir)
with open(os.path.abspath("Instagram/Data/quotes.json")) as f:
  data = json.load(f)
def getQuote():
    quote = random.choice(data)
    return ('"'+quote['text']+'" - '+quote['author']+" \n\n Follow us for more! \n \n #photography #travelphotography #naturephotography #streetphotography #foodphotography #portraitphotography #photographylovers #landscapephotography #weddingphotography #blackandwhitephotography #filmphotography #canonphotography #fashionphotography #mobilephotography #photographyislife #nikonphotography #photographyeveryday #photographylover #photographysouls #architecturephotography #photographyislifee #wildlifephotography #nightphotography #iphonephotography #macrophotography #urbanphotography #bnwphotography #analogphotography #dogphotography #photographylife")
print(getQuote())
bot = Bot() 
bot.login(username = "Instagram_Username",  password = "Instagram_Password")
def upload(path): 
    bot.upload_photo(path, caption="Follow for more!")
    toast.show_toast("Notification",str(num)+" images are uploaded",duration=300,threaded=True)
    print(str(num)+" images are uploaded")
    print("----------------------------------")
    try:
        os.remove(os.path.join(os.getcwd(), path+""))
    except:
        os.remove(os.path.join(os.getcwd(), path+".REMOVE_ME"))
while True:
    GetImage()
    col = glob(col_dir)
    ranTime=random.randrange(1800,3600)
    print("Images in stack: "+str(col))
    print("Waiting 30 to 60 minutes. Resuming at "+str(time.ctime(time.time() + ranTime)))
    #time.sleep(ranTime)
    print("Upload sequence has begun...")
    lbl.configure(text=num)
    window.update()
    if num % 50 == 0:
        sendMessage(str(num)+" images uploaded.")
    for i in col:
        num+=1
        lbl.configure(text=num)
        window.update()
        ChangeNum(num)
        upload(i)
        imageDir = os.listdir(os.getcwd())
        for item in imageDir:
            if item.endswith(".REMOVE_ME"):
                os.remove(os.path.join(os.getcwd(), item))