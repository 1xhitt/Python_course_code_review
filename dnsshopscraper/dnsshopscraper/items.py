# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from platform import architecture
from requests import check_compatibility
import scrapy


class DnsshopscraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class GPUItem(scrapy.Item):
    name = scrapy.Field()
    price = scrapy.Field()
    processor = scrapy.Field()
    microachitecture = scrapy.Field()
    base_frequency = scrapy.Field()
    turbo_frequentcy = scrapy.Field()
    alu = scrapy.Field()
    number_of_texture_blocks = scrapy.Field()
    number_of_raster_blocks = scrapy.Field()
    rtx_support = scrapy.Field()
    rt_cores = scrapy.Field()
    tensor_cores = scrapy.Field()
    VRAM = scrapy.Field()
    memory_type = scrapy.Field()
    width_of_memory_bus = scrapy.Field()
    memory_bandwidth = scrapy.Field()
    effective_memory_frequency = scrapy.Field()
    disply_port_count = scrapy.Field()
    HDMI_version = scrapy.Field()
    DisplyPort_version = scrapy.Field()
    max_number_of_monitors = scrapy.Field()
    interface = scrapy.Field()
    form_of_interface = scrapy.Field()
    number_of_PCIE_lilnes = scrapy.Field()
    addititonal_power_inputs = scrapy.Field()
    recomended_power_source = scrapy.Field()
    height = scrapy.Field()
    width = scrapy.Field()
    thickness = scrapy.Field()

# For now, I limit my scope to GPUs

# class CPUItem(scrapy.Item):
#     name = scrapy.Field()
#     price = scrapy.Field()
#     chipset = scrapy.Field() #intel / amd
#     core = scrapy.Field()
#     base_frequency = scrapy.Field()
#     turbo_frequentcy = scrapy.Field()
#     supported_memory_type = scrapy.Field()
#     supported_memory_size = scrapy.Field()
#     supported_memory_frequency = scrapy.Field()
#     number_of_memory_channels = scrapy.Field()
#     EEC = scrapy.Field()
#     TDP = scrapy.Field()
#     base_TDP = scrapy.Field()
#     max_temperature = scrapy.Field()
#     Integrated_GPU = scrapy.Field()
#     PCIE_version = scrapy.Field()
#     number_of_PCIE_lanes = scrapy.Field()

# class MotherBoardItem(scrapy.Item):
#     name = scrapy.Field()
#     price = scrapy.Field()
#     chipset = scrapy.Field()
#     compatibility = scrapy.Field()

#     supported_memory = scrapy.Field()
#     supported_memory_form = scrapy.Field()
#     supported_memory_size = scrapy.Field()
#     supported_memory_freqency = scrapy.Field()
#     real_memory_freqencies = scrapy.Field()
#     memory_slots = scrapy.Field()
#     memory_channels = scrapy.Field()
    
#     PCIE_version = scrapy.Field()
#     PCIEx16_slots = scrapy.Field()
#     PCIEx1_slots = scrapy.Field()
#     SLI_support = scrapy.Field()
#     SLI_count = scrapy.Field()
    
#     NVMe_support = scrapy.Field()
#     PCIEM2_version = scrapy.Field()
#     M2_slots = scrapy.Field()
#     SATA_slots = scrapy.Field()
#     SATA_RAID_mode = scrapy.Field()

#     #TODO
    
#     height = scrapy.Field()
#     width = scrapy.Field()