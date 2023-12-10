import os
# import sqlite3
import psycopg2

DATABASE = "gpus"
HOST = "database"
USER = "pguser"
PASSWORD = "sadpguser123"
PORT = "5432"

def save_gpu(specs: dict[str: str]):
    conn = psycopg2.connect(database=DATABASE,
                            host=HOST,
                            user=USER,
                            password=PASSWORD,
                            port=PORT)
    cur = conn.cursor()
    cmd = f"""INSERT INTO gpus (id, url, price, perf_index, brand, name, chipset, base_freq, boost_freq, VRAM, VRAM_freq, HDMI_count, DisplayPort_count, power_input, pin_count) VALUES ({specs['id']}, '{specs['url']}', {specs['price']}, {compute_performance_index(specs)}, '{specs['brand']}', '{specs['name']}', '{specs['chipset']}', {specs['base_freq']}, {specs['boost_freq']}, {specs['VRAM']}, {specs['VRAM_freq']}, {specs['HDMI_count']}, {specs['DisplayPort_count']}, {specs['power_input']}, {specs['pin_count']});"""
    cur.execute(cmd)
    conn.commit()


def compute_performance_index(specs: dict) -> int:
    memq = specs['VRAM']
    memq *= specs['VRAM_freq'] if 'VRAM_freq' in specs.keys() else 500
    procq = (specs['base_freq'] + (2 * specs['boost_freq'])) / 3 if specs['boost_freq'] != "NULL" else 500
    return int((memq * procq) ** 1 / 2)

def remake_db(drop_tables = False):
    conn = psycopg2.connect(database=DATABASE,
                            host=HOST,
                            user=USER,
                            password=PASSWORD,
                            port=PORT)
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
                brand CHAR(64) NOT NULL,
                name CHAR(64) NOT NULL,
                chipset CHAR(64) NOT NULL,
                base_freq INTEGER,
                boost_freq INTEGER,
                VRAM INTEGER,
                VRAM_freq INTEGER,
                HDMI_count INTEGER,
                DisplayPort_count INTEGER,
                power_input INTEGER,
                pin_count INTEGER);""")
    # needed to store awailable brands and chipsets
    cur.execute("CREATE TABLE brands(id INTEGER PRIMARY KEY, brand CHAR(64));")
    cur.execute("CREATE TABLE chipsets(id INTEGER PRIMARY KEY, chipset CHAR(64));")
    conn.commit()

def collect_brands():
    conn = psycopg2.connect(database=DATABASE,
                            host=HOST,
                            user=USER,
                            password=PASSWORD,
                            port=PORT)
    cur = conn.cursor()
    cur.execute("SELECT brand FROM gpus;")
    brands = list(set([i[0] for i in cur.fetchall()]))
    id = 0
    for brand in brands:
        brand:str = brand[:brand.find(' ')]
        cur.execute(f"INSERT INTO brands (id, brand) VALUES ({id}, '{brand}');")
        id += 1
    conn.commit()


def collect_chipsets():
    conn = psycopg2.connect(database=DATABASE,
                            host=HOST,
                            user=USER,
                            password=PASSWORD,
                            port=PORT)
    cur = conn.cursor()
    cur.execute("SELECT chipset FROM gpus;")
    chipsets = list(set([i[0] for i in cur.fetchall()]))
    id = 0
    for chipset in chipsets:
        chipset:str = chipset[:chipset.find(' ')]
        cur.execute(f"INSERT INTO chipsets (id, chipset) VALUES ({id}, '{chipset}');")
        id += 1
    conn.commit()

def get_all_ids() -> list[int]:
    conn = psycopg2.connect(database=DATABASE,
                            host=HOST,
                            user=USER,
                            password=PASSWORD,
                            port=PORT)
    cur = conn.cursor()
    cur.execute(f"SELECT id FROM gpus;")
    ids = cur.fetchall()
    conn.close()
    return [i[0] for i in ids]


def get_gpu(id: int) -> tuple:
    conn = psycopg2.connect(database=DATABASE,
                            host=HOST,
                            user=USER,
                            password=PASSWORD,
                            port=PORT)
    cur = conn.cursor()
    conn.close()
    return cur.execute(f"SELECT * FROM gpus WHERE id={id};").fetchone()


# url, price, full_name, chipset, base_freq, boost_freq, VRAM, VRAM_freq, HDMI_count, DisplayPort_count, power_input, pin_count
def suggest_gpu(price: int):
    conn = psycopg2.connect(database=DATABASE,
                            host=HOST,
                            user=USER,
                            password=PASSWORD,
                            port=PORT)
    cur = conn.cursor()
    cmd = f"SELECT id, url, price, full_name, chipset, base_freq, boost_freq, VRAM, VRAM_freq, HDMI_count, DisplayPort_count, power_input, pin_count FROM gpus WHERE price < {price} ORDER BY -1*perf_index;"
    # print(cmd)
    cur.execute(cmd)
    gpus = cur.fetchone()
    conn.close()
    return gpus


# if __name__ == "__main__":
#     make_db()
