import bs4
import re
NUMBER_PATTERN = re.compile("[0-9]+")


def extract_spec(spec_div: bs4.Tag) -> (str, str):
        
    value = spec_div.find(
        'span', {"class": "e1ckvoeh0 e106ikdt0 app-catalog-1uhv1s4 e1gjr6xo0"}).span.text
    if "Процессоров" in spec_div.text:
        key = "Процессоров"
    else:
        key = spec_div.find(
        'span', {"class": "e1ckvoeh3 e106ikdt0 app-catalog-1eqtzki e1gjr6xo0"}).span.text
    return (key, value)


def extract_specs(block: bs4.Tag):
    specs_fields = block.find_all(
        'div', {'class': "app-catalog-xc0ceg e1ckvoeh5"})
    raw_specs = {}
    for spec in specs_fields:
        # print(type(spec))
        key, value = extract_spec(spec)
        if "процессоров" in key or "ALU" in key or "CUDA" in key:  # ALU / CUDA
            raw_specs["Процессоров"] = value
            continue
        raw_specs[key] = value
    return raw_specs


def parse_main(block: bs4.Tag) -> dict[str: any]:
    raw_specs = extract_specs(block)
    specs = dict()

    if "Бренд" in raw_specs.keys():
        specs['brand'] = raw_specs['Бренд']
    else:
        specs["brand"] = "NULL"

    if "Модель" in raw_specs.keys():
        specs['model'] = raw_specs['Модель']
    else:
        specs["model"] = "NULL"

    if " Видеочипсет" in raw_specs.keys():
        specs['chipset'] = raw_specs[' Видеочипсет']
    else:
        specs["chipset"] = "NULL"

    if "Максимальное" in raw_specs.keys():
        specs['max_definition'] = raw_specs['Максимальное']
    else:
        specs["max_definition"] = "NULL"
    if 'Частота графического' in specs.keys():
        freq_raw = raw_specs['Частота графического']
        freqs = list(map(int, NUMBER_PATTERN.findall(freq_raw)))
        if len(freqs) > 1:
            specs['base_freq'], specs['boost_freq'] = map(int, freqs)
        else:
            specs['base_freq'] = specs['boost_freq'] = freqs[0]
    else:
        specs['base_freq'] = specs['boost_freq'] = "NULL"

    if 'Процессоров' in specs.keys():
        specs['core_count'] = int(raw_specs['Процессоров'])
    else:
        specs['core_count'] = "NULL"
    return specs


def parse_memory(block: bs4.Tag) -> dict[str: str]:
    raw_specs = extract_specs(block)
    specs = dict()
    if "Частота" in raw_specs.keys():
        specs["VRAM_freq"] = int(NUMBER_PATTERN.findall(raw_specs['Частота'])[0])
    else:
        specs["VRAM_freq"] = "NULL"

    specs["VRAM"] = int(NUMBER_PATTERN.findall(raw_specs['Объем'])[0])
    if "bandwidth" in specs.keys():
        specs["bandwidth"] = int(NUMBER_PATTERN.findall(raw_specs['Пропускная способность памяти'])[0])
    else:
        specs["bandwidth"] = "NULL"
    return specs


def parse_sockets(block: bs4.Tag) -> dict[str: str]:
    raw_specs = extract_specs(block)
    specs = dict()
    if "Разъемов" in raw_specs.keys():
        specs["HDMI_count"] = int(
            NUMBER_PATTERN.findall(raw_specs["Разъемов"])[0])
    else:
        specs["HDMI_count"] = "NULL"
    if "Количество разъемов" in raw_specs.keys():
        specs["DisplayPort_count"] = int(
            NUMBER_PATTERN.findall(raw_specs["Количество разъемов"])[0])
    else:
        specs["DisplayPort_count"] = "NULL"
    return specs


def parse_power(block: bs4.Tag) -> dict[str: str]:
    raw_specs = extract_specs(block)
    specs = dict()
    if "Разъемы дополнительного" in raw_specs.keys():
        numbers = NUMBER_PATTERN.match(raw_specs["Разъемы дополнительного"])
        if numbers:
            specs["power_pin_count"] = int(numbers[0])
        else:
            specs["power_pin_count"] = 0
    else:
        specs["power_pin_count"] = "NULL"
    # if "TDP" in raw_specs.keys():
    #     specs["TDP"] = int(NUMBER_PATTERN.match(raw_specs["Максимальное"])[0])
    # else:
    #     specs["TDP"] = "NULL"
    return specs


def parse_guarantee(block: bs4.Tag) -> dict[str: str]:
    raw_specs = extract_specs(block)
    specs = dict()
    if "Гарантия" in raw_specs.keys():
        specs["guarantee"] = int(
            NUMBER_PATTERN.match(raw_specs["Гарантия"])[0])
    else:
        specs["guarantee"] = "NULL"

    return specs
