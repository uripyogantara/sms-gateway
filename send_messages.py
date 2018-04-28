import requests

url="http://192.168.43.1:8080/v1/sms"

phone = input("Masukan Nomor Telepon ")
message = input("Masukan Pesan Anda ")
params={
    "phone":phone,
    "message":message,
}
r=requests.post(url,params)
# response = r.json()
print(r)