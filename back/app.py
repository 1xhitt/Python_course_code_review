import os, flask
import scraper, db

app = flask.Flask(__name__)

@app.route("/suggest", methods=["GET"])
def suggest():
    """
    :param:{
        price : int
    }
    :return:{
        id : int
        url : str
        price : int
        perf_index : int
        brand : str
        model : str
        chipset : str
        max_definition : str
        core_count : int
        base_freq : int
        boost_freq : int
        VRAM : int
        VRAM_freq : int
        bandwidth : int
        HDMI_count : int
        DisplayPort_count : int
        power_pin_count : int
        TDP : int
        guarantee : int
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
            perf_index = None,
            brand = None,
            model = None,
            chipset = None,
            max_definition = None,
            core_count = None,
            base_freq = None,
            boost_freq = None,
            VRAM = None,
            VRAM_freq = None,
            bandwidth = None,
            HDMI_count = None,
            DisplayPort_count = None,
            power_pin_count = None,
            guarantee = None
        )
    else:
        gpu = flask.jsonify(
            id = specs[0],
            url = specs[1],
            price = specs[2],
            perf_index = specs[3],
            brand = specs[4],
            model = specs[5],
            chipset = specs[6],
            max_definition = specs[7],
            core_count = specs[8],
            base_freq = specs[9],
            boost_freq = specs[10],
            VRAM = specs[11],
            VRAM_freq = specs[12],
            bandwidth = specs[13],
            HDMI_count = specs[14],
            DisplayPort_count = specs[15],
            power_pin_count = specs[16],
            guarantee = specs[17]
        )
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