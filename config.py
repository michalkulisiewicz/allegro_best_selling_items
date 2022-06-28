'''
Config file containing all xpath selectors needed for scraping
'''
#Selector used to get product_name and url from category
cat_product_selector = '//*[@class="_w7z6o _uj8z7 meqh_en mpof_z0 mqu1_16 m6ax_n4 _6a66d_LX75-  m7er_k4 msa3_z4"]'
#Selector used to get maximum number of pages in category
cat_max_page_selector = '//*[@class="_1h7wt mh36_8 mvrt_8 _6d89c_3i0GV _6d89c_XEsAE"]'
#Selector used to get price of product
product_price_selector = '//*[@class="mli8_k4 msa3_z4 mqu1_1 mp0t_ji m9qz_yo mgmw_qw mgn2_27 mgn2_30_s mpof_vs munh_8 mp4t_4"]'
#Selector used to get shipping price of product
shipping_price_selector = '//*[@class="_5f9aa_PO2es"]'
#Selector used to get number of sold items
number_of_sold_items_selector = '//*[@class="mp0t_0a mqu1_21 mli8_k4 mgn2_13 mgmw_ag mp4t_8"]'