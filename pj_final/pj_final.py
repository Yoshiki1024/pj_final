import cv2
import os
import sys
import datetime
import numpy as np
import smtplib
from smtplib import SMTP
import ssl
import paho.mqtt.client as mqtt
import json
import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication


TOKEN = "token_2v96bmbNZevNy148"
HOSTNAME = "mqtt.beebotte.com"
PORT = 8883
TOPIC = "raspberrypi/action"
CACERT = "mqtt.beebotte.com.pem"

# Outlook設定
my_account = 't815072@st.pu-toyama.ac.jp'
my_password = 'yui1024'

#ヘッダーの追加，定型メールの作成
def add_header():
    body = "メールの本文"
    msg = MIMEMultipart()
    msg['Subject'] = "部屋の利用状況"
    msg['To'] = 't815072@st.pu-toyama.ac.jp'
    msg['From'] = 't815072@st.pu-toyama.ac.jp '
    #ここで，nowimageを読み込んでいる？？
    with open("/Users/rum/Desktop/pj_final/pj_final/nowimage.jpg","rb") as f:
        attachment = MIMEApplication(f.read())
    attachment.add_header("Content-Disposition", "attachment", filename="nowimage.jpg")
    msg.attach(MIMEText(body))
    msg.attach(attachment)
    return msg

#



def on_connect(client, userdata, flags, respons_code):
    print('status {0}'.format(respons_code))
    client.subscribe(TOPIC)
    print('connect')

# メッセージが届いたときの処理
def on_message(client, userdata, msg):
  # msg.topicにトピック名が，msg.payloadに届いたデータ本体が入っている
  print("Received message '" + str(msg.payload) + "' on topic '" + msg.topic + "' with QoS " + str(msg.qos))
  save_frame_camera_cycle(0, 'data/temp', 'camera_capture_cycle', 20)
  os.execl(sys.executable, sys.executable, *sys.argv)


def save_frame_camera_cycle(device_num, dir_path, basename, cycle, ext='jpg', delay=1, window_name='frame'):
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        return
    n = 0
    k = 0
    while True:
        ret, frame = cap.read()
        cv2.imshow("window_name", frame)
        if cv2.waitKey(delay) & 0xFF == ord('q'):
            break
        if n == cycle:
            n = 0
            #cv2.imwrite('originalimage.jpg',frame)
            cv2.imwrite("nowimage.jpg", frame)
            img = cv2.imread("nowimage.jpg", 1)
            #画像情報のメールを送る
            smtp_obj = smtplib.SMTP('smtp.office365.com', 587)
            smtp_obj.starttls()
            smtp_obj.login('t815072@st.pu-toyama.ac.jp', 'yui1024')
            print('メールをおくりました。確認してください。')
            cap.release()
            cv2.destroyAllWindows()
            break
         

        n += 1
    
    #key = cv2.waitKey(1)

   
    # Escキーを入力されたら画面を閉じる
    #if key == 27:
       # break

    

#main関数
def main():
    client = mqtt.Client()
    client.username_pw_set("token:%s"%TOKEN)
    client.on_connect = on_connect
    client.on_message = on_message
    client.tls_set(CACERT)
    client.connect(HOSTNAME, port=PORT, keepalive=60)
    client.loop_forever()
if __name__ == '__main__':
    main()
   



