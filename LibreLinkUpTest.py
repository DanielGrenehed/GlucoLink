# Created 18/10/2023 by Daniel Amos Grenehed
# based on https://gist.github.com/khskekec/6c13ba01b10d3018d816706a32ae8ab2
import requests

url_base='https://api-eu.libreview.io'
headers={'accept-encoding':'gzip',
         'cache-control':'no-cache',
         'connection':'Keep-Alive',
         'content-type':'application/json',
         'product':'llu.android',
         'version':'4.7'
}

def login(credentials):
    endpoint = url_base + "/llu/auth/login"
    return requests.post(endpoint, json=credentials, headers=headers)

def connections():
    endpoint = url_base + "/llu/connections"
    return requests.get(endpoint, headers=headers)

def gmc_data(pid):
    endpoint = url_base + "/llu/connections/" + str(pid) + "/graph"
    return requests.get(endpoint, headers=headers)


# login
credentials = {"email": str(input("email: ")), "password":str(input("password: "))}
auth_req = login(credentials)
if (auth_req.status_code != 200):
    print(f"Failed to login: (status {req.status_code})\nExiting...")
    exit()
if (auth_req.json()['status'] != 0):
    print(f"login failed: {req.json()['error']['message']}\nExiting...")
    exit()
print(f"\nLogin: {auth_req}")
headers['Authorization'] = f"Bearer {str(auth_req.json()['data']['authTicket']['token'])}"


# get connections
con_req = connections()
if (con_req.status_code != 200):
    print(f"Failed to get connections: (status {con_req.status_code})\nExiting...")
    exit()
if (con_req.json()['status'] != 0):
    print(f"Failed to get connections: {con_req.json()['error']['message']}\nExiting...")
    exit()
print(f"\nConnections: {con_req}")
print(con_req.json()['data'][0])
pid = con_req.json()['data'][0]['patientId']


# get gmc data
gmc_req = gmc_data(pid)
if (gmc_req.status_code != 200):
    print("Failed to read gmc data: (status {gmc_req.status_code})\nExiting...")
    exit()
if (gmc_req.json()['status'] != 0):
    print(f"GMC retrieval failed: {gmc_req.json()['error']['message']}\nExiting...")
    exit()
print(f"\nGMC data: {gmc_req}")
print(gmc_req.json())
