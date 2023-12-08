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
    cmd = f"""INSERT INTO gpus (id, url, price, perf_index, full_name, chipset, base_freq, boost_freq, VRAM, VRAM_freq, HDMI_count, DisplayPort_count, power_input, pin_count) VALUES ({specs['id']}, '{specs['url']}', {specs['price']}, {compute_performance_index(specs)}, '{specs['full_name']}', '{specs['chipset']}', {specs['base_freq']}, {specs['boost_freq']}, {specs['VRAM']}, {specs['VRAM_freq']}, {specs['HDMI_count']}, {specs['DisplayPort_count']}, {specs['power_input']}, {specs['pin_count']});"""
    print(cmd)
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
    cur.execute("""CREATE TABLE  gpus(
                id INTEGER PRIMARY KEY,
                perf_index INTEGER NOT NULL,
                url CHAR(255) NOT NULL,
                price INTEGER NOT NULL,
                full_name CHAR(255) NOT NULL,
                chipset CHAR(255) NOT NULL,
                base_freq INTEGER,
                boost_freq INTEGER,
                VRAM INTEGER,
                VRAM_freq INTEGER,
                HDMI_count INTEGER,
                DisplayPort_count INTEGER,
                power_input INTEGER,
                pin_count INTEGER);""")
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


def print_db():
    conn = psycopg2.connect(database=DATABASE,
                            host=HOST,
                            user=USER,
                            password=PASSWORD,
                            port=PORT)
    cur = conn.cursor()
    cur.execute("SELECT * FROM gpus")
    print(cur.fetchall())
    conn.close()
    

def suggest_gpu(price: int):
    conn = psycopg2.connect(database=DATABASE,
                            host=HOST,
                            user=USER,
                            password=PASSWORD,
                            port=PORT)
    cur = conn.cursor()
    cmd = f"SELECT * FROM gpus WHERE price < {price} ORDER BY -1*perf_index;"
    print(cmd)
    cur.execute(cmd)
    gpus = cur.fetchone()
    conn.close()
    return gpus


# if __name__ == "__main__":
#     make_db()
