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
import requests
import json
import math
from bs4 import BeautifulSoup


# --------------scraping from Agoda by bs4 ---------------
class CrawlAgoda(scrapy.Spider):
    name = 'agoda_scraping'
    allowed_domains = ['agoda.com']
    start_urls = [
                    'https://www.agoda.com/vi-vn/city/c-n-tho-vn.html',
                    # 'https://www.tripadvisor.com.vn/Hotels-g298184-Tokyo_Tokyo_Prefecture_Kanto-Hotels.html',
                
                ]

    def parse(self, response):
        driver_path = CHROME_DRIVER_PATH
        driver = webdriver.Chrome(driver_path)
        driver.get(response.url)
        time.sleep(2)
        try:
            print('maaaa11111111111111')
            # seeALL_button = driver.find_element(By.CLASS_NAME, 'div.fMuMFt > div.hRUYUu> span.kkSkZk')
            seeALL_button = driver.find_element(By.XPATH, "//div[@class='fMuMFt']/div[@class='hRUYUu']/span[@class='kkSkZk']")
            print('maaaaaa')
            seeALL_button.click()
            print('maaa clickkkkkkkkkk')
            time.sleep(30)
        except:
                driver.quit()






# # --------------scraping from Agoda by hidden apis ----------------
# class CrawlAgoda(scrapy.Spider):
#     name = 'agoda_scraping'
#     # allowed_domains = ['agoda.com']
#     # allowed_domains = ['tripadvisor.com.vn']
#     start_urls = [
#                     'https://www.agoda.com/vi-vn/city/c-n-tho-vn.html',
#                     # 'https://www.tripadvisor.com.vn/Hotels-g298184-Tokyo_Tokyo_Prefecture_Kanto-Hotels.html',
                
#                 ]

#     def parse(self, response):
#         #-------press seeAll button by Selenium
#         # driver_path = CHROME_DRIVER_PATH
#         # driver = webdriver.Chrome(driver_path)
#         # driver.get(response.url)
#         # time.sleep(5)
#         # try:
#         #     # seeAll_button = driver.find_element_by_class_name("biGQs._P.ttuOS").click()
#         #     seeAll_button = driver.find_element(By.CLASS_NAME, 'Spanstyled__SpanStyled-sc-16tp9kb-0.kkSkZk.kite-js-Span')
#         #     # seeAll_button = driver.find_element(By.CLASS_NAME, 'biGQs._P.ttuOS')
#         #     seeAll_button.click()
#         # except:
#         #     driver.quit()

#         #get city id
#         def get_city_id():
#             this_url = response.url.split('/')[-1].split('.')[0]
#             endpoint = 'https://www.agoda.com/api/cronos/geo/country/GetCountryTopCities'
#             headers = {
#                 'authority': 'www.agoda.com',
#                 'accept': '*/*',
#                 'accept-language': 'en-US,en;q=0.9,vi;q=0.8',
#                 'ag-language-id': '24',
#                 'ag-language-locale': 'vi-vn',
#                 'content-type': 'application/json; charset=UTF-8',
#                 # 'cookie': 'agoda.user.03=UserId=865c4264-9192-4852-ac58-f7a38b07a143; agoda.prius=PriusID=0&PointsMaxTraffic=Agoda; ASP.NET_SessionId=uc21kqesxd5lrteldvdaxylr; agoda.firstclicks=1844104||||2023-02-08T17:24:27||uc21kqesxd5lrteldvdaxylr||{"IsPaid":false,"gclid":"","Type":""}; agoda.price.01=PriceView=1; deviceId=308a80ab-694c-4001-999f-f7299ce5a00a; _ab50group=GroupA; _40-40-20Split=Group40B; ab.storage.userId.d999de98-30bc-4346-8124-a15900a101ae=%7B%22g%22%3A%22865c4264-9192-4852-ac58-f7a38b07a143%22%2C%22c%22%3A1675933439406%2C%22l%22%3A1675933439406%7D; ab.storage.deviceId.d999de98-30bc-4346-8124-a15900a101ae=%7B%22g%22%3A%225c3b9cdb-e698-731e-1a9c-41403cbd2581%22%2C%22c%22%3A1675933439410%2C%22l%22%3A1675933439410%7D; FPID=FPID2.2.Ta63%2Fdr6T41UIvuq%2FTF38bYDtXZSbV0EfC7FoUvXUTM%3D.1675933438; agoda.familyMode=Mode=0; agoda.consent=VN||2023-02-10 11:15:06Z; tealiumEnable=true; _gid=GA1.2.1202394643.1676255939; agoda.vuser=UserId=1ecd2134-f3fb-493f-97a3-ccbe9882cb97; UserSession=865c4264-9192-4852-ac58-f7a38b07a143; session_cache={"Cache":"hkdata1","Time":"638118774614634583","SessionID":"uc21kqesxd5lrteldvdaxylr","CheckID":"c43b6ef9016e8e5300b22ef14c741f1aedca85cb","CType":"N"}; FPLC=BCa94cKnSC9EkWz6iarmxQXTy9kppzY3EZ2jwqUOWGAuYT6r50C2xfzyEaQm7F3UlnhWYDg7ccso6Km0aftfqAxoQCYfwHOeJ2ZM3%2FOxGIVG5gq5vuX7APG15l2UfQ%3D%3D; agoda.attr.03=ATItems=1844104$02-15-2023 15:25$; agoda.version.03=CookieId=bb777edb-460a-4318-b66d-797324be3582&TItems=2$1844104$02-15-2023 15:25$03-17-2023 15:25$&DLang=vi-vn&CurLabel=VND&CuLang=24&AllocId=6fcb27d9917ed1e032b52a25d5dd41c4d5426081a105913c204ae3e3169f37a15b110fc9194ca0c6d507b766476c1a5641a3387a30a66c2371b4a2741a7dc7a3a894ae1d26d08f8960ef32785e740be3a1e2d90295bb777edb460a31866d797324be3582&DPN=1&CulCd=&UrlV=1&Alloc=953$64|2069$88|2071$83|2079$12|2221$8|2188$88|2192$22|2211$83|2201$1|2273$96|2291$28|2346$74|2226$74|2229$81|2288$37|2308$35|2333$95|2528$60&FEBuildVersion=; agoda.pp.land=0=TVRnME5ERXdOSHcwTXpNNU9YeEdZV3h6WlE9PQ; agoda.lastclicks=1844104||||2023-02-15T15:25:41||uc21kqesxd5lrteldvdaxylr||{"IsPaid":false,"gclid":"","Type":""}; agoda.landings=1844104|||uc21kqesxd5lrteldvdaxylr|2023-02-08T17:24:27|False|19----1844104|||uc21kqesxd5lrteldvdaxylr|2023-02-15T15:25:41|False|20----1844104|||uc21kqesxd5lrteldvdaxylr|2023-02-15T15:25:41|False|99; xsrf_token=CfDJ8Dkuqwv-0VhLoFfD8dw7lYzSyOehNS4Yebu6avRxCCS5RA4OjgTk25lnsRvh3ZG0BylD9TwNrs3R1nA0frRT7mrXZIEIxYjqVM8DCjVSTj8ILcBcKpJcYcrCPC47cK0mWQ5Yx9qgBZZZN8vSIuYkYu8; agoda.search.01=SHist=1$13170$8083$1$1$1$0$0$$$0|1$16079$8083$1$1$1$0$0$$$0|1$16079$8084$1$1$1$0$0$$$0|4$561890$8084$1$1$1$0$0$$$0|1$16079$8085$1$1$1$0$0$$$0|1$16079$8087$1$1$1$0$0$$$0|4$1519798$8087$1$1$1$0$0$$$0|1$16079$8088$1$1$1$0$0$$$0|1$234333$8089$1$1$1$0$0$$$0|1$16079$8089$1$1$1$0$0$$$0|1$2758$8089$1$1$1$0$0$$$0&H=8080|5$561890|4$561890|2$1519798$907601|1$108533$907601$8091632$36780685$6909078|0$43399; _ga=GA1.2.1964826560.1675933438; _uetsid=fd3f4d40ab5511eda8871d2b3b2dd5ae; _uetvid=b213ab70a85811ed8f6ab55e410d1d3c; ab.storage.sessionId.d999de98-30bc-4346-8124-a15900a101ae=%7B%22g%22%3A%221bb3fc71-5d4e-0ba2-c5b8-ab0661d7f9f2%22%2C%22e%22%3A1676451378423%2C%22c%22%3A1676446567812%2C%22l%22%3A1676449578423%7D; cto_bundle=23v6jF9ZY3lqMERKejFjdnpxQlhWN2NwQk5yVXp5b0Zldmh3bEVFYyUyQk9jSmJGOEtPZmEzSmp5YnN1UlpLWiUyQmdEM1lqQmNSZ2VwVWRLVXozMUZ4UlVxMmtvTmpXYThzeG92UlVIT3BnVllRanV2aUwxVnVtbmNpNmt2UHZDZ3hLRUdJbGg4eFZOc3hlQXVYJTJCNUdjRDVVMnpFc0ElM0QlM0Q; _ga_T408Z268D2=GS1.1.1676446560.16.1.1676451014.60.0.0; utag_main=v_id:0186356ace4f0011f295ce0c75eb05065002205d00978$_sn:19$_se:35$_ss:0$_st:1676452815152$ses_id:1676446562101%3Bexp-session$_pn:17%3Bexp-session; _gat_t3=1; agoda.analytics=Id=5167290032545630042&Signature=-5676810151368555369&Expiry=1676454627847',
#                 'cr-currency-code': 'VND',
#                 'cr-currency-id': '78',
#                 'dnt': '1',
#                 'origin': 'https://www.agoda.com',
#                 'referer': 'https://www.agoda.com/vi-vn/city/c-n-tho-vn.html',
#                 'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
#                 'sec-ch-ua-mobile': '?0',
#                 'sec-ch-ua-platform': '"Linux"',
#                 'sec-fetch-dest': 'empty',
#                 'sec-fetch-mode': 'cors',
#                 'sec-fetch-site': 'same-origin',
#                 'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
#                 'x-requested-with': 'XMLHttpRequest',
#             }
#             json_data = 38
#             res = requests.post(endpoint, headers=headers, data=json.dumps(json_data))
#             list_id = json.loads(res.text)
#             for dic in list_id:
#                 for key in dic:
#                     if key == 'url':
#                         city_url = dic[key].split('/')[-1].split('.')[0]
#                         if city_url == this_url:
#                             return dic['id']
        
