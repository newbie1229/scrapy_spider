import scrapy
from datetime import datetime
from datetime import datetime
import hashlib
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
from job_scraper.items import JobItem
from urllib.parse import quote

class JobspiderSpider(scrapy.Spider):
    name = "jobspider"
    allowed_domains = ["www.topcv.vn", 'ltuquanghuy1101.workers.dev'] # chặn spider đi crawl các websites khác
    # start_urls = ["https://www.topcv.vn/tim-viec-lam-moi-nhat"]
    start_urls = ["https://scrapy.ltuquanghuy1101.workers.dev/?url=https://www.topcv.vn/tim-viec-lam-moi-nhat"]
    proxy_url = "https://scrapy.ltuquanghuy1101.workers.dev"

    custom_settings = {
        'DOWNLOAD_DELAY': 10,
        'RANDOMIZE_DOWNLOAD_DELAY': True,
        'CONCURRENT_REQUESTS': 4, # Giảm xuống để an toàn
        'CONCURRENT_REQUESTS_PER_DOMAIN': 2,
        
        'RETRY_TIMES': 5, # Tăng số lần thử lại
        'RETRY_HTTP_CODES': [429, 500, 502, 503, 504, 403, 404], # Bắt lỗi 429 để thử lại
        
        'AUTOTHROTTLE_ENABLED': True,
        'AUTOTHROTTLE_START_DELAY': 5,
        'AUTOTHROTTLE_MAX_DELAY': 60,
        'AUTOTHROTTLE_TARGET_CONCURRENCY': 1.0,

    }

    # def start_requests(self):
    #     target_url="https://www.topcv.vn/tim-viec-lam-moi-nhat"
    #     final_url=f"{self.proxy_url}?url={quote(target_url)}"
    #     yield scrapy.Request(url=final_url, callback=self.parse)


    # fetch(start_url)
    def parse(self, response): # hàm này được gọi mỗi khi Request được trả về
        jobs = response.css("div.job-item-search-result") 
        # lấy list các selector object (job) ở trang ngoài chứ ko phải đi vào trong từng job
        # self.logger.info(f"Response Headers: {response.headers}")
        # if response.status == 403:
        #     self.logger.error("DÃ BỊ CHẶN 403! NỘI DUNG TRANG LỖI:")
        #     self.logger.error(response.text[:5000])
        for job in jobs:
            job_url = job.css("h3.title a::attr('href')").get()
            if job_url:
                job_url_via_worker = f"https://scrapy.ltuquanghuy1101.workers.dev/?url={quote(job_url)}"
                # đi vào từng job
                yield scrapy.Request(job_url_via_worker, callback=self.parse_job_page)
        next_page_url = response.css('ul.pagination li a[rel="next"]::attr(data-href)').get()
        if next_page_url:
            next_page_via_worker = f"https://scrapy.ltuquanghuy1101.workers.dev/?url={quote(next_page_url)}"
            yield scrapy.Request(next_page_via_worker, callback=self.parse, dont_filter=True)


    # fecth(job_url)
    def parse_job_page(self, response):
        # https://www.topcv.vn/viec-lam/nhan-vien-kinh-doanh-tu-van-sale-bat-dong-san-co-luong-cung-thu-nhap-khong-gioi-han/1981457.html?ta_source=JobSearchList_LinkDetail&u_sr_id=EiVwZSZgmkda9z3rf4pJXUHzGFpyvGlge0NCv6dS_1769179483
        # https://www.topcv.vn/brand/chinhanhtranscosmoshochiminh/tuyen-dung/nhan-vien-cham-soc-khach-hang-tong-dai-vien-ngan-hang-quan-doi-mb-bank-khong-yeu-cau-kinh-nghiem-tai-ha-noi-j2010084.html?ta_source=JobSearchList_LinkDetail&u_sr_id=EiVwZSZgmkda9z3rf4pJXUHzGFpyvGlge0NCv6dS_1769179483
        
        url_encoded = response.url.encode('utf-8')
        crawl_id = hashlib.sha1(url_encoded).hexdigest()
        
        job_1 = response.css("h1.job-detail__info--title a::attr('title')").getall() # truy cập đến thẻ a rồi thuộc tính title
        job_2 = response.css("div.box-header h2.title::text").getall()

        company_name_1 = response.css("div.company-name-label a.name::attr('title')").get()
        
        salary_1 = response.css("div.job-detail__info--section.section-salary .job-detail__info--section-content-value::text").get()
        # class có space thì viết liền nhau và có dấu chấm
        salary_2 = response.xpath('//h2[contains(., "Thông tin")]/following-sibling::div[1]//text()').getall()

        location_1 = response.css(".job-description__item").xpath('self::*[contains(., "Địa điểm làm việc")]//text()').getall()
        location_2 = response.xpath('//h2[contains(., "Địa điểm làm việc")]/following-sibling::div[1]//text()').getall()

        experience_1 = response.css("div.job-detail__info--section.section-experience .job-detail__info--section-content-value::text").get()
        experience_2 = response.xpath('//h2[contains(., "Thông tin")]/following-sibling::div[1]//text()').getall()

        industry_1 =  response.css('div.box-category-tags a.box-category-tag::text').getall()

        skills_1 = response.css('div.box-category-tags >  span.box-category-tag::text').getall() # chỉ lấy những thẻ span là con trực tiếp của div

        specialty_div = response.xpath('//div[div[@class="job-tags__group-name" and contains(text(), "Chuyên môn")]]')
        chuyen_mon_1 = specialty_div.xpath('.//a[@class="item search-from-tag link"]/text()').getall()


        jd_1 = response.xpath('//h3[contains(., "Mô tả công việc")]/following-sibling::div[1]//text()').getall()
        jd_2 = response.xpath('//h2[contains(., "Mô tả công việc")]/following-sibling::div[1]//text()').getall()

        requirement_1 = response.xpath('//h3[contains(., "Yêu cầu ứng viên")]/following-sibling::div[1]//text()').getall()
        requirement_2 = response.xpath('//h2[contains(., "Yêu cầu ứng viên")]/following-sibling::div[1]//text()').getall()

        benefit_1 = response.xpath('//h3[contains(., "Quyền lợi")]/following-sibling::div[1]//text()').getall()
        benefit_2 = response.xpath('//h2[contains(., "Quyền lợi")]/following-sibling::div[1]//text()').getall()

        working_time_1 = response.xpath('//h3[contains(., "Thời gian làm việc")]/following-sibling::div[1]//text()').getall()
        working_time_2 = response.xpath('//h2[contains(., "Thời gian làm việc")]/following-sibling::div[1]//text()').getall()

        application_dl = response.css("div.job-detail__information-detail--actions-label::text").get()

        job_item = JobItem()

        job_item['crawl_id']=crawl_id
        job_item['url'] = response.url
        job_item['cong_viec'] = job_1 if job_1 else job_2
        job_item['cong_ty'] = company_name_1 if company_name_1 else None
        job_item['muc_luong'] = salary_1 if salary_1 else salary_2
        job_item['dia_diem_cap_nhat_theo_danh_muc_hanh_chinh'] = location_1 if location_1 else location_2
        job_item['kinh_nghiem'] = experience_1 if experience_1 else experience_2
        job_item['danh_muc_nghe_lien_quan'] = industry_1 if industry_1 else None
        job_item['ky_nang_can_co'] = skills_1 if skills_1 else None
        job_item['chuyen_mon'] = chuyen_mon_1
        job_item['mo_ta_cong_viec'] = jd_1 if jd_1 else jd_2
        job_item['yeu_cau_ung_vien'] = requirement_1 if requirement_1 else requirement_2
        job_item['quyen_loi'] = benefit_1 if benefit_1 else benefit_2
        job_item['thoi_gian_lam_viec'] = working_time_1 if working_time_1 else working_time_2
        job_item['han_nop_ho_so'] = application_dl if application_dl else None
        job_item['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        yield job_item
