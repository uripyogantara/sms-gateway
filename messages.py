import requests,pymysql,time

# Connect to the database
connection = pymysql.connect(host='localhost',
                             user='root',
                             password='',
                             db='sms_gateway',
                             cursorclass=pymysql.cursors.DictCursor)
cursor =connection.cursor()

# url
# url="http://192.168.43.1:8080/v1/sms"

def checkApi(device):
    print("cek device %s.." % device['id'])
    url="http://"+device['ip_address']+"/v1/sms"
    # print(type(url))
    r = requests.get(url)
    response = r.json()
    # print(response)
    sql="SELECT max(id_message) as max FROM inbox where received_by=%s"%device['id']
    # # print(url)
    cursor.execute(sql)
    # # return
    id = cursor.fetchone()
    # #
    # # # print(type(id['max']))
    # # # max=None
    if id['max'] is None :
        max=0
    else:
        max=id['max']
    # # print(type(max))
    #
    # # get result and filter max id
    result = response['messages']
    filter = [item for item in result if int(item['_id']) > max and item['msg_box']=='inbox']
    if filter:
        for message in filter:
            alert=''
            if (message['msg_box']=='inbox'):
                alert = "Pesan Masuk dari %s" % message['address']
            elif (message['msg_box']=='outbox'):
                alert = "Pesan Terkirim ke %s" % message['address']
            print(alert)

            # print(message)

            sql = 'INSERT INTO inbox values(null,"%s","%s","%s","%s")' % (
            message['_id'], device['id'],message['address'], message['body'])

            # print(sql)
            cursor.execute(sql)
            connection.commit()
            connection.rollback()
    else:
        print("tidak ada pesan masuk di %s"%device['id'])
def selectDevice():
    sql="select * from device"
    cursor.execute(sql)
    devices=cursor.fetchall()
    # print(device)
    for device in devices:
        checkApi(device)
    connection.rollback()
while 1:
    selectDevice()
    # checkApi()
    time.sleep(3)