#         city_id = get_city_id()
#         fullSearchUrl = "https://www.agoda.com/vi-vn/search?city="+ str(city_id)
#         yield scrapy.Request(fullSearchUrl, callback=self.get_hotel_links)


#     def get_hotel_links(self, response, city_id):

#         """
#             Description: Get all hotel links in a city

#         """

#         def get_num_hotels():
#             """
#                 Description: Get number of hotels in a city
#             """
#             endpoint = 'https://www.agoda.com/graphql/search'

#             headers = {
#             'authority': 'www.agoda.com',
#             'accept': '*/*',
#             'accept-language': 'en-US,en;q=0.9,vi;q=0.8',
#             'access-control-max-age': '7200',
#             'ag-analytics-session-id': '5167290032545630042',
#             'ag-correlation-id': '4faf4266-de69-4234-9f77-ab0af06b02ac',
#             'ag-debug-override-origin': 'VN',
#             'ag-language-locale': 'vi-vn',
#             'ag-page-type-id': '103',
#             'ag-request-attempt': '1',
#             'ag-request-id': '29554256-2c52-4b7e-ad54-3f31eb3ed0e8',
#             'ag-retry-attempt': '0',
#             'content-type': 'application/json',
#             # 'cookie': 'agoda.user.03=UserId=865c4264-9192-4852-ac58-f7a38b07a143; agoda.prius=PriusID=0&PointsMaxTraffic=Agoda; ASP.NET_SessionId=uc21kqesxd5lrteldvdaxylr; agoda.firstclicks=1844104||||2023-02-08T17:24:27||uc21kqesxd5lrteldvdaxylr||{"IsPaid":false,"gclid":"","Type":""}; agoda.price.01=PriceView=1; deviceId=308a80ab-694c-4001-999f-f7299ce5a00a; _ab50group=GroupA; _40-40-20Split=Group40B; ab.storage.userId.d999de98-30bc-4346-8124-a15900a101ae=%7B%22g%22%3A%22865c4264-9192-4852-ac58-f7a38b07a143%22%2C%22c%22%3A1675933439406%2C%22l%22%3A1675933439406%7D; ab.storage.deviceId.d999de98-30bc-4346-8124-a15900a101ae=%7B%22g%22%3A%225c3b9cdb-e698-731e-1a9c-41403cbd2581%22%2C%22c%22%3A1675933439410%2C%22l%22%3A1675933439410%7D; FPID=FPID2.2.Ta63%2Fdr6T41UIvuq%2FTF38bYDtXZSbV0EfC7FoUvXUTM%3D.1675933438; agoda.familyMode=Mode=0; agoda.consent=VN||2023-02-10 11:15:06Z; tealiumEnable=true; _gid=GA1.2.1202394643.1676255939; agoda.vuser=UserId=1ecd2134-f3fb-493f-97a3-ccbe9882cb97; UserSession=865c4264-9192-4852-ac58-f7a38b07a143; session_cache={"Cache":"hkdata1","Time":"638118774614634583","SessionID":"uc21kqesxd5lrteldvdaxylr","CheckID":"c43b6ef9016e8e5300b22ef14c741f1aedca85cb","CType":"N"}; FPLC=BCa94cKnSC9EkWz6iarmxQXTy9kppzY3EZ2jwqUOWGAuYT6r50C2xfzyEaQm7F3UlnhWYDg7ccso6Km0aftfqAxoQCYfwHOeJ2ZM3%2FOxGIVG5gq5vuX7APG15l2UfQ%3D%3D; agoda.attr.03=ATItems=1844104$02-15-2023 15:25$; agoda.version.03=CookieId=bb777edb-460a-4318-b66d-797324be3582&TItems=2$1844104$02-15-2023 15:25$03-17-2023 15:25$&DLang=vi-vn&CurLabel=VND&CuLang=24&AllocId=6fcb27d9917ed1e032b52a25d5dd41c4d5426081a105913c204ae3e3169f37a15b110fc9194ca0c6d507b766476c1a5641a3387a30a66c2371b4a2741a7dc7a3a894ae1d26d08f8960ef32785e740be3a1e2d90295bb777edb460a31866d797324be3582&DPN=1&CulCd=&UrlV=1&Alloc=953$64|2069$88|2071$83|2079$12|2221$8|2188$88|2192$22|2211$83|2201$1|2273$96|2291$28|2346$74|2226$74|2229$81|2288$37|2308$35|2333$95|2528$60&FEBuildVersion=; agoda.lastclicks=1844104||||2023-02-15T15:25:41||uc21kqesxd5lrteldvdaxylr||{"IsPaid":false,"gclid":"","Type":""}; agoda.landings=1844104|||uc21kqesxd5lrteldvdaxylr|2023-02-08T17:24:27|False|19----1844104|||uc21kqesxd5lrteldvdaxylr|2023-02-15T15:25:41|False|20----1844104|||uc21kqesxd5lrteldvdaxylr|2023-02-15T15:25:41|False|99; xsrf_token=CfDJ8Dkuqwv-0VhLoFfD8dw7lYzSyOehNS4Yebu6avRxCCS5RA4OjgTk25lnsRvh3ZG0BylD9TwNrs3R1nA0frRT7mrXZIEIxYjqVM8DCjVSTj8ILcBcKpJcYcrCPC47cK0mWQ5Yx9qgBZZZN8vSIuYkYu8; agoda.search.01=SHist=1$13170$8083$1$1$1$0$0$$$0|1$16079$8083$1$1$1$0$0$$$0|1$16079$8084$1$1$1$0$0$$$0|4$561890$8084$1$1$1$0$0$$$0|1$16079$8085$1$1$1$0$0$$$0|1$16079$8087$1$1$1$0$0$$$0|4$1519798$8087$1$1$1$0$0$$$0|1$16079$8088$1$1$1$0$0$$$0|1$234333$8089$1$1$1$0$0$$$0|1$2758$8089$1$1$1$0$0$$$0|1$16079$8089$1$1$1$0$0$$$0&H=8080|5$561890|4$561890|2$1519798$907601|1$108533$907601$8091632$36780685$6909078|0$43399; utag_main=v_id:0186356ace4f0011f295ce0c75eb05065002205d00978$_sn:19$_se:39$_ss:0$_st:1676454583749$ses_id:1676446562101%3Bexp-session$_pn:19%3Bexp-session; _uetsid=fd3f4d40ab5511eda8871d2b3b2dd5ae; _uetvid=b213ab70a85811ed8f6ab55e410d1d3c; _ga=GA1.2.1964826560.1675933438; ab.storage.sessionId.d999de98-30bc-4346-8124-a15900a101ae=%7B%22g%22%3A%22181557d6-b242-23a3-bdcd-462f6c6ccac7%22%2C%22e%22%3A1676454584689%2C%22c%22%3A1676452784678%2C%22l%22%3A1676452784689%7D; _gat_t3=1; cto_bundle=L6KmuV9ZY3lqMERKejFjdnpxQlhWN2NwQk5vR1BnVVVwdW9Kc0FsUjMlMkYlMkYxT3puT0xlaXkyeiUyQklnWmRqU1olMkI3UlgzdXJGSW9oUDRiJTJCYllWNzZNYXdTcTdHWXRXYjU0UElZdHBEJTJCcnhyaE1qYzRMNnBvYW9XRGlndHpUczFCNjNyWXdjb0dHeE84RiUyQnRYSE5XbjBSViUyQmc5Z0pnJTNEJTNE; agoda.analytics=Id=5167290032545630042&Signature=-7485616655935041867&Expiry=1676456392942; _ga_T408Z268D2=GS1.1.1676446560.16.1.1676452796.41.0.0',
#             'dnt': '1',
#             'origin': 'https://www.agoda.com',
#             'referer': 'https://www.agoda.com/vi-vn/search?city=16079',
#             'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
#             'sec-ch-ua-mobile': '?0',
#             'sec-ch-ua-platform': '"Linux"',
#             'sec-fetch-dest': 'empty',
#             'sec-fetch-mode': 'cors',
#             'sec-fetch-site': 'same-origin',
#             'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
#         }

