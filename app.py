from flask import Flask, redirect
from dotenv import load_dotenv
from utils.get_ips import get_ips

load_dotenv()

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
