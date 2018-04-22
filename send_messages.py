import requests,auth,pymysql,time

EMAIL=auth.EMAIL
PASSWORD=auth.PASSWORD
DEVICE=86921

url="http://smsgateway.me/api/v3/messages/send"
params={
    "email":EMAIL,
    "password":PASSWORD,
    "device":DEVICE,
    "number":"+628539301350",
    "message":"tes tes tes",
}
r=requests.post(url,params)
response = r.json()

print(response)