#             json_data = {
#                 'operationName': 'citySearch',
#                 'variables': {
#                     'CitySearchRequest': {
#                         'cityId': 16079,
#                         'searchRequest': {
#                             'searchCriteria': {
#                                 'isAllowBookOnRequest': True,
#                                 'bookingDate': '2023-02-15T09:19:56.899Z',
#                                 'checkInDate': '2023-02-24T09:19:56.022Z',
#                                 'localCheckInDate': '2023-02-24',
#                                 'los': 1,
#                                 'rooms': 1,
#                                 'adults': 1,
#                                 'children': 0,
#                                 'childAges': [],
#                                 'ratePlans': [],
#                                 'featureFlagRequest': {
#                                     'fetchNamesForTealium': True,
#                                     'fiveStarDealOfTheDay': True,
#                                     'isAllowBookOnRequest': False,
#                                     'showUnAvailable': True,
#                                     'showRemainingProperties': True,
#                                     'isMultiHotelSearch': False,
#                                     'enableAgencySupplyForPackages': True,
#                                     'flags': [
#                                         {
#                                             'feature': 'FamilyChildFriendlyPopularFilter',
#                                             'enable': True,
#                                         },
#                                         {
#                                             'feature': 'FamilyChildFriendlyPropertyTypeFilter',
#                                             'enable': True,
#                                         },
#                                         {
#                                             'feature': 'FamilyMode',
#                                             'enable': False,
#                                         },
#                                     ],
#                                     'enablePageToken': False,
#                                     'enableDealsOfTheDayFilter': False,
#                                     'isEnableSupplierFinancialInfo': False,
#                                     'ignoreRequestedNumberOfRoomsForNha': False,
#                                 },
#                                 'isUserLoggedIn': False,
#                                 'currency': 'VND',
#                                 'travellerType': 'Couple',
#                                 'isAPSPeek': False,
#                                 'enableOpaqueChannel': False,
#                                 'isEnabledPartnerChannelSelection': None,
#                                 'sorting': {
#                                     'sortField': 'Ranking',
#                                     'sortOrder': 'Desc',
#                                     'sortParams': None,
#                                 },
#                                 'requiredBasis': 'PRPN',
#                                 'requiredPrice': 'Exclusive',
#                                 'suggestionLimit': 0,
#                                 'synchronous': False,
#                                 'supplierPullMetadataRequest': None,
#                                 'isRoomSuggestionRequested': False,
#                                 'isAPORequest': False,
#                                 'hasAPOFilter': False,
#                             },
#                             'searchContext': {
#                                 'userId': '865c4264-9192-4852-ac58-f7a38b07a143',
#                                 'memberId': 0,
#                                 'locale': 'vi-vn',
#                                 'cid': 1844104,
#                                 'origin': 'VN',
#                                 'platform': 1,
#                                 'deviceTypeId': 1,
#                                 'experiments': {
#                                     'forceByVariant': None,
#                                     'forceByExperiment': [
#                                         {
#                                             'id': 'UMRAH-B2B',
#                                             'variant': 'B',
#                                         },
#                                         {
#                                             'id': 'UMRAH-B2C-REGIONAL',
#                                             'variant': 'B',
#                                         },
#                                         {
#                                             'id': 'UMRAH-B2C',
#                                             'variant': 'Z',
#                                         },
#                                         {
#                                             'id': 'JGCW-204',
#                                             'variant': 'B',
#                                         },
#                                         {
#                                             'id': 'JGCW-264',
#                                             'variant': 'B',
#                                         },
#                                         {
#                                             'id': 'JGCW-202',
#                                             'variant': 'B',
#                                         },
#                                         {
#                                             'id': 'JGCW-299',
#                                             'variant': 'B',
#                                         },
#                                         {
#                                             'id': 'FD-3936',
#                                             'variant': 'B',
#                                         },
#                                     ],
#                                 },
#                                 'isRetry': False,
#                                 'showCMS': False,
#                                 'storeFrontId': 3,
#                                 'pageTypeId': 103,
#                                 'whiteLabelKey': None,
#                                 'ipAddress': '123.16.13.79',
#                                 'endpointSearchType': 'CitySearch',
#                                 'trackSteps': None,
#                                 'searchId': 'bee4e848-4250-4c28-8ee1-07f18b8832c4',
#                             },
#                             'matrix': None,
#                             'matrixGroup': [
#                                 {
#                                     'matrixGroup': 'NumberOfBedrooms',
#                                     'size': 100,
#                                 },
#                                 {
#                                     'matrixGroup': 'LandmarkIds',
#                                     'size': 10,
#                                 },
#                                 {
#                                     'matrixGroup': 'AllGuestReviewBreakdown',
#                                     'size': 100,
#                                 },
#                                 {
#                                     'matrixGroup': 'GroupedBedTypes',
#                                     'size': 100,
#                                 },
#                                 {
#                                     'matrixGroup': 'RoomBenefits',
#                                     'size': 100,
#                                 },
#                                 {
#                                     'matrixGroup': 'AtmosphereIds',
#                                     'size': 100,
#                                 },
#                                 {
#                                     'matrixGroup': 'RoomAmenities',
#                                     'size': 100,
#                                 },
#                                 {
#                                     'matrixGroup': 'AffordableCategory',
#                                     'size': 100,
#                                 },
#                                 {
#                                     'matrixGroup': 'HotelFacilities',
#                                     'size': 100,
#                                 },
#                                 {
#                                     'matrixGroup': 'BeachAccessTypeIds',
#                                     'size': 100,
#                                 },
#                                 {
#                                     'matrixGroup': 'StarRating',
#                                     'size': 20,
#                                 },
#                                 {
#                                     'matrixGroup': 'MetroSubwayStationLandmarkIds',
#                                     'size': 20,
#                                 },
#                                 {
#                                     'matrixGroup': 'CityCenterDistance',
#                                     'size': 100,
#                                 },
#                                 {
#                                     'matrixGroup': 'ProductType',
#                                     'size': 100,
#                                 },
#                                 {
#                                     'matrixGroup': 'BusStationLandmarkIds',
#                                     'size': 20,
#                                 },
#                                 {
#                                     'matrixGroup': 'IsSustainableTravel',
#                                     'size': 2,
#                                 },
#                                 {
#                                     'matrixGroup': 'ReviewLocationScore',
#                                     'size': 3,
#                                 },
#                                 {
#                                     'matrixGroup': 'LandmarkSubTypeCategoryIds',
#                                     'size': 20,
#                                 },
#                                 {
#                                     'matrixGroup': 'ReviewScore',
#                                     'size': 100,
#                                 },
#                                 {
#                                     'matrixGroup': 'AccommodationType',
#                                     'size': 100,
#                                 },
#                                 {
#                                     'matrixGroup': 'PaymentOptions',
#                                     'size': 100,
#                                 },
#                                 {
#                                     'matrixGroup': 'TrainStationLandmarkIds',
#                                     'size': 20,
#                                 },
#                                 {
#                                     'matrixGroup': 'HotelAreaId',
#                                     'size': 100,
#                                 },
#                                 {
#                                     'matrixGroup': 'HotelChainId',
#                                     'size': 10,
#                                 },
#                                 {
#                                     'matrixGroup': 'RecommendedByDestinationCity',
#                                     'size': 10,
#                                 },
#                                 {
#                                     'matrixGroup': 'Deals',
#                                     'size': 100,
#                                 },
#                             ],
#                             'filterRequest': {
#                                 'idsFilters': [],
#                                 'rangeFilters': [],
#                                 'textFilters': [],
#                             },
#                             'page': {
#                                 'pageSize': 45,
#                                 'pageNumber': 1,
#                                 'pageToken': '',
#                             },
#                             'apoRequest': {
#                                 'apoPageSize': 10,
#                             },
#                             'searchHistory': [
#                                 {
#                                     'objectId': 561890,
#                                     'searchDate': '2023-2-10',
#                                     'searchType': 'PropertySearch',
#                                     'childrenAges': [],
#                                 },
#                                 {
#                                     'objectId': 561890,
#                                     'searchDate': '2023-2-11',
#                                     'searchType': 'PropertySearch',
#                                     'childrenAges': [],
#                                 },
#                                 {
#                                     'objectId': 1519798,
#                                     'searchDate': '2023-2-13',
#                                     'searchType': 'PropertySearch',
#                                     'childrenAges': [],
#                                 },
#                                 {
#                                     'objectId': 907601,
#                                     'searchDate': '2023-2-13',
#                                     'searchType': 'PropertySearch',
#                                     'childrenAges': [],
#                                 },
#                                 {
#                                     'objectId': 108533,
#                                     'searchDate': '2023-2-14',
#                                     'searchType': 'PropertySearch',
#                                     'childrenAges': [],
#                                 },
#                                 {
#                                     'objectId': 907601,
#                                     'searchDate': '2023-2-14',
#                                     'searchType': 'PropertySearch',
#                                     'childrenAges': [],
#                                 },
#                                 {
#                                     'objectId': 8091632,
#                                     'searchDate': '2023-2-14',
#                                     'searchType': 'PropertySearch',
#                                     'childrenAges': [],
#                                 },
#                                 {
#                                     'objectId': 36780685,
#                                     'searchDate': '2023-2-14',
#                                     'searchType': 'PropertySearch',
#                                     'childrenAges': [],
#                                 },
#                                 {
#                                     'objectId': 6909078,
#                                     'searchDate': '2023-2-14',
#                                     'searchType': 'PropertySearch',
#                                     'childrenAges': [],
#                                 },
#                                 {
#                                     'objectId': 43399,
#                                     'searchDate': '2023-2-15',
#                                     'searchType': 'PropertySearch',
#                                     'childrenAges': [],
#                                 },
#                             ],
#                             'searchDetailRequest': {
#                                 'priceHistogramBins': 50,
#                             },
#                             'isTrimmedResponseRequested': False,
#                             'featuredAgodaHomesRequest': None,
#                             'featuredLuxuryHotelsRequest': None,
#                             'highlyRatedAgodaHomesRequest': {
#                                 'numberOfAgodaHomes': 30,
#                                 'minimumReviewScore': 7.5,
#                                 'minimumReviewCount': 3,
#                                 'accommodationTypes': [
#                                     28,
#                                     29,
#                                     30,
#                                     102,
#                                     103,
#                                     106,
#                                     107,
#                                     108,
#                                     109,
#                                     110,
#                                     114,
#                                     115,
#                                     120,
#                                     131,
#                                 ],
#                                 'sortVersion': 0,
#                             },
#                             'extraAgodaHomesRequest': None,
#                             'extraHotels': {
#                                 'extraHotelIds': [],
#                                 'enableFiltersForExtraHotels': False,
#                             },
#                             'packaging': None,
#                             'flexibleSearchRequest': {
#                                 'fromDate': '2023-02-15',
#                                 'toDate': '2023-03-26',
#                                 'alternativeDateSize': 4,
#                                 'isFullFlexibleDateSearch': False,
#                             },
#                             'rankingRequest': {
#                                 'isNhaKeywordSearch': False,
#                                 'isPulseRankingBoost': False,
#                             },
#                             'rocketmilesRequestV2': None,
#                         },
#                     },
#                     'ContentSummaryRequest': {
#                         'context': {
#                             'rawUserId': '865c4264-9192-4852-ac58-f7a38b07a143',
#                             'memberId': 0,
#                             'userOrigin': 'VN',
#                             'locale': 'vi-vn',
#                             'forceExperimentsByIdNew': [
#                                 {
#                                     'key': 'UMRAH-B2B',
#                                     'value': 'B',
#                                 },
#                                 {
#                                     'key': 'UMRAH-B2C-REGIONAL',
#                                     'value': 'B',
#                                 },
#                                 {
#                                     'key': 'UMRAH-B2C',
#                                     'value': 'Z',
#                                 },
#                                 {
#                                     'key': 'JGCW-204',
#                                     'value': 'B',
#                                 },
#                                 {
#                                     'key': 'JGCW-264',
#                                     'value': 'B',
#                                 },
#                                 {
#                                     'key': 'JGCW-202',
#                                     'value': 'B',
#                                 },
#                                 {
#                                     'key': 'JGCW-299',
#                                     'value': 'B',
#                                 },
#                                 {
#                                     'key': 'FD-3936',
#                                     'value': 'B',
#                                 },
#                             ],
#                             'apo': False,
#                             'searchCriteria': {
#                                 'cityId': 16079,
#                             },
#                             'platform': {
#                                 'id': 1,
#                             },
#                             'storeFrontId': 3,
#                             'cid': '1844104',
#                             'occupancy': {
#                                 'numberOfAdults': 1,
#                                 'numberOfChildren': 0,
#                                 'travelerType': 0,
#                                 'checkIn': '2023-02-24T09:19:56.022Z',
#                             },
#                             'deviceTypeId': 1,
#                             'whiteLabelKey': '',
#                             'correlationId': '',
#                         },
#                         'summary': {
#                             'highlightedFeaturesOrderPriority': None,
#                             'description': False,
#                             'includeHotelCharacter': True,
#                         },
#                         'reviews': {
#                             'commentary': None,
#                             'demographics': {
#                                 'providerIds': None,
#                                 'filter': {
#                                     'defaultProviderOnly': True,
#                                 },
#                             },
#                             'summaries': {
#                                 'providerIds': None,
#                                 'apo': True,
#                                 'limit': 1,
#                                 'travellerType': 0,
#                             },
#                             'cumulative': {
#                                 'providerIds': None,
#                             },
#                             'filters': None,
#                         },
#                         'images': {
#                             'page': None,
#                             'maxWidth': 0,
#                             'maxHeight': 0,
#                             'imageSizes': None,
#                             'indexOffset': None,
#                         },
#                         'rooms': {
#                             'images': None,
#                             'featureLimit': 0,
#                             'filterCriteria': None,
#                             'includeMissing': False,
#                             'includeSoldOut': False,
#                             'includeDmcRoomId': False,
#                             'soldOutRoomCriteria': None,
#                             'showRoomSize': True,
#                             'showRoomFacilities': True,
#                             'showRoomName': False,
#                         },
#                         'nonHotelAccommodation': True,
#                         'engagement': True,
#                         'highlights': {
#                             'maxNumberOfItems': 0,
#                             'images': {
#                                 'imageSizes': [
#                                     {
#                                         'key': 'full',
#                                         'size': {
#                                             'width': 0,
#                                             'height': 0,
#                                         },
#                                     },
#                                 ],
#                             },
#                         },
#                         'personalizedInformation': False,
#                         'localInformation': {
#                             'images': None,
#                         },
#                         'features': None,
#                         'rateCategories': True,
#                         'contentRateCategories': {
#                             'escapeRateCategories': {},
#                         },
#                         'synopsis': True,
#                     },
#                     'PricingSummaryRequest': {
#                         'cheapestOnly': True,
#                         'context': {
#                             'isAllowBookOnRequest': True,
#                             'abTests': [
#                                 {
#                                     'testId': 9021,
#                                     'abUser': 'B',
#                                 },
#                                 {
#                                     'testId': 9023,
#                                     'abUser': 'B',
#                                 },
#                                 {
#                                     'testId': 9024,
#                                     'abUser': 'B',
#                                 },
#                                 {
#                                     'testId': 9025,
#                                     'abUser': 'B',
#                                 },
#                                 {
#                                     'testId': 9027,
#                                     'abUser': 'B',
#                                 },
#                                 {
#                                     'testId': 9029,
#                                     'abUser': 'B',
#                                 },
#                             ],
#                             'clientInfo': {
#                                 'cid': 1844104,
#                                 'languageId': 24,
#                                 'languageUse': 1,
#                                 'origin': 'VN',
#                                 'platform': 1,
#                                 'searchId': 'bee4e848-4250-4c28-8ee1-07f18b8832c4',
#                                 'storefront': 3,
#                                 'userId': '865c4264-9192-4852-ac58-f7a38b07a143',
#                                 'ipAddress': '123.16.13.79',
#                             },
#                             'experiment': [
#                                 {
#                                     'name': 'UMRAH-B2B',
#                                     'variant': 'B',
#                                 },
#                                 {
#                                     'name': 'UMRAH-B2C-REGIONAL',
#                                     'variant': 'B',
#                                 },
#                                 {
#                                     'name': 'UMRAH-B2C',
#                                     'variant': 'Z',
#                                 },
#                                 {
#                                     'name': 'JGCW-204',
#                                     'variant': 'B',
#                                 },
#                                 {
#                                     'name': 'JGCW-264',
#                                     'variant': 'B',
#                                 },
#                                 {
#                                     'name': 'JGCW-202',
#                                     'variant': 'B',
#                                 },
#                                 {
#                                     'name': 'JGCW-299',
#                                     'variant': 'B',
#                                 },
#                                 {
#                                     'name': 'FD-3936',
#                                     'variant': 'B',
#                                 },
#                             ],
#                             'isDebug': False,
#                             'sessionInfo': {
#                                 'isLogin': False,
#                                 'memberId': 0,
#                                 'sessionId': 1,
#                             },
#                             'packaging': None,
#                         },
#                         'isSSR': True,
#                         'roomSortingStrategy': None,
#                         'pricing': {
#                             'bookingDate': '2023-02-15T09:19:56.878Z',
#                             'checkIn': '2023-02-24T09:19:56.022Z',
#                             'checkout': '2023-02-25T09:19:56.022Z',
#                             'localCheckInDate': '2023-02-24',
#                             'localCheckoutDate': '2023-02-25',
#                             'currency': 'VND',
#                             'details': {
#                                 'cheapestPriceOnly': False,
#                                 'itemBreakdown': False,
#                                 'priceBreakdown': False,
#                             },
#                             'featureFlag': [
#                                 'ClientDiscount',
#                                 'PriceHistory',
#                                 'VipPlatinum',
#                                 'RatePlanPromosCumulative',
#                                 'PromosCumulative',
#                                 'CouponSellEx',
#                                 'MixAndSave',
#                                 'APSPeek',
#                                 'StackChannelDiscount',
#                                 'AutoApplyPromos',
#                                 'EnableAgencySupplyForPackages',
#                                 'EnableCashback',
#                                 'CreditCardPromotionPeek',
#                                 'EnableCofundedCashback',
#                                 'DispatchGoLocalForInternational',
#                                 'EnableGoToTravelCampaign',
#                             ],
#                             'features': {
#                                 'crossOutRate': False,
#                                 'isAPSPeek': False,
#                                 'isAllOcc': False,
#                                 'isApsEnabled': False,
#                                 'isIncludeUsdAndLocalCurrency': False,
#                                 'isMSE': True,
#                                 'isRPM2Included': True,
#                                 'maxSuggestions': 0,
#                                 'isEnableSupplierFinancialInfo': False,
#                                 'isLoggingAuctionData': False,
#                                 'newRateModel': False,
#                                 'overrideOccupancy': False,
#                                 'filterCheapestRoomEscapesPackage': False,
#                                 'priusId': 0,
#                                 'synchronous': False,
#                                 'enableRichContentOffer': True,
#                                 'showCouponAmountInUserCurrency': False,
#                                 'disableEscapesPackage': False,
#                                 'enablePushDayUseRates': False,
#                                 'enableDayUseCor': False,
#                             },
#                             'filters': {
#                                 'cheapestRoomFilters': [],
#                                 'filterAPO': False,
#                                 'ratePlans': [
#                                     1,
#                                 ],
#                                 'secretDealOnly': False,
#                                 'suppliers': [],
#                                 'nosOfBedrooms': [],
#                             },
#                             'includedPriceInfo': False,
#                             'occupancy': {
#                                 'adults': 1,
#                                 'children': 0,
#                                 'childAges': [],
#                                 'rooms': 1,
#                                 'childrenTypes': [],
#                             },
#                             'supplierPullMetadata': {
#                                 'requiredPrecheckAccuracyLevel': 0,
#                             },
#                             'mseHotelIds': [],
#                             'ppLandingHotelIds': [],
#                             'searchedHotelIds': [],
#                             'paymentId': -1,
#                             'externalLoyaltyRequest': None,
#                         },
#                         'suggestedPrice': 'Exclusive',
#                     },
#                     'PriceStreamMetaLabRequest': {
#                         'attributesId': [
#                             8,
#                             1,
#                             18,
#                             7,
#                             11,
#                             2,
#                             3,
#                         ],
#                     },
#                 },
#                 'query': 'query citySearch($CitySearchRequest: CitySearchRequest!, $ContentSummaryRequest: ContentSummaryRequest!, $PricingSummaryRequest: PricingRequestParameters, $PriceStreamMetaLabRequest: PriceStreamMetaLabRequest) {\n  citySearch(CitySearchRequest: $CitySearchRequest) {\n    searchResult {\n      sortMatrix {\n        result {\n          fieldId\n          sorting {\n            sortField\n            sortOrder\n            sortParams {\n              id\n            }\n          }\n          display {\n            name\n          }\n          childMatrix {\n            fieldId\n            sorting {\n              sortField\n              sortOrder\n              sortParams {\n                id\n              }\n            }\n            display {\n              name\n            }\n            childMatrix {\n              fieldId\n              sorting {\n                sortField\n                sortOrder\n                sortParams {\n                  id\n                }\n              }\n              display {\n                name\n              }\n            }\n          }\n        }\n      }\n      searchInfo {\n        flexibleSearch {\n          currentDate {\n            checkIn\n            price\n          }\n          alternativeDates {\n            checkIn\n            price\n          }\n        }\n        hasSecretDeal\n        isComplete\n        totalFilteredHotels\n        hasEscapesPackage\n        searchStatus {\n          searchCriteria {\n            checkIn\n          }\n          searchStatus\n        }\n        objectInfo {\n          objectName\n          cityName\n          cityEnglishName\n          countryId\n          countryEnglishName\n          mapLatitude\n          mapLongitude\n          mapZoomLevel\n          wlPreferredCityName\n          wlPreferredCountryName\n          cityId\n          cityCenterPolygon {\n            geoPoints {\n              lon\n              lat\n            }\n            touristAreaCenterPoint {\n              lon\n              lat\n            }\n          }\n        }\n      }\n      urgencyDetail {\n        urgencyScore\n      }\n      histogram {\n        bins {\n          numOfElements\n          upperBound {\n            perNightPerRoom\n            perPax\n          }\n        }\n      }\n      nhaProbability\n    }\n    properties(ContentSummaryRequest: $ContentSummaryRequest, PricingSummaryRequest: $PricingSummaryRequest, PriceStreamMetaLabRequest: $PriceStreamMetaLabRequest) {\n      propertyId\n      sponsoredDetail {\n        sponsoredType\n        trackingData\n        isShowSponsoredFlag\n      }\n      propertyResultType\n      content {\n        informationSummary {\n          hotelCharacter {\n            hotelTag {\n              name\n              symbol\n            }\n            hotelView {\n              name\n              symbol\n            }\n          }\n          propertyLinks {\n            propertyPage\n          }\n          atmospheres {\n            id\n            name\n          }\n          isSustainableTravel\n          localeName\n          defaultName\n          displayName\n          accommodationType\n          awardYear\n          hasHostExperience\n          address {\n            countryCode\n            country {\n              id\n              name\n            }\n            city {\n              id\n              name\n            }\n            area {\n              id\n              name\n            }\n          }\n          propertyType\n          rating\n          agodaGuaranteeProgram\n          remarks {\n            renovationInfo {\n              renovationType\n              year\n            }\n          }\n          spokenLanguages {\n            id\n          }\n          geoInfo {\n            latitude\n            longitude\n          }\n        }\n        propertyEngagement {\n          lastBooking\n          peopleLooking\n        }\n        nonHotelAccommodation {\n          masterRooms {\n            noOfBathrooms\n            noOfBedrooms\n            noOfBeds\n            roomSizeSqm\n            highlightedFacilities\n          }\n          hostLevel {\n            id\n            name\n          }\n          supportedLongStay\n        }\n        facilities {\n          id\n        }\n        images {\n          hotelImages {\n            id\n            caption\n            providerId\n            urls {\n              key\n              value\n            }\n          }\n        }\n        reviews {\n          contentReview {\n            isDefault\n            providerId\n            demographics {\n              groups {\n                id\n                grades {\n                  id\n                  score\n                }\n              }\n            }\n            summaries {\n              recommendationScores {\n                recommendationScore\n              }\n              snippets {\n                countryId\n                countryCode\n                countryName\n                date\n                demographicId\n                demographicName\n                reviewer\n                reviewRating\n                snippet\n              }\n            }\n            cumulative {\n              reviewCount\n              score\n            }\n          }\n          cumulative {\n            reviewCount\n            score\n          }\n        }\n        familyFeatures {\n          hasChildrenFreePolicy\n          isFamilyRoom\n          hasMoreThanOneBedroom\n          isInterConnectingRoom\n          isInfantCottageAvailable\n          hasKidsPool\n          hasKidsClub\n        }\n        personalizedInformation {\n          childrenFreePolicy {\n            fromAge\n            toAge\n          }\n        }\n        localInformation {\n          landmarks {\n            transportation {\n              landmarkName\n              distanceInM\n            }\n            topLandmark {\n              landmarkName\n              distanceInM\n            }\n            beach {\n              landmarkName\n              distanceInM\n            }\n          }\n          hasAirportTransfer\n        }\n        highlight {\n          cityCenter {\n            distanceFromCityCenter\n          }\n          favoriteFeatures {\n            features {\n              id\n              title\n              category\n            }\n          }\n          hasNearbyPublicTransportation\n        }\n        rateCategories {\n          escapeRateCategories {\n            rateCategoryId\n            localizedRateCategoryName\n          }\n        }\n      }\n      soldOut {\n        soldOutPrice {\n          averagePrice\n        }\n      }\n      pricing {\n        pulseCampaignMetadata {\n          promotionTypeId\n          webCampaignId\n          campaignTypeId\n          campaignBadgeText\n          campaignBadgeDescText\n          dealExpiryTime\n          showPulseMerchandise\n        }\n        isAvailable\n        isReady\n        benefits\n        cheapestRoomOffer {\n          agodaCash {\n            showBadge\n            giftcardGuid\n            dayToEarn\n            earnId\n            percentage\n            expiryDay\n          }\n          cashback {\n            cashbackGuid\n            showPostCashbackPrice\n            cashbackVersion\n            percentage\n            earnId\n            dayToEarn\n            expiryDay\n            cashbackType\n            appliedCampaignName\n          }\n        }\n        isEasyCancel\n        isInsiderDeal\n        isMultiHotelEligible\n        suggestPriceType {\n          suggestPrice\n        }\n        roomBundle {\n          bundleId\n          bundleType\n          saveAmount {\n            perNight {\n              ...Frag34igc2aa297ecg4i0f27\n            }\n          }\n        }\n        pointmax {\n          channelId\n          point\n        }\n        priceChange {\n          changePercentage\n          searchDate\n        }\n        payment {\n          cancellation {\n            cancellationType\n            freeCancellationDate\n          }\n          payLater {\n            isEligible\n          }\n          payAtHotel {\n            isEligible\n          }\n          noCreditCard {\n            isEligible\n          }\n          taxReceipt {\n            isEligible\n          }\n        }\n        cheapestStayPackageRatePlans {\n          stayPackageType\n          ratePlanId\n        }\n        pricingMessages {\n          location\n          ids\n        }\n        suppliersSummaries {\n          id\n          supplierHotelId\n        }\n        supplierInfo {\n          id\n          name\n          isAgodaBand\n        }\n        offers {\n          roomOffers {\n            room {\n              extraPriceInfo {\n                displayPriceWithSurchargesPRPN\n                corDisplayPriceWithSurchargesPRPN\n              }\n              availableRooms\n              isPromoEligible\n              promotions {\n                typeId\n                promotionDiscount {\n                  value\n                }\n                isRatePlanAsPromotion\n                cmsTypeId\n                description\n              }\n              bookingDuration {\n                unit\n                value\n              }\n              supplierId\n              corSummary {\n                hasCor\n                corType\n                isOriginal\n                hasOwnCOR\n                isBlacklistedCor\n              }\n              localVoucher {\n                currencyCode\n                amount\n              }\n              pricing {\n                currency\n                price {\n                  perNight {\n                    exclusive {\n                      display\n                      cashbackPrice\n                      displayAfterCashback\n                      originalPrice\n                    }\n                    inclusive {\n                      display\n                      cashbackPrice\n                      displayAfterCashback\n                      originalPrice\n                    }\n                  }\n                  perBook {\n                    exclusive {\n                      display\n                      cashbackPrice\n                      displayAfterCashback\n                      rebatePrice\n                      originalPrice\n                      autoAppliedPromoDiscount\n                    }\n                    inclusive {\n                      display\n                      cashbackPrice\n                      displayAfterCashback\n                      rebatePrice\n                      originalPrice\n                      autoAppliedPromoDiscount\n                    }\n                  }\n                  perRoomPerNight {\n                    exclusive {\n                      display\n                      crossedOutPrice\n                      cashbackPrice\n                      displayAfterCashback\n                      rebatePrice\n                      pseudoCouponPrice\n                      originalPrice\n                    }\n                    inclusive {\n                      display\n                      crossedOutPrice\n                      cashbackPrice\n                      displayAfterCashback\n                      rebatePrice\n                      pseudoCouponPrice\n                      originalPrice\n                    }\n                  }\n                  totalDiscount\n                  priceAfterAppliedAgodaCash {\n                    perBook {\n                      ...Fragj31c6if1h4idc82d781a\n                    }\n                    perRoomPerNight {\n                      ...Fragj31c6if1h4idc82d781a\n                    }\n                  }\n                }\n                apsPeek {\n                  perRoomPerNight {\n                    ...Frag34igc2aa297ecg4i0f27\n                  }\n                }\n                promotionPricePeek {\n                  display {\n                    perBook {\n                      ...Frag34igc2aa297ecg4i0f27\n                    }\n                    perRoomPerNight {\n                      ...Frag34igc2aa297ecg4i0f27\n                    }\n                    perNight {\n                      ...Frag34igc2aa297ecg4i0f27\n                    }\n                  }\n                  discountType\n                  promotionCodeType\n                  promotionCode\n                  promoAppliedOnFinalPrice\n                  childPromotions {\n                    campaignId\n                  }\n                  campaignName\n                }\n                channelDiscountSummary {\n                  channelDiscountBreakdown {\n                    display\n                    discountPercent\n                    channelId\n                  }\n                }\n                promotionsCumulative {\n                  promotionCumulativeType\n                  amountPercentage\n                  minNightsStay\n                }\n              }\n              uid\n              payment {\n                cancellation {\n                  cancellationType\n                }\n              }\n              discount {\n                deals\n                channelDiscount\n              }\n              saveUpTo {\n                perRoomPerNight\n              }\n              benefits {\n                id\n                targetType\n              }\n              channel {\n                id\n              }\n              mseRoomSummaries {\n                supplierId\n                subSupplierId\n                pricingSummaries {\n                  currency\n                  channelDiscountSummary {\n                    channelDiscountBreakdown {\n                      channelId\n                      discountPercent\n                      display\n                    }\n                  }\n                  price {\n                    perRoomPerNight {\n                      exclusive {\n                        display\n                      }\n                      inclusive {\n                        display\n                      }\n                    }\n                  }\n                }\n              }\n              cashback {\n                cashbackGuid\n                showPostCashbackPrice\n                cashbackVersion\n                percentage\n                earnId\n                dayToEarn\n                expiryDay\n                cashbackType\n                appliedCampaignName\n              }\n              agodaCash {\n                showBadge\n                giftcardGuid\n                dayToEarn\n                expiryDay\n                percentage\n              }\n              corInfo {\n                corBreakdown {\n                  taxExPN {\n                    ...Fragf8cf30h64igidd5de53a\n                  }\n                  taxInPN {\n                    ...Fragf8cf30h64igidd5de53a\n                  }\n                  taxExPRPN {\n                    ...Fragf8cf30h64igidd5de53a\n                  }\n                  taxInPRPN {\n                    ...Fragf8cf30h64igidd5de53a\n                  }\n                }\n                corInfo {\n                  corType\n                }\n              }\n              loyaltyDisplay {\n                items\n              }\n              capacity {\n                extraBedsAvailable\n              }\n              pricingMessages {\n                formatted {\n                  location\n                  texts {\n                    index\n                    text\n                  }\n                }\n              }\n              campaign {\n                selected {\n                  campaignId\n                  promotionId\n                  messages {\n                    campaignName\n                    title\n                    titleWithDiscount\n                    description\n                    linkOutText\n                    url\n                  }\n                }\n              }\n              stayPackageType\n            }\n          }\n        }\n      }\n      metaLab {\n        attributes {\n          attributeId\n          dataType\n          value\n          version\n        }\n      }\n      enrichment {\n        topSellingPoint {\n          tspType\n          value\n        }\n        pricingBadges {\n          badges\n        }\n        uniqueSellingPoint {\n          rank\n          segment\n          uspType\n          uspPropertyType\n        }\n        bookingHistory {\n          bookingCount {\n            count\n            timeFrame\n          }\n        }\n        showReviewSnippet\n        isPopular\n        roomInformation {\n          cheapestRoomSizeSqm\n          facilities {\n            id\n            propertyFacilityName\n            symbol\n          }\n        }\n      }\n    }\n    searchEnrichment {\n      suppliersInformation {\n        supplierId\n        supplierName\n        isAgodaBand\n      }\n    }\n    aggregation {\n      matrixGroupResults {\n        matrixGroup\n        matrixItemResults {\n          id\n          name\n          count\n          filterKey\n          filterRequestType\n          extraDataResults {\n            text\n            matrixExtraDataType\n          }\n        }\n      }\n    }\n  }\n}\n\nfragment Fragj31c6if1h4idc82d781a on DisplayPrice {\n  exclusive\n  allInclusive\n}\n\nfragment Frag34igc2aa297ecg4i0f27 on DFDisplayPrice {\n  exclusive\n  allInclusive\n}\n\nfragment Fragf8cf30h64igidd5de53a on DFCorBreakdownItem {\n  price\n  id\n}\n',
#             }

#             res = requests.post(endpoint, data=json.dumps(json_data), headers=headers)
#             output = json.loads(res.text)
#             num_hotel = output['data']['citySearch']['searchResult']['searchInfo']['totalFilteredHotels']
            
#             return num_hotel
        
#         num_hotels = get_num_hotels(city_id)
        




#         urls = output['data']['url']
#         for url in urls:
#             yield scrapy.Request(url=url, callback=self.parse_hotel)
        

#     def parse_hotel(self, response):
#         pass




# """
    
# --------------scraping from Tripadvisor----------------
# class CrawlReviewSpider(scrapy.Spider):
#     name = 'tripadvisor_scraping'
#     allowed_domains = ['tripadvisor.com.vn']
#     start_urls = [
#                     'https://www.tripadvisor.com.vn/Hotels-g293928-Nha_Trang_Khanh_Hoa_Province-Hotels.html',
#                     # 'https://www.tripadvisor.com.vn/Hotels-g298085-Da_Nang-Hotels.html',
#                     # 'https://www.tripadvisor.com.vn/Hotels-g293924-Hanoi-Hotels.html',
#                     # 'https://www.tripadvisor.com.vn/Hotels-g293922-Da_Lat_Lam_Dong_Province-Hotels.html',
#                     # 'https://www.tripadvisor.com.vn/Hotels-g293925-Ho_Chi_Minh_City-Hotels.html',
#                     # 'https://www.tripadvisor.com.vn/Hotels-g2146235-Nghe_An_Province-Hotels.html',
#                     # 'https://www.tripadvisor.com.vn/Hotels-g1554764-Vinh_Nghe_An_Province-Hotels.html',
#                     # 'https://www.tripadvisor.com.vn/Hotels-g2145099-An_Giang_Province-Hotels.html'
#                     # 'https://www.tripadvisor.com.vn/Hotels-g2145104-Ba_Ria_Vung_Tau_Province-Hotels.html',
#                     # 'https://www.tripadvisor.com.vn/Hotels-g5556252-Bac_Lieu_Province_Mekong_Delta-Hotels.html',
#                     # 'https://www.tripadvisor.com.vn/Hotels-g6776104-Bac_Giang_Bac_Giang_Province-Hotels.html',
#                     # 'https://www.tripadvisor.com.vn/Hotels-g2145106-Bac_Ninh_Province-Hotels.html',
#                     # 'https://www.tripadvisor.com.vn/Hotels-g3311193-Binh_Duong_Province-Hotels.html',
#                     # 'https://www.tripadvisor.com.vn/Hotels-g6939209-Binh_Phuoc_Province-Hotels.html',
#                     # 'https://www.tripadvisor.com.vn/Hotels-g303942-Can_Tho_Mekong_Delta-Hotels.html',
#                     # 'https://www.tripadvisor.com.vn/Hotels-g303944-Hai_Phong-Hotels.html',
#                     # 'https://www.tripadvisor.com.vn/Hotels-g2146209-c3-zff17-Hai_Duong_Province-Hotels.html',
#                     # 'https://www.tripadvisor.com.vn/Hotels-g3320435-Hoa_Binh_Hoa_Binh_Province-Hotels.html',
#                     # 'https://www.tripadvisor.com.vn/Hotels-g737052-Lao_Cai_Lao_Cai_Province-Hotels.html',
#                     # 'https://www.tripadvisor.com.vn/Hotels-g2146283-Quang_Ninh_Province-Hotels.html',
#                     # 'https://www.tripadvisor.com.vn/SmartDeals-g303945-Ninh_Binh_Ninh_Binh_Province-Hotel-Deals.html',
#                     # 'https://www.tripadvisor.com.vn/Hotels-g1236104-Thanh_Hoa_Thanh_Hoa_Province-Hotels.html',
#                     # 'https://www.tripadvisor.com.vn/Hotels-g293926-Hue_Thua_Thien_Hue_Province-Hotels.html',
#                     # 'https://www.tripadvisor.com.vn/Hotels-g2062763-Vinh_Yen_Vinh_Phuc_Province-Hotels.html',
#                     # 'https://www.tripadvisor.com.vn/Hotels-g2146363-Vinh_Phuc_Province-Hotels.html',
#                     # 'https://www.tripadvisor.com.vn/Hotels-g800616-Yen_Bai_Yen_Bai_Province-Hotels.html'

