from flask import Flask, redirect
# from dotenv import load_dotenv
# import os
import json


# load_dotenv()


def get_ips():
    json_fstr = {}


    # dowload first the json_file from s3

    with open('config.json', 'r') as file:
        doc = file.read()
        json_fstr = json.loads(doc)

    return json_fstr['IP_LIST'], json_fstr['IP_PORT']


IP_LIST, PORT = get_ips()
IP_POS = 0

app = Flask(__name__)


@app.route("/", defaults={"path": ""}, methods=['GET', 'POST'])
@app.route("/<path:path>", methods=['GET', 'POST'])
def catch_all(path):
    global IP_POS

    new_url = f"http://{IP_LIST[IP_POS]}:{PORT}/{path}"
    IP_POS = (IP_POS + 1) % len(IP_LIST)

    return redirect(new_url, code=302)


if __name__ == "__main__":
    app.run(port=8080)
