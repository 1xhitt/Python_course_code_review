import os
import flask
import scraper
import db

app = flask.Flask(__name__)


@app.route("/suggest", methods=["GET"])
def suggest():
    """
    :param:{
        price : int
    }
    :return:{
        'id' : int,
        'url' : str,
        'price' : int,
        'full_name' : str, 
        'chipset' : str, 
        'base_freq' : int,
        'boost_freq' : int,
        'VRAM' : int,
        'VRAM_freq' : int, 
        'HDMI_count' : int, 
        'DisplayPort_count' : int, 
        'power_input' : int,
        'pin_count' : int, 
    }
    """
    print("getting")
    resp = flask.json.loads(flask.request.json)
    print(resp)
    specs = db.suggest_gpu(resp['price'])
    if specs is None:
        gpu = flask.jsonify(
            id = None,
            url = None,
            price = None,
            full_name = None,
            chipset = None,
            base_freq = None,
            boost_freq = None,
            VRAM = None,
            VRAM_freq = None,
            HDMI_count = None,
            DisplayPort_count = None,
            power_input = None,
            pin_count = None
        )
    else:
        gpu = flask.jsonify(
            id=specs[0],
            url=specs[1],
            price=specs[2],
            full_name=specs[3],
            chipset=specs[4],
            base_freq=specs[5],
            boost_freq=specs[6],
            VRAM=specs[7],
            VRAM_freq=specs[8],
            HDMI_count=specs[9],
            DisplayPort_count=specs[10],
            power_input=specs[11],
            pin_count=specs[12],
        )
# 0 1 2 4
# id, url, price, perf_index, full_name, chipset, base_freq, boost_freq, VRAM, VRAM_freq, HDMI_count, DisplayPort_count, power_input, pin_count
# 0, 1, 2, perf_index, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13
    
    return gpu, 200


@app.route("/refresh", methods=["POST"])
def refresh():
    """
    for manual start of scraping
    goes ahead and scrapes the website
    """
    if os.path.exists("../database/db"):
        os.remove("../database/db")
    scraper.scrape()
    return flask.jsonify(), 200


if __name__ == "__main__":
    app.run("0.0.0.0", "6000")