#                 ]

#     def parse(self, response):
#         #press show all button
#         driver_path = CHROME_DRIVER_PATH
#         driver = webdriver.Chrome(driver_path)
#         driver.get(response.url)
#         time.sleep(30)
#         try:
#             # seeAll_button = driver.find_element_by_class_name("biGQs._P.ttuOS").click()
#             seeALL_button = driver.find_element(By.CLASS_NAME, 'biGQs._P.ttuOS')
#             seeALL_button.click()
#             time.sleep(30)
#         except:
#             driver.quit()
#             time.sleep(30)

#         #move to hotel link
#         # hotel_links = response.css("div.listing_title > a::attr(href)").extract_first()
#         # if hotel_links:
#         #     yield response.follow(hotel_links, self.parse_hotel)
#         yield from response.follow_all(css="div.listing_title > a::attr(href)", callback=self.parse_hotel)

#         # move to next page of hotel list
#         stdPagination_links = response.css("div.standard_pagination > a::attr(href)").extract_first()
#         if stdPagination_links:
#             yield response.follow(stdPagination_links, self.parse)
#         # yield from response.follow_all(css="div.standard_pagination > a::attr(href)", callback=self.parse)


#     def parse_hotel(self, response):
#         h_name = response.css("h1#HEADING::text").get()
        
