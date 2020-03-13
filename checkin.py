#!/usr/bin/python3

import json
import requests
import time

config_json = open('config.json', encoding='utf-8').read()
config = json.loads(config_json)
data_json = open('data.json', encoding='utf-8').read()
data = json.loads(data_json)

url = "http://stuinfo.neu.edu.cn/api/auth/oauth/token?username={0}&grant_type=password&password={1}&imageCodeResult=&imageKey=".format(config['username'], config['password'])
header = {
    "Host": "stuinfo.neu.edu.cn",
    "Authorization": "Basic dnVlOnZ1ZQ==",
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36"
}

url2 = "http://stuinfo.neu.edu.cn/cloud-xxbl/studenLogin"
url3 = "http://stuinfo.neu.edu.cn/cloud-xxbl/getStudentInfo"
url4 = "http://stuinfo.neu.edu.cn/cloud-xxbl/studentinfo"
url5 = "http://stuinfo.neu.edu.cn/cloud-xxbl/updateStudentInfo"

sess = requests.Session()

resp = sess.post(url, data="_t={}".format(int(time.time())), headers=header)

login_data = json.loads(resp.text)

requests.utils.add_dict_to_cookiejar(sess.cookies, {"accessToken": login_data['access_token'], "userName": login_data['userName']})

header['Authorization'] = login_data['token_type'] + " " + login_data['access_token']

resp = sess.post(url2, data="_t={}&username={}&grant_type=password&password={}".format(int(time.time()), config['username'], config['password']), headers=header)

xxbl_tag = json.loads(resp.text)['data']

info_url = url4 + "?tag=" + xxbl_tag

resp = sess.get(info_url, data="", headers=header)

header['Referer'] = info_url
header['X-Requested-With'] = "XMLHttpRequest"

resp = sess.get(url3, data="", headers=header)

last_data = json.loads(resp.text)['data']

for key in data.keys():
    if key in last_data:
        data[key] = last_data[key]

header['Content-Type'] = "application/json"

resp = sess.post(url5+"?t={}".format(int(time.time())), data=json.dumps(data), headers=header)

if resp.status_code == 200 and json.loads(resp.text)['success'] == True:
    print('Success')
else:
    print(resp.status_code)
    print(resp.text)

