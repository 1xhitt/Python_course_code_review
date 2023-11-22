from curses import raw
import bs4, re
NUMBER_PATTERN = re.compile("[0-9]+")

def extract_spec(char_div: bs4.Tag) -> tuple(str, str):
    value = char_div.findChild("span").findChild("span").text
    key = char_div.find(
        'span', {'class': 'e1ckvoeh1 e106ikdt0 app-catalog-13gqfj6 e1gjr6xo0'}).text
    return (key, value)

def extract_specs(block: bs4.Tag):
    specs_fields = block.find_all('div', {'class': "app-catalog-xc0ceg e1ckvoeh5"})
    raw_specs = {}
    for spec in specs_fields:
        key, value = extract_spec(spec)
        raw_specs[key] = value
    return raw_specs

def parse_main(block: bs4.Tag) -> dict[str: any]:
    raw_specs = extract_specs(block)
    specs = dict()
    specs['brand'] = raw_specs['Бренд']
    specs['model'] = raw_specs['Модель']
    specs['chipset'] = raw_specs['Видеочипсет']
    specs['max_definition'] = raw_specs['Максимальное разрешение']
    freq_raw = raw_specs['Частота графического процессора']
    specs['base_freq'], specs['boost_freq'] = map(int, NUMBER_PATTERN.findall(freq_raw))
    return specs


def parse_memory(block: bs4.Tag) -> dict[str: str]:
    raw_specs = extract_specs(block)
    specs = dict()
    specs["VRAM"] = int(NUMBER_PATTERN.findall(raw_specs['Объем видеопамяти'])[0])
    specs["VRAM_freq"] = int(NUMBER_PATTERN.findall(raw_specs['Частота видеопамяти'])[0])
    specs["bandwidth"] = int(NUMBER_PATTERN.findall(raw_specs['Пропускная способность памяти'])[0])
    return specs


def parse_sockets(block: bs4.Tag) -> dict[str: str]:
    raw_specs = extract_specs(block)
    specs = dict()
    specs["HDMI_count"] = int(NUMBER_PATTERN.findall(raw_specs["Разъемов HDMI"])[0])
    specs["DisplayPort_count"] = int(NUMBER_PATTERN.findall(raw_specs["Количество разъемов DisplayPort"])[0])
    return specs


def parse_power(block: bs4.Tag) -> dict[str: str]:
    raw_specs = extract_specs(block)
    specs = dict()
    specs["pin_count"] = int(NUMBER_PATTERN.match(raw_specs["Разъемы дополнительного питания"])[0])
    specs["TDP"] = int(NUMBER_PATTERN.match(raw_specs["Максимальное энергопотребление"])[0])
    return specs

def parse_size(block: bs4.Tag) -> dict[str: str]:
    raw_specs = extract_specs(block)
    specs = dict()
    specs["length"] = int(NUMBER_PATTERN.match(raw_specs["Длина видеокарты"])[0])
    specs["width"] = int(NUMBER_PATTERN.match(raw_specs["Высота видеокарты"])[0])
    specs["thickness"] = int(NUMBER_PATTERN.match(raw_specs["Толщина видеокарты"])[0])
    return specs


def parse_guarantee(block: bs4.Tag) -> dict[str: str]:
    raw_specs = extract_specs(block)
    specs = dict()
    specs["guarantee"] = int(NUMBER_PATTERN.match(raw_specs["Гарантия"])[0])
    return specs