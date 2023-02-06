import scrapy
# from crawl_data.crawl_data.items import CrawlDataItem
from crawl_data.items import CrawlDataItem
from crawl_data.settings import CHROME_DRIVER_PATH

from selenium import webdriver
# from scrapy.selector import Selector
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
# from scrapy.utils.project import get_project_settings
import time
import pandas as pd

path_csv = '/home/user/Desktop/review/eda/crawl_data/amandia_trial1.csv'


# """
# --------------scraping from searching hotel
class CrawlReviewSpider(scrapy.Spider):
    name = 'review_scraping'
    allowed_domains = ['tripadvisor.com.vn']
    start_urls = [
                    'https://www.tripadvisor.com.vn/Hotels-g293928-Nha_Trang_Khanh_Hoa_Province-Hotels.html',
                    'https://www.tripadvisor.com.vn/Hotels-g298085-Da_Nang-Hotels.html',
                    'https://www.tripadvisor.com.vn/Hotels-g293924-Hanoi-Hotels.html',
                    'https://www.tripadvisor.com.vn/Hotels-g293922-Da_Lat_Lam_Dong_Province-Hotels.html',
                    'https://www.tripadvisor.com.vn/Hotels-g293925-Ho_Chi_Minh_City-Hotels.html',
                    'https://www.tripadvisor.com.vn/Hotels-g2146235-Nghe_An_Province-Hotels.html',
                    'https://www.tripadvisor.com.vn/Hotels-g1554764-Vinh_Nghe_An_Province-Hotels.html',
                    'https://www.tripadvisor.com.vn/Hotels-g2145099-An_Giang_Province-Hotels.html'
                    'https://www.tripadvisor.com.vn/Hotels-g2145104-Ba_Ria_Vung_Tau_Province-Hotels.html',
                    'https://www.tripadvisor.com.vn/Hotels-g5556252-Bac_Lieu_Province_Mekong_Delta-Hotels.html',
                    'https://www.tripadvisor.com.vn/Hotels-g6776104-Bac_Giang_Bac_Giang_Province-Hotels.html',
                    'https://www.tripadvisor.com.vn/Hotels-g2145106-Bac_Ninh_Province-Hotels.html',
                    'https://www.tripadvisor.com.vn/Hotels-g3311193-Binh_Duong_Province-Hotels.html',
                    'https://www.tripadvisor.com.vn/Hotels-g6939209-Binh_Phuoc_Province-Hotels.html',
                    'https://www.tripadvisor.com.vn/Hotels-g303942-Can_Tho_Mekong_Delta-Hotels.html',
                    'https://www.tripadvisor.com.vn/Hotels-g303944-Hai_Phong-Hotels.html',
                    'https://www.tripadvisor.com.vn/Hotels-g2146209-c3-zff17-Hai_Duong_Province-Hotels.html',
                    'https://www.tripadvisor.com.vn/Hotels-g3320435-Hoa_Binh_Hoa_Binh_Province-Hotels.html',
                    'https://www.tripadvisor.com.vn/Hotels-g737052-Lao_Cai_Lao_Cai_Province-Hotels.html',
                    'https://www.tripadvisor.com.vn/Hotels-g2146283-Quang_Ninh_Province-Hotels.html',
                    'https://www.tripadvisor.com.vn/SmartDeals-g303945-Ninh_Binh_Ninh_Binh_Province-Hotel-Deals.html',
                    'https://www.tripadvisor.com.vn/Hotels-g1236104-Thanh_Hoa_Thanh_Hoa_Province-Hotels.html',
                    'https://www.tripadvisor.com.vn/Hotels-g293926-Hue_Thua_Thien_Hue_Province-Hotels.html',
                    'https://www.tripadvisor.com.vn/Hotels-g2062763-Vinh_Yen_Vinh_Phuc_Province-Hotels.html',
                    'https://www.tripadvisor.com.vn/Hotels-g2146363-Vinh_Phuc_Province-Hotels.html',
                    'https://www.tripadvisor.com.vn/Hotels-g800616-Yen_Bai_Yen_Bai_Province-Hotels.html'

                ]

    def parse(self, response):
        #press show all button
        driver_path = CHROME_DRIVER_PATH
        driver = webdriver.Chrome(driver_path)
        driver.get(response.url)
        time.sleep(2)
        try:
            # seeAll_button = driver.find_element_by_class_name("biGQs._P.ttuOS").click()
            seeALL_button = driver.find_element(By.CLASS_NAME, 'biGQs._P.ttuOS')
            seeALL_button.click()
        except:
            driver.quit()

        #move to hotel link
        hotel_links = response.css("div.listing_title > a::attr(href)").extract_first()
        # if hotel_links:
        #     yield response.follow(hotel_links, self.parse_hotel)
        yield from response.follow_all(css="div.listing_title > a::attr(href)", callback=self.parse_hotel)

        # move to next page of hotel list
        stdPagination_links = response.css("div.standard_pagination > a::attr(href)").extract_first()
        if stdPagination_links:
            yield response.follow(stdPagination_links, self.parse)
        # yield from response.follow_all(css="div.standard_pagination > a::attr(href)", callback=self.parse)


    def parse_hotel(self, response):
        h_name = response.css("h1#HEADING::text").get()
        
        for review in response.css('div[data-test-target="HR_CC_CARD"]'):
        # for review in response.css('div[data-test-target="review-tab"]'):
            
            h_rating = review.css('div[data-test-target="review-rating"] > span::attr(class)').get()
            # date_review = review.css('div.cRVSd > span::text').get()

            # if 'đã viết đánh giá vào' in date_review:
            #     h_date = date_review.replace('đã viết đánh giá vào', '')
            # else:
            #     continue
            h_date = review.css('div.cRVSd > span::text').get()
            h_date = h_date.replace('đã viết đánh giá vào', '')

            if h_rating != 'ui_bubble_rating bubble_50' and h_rating is not None:
                item = CrawlDataItem()
                item['h_rating'] = h_rating
                item['h_name'] = h_name
                item['h_reviewer_name'] = review.css("div.cRVSd > span > a::text").get()

                #get date
                # item['h_date'] = review.css('div.EftBQ > span.S4::text').get()
                item['h_date'] = h_date

                item['h_title_comment'] = review.css('div[data-test-target = "review-title"] > a.Qwuub:first-child > span > span::text').get()
                comment = review.css('div.fIrGe._T > q.H4 > span::text').getall()

                if comment is None or comment==[''] :
                    continue
                #"load more" button
                h_comment = ' '.join(comment)
                item['h_comment'] = h_comment

                yield item

            else: 
                continue

        #move to next page of review list
        review_links = response.css("a.next::attr(href)").extract_first()
        if review_links:
            yield response.follow(review_links, self.parse_hotel)

