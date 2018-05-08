import requests

import requests,pymysql,time

# Connect to the database
connection = pymysql.connect(host='localhost',
                             user='root',
                             password='',
                             db='sms_gateway',
                             cursorclass=pymysql.cursors.DictCursor)
cursor =connection.cursor()

def send():
    sql ="SELECT outbox.`id`,device.`ip_address`,outbox.`address`,outbox.`body` FROM outbox INNER JOIN device ON device.`id`=outbox.`sent_by` WHERE outbox.`status`=1"
    cursor.execute(sql)
    outboxes=cursor.fetchall()

    for outbox in outboxes:
        params={
            "phone":outbox['address'],
            "message":outbox['body'],
        }

        url = "http://" + outbox['ip_address'] + "/v1/sms"
        print("send to %s"%outbox['address'])
        r=requests.post(url,params)
        print(r)
        sql_update="update outbox set status=0 where id=%s"%outbox['id']
        cursor.execute(sql_update)
        connection.commit()
        # print(sql_update)
    connection.rollback()

while 1:
    send()
    # checkApi()
    print("cek")
    time.sleep(3)
