# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JobScraperItem(scrapy.Item):
    # define the fields for your item here like:
    pass

class JobItem(scrapy.Item):
    crawl_id = scrapy.Field()
    url = scrapy.Field()
    cong_viec = scrapy.Field()
    cong_ty = scrapy.Field()
    muc_luong = scrapy.Field()
    dia_diem_cap_nhat_theo_danh_muc_hanh_chinh = scrapy.Field() # list rỗng = False
    kinh_nghiem = scrapy.Field()
    danh_muc_nghe_lien_quan = scrapy.Field()
    ky_nang_can_co = scrapy.Field()
    chuyen_mon = scrapy.Field()
    mo_ta_cong_viec = scrapy.Field()
    yeu_cau_ung_vien = scrapy.Field()
    quyen_loi = scrapy.Field()
    thoi_gian_lam_viec = scrapy.Field()
    han_nop_ho_so = scrapy.Field()
    timestamp = scrapy.Field()