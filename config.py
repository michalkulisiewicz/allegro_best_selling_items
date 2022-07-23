# Chrome driver version used by selenium, must match installed browser on your system
# Temporary version 102.0.5005.61 of chrome is used as the latest version does not work properly with selenium
chrome_driver_version = '102.0.5005.61'
### Selectors for category scraper
# Selector used to accept cookies policy
accept_cookies_selector = '//*[@class="mgn2_14 mp0t_0a m9qz_yp mp7g_oh mse2_40 mqu1_40 mtsp_ib mli8_k4 mp4t_0 munh_0 ' \
                          'm911_5r mefy_5r mnyp_5r mdwl_5r msbw_2 mldj_2 mtag_2 mm2b_2 mqvr_2 msa3_z4 mqen_m6 meqh_en ' \
                          'm0qj_5r mh36_16 mvrt_16 mg9e_0 mj7a_0 mjir_sv m2ha_2 m8qd_qh mjt1_n2 b1vf8 mgmw_9u ' \
                          'msts_enp mrmn_qo mrhf_u8 m31c_kb m0ux_fp bnpxh m7er_0k m7er_56_s mjru_k4 _158e2_rNMWZ ' \
                          'mryx_24 mryx_0_s m3h2_0 m3h2_16_s"] '
# Selector used to get a parent from which all product scraping is done
parent_product_selector = '//*[@class="mpof_ki mqen_m6 mp7g_oh mh36_8 mvrt_8 mg9e_8 mj7a_8 m7er_k4 mjyo_6x _1y62o ' \
                          '_6a66d_snEkI _6a66d_wdSAd"] '
# Selector used to get product_name and url from parent product selector
child_product_selector = '//a[@class="_w7z6o _uj8z7 meqh_en mpof_z0 mqu1_16 m6ax_n4 _6a66d_LX75-  "]'
# Selector used to get price of product from parent product selector
product_price_selector = '//span[@class="mli8_k4 msa3_z4 mqu1_1 mgmw_qw mp0t_ji m9qz_yo mgn2_27 mgn2_30_s"]'
# Selector used to get shipping price of product from parent product selector
shipping_price_selector = '//div[@class="mqu1_g3 mgn2_12"]'
# Selector used to get number of sold items from parent product selector
number_of_sold_items_selector = '//span[@class="msa3_z4 mgn2_12"]'
# Selector used to get maximum number of pages in category
max_page_selector = '//*[@class="_1h7wt mh36_8 mvrt_8 _6d89c_3i0GV _6d89c_XEsAE"]'
# Selector used to toggle view of a list of auctions in category
toggle_view_selector = '//*[@class="_nem5f _1nezw"]'