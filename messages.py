import requests
import auth
import pymysql
from datetime import datetime
# Connect to the database
connection = pymysql.connect(host='localhost',
                             user='root',
                             password='',
                             db='sms_gateway',
                             cursorclass=pymysql.cursors.DictCursor)
cursor =connection.cursor()

EMAIL=auth.EMAIL
PASSWORD=auth.PASSWORD

# url and parameter API
url="http://smsgateway.me/api/v3/messages"
params={"email":EMAIL,"password":PASSWORD}

# get request & convert json
r=requests.get(url,params)
response=r.json()

cursor.execute("SELECT max(id) as max FROM messages")
id=cursor.fetchone()
# print(type(max))


# get result and filter max id
result=response['result']
filter= [item for item in result if int(item['id'])> id['max']]

if filter:

    for message in filter:
        received_at="0000-00-00 00:00:00"
        sent_at = "0000-00-00 00:00:00"
        created_at=datetime.fromtimestamp(message['created_at']).strftime('%Y-%m-%d %H:%M:%S')
        if(message['sent_at']):
            sent_at=datetime.fromtimestamp(message['sent_at']).strftime('%Y-%m-%d %H:%M:%S')

        if (message['received_at']):
            received_at = datetime.fromtimestamp(message['received_at']).strftime('%Y-%m-%d %H:%M:%S')

        sql="INSERT INTO messages values(%s,%s,'%s','%s','%s','%s','%s','%s','%s')"%(message['id'],message['device_id'],message['message'],message['status'],received_at,sent_at,created_at,message['contact']['name'],message['contact']['number'])

        cursor.execute(sql)
        connection.commit()
        connection.rollback()
else:
    print("cek...")