from flask import Flask, redirect, abort
import json
import boto3
import requests


def get_ips():
    json_fstr = {}
    s3 = boto3.client('s3')

    bucket_name = 'hs.ds'
    file_key = 'config.json'
    local_file_path = 'config.json'

    s3.download_file(bucket_name, file_key, local_file_path)

    with open(local_file_path, 'r') as file:
        doc = file.read()
        json_fstr = json.loads(doc)

    return json_fstr['IP_LIST'], json_fstr['IP_PORT']


IP_LIST, PORT = get_ips()
IP_POS = 0
MAX_IT = 10 * len(IP_LIST)


app = Flask(__name__)


@app.route("/", defaults={"path": ""}, methods=['GET', 'POST'])
@app.route("/<path:path>", methods=['GET', 'POST'])
def catch_all(path):
    global IP_POS

    counter = 0
    while counter < MAX_IT:
        url_i = f"http://{IP_LIST[IP_POS]}:{PORT}/v1/healthcheck"
        response = requests.get(url_i)

        if response.status_code == 200:
            break
        else:
            counter += 1
            IP_POS = (IP_POS + 1) % len(IP_LIST)

    if counter < MAX_IT:
        new_url = f"http://{IP_LIST[IP_POS]}:{PORT}/{path}"
        IP_POS = (IP_POS + 1) % len(IP_LIST)
        return redirect(new_url, code=302)
    else:
        return abort(400)


if __name__ == "__main__":
    app.run(port=8080)
