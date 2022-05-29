import requests
import json

config = json.load(open('config.json', 'r'))


def get_key_from_dc(user_id):
    endpoint = "https://cordify.app/api/get-verified-key"
    payload = {"DiscordID": user_id}
    response = requests.post(endpoint, json=payload)
    if response.status_code == 200:
        verified_key = response.json()["verifiedKey"]
        return verified_key
    else:
        print(f"Error: {response.status_code}\n{response.json()}")
        return None


def holds_weeblet_dao(publicKey):
    # verified_key = "BC1YLhF5DHfgqM7rwYK8PVnfKDmMXyVeQqJyeJ8YGsmbVb14qTm123G"
    dao_endpoint = "https://diamondapp.com/api/v0/is-hodling-public-key"
    dao_payload = {
        "PublicKeyBase58Check": publicKey,
        "IsHodlingPublicKeyBase58Check": config["weebletDAO"],
        "IsDAOCoin": True
    }
    dao_response = requests.post(dao_endpoint, json=dao_payload)
    if dao_response.status_code == 200:
        res_json = dao_response.json()
        amt_hodl = res_json["BalanceEntry"]["BalanceNanos"]
        if amt_hodl > 0:
            return True
        else:
            return False
    else:
        print(dao_response.status_code, dao_response.json())
        return False


def get_bulk_keys(idlist):
    endpoint = "https://cordify.app/api/get-verified-key"
    payload = {"DiscordIDList": idlist}
    res = requests.post(endpoint, json=payload)
    if res.status_code == 200:
        return res.json()
    else:
        print(res.status_code, res.text)
        return []