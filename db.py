import os
import sqlite3
import sqlalchemy

DB_NAME = "db"


def save_gpu(specs: dict[str: str]):
    if not os.path.isfile("./db"):
        print("made new db")
        make_db()
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cmd = f"""INSERT INTO gpus (id, url, price, brand, model, chipset, max_definition, core_count, base_freq, boost_freq, VRAM, VRAM_freq, bandwidth, HDMI_count, DisplayPort_count, power_pin_count, guarantee) VALUES ({make_id("GPU")}, '{specs['url']}', {specs['price']}, '{specs['brand']}', '{specs['model']}', '{specs['chipset']}', '{specs['max_definition']}', {specs['core_count']}, {specs['base_freq']}, {specs['boost_freq']}, {specs['VRAM']}, {specs['VRAM_freq']}, {specs['bandwidth']}, {specs['HDMI_count']}, {specs['DisplayPort_count']}, {specs['power_pin_count']}, {specs['guarantee']});"""
    cmd.replace('None', 'NULL', -1)
    print(cmd)
    cur.execute(cmd)
    conn.commit()


def make_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""CREATE TABLE gpus(
                id INTEGER PRIMARY KEY,
                url CHAR(255),
                price INTEGER,
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
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    count = cur.execute(
        f"SELECT count FROM counts WHERE name='{name}'").fetchone()[0]
    cur.execute(f"UPDATE counts SET count={count + 1} WHERE name='{name}'")
    conn.commit()
    return count


def get_all_ids() -> list[int]:
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    ids = cur.execute(f"SELECT id FROM gpus;").fetchall()
    return [i[0] for i in ids]


def get_gpu(id: int) -> tuple:
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    return cur.execute(f"SELECT * FROM gpus WHERE id={id};").fetchone()


# if __name__ == "__main__":
#     make_db()