"""

# ## ----------- scraping for a specific hotel-------
class CrawlReviewSpider(scrapy.Spider):
    name = 'review_scraping'
    allowed_domains = ['tripadvisor.com.vn']
    start_urls = [
                    'https://www.tripadvisor.com.vn/Hotel_Review-g293928-d4172546-Reviews-or255-Amiana_Resort_Nha_Trang-Nha_Trang_Khanh_Hoa_Province.html',
                #    'https://www.tripadvisor.com.vn/Hotel_Review-g293928-d12682708-Reviews-Ibis_Styles_Nha_Trang-Nha_Trang_Khanh_Hoa_Province.html',
                    # 'https://www.tripadvisor.com.vn/Hotel_Review-g293928-d15328095-Reviews-Xala_Boutique_Hotel-Nha_Trang_Khanh_Hoa_Province.html',
                ]

    def parse(self, response):
        # driver_path = CHROME_DRIVER_PATH
        # driver = webdriver.Chrome(driver_path)
        # driver.get(response.url)
        # time.sleep(2)
        # # # try:
        # # #     # seeAll_button = driver.find_element_by_class_name("biGQs._P.ttuOS").click()
        # seeALL_button = driver.find_element(By.CLASS_NAME, 'Ignyf._S.Z')
        # seeALL_button.click()
        # # except:
        #     # driver.quit()
  
        h_name = response.css("h1#HEADING::text").get()
        
        for review in response.css('div[data-test-target="HR_CC_CARD"]'):
            
            # item['h_url'] = h_url
            h_rating = review.css('div[data-test-target="review-rating"] > span::attr(class)').get()
            date_review = review.css('div.cRVSd > span::text').get()

            if 'đã viết đánh giá vào' in date_review:
                h_date = date_review.replace('đã viết đánh giá vào', '')
            else:
                continue

            if h_rating != 'ui_bubble_rating bubble_50' and h_rating is not None:
                item = CrawlDataItem()
                item['h_rating'] = h_rating
                item['h_name'] = h_name
                item['h_reviewer_name'] = review.css("div.cRVSd > span > a::text").get()

                #get date
                # item['h_date'] = review.css('div.EftBQ > span.S4::text').get()
                item['h_date'] = h_date

                item['h_title_comment'] = review.css('div[data-test-target = "review-title"] > a.Qwuub:first-child > span > span::text').get()
                comment = review.css('div.fIrGe._T > q.H4 > span::text').getall()

                if comment is None or comment==[''] :
                    continue
                review = ' '.join(comment)
                item['h_comment'] = str(review)

                yield item
            
            else: 
                continue

        #move to the next page
        next_page = response.css("a.next::attr(href)").extract_first()
        if next_page:
            # yield scrapy.Request(response.urljoin(next_page), callback=self.parse)
            yield response.follow(next_page, self.parse)
        # try:
        #     next_button = driver.find_element(By.CSS_SELECTOR, 'a.next::attr(href)')
        #     next_button.click()
        # except:
        #     driver.quit()
        # driver.quit()

"""

