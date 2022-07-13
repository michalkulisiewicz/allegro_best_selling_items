'''
Config file containing all xpath selectors
'''
###Selectors for category scraper
#Selector used to get product_name and url from category
cat_product_selector = '//*[@class="_w7z6o _uj8z7 meqh_en mpof_z0 mqu1_16 m6ax_n4 _6a66d_LX75-  m7er_k4 msa3_z4"]'
#Selector used to get maximum number of pages in category
cat_max_page_selector = '//*[@class="_1h7wt mh36_8 mvrt_8 _6d89c_3i0GV _6d89c_XEsAE"]'

###Selectors for auction scraper
#Selector used to get price of product
product_price_selector = '//*[@class="mli8_k4 msa3_z4 mqu1_1 mp0t_ji m9qz_yo mgmw_qw mgn2_27 mgn2_30_s mpof_vs munh_8 mp4t_4"]'
#Selector used to get shipping price of product
shipping_price_selector = '//*[@class="_5f9aa_PO2es" and contains(text(), "Dostawa")]'
#Selector used to get number of sold items
number_of_sold_items_selector = '//*[@class="mp0t_0a mqu1_21 mli8_k4 mgn2_13 mgmw_ag mp4t_8"]'
#Selector used to get name of the seller
name_of_the_seller_selector = '//*[@class="mp0t_ji m9qz_yq mgn2_16 mgn2_17_s munh_0 m3h2_0 mp4t_0 mryx_8 mqu1_1j mgmw_wo "]'
#Selector used to get rating, num of reviews and number of ratings
product_rating_selector = '//*[@class="mpof_ki mwdn_1"]'
#Selector used to get description element needed for further scraping
description_selector = '//*[@class="mp0t_ji munh_0 m3h2_0 mqu1_1j mgn2_21 mgn2_25_s m9qz_yo mryx_16 mgmw_wo mp4t_0 msts_n7" and contains(text(),"Opis")]'
#Selector used to get first image of product from auction
product_img_selector = '//*[@class="msub_k4 mupj_5k mjru_k4 mse2_k4 mp7g_f6 mq1m_0 mj7u_0 m7er_k4 lazyloaded"]'
#Selector used to get a number of auction being scraped from
auction_number_selector = '//*[@class="mgn2_14 mp0t_0a mqu1_21 mgmw_wo mli8_k4 mp4t_0 m3h2_0 munh_0 mryx_16 _5b60e_OlIZ- " and contains(text(), "Numer oferty:")]'