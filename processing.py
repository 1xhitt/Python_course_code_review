from email.mime import base
import db


class GPU:
    """
    loads gpu from db by id\n
    stores base specs and computes performance indecies
    """
    id: int
    price: int
    brand: str
    model: str
    chipset: str
    max_definition: str
    base_freq: int
    boost_freq: int
    VRAM: int
    VRAM_freq: int
    bandwidth: int
    HDMI_count: int
    DisplayPort_count: int
    power_pin_count: int
    guarantee: int

    performance_index: int

    def __init__(self, id):
        specs = db.get_gpu(id)
        if specs is None:
            raise ValueError("No gpu with such id")
        # meta
        self.id = specs[0]
        self.url = specs[1]
        self.price = specs[2]
        self.brand = specs[3]
        self.model = specs[4]
        self.chipset = specs[5]
        self.max_definition = specs[6]
        self.core_count = specs[7]
        self.base_freq = specs[8]
        self.boost_freq = specs[9]
        self.VRAM = specs[10]
        self.VRAM_freq = specs[11]
        self.bandwidth = specs[12]
        self.HDMI_count = specs[13]
        self.DisplayPort_count = specs[14]
        self.power_pin_count = specs[15]
        self.guarantee = specs[16]
        # derived
        self.performance_index = self.compute_performance_index()
    
    def compute_performance_index(self) -> int:
        
        memq = self.VRAM ** 2
        memq *= self.VRAM_freq if self.VRAM_freq else 500
        memq *= self.core_count if self.core_count else 100
        
        if self.base_freq:
            procq = (self.base_freq +(2 * self.boost_freq)) / 3
            # note that if boost freq is not mentioned it is assumed to be equal to base freq
        else:
            procq = 500
        return int((memq * procq) ** 1 / 2)

    def get_full_name(self) -> str:
        return self.brand + self.model


class Suggestor:
    gpus: list[GPU]  # sorted by performance index of choice
    ids: list[int]

    def __init__(self) -> None:
        """
        expects gpus to be scraped beforehand
        """
        self.ids = db.get_all_ids()
        self.gpus = []
        for id in self.ids:
            self.gpus.append(GPU(id))
        self.gpus.sort(key=lambda gpu: gpu.performance_index, reverse=True)

    def suggest(self, price: int) -> GPU:
        """
        returns best (according to index) gpu for your budget (exclusively on gpu)\n
        or None if you are broke...
        """
        # 1k gpus expected, soo...
        for gpu in self.gpus:
            if gpu.price < price:
                return gpu
        return None
