from flask import Flask, redirect
from dotenv import load_dotenv
import os
import json


load_dotenv()


def get_ips():
    json_fstr = {'IP_LIST': []}

    with open(os.getenv('IP_LIST_PATH'), 'r') as file:
        doc = file.read()
        json_fstr = json.loads(doc)

    return json_fstr['IP_LIST']


IP_LIST = get_ips()
IP_POS = 0
PORT = os.getenv("IP_PORT")

app = Flask(__name__)


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def catch_all(path):
    global IP_POS

    new_url = f"{IP_LIST[IP_POS]}:{PORT}/{path}"
    IP_POS = (IP_POS + 1) % len(IP_LIST)

    return redirect(new_url, code=302)


if __name__ == "__main__":
    app.run()
