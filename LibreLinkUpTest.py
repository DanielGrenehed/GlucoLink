# Created 18/10/2023 by Daniel Amos Grenehed
# based on https://gist.github.com/khskekec/6c13ba01b10d3018d816706a32ae8ab2
import requests

url_base='https://api-eu.libreview.io'
headers={'accept-encoding':'gzip','cache-control':'no-cache','connection':'Keep-Alive','content-type':'application/json','product':'llu.android','version':'4.7'}

def login(data):
    endpoint = url_base + "/llu/auth/login"
    return requests.post(endpoint, json=data, headers=headers)

def connections(auth, data):
    endpoint = url_base + "/llu/connections"
    return requests.get(endpoint, headers=headers)

def gmc_data(pid):
    endpoint = url_base + "/llu/connections/" + str(pid) + "/graph"
    return requests.get(endpoint, headers=headers)


data = {"email": str(input("email: ")), "password":str(input("password: "))}
req = login(data)

if (req.status_code != 200):
    print(f"Failed to login: (status {req.status_code})\nExiting...")
    exit()

if (req.json()['status'] != 0):
    print(f"login failed: {req.json()['error']['message']}\nExiting...")
    exit()

print(f"\nLogin: {req}")
json = req.json()
auth = str(json['data']['authTicket']['token'])

headers['Authorization'] = f"Bearer {auth}"
pats = connections(auth, data)

if (pats.status_code != 200):
    print(f"Failed to get connections: (status {pats.status_code})\nExiting...")
    exit()
if (pats.json()['status'] != 0):
    print(f"Failed to get connections: {pats.json()['error']['message']}\nExiting...")
    exit()

pson = pats.json()
print(f"\nConnections: {pats}")
print(pson['data'][0])
pid = pson['data'][0]['patientId']

dat = gmc_data(pid)
if (dat.status_code != 200):
    print("Failed to read gmc data: (status {dat.status_code})\nExiting...")
    exit()
if (dat.json()['status'] != 0):
    print(f"GMC retrieval failed: {dat.json()['error']['message']}\nExiting...")
    exit()

print(f"\nGMC data: {dat}")
print(dat.json())
