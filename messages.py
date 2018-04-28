import requests,auth,pymysql,time
from datetime import datetime
# Connect to the database
connection = pymysql.connect(host='localhost',
                             user='root',
                             password='',
                             db='sms_gateway',
                             cursorclass=pymysql.cursors.DictCursor)
cursor =connection.cursor()

# url
url="http://192.168.43.1:8080/v1/sms"

def checkApi():
    r = requests.get(url)
    response = r.json()
    # print(response)
    cursor.execute("SELECT max(id) as max FROM messages")
    id = cursor.fetchone()

    # print(type(id['max']))
    # max=None
    if id['max'] is None :
        max=0
    else:
        max=id['max']
    # # print(type(max))
    #
    # # get result and filter max id
    result = response['messages']
    filter = [item for item in result if int(item['_id']) > max]
    # print(filter)
    #
    if filter:
        for message in filter:
            alert=''
            if (message['msg_box']=='inbox'):
                alert = "Pesan Masuk dari %s" % message['address']
            elif (message['msg_box']=='outbox'):
                # received_at = datetime.fromtimestamp(message['received_at']).strftime('%Y-%m-%d %H:%M:%S')
                alert = "Pesan Terkirim ke %s" % message['address']
            print(alert)

            sql = "INSERT INTO messages values('%s','%s','%s','%s','%s')" % (
            message['_id'], message['address'], message['body'], message['msg_box'],message['sim_slot'])


            cursor.execute(sql)
            connection.commit()
            connection.rollback()
    else:
        print("cek...")
    # time.sleep(5)

# while 1:
checkApi()
# time.sleep(3)