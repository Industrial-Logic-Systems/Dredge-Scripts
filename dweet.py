import json
import requests

import config


def dweet_login():
    url = "https://dweetpro.io:443/v2/users/login"
    if config.env["user"] is None or config.env["pass"] is None:
        config.env["user"] = input("Username: ")
        config.env["pass"] = input("Password: ")

    body = {"username": config.env["user"], "password": config.env["pass"]}
    headers = {
        "Content-type": "application/json",
    }
    body = json.dumps(body)
    result = requests.post(url, data=body, headers=headers)
    j = json.loads(result.text)
    config.env["key"] = j["ILS"]["token"]
    config.save_env(config.env)
    return result


def send_dweet(name, data, attempts=3):
    url = "https://dweetpro.io:443/v2/dweets"
    if config.env["key"] is None:
        dweet_login()
    content = {"thing": name, "content": data}
    headers = {
        "Content-type": "application/json",
        "X-DWEET-AUTH": config.env["key"],
    }
    content = json.dumps(content)
    response = requests.post(url, data=content, headers=headers)
    if "Session has expired, please re-login" in response.text and attempts > 0:
        dweet_login()
        return send_dweet(name, data, attempts - 1)
    return response.text


def get_dweets(name, attempts=3):
    url = "https://dweetpro.io:443/v2/dweets"
    if config.env["key"] is None:
        dweet_login()
    headers = {"X-DWEET-AUTH": config.env["key"]}
    params = {"thing": name}
    response = requests.get(url, params=params, headers=headers)
    if "Session has expired, please re-login" in response.text and attempts > 0:
        dweet_login()
        return get_dweets(name, attempts - 1)
    return response.text


if __name__ == "__main__":
    pass