#         for review in response.css('div[data-test-target="HR_CC_CARD"]'):
#         # for review in response.css('div[data-test-target="review-tab"]'):
            
#             h_rating = review.css('div[data-test-target="review-rating"] > span::attr(class)').get()
#             # date_review = review.css('div.cRVSd > span::text').get()

#             # if 'đã viết đánh giá vào' in date_review:
#             #     h_date = date_review.replace('đã viết đánh giá vào', '')
#             # else:
#             #     continue
#             h_date = review.css('div.cRVSd > span::text').get()
#             h_date = h_date.replace('đã viết đánh giá vào', '')

#             if h_rating != 'ui_bubble_rating bubble_50' and h_rating is not None:
#                 item = CrawlDataItem()
#                 item['h_rating'] = h_rating
#                 item['h_name'] = h_name
#                 item['h_reviewer_name'] = review.css("div.cRVSd > span > a::text").get()

#                 #get date
#                 # item['h_date'] = review.css('div.EftBQ > span.S4::text').get()
#                 item['h_date'] = h_date

#                 item['h_title_comment'] = review.css('div[data-test-target = "review-title"] > a.Qwuub:first-child > span > span::text').get()
#                 comment = review.css('div.fIrGe._T > q.H4 > span::text').getall()

#                 if comment is None or comment==[''] :
#                     continue
#                 #"load more" button
#                 h_comment = ' '.join(comment)
#                 item['h_comment'] = h_comment

