import os
# import sqlite3
import psycopg2

DATABASE = "gpus"
HOST = "pguser"
USER = "sadpguser123"
PASSWORD = "db_pass"
PORT = "5432"


def save_gpu(specs: dict[str: str]):
    conn = psycopg2.connect(database=DATABASE,
                            host=HOST,
                            user=USER,
                            password=PASSWORD,
                            port=PORT)
    cur = conn.cursor()
    cmd = f"""INSERT INTO gpus (id, url, price, perf_index, brand, model, chipset, max_definition, core_count, base_freq, boost_freq, VRAM, VRAM_freq, bandwidth, HDMI_count, DisplayPort_count, power_pin_count, guarantee) VALUES ({make_id("GPU")}, '{specs['url']}', {specs['price']}, {compute_performance_index(specs)}, '{specs['brand']}', '{specs['model']}', '{specs['chipset']}', '{specs['max_definition']}', {specs['core_count']}, {specs['base_freq']}, {specs['boost_freq']}, {specs['VRAM']}, {specs['VRAM_freq']}, {specs['bandwidth']}, {specs['HDMI_count']}, {specs['DisplayPort_count']}, {specs['power_pin_count']}, {specs['guarantee']});"""
    cmd.replace('None', 'NULL', -1)
    print(cmd)
    cur.execute(cmd)
    conn.commit()


def compute_performance_index(specs: dict) -> int:
    memq = specs['VRAM']
    memq *= specs['VRAM_freq'] if 'VRAM_freq' in specs.keys() else 500
    procq = (specs['base_freq'] + (2 * specs['boost_freq'])) / \
        3 if specs['boost_freq'] != "NULL" else 500
    procq *= specs['core_count'] if specs['core_count'] != "NULL" else 100
    # print(memq)
    # print(procq)
    return int((memq * procq) ** 1 / 2)


def make_db():
    conn = psycopg2.connect(database=DATABASE,
                            host=HOST,
                            user=USER,
                            password=PASSWORD,
                            port=PORT)
    cur = conn.cursor()
    cur.execute("""CREATE TABLE gpus(
                id INTEGER PRIMARY KEY,
                url CHAR(255),
                price INTEGER NOT NULL,
                perf_index INTEGER NOT NULL,
                brand CHAR(255),
                model CHAR(255),
                chipset CHAR(255),
                max_definition CHAR(16),
                core_count INTEGER,
                base_freq INTEGER,
                boost_freq INTEGER,
                VRAM INTEGER,
                VRAM_freq INTEGER,
                bandwidth INTEGER,
                HDMI_count INTEGER,
                DisplayPort_count INTEGER,
                power_pin_count INTEGER,
                TDP INTEGER,
                guarantee INTEGER
    );""")

    cur.execute(f"""CREATE TABLE counts(
                name CHAR(63),
                count INT);""")
    cur.execute('INSERT INTO counts (name, count) VALUES ("GPU", 0);')
    conn.commit()


def make_id(name: str):
    conn = psycopg2.connect(database=DATABASE,
                            host=HOST,
                            user=USER,
                            password=PASSWORD,
                            port=PORT)
    cur = conn.cursor()
    count = cur.execute(
        f"SELECT count FROM counts WHERE name='{name}'").fetchone()[0]
    cur.execute(f"UPDATE counts SET count={count + 1} WHERE name='{name}'")
    conn.commit()
    return count


def get_all_ids() -> list[int]:
    conn = psycopg2.connect(database=DATABASE,
                            host=HOST,
                            user=USER,
                            password=PASSWORD,
                            port=PORT)
    cur = conn.cursor()
    ids = cur.execute(f"SELECT id FROM gpus;").fetchall()
    return [i[0] for i in ids]


def get_gpu(id: int) -> tuple:
    conn = psycopg2.connect(database=DATABASE,
                            host=HOST,
                            user=USER,
                            password=PASSWORD,
                            port=PORT)
    cur = conn.cursor()
    return cur.execute(f"SELECT * FROM gpus WHERE id={id};").fetchone()


def suggest_gpu(price: int):
    conn = psycopg2.connect(database=DATABASE,
                            host=HOST,
                            user=USER,
                            password=PASSWORD,
                            port=PORT)
    cur = conn.cursor()
    gpus = cur.execute(
        f"SELECT * FROM gpus WHERE price < {price} ORDER BY -1*perf_index").fetchone()
    return gpus


# if __name__ == "__main__":
#     make_db()
