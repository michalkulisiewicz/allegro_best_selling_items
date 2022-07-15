# Chrome driver version used by selenium, must match installed browser on your system
# Temporary version 102.0.5005.61 of chrome is used as the latest version does not work properly with selenium
chrome_driver_version = '102.0.5005.61'
### Selectors for category scraper
# Selector used to get product_name and url from category
product_selector = '//*[@class="//a[@class="_w7z6o _uj8z7 meqh_en mpof_z0 mqu1_16 m6ax_n4 _6a66d_LX75-  "]'
# Selector used to get price of product
product_price_selector = '//span[@class="mli8_k4 msa3_z4 mqu1_1 mgmw_qw mp0t_ji m9qz_yo mgn2_27 mgn2_30_s"]'
# Selector used to get shipping price of product
shipping_price_selector = '//div[@class="mqu1_g3 mgn2_12"]'
# Selector used to get number of sold items
number_of_sold_items_selector = '//span[@class="msa3_z4 mgn2_12"]'
# Selector used to get maximum number of pages in category
max_page_selector = '//*[@class="_1h7wt mh36_8 mvrt_8 _6d89c_3i0GV _6d89c_XEsAE"]'
# Selector used to toggle view of a list of auctions in category
toggle_view_selector = '//*[@class="_nem5f _1nezw"]'