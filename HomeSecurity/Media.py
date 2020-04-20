import os
from twilio.rest import Client
import cv2
from django.templatetags.static import static

#ID AND PASSWORD NEED TO BE ACCESSED FROM TWILIO ACCOUNT
def sms(number,frame):
    ID="AC7cd11ad6fc1857d9b1982c04f766c2b8"
    PASS = "6798b197b8e3e940d63a17fd84ac2add"
    client = Client(ID,PASS)
    directoryold=r'F:\Study\Practise\Security'
    directory = r'F:\Study\Practise\Security\Static\Image'
    os.chdir(directory)
    cv2.imwrite("frame.jpg", frame)
    os.chdir(directoryold)
    from_whatsapp_number = 'whatsapp:+14155238886'
    to_whatsapp_number = 'whatsapp:+91'+number
    print("SENDING SMS")
    client.messages.create(body='Some One has Entered Your property .. Here is an image', media_url='https://intense-stream-64362.herokuapp.com/static/images/rishav.jpg',from_ = from_whatsapp_number ,to= to_whatsapp_number)
