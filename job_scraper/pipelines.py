# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class JobScraperPipeline:
    def process_item(self, item, spider):
        # truy xuất dữ liệu đồng bộ, dù cho item có là dict hay class -> item là các fields deifned trong items.py
        # adapter sẽ là 1 list các cột, để lấy value thì dùng adapter.get(col)
        adapter = ItemAdapter(item)
        # xóa ký tự xuống dòngs
        cols = ['cong_viec','cong_ty', 'muc_luong', 'dia_diem_cap_nhat_theo_danh_muc_hanh_chinh', 'kinh_nghiem', 'danh_muc_nghe_lien_quan', 'ky_nang_can_co' , 'chuyen_mon', 'mo_ta_cong_viec', 'yeu_cau_ung_vien', 'quyen_loi', 'thoi_gian_lam_viec']
        for col in cols:
            value = adapter.get(col) # lấy value của từng cột
            try: # value nào rỗng thì đi tiếp
                for i in value:
                    clean_list = [i.strip() for i in value if i.strip()] 
                    '''
                    ko gán trực tiếp list comprehension này cho biến value vì sẽ bị lỗi logic, phần tử đầu tiên xử lý xong thì 
                    phần tử thứ 2 đã ko còn
                    '''
                adapter[col] = ", ".join(clean_list)
            except:
                continue
        try:
            adapter['han_nop_ho_so'] = adapter.get('han_nop_ho_so').strip()
        except:
            pass
        return item
