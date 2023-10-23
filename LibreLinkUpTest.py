# Created 18/10/2023 by Daniel Amos Grenehed
# based on https://gist.github.com/khskekec/6c13ba01b10d3018d816706a32ae8ab2
import requests

def save_file(filename, data):
    f = open(filename, "w")
    f.write(str(data))
    f.close()

def format_json(json):
    s = str(json)
    out = ""
    indent_s = ""
    is_str = False
    skip = False
    for i in range(0, len(s)):
        if skip:
            skip = False
            continue
        c = s[i]
        if c == '\'':
            is_str = not is_str
        if not is_str:
            if s[i:i+2] == '{}' or s[i:i+2] == '[]':
                out += s[i:i+2]
                skip = True
                continue
            elif c == '{' or c == '[':
                indent_s += '\t'
                out += c + '\n' + indent_s
            elif c == '}' or c == ']':
                indent_s = indent_s[:-1]
                out += '\n' + indent_s + c
            elif c == ',':
                out += c + '\n' + indent_s
                if s[i+1] == ' ':
                    skip = True
            else:
                out += c
        else:
            out += c
    return out

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

def handle_response(response, tag):
    if (response.status_code != 200):
        print(f"{tag} failed: (status {response.status_code})\nExiting...")
        exit()
    if (response.json()['status'] != 0):
        print(f"{tag} failed: {response.json()['error']['message']}\nExiting...")
        exit()

# login
credentials = {"email": str(input("email: ")), "password":str(input("password: "))}
auth_req = login(credentials)
handle_response(auth_req, "login")
print(f"\nLogin: {auth_req}")
headers['Authorization'] = f"Bearer {str(auth_req.json()['data']['authTicket']['token'])}"
save_file("login.json", format_json(auth_req.json()))

# get connections
con_req = connections()
handle_response(con_req, "Get connections")
print(f"\nConnections: {con_req}")
print(con_req.json()['data'][0])
pid = con_req.json()['data'][0]['patientId']
save_file("connections.json", format_json(con_req.json()))


# get gmc data
gmc_req = gmc_data(pid)
handle_response(gmc_req, "Get GMC data")
print(f"\nGMC data: {gmc_req}")
print(gmc_req.json())
save_file("gmc.json", format_json(gmc_req.json()))