#                 yield item

#             else: 
#                 continue

#         #move to next page of review list
#         review_links = response.css("a.next::attr(href)").extract_first()
#         if review_links:
#             yield response.follow(review_links, self.parse_hotel)



# # ## ----------- scraping for a specific hotel-------
# class CrawlReviewSpider(scrapy.Spider):
#     name = 'review_scraping'
#     allowed_domains = ['tripadvisor.com.vn']
#     start_urls = [
#                     'https://www.tripadvisor.com.vn/Hotel_Review-g293928-d4172546-Reviews-or255-Amiana_Resort_Nha_Trang-Nha_Trang_Khanh_Hoa_Province.html',
#                 #    'https://www.tripadvisor.com.vn/Hotel_Review-g293928-d12682708-Reviews-Ibis_Styles_Nha_Trang-Nha_Trang_Khanh_Hoa_Province.html',
#                     # 'https://www.tripadvisor.com.vn/Hotel_Review-g293928-d15328095-Reviews-Xala_Boutique_Hotel-Nha_Trang_Khanh_Hoa_Province.html',
#                 ]

#     def parse(self, response):
#         # driver_path = CHROME_DRIVER_PATH
#         # driver = webdriver.Chrome(driver_path)
#         # driver.get(response.url)
#         # time.sleep(2)
#         # # # try:
#         # # #     # seeAll_button = driver.find_element_by_class_name("biGQs._P.ttuOS").click()
#         # seeALL_button = driver.find_element(By.CLASS_NAME, 'Ignyf._S.Z')
#         # seeALL_button.click()
#         # # except:
#         #     # driver.quit()
  
