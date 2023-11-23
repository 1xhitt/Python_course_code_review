import sqlite3, sqlalchemy

DB_NAME = "db"

def save_gpu(specs: dict[str : str]):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cmd = f"""INSERT INTO gpus (id, brand, model, chipset, max_definition, base_freq, boost_freq, VRAM, VRAM_freq, bandwidth, HDMI_count, DisplayPort_count, power_pin_count, TDP, guarantee) VALUES ({get_id("GPU")}, '{specs['brand']}', '{specs['model']}', '{specs['chipset']}', '{specs['max_definition']}', {specs['base_freq']}, {specs['boost_freq']}, {specs['VRAM']}, {specs['VRAM_freq']}, {specs['bandwidth']}, {specs['HDMI_count']}, {specs['DisplayPort_count']}, {specs['power_pin_count']}, {specs['TDP']}, {specs['guarantee']});"""
    cmd.replace('None', 'NULL', -1)
    print(cmd)
    cur.execute(cmd)
    conn.commit()


def make_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""CREATE TABLE gpus(
                id INTEGER PRIMARY KEY,
                brand CHAR(255),
                model CHAR(255),
                chipset CHAR(255) NOT NULL,
                max_definition CHAR(16),
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

def get_id(name:str):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    count = cur.execute(f"SELECT count FROM counts WHERE name='{name}'").fetchone()[0]
    cur.execute(f"UPDATE counts SET count={count + 1} WHERE name='{name}'")
    conn.commit()
    return count



# if __name__ == "__main__":
#     make_db()