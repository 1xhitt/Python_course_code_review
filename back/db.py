import os
import psycopg2
import config


def save_gpu(specs: dict[str: str]):
    conn = psycopg2.connect(database=config.DATABASE,
                            host=config.HOST,
                            user=config.USER,
                            password=config.PASSWORD,
                            port=config.PORT)
    cur = conn.cursor()
    cmd = f"""INSERT INTO gpus (id, url, price, perf_index, brand, name, chipset, base_freq, boost_freq, VRAM, VRAM_freq, HDMI_count, DisplayPort_count, power_input, pin_count) VALUES ({specs['id']}, '{specs['url']}', {specs['price']}, {compute_performance_index(specs)}, '{specs['brand']}', '{specs['name']}', '{specs['chipset']}', {specs['base_freq']}, {specs['boost_freq']}, {specs['VRAM']}, {specs['VRAM_freq']}, {specs['HDMI_count']}, {specs['DisplayPort_count']}, {specs['power_input']}, {specs['pin_count']});"""
    cur.execute(cmd)
    conn.commit()


def compute_performance_index(specs: dict) -> int:
    memq = ((specs['VRAM'] ** config.VRAM_WEIGHT)
            * (specs['VRAM_freq'] ** config.VRAM_FREQ_WEIGHT)) \
        ** (1 / (config.VRAM_WEIGHT + config.VRAM_FREQ_WEIGHT))
    procq = (config.BASE_CORE_FREQ_WEIGHT * specs['base_freq']
             + config.BOOST_CORE_FREQ_WEIGHT * specs['boost_freq']) \
        / (config.BASE_CORE_FREQ_WEIGHT + config.BOOST_CORE_FREQ_WEIGHT)
    perf_index = ((memq ** config.MEM_WEIGHT)
                  * (procq ** config.PROC_WEIGHT)) \
        ** (1 / (config.MEM_WEIGHT + config.PROC_WEIGHT))
    return int(perf_index)


def remake_db(drop_tables=False):
    conn = psycopg2.connect(database=config.DATABASE,
                            host=config.HOST,
                            user=config.USER,
                            password=config.PASSWORD,
                            port=config.PORT)
    cur = conn.cursor()
    if drop_tables:
        cur.execute("DROP TABLE IF EXISTS gpus;")
        cur.execute("DROP TABLE IF EXISTS counts;")
        cur.execute("DROP TABLE IF EXISTS brands;")
        cur.execute("DROP TABLE IF EXISTS chipsets;")
    cur.execute("""CREATE TABLE  gpus(
                id INTEGER PRIMARY KEY,
                perf_index INTEGER NOT NULL,
                url CHAR(255) NOT NULL,
                price INTEGER NOT NULL,
                brand CHAR(16) NOT NULL,
                name CHAR(256) NOT NULL,
                chipset CHAR(256) NOT NULL,
                base_freq INTEGER,
                boost_freq INTEGER,
                VRAM INTEGER,
                VRAM_freq INTEGER,
                HDMI_count INTEGER,
                DisplayPort_count INTEGER,
                power_input INTEGER,
                pin_count INTEGER);""")
    # needed to store awailable brands and chipsets
    cur.execute("CREATE TABLE brands(id INTEGER PRIMARY KEY, brand CHAR(16));")
    cur.execute(
        "CREATE TABLE chipsets(id INTEGER PRIMARY KEY, chipset CHAR(256));")
    conn.commit()


def collect_brands():
    conn = psycopg2.connect(database=config.DATABASE,
                            host=config.HOST,
                            user=config.USER,
                            password=config.PASSWORD,
                            port=config.PORT)
    cur = conn.cursor()
    cur.execute("SELECT brand FROM gpus;")
    brands = list(set([i[0] for i in cur.fetchall()]))
    id = 0
    for brand in brands:
        brand: str = brand[:brand.find('   ')]
        cur.execute(
            f"INSERT INTO brands (id, brand) VALUES ({id}, '{brand}');")
        id += 1
    conn.commit()


def collect_chipsets():
    conn = psycopg2.connect(database=config.DATABASE,
                            host=config.HOST,
                            user=config.USER,
                            password=config.PASSWORD,
                            port=config.PORT)
    cur = conn.cursor()
    cur.execute("SELECT chipset FROM gpus;")
    chipsets = list(set([i[0] for i in cur.fetchall()]))
    id = 0
    for chipset in chipsets:
        chipset: str = chipset[:chipset.find('   ')]
        cur.execute(
            f"INSERT INTO chipsets (id, chipset) VALUES ({id}, '{chipset}');")
        id += 1
    conn.commit()


def run(cmd: str) -> list[int]:
    """debug use only.\n 
    called exclusively from scraper.py
    to see if data was saved in a correct manner"""
    conn = psycopg2.connect(database=config.DATABASE,
                            host=config.HOST,
                            user=config.USER,
                            password=config.PASSWORD,
                            port=config.PORT)
    cur = conn.cursor()
    cur.execute(cmd)
    ids = cur.fetchall()
    conn.close()
    return ids


def get_all_brands() -> list[str]:
    conn = psycopg2.connect(database=config.DATABASE,
                            host=config.HOST,
                            user=config.USER,
                            password=config.PASSWORD,
                            port=config.PORT)
    cur = conn.cursor()
    cur.execute(f"SELECT brand FROM brands;")
    vals = cur.fetchall()
    conn.close()
    return [i[0][:i[0].find('   ')] for i in vals]


def get_all_chipsets() -> list[str]:
    conn = psycopg2.connect(database=config.DATABASE,
                            host=config.HOST,
                            user=config.USER,
                            password=config.PASSWORD,
                            port=config.PORT)
    cur = conn.cursor()
    cur.execute(f"SELECT chipset FROM chipsets;")
    vals = cur.fetchall()
    conn.close()
    return [i[0][:i[0].find('   ')] for i in vals]


def get_gpu(id: int) -> tuple:
    conn = psycopg2.connect(database=config.DATABASE,
                            host=config.HOST,
                            user=config.USER,
                            password=config.PASSWORD,
                            port=config.PORT)
    cur = conn.cursor()
    conn.close()
    return cur.execute(f"SELECT * FROM gpus WHERE id={id};").fetchone()


def suggest_gpu(price: int, brand: str = "ANY", chipset: str = "ANY"):
    conn = psycopg2.connect(database=config.DATABASE,
                            host=config.HOST,
                            user=config.USER,
                            password=config.PASSWORD,
                            port=config.PORT)
    cur = conn.cursor()
    cmd = f"SELECT id, url, price, brand, name, chipset, base_freq, boost_freq, VRAM, VRAM_freq, HDMI_count, DisplayPort_count, power_input, pin_count FROM gpus WHERE price < {price}"
    if brand != "ANY":
        cmd += f" AND brand='{brand}'"
    if chipset != "ANY":
        cmd += f" AND chipset='{chipset}'"
    cmd += " ORDER BY -1*perf_index;"
    cur.execute(cmd)

    gpu = cur.fetchone()
    conn.close()
    return gpu
