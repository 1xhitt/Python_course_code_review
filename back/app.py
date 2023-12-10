import os
import flask
import scraper
import db
from apscheduler.schedulers.background import BackgroundScheduler

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
        'brand' : str, 
        'name' : str, 
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
    specs = db.suggest_gpu(resp['price'], resp["brand"], resp["chipset"])
    if specs is None:
        gpu = flask.jsonify(
            id = None,
            url = None,
            price = None,
            brand = None,
            name = None,
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
            brand=specs[3],
            name=specs[4],
            chipset=specs[5],
            base_freq=specs[6],
            boost_freq=specs[7],
            VRAM=specs[8],
            VRAM_freq=specs[9],
            HDMI_count=specs[10],
            DisplayPort_count=specs[11],
            power_input=specs[12],
            pin_count=specs[13],
        ) 
    return gpu, 200


@app.route("/refresh", methods=["POST"])
def refresh():
    """
    for manual start of scraping
    goes ahead and scrapes the website
    """
    scraper.scrape()
    return flask.jsonify(), 200

@app.route("/brands", methods=["GET"])
def fetch_brands():
    """
    :returns:
    {[brands:str]}
    """
    brands = db.get_all_brands()
    return flask.jsonify(brands), 200


@app.route("/chipsets", methods=["GET"])
def fetch_chipsets():
    """
    :returns:
    {[chipsets:str]}
    """
    chipsets = db.get_all_chipsets()
    return flask.jsonify(chipsets), 200


if __name__ == "__main__":
    s = BackgroundScheduler()
    s.add_job(func = scraper.scrape, trigger='interval', hours=8)
    s.start()
    app.run("0.0.0.0", "6000")