#         h_name = response.css("h1#HEADING::text").get()
        
#         for review in response.css('div[data-test-target="HR_CC_CARD"]'):
            
#             # item['h_url'] = h_url
#             h_rating = review.css('div[data-test-target="review-rating"] > span::attr(class)').get()
#             date_review = review.css('div.cRVSd > span::text').get()

#             if 'đã viết đánh giá vào' in date_review:
#                 h_date = date_review.replace('đã viết đánh giá vào', '')
#             else:
#                 continue

#             if h_rating != 'ui_bubble_rating bubble_50' and h_rating is not None:
#                 item = CrawlDataItem()
#                 item['h_rating'] = h_rating
#                 item['h_name'] = h_name
#                 item['h_reviewer_name'] = review.css("div.cRVSd > span > a::text").get()

#                 #get date
#                 # item['h_date'] = review.css('div.EftBQ > span.S4::text').get()
#                 item['h_date'] = h_date

#                 item['h_title_comment'] = review.css('div[data-test-target = "review-title"] > a.Qwuub:first-child > span > span::text').get()
#                 comment = review.css('div.fIrGe._T > q.H4 > span::text').getall()

#                 if comment is None or comment==[''] :
#                     continue
#                 review = ' '.join(comment)
#                 item['h_comment'] = str(review)

#                 yield item
            
#             else: 
#                 continue

#         #move to the next page
#         next_page = response.css("a.next::attr(href)").extract_first()
#         if next_page:
#             # yield scrapy.Request(response.urljoin(next_page), callback=self.parse)
#             yield response.follow(next_page, self.parse)
#         # try:
#         #     next_button = driver.find_element(By.CSS_SELECTOR, 'a.next::attr(href)')
#         #     next_button.click()
#         # except:
#         #     driver.quit()
#         # driver.quit()


