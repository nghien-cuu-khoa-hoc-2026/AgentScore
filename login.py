import requests
import getpass

login_url = "https://mobile.oneuni.com.vn/AUTH/connect/token?"
def login(username, password):
    payload = {
        "url_uni": "https://sinhvien.huce.edu.vn/AppSVGV/",
        "username": username + "2HUCE",
        "password": password,
        "client_secret": "LcC4X5PeQ<MiQ;L",
        "grant_type": "password",
        "client_id": "mobile_flutter",
        "scope": "offline_access openid"
    }
    headers = {
        "accept": "application/json",
        "user-agent": "Dart/3.0 (dart:io)"

    }
    response = requests.post(login_url, data=payload, headers=headers)
    response.raise_for_status()
    data = response.json()
    return data["access_token"]

# if __name__ == "__main__":
#     username = input("Username: ")
#     password = getpass.getpass("Password: ")

#     token = login(username, password)
#     print(token)


