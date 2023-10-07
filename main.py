import draw_data as dd
import get_data as gd
import txtfile_parser as tp

if __name__ == '__main__':
    # dd.draw_1_offset_pdf('./data/oss_test_gm_mid_2.txt', 0)
    # dd.draw_1_offset_pdf('./data/oss_test_hg.txt', 1)
    # dd.draw_1_gmRR_plot('./data/oss_test_hg.txt', 1)
    # dd.draw_1_offset_plot('./data/oss_test_hg.txt', 1)
    # dd.draw_1_r_gmrr_offset_plot('./data/oss_test_hg.txt', 1)
    # dd.draw_1_offset_plot('./data/oss_test_hg_fs.txt', 1)
    # dd.draw_1_offset_plot('./data/oss_test_hg_no_fs.txt', 1)
    # dd.draw_1_neighbourRateRatio_plot('./data/oss_test_hg_fs.txt', 2)
    # sync_records, delay_records = tp.parse_txtfile('./data/oss_test_hg.txt', 2)
    # nrr_list = gd.get_linkdelay_nrr_list(delay_records,2)
    # for link in nrr_list:
    #     link_name = 
    #     for temp in link:
    #         if temp >= 1:
    #             print ("邻居频比异常：",temp)
    # dd.draw_1_offset_pdf_split('./data/oss_test_gm_mid_0.txt', 0)
    # dd.draw_1_offset_pdf_split('./data/oss_test_gm_mid_1.txt', 0)  
    # dd.draw_1_offset_pdf_split('./data/oss_test_gm_mid_2.txt', 0)
    # dd.draw_1_offset_pdf_split('./data/oss_test_32ms.txt', 0)
    # dd.draw_1_offset_pdf_split('./data/oss_test_64ms.txt', 0)
    # dd.draw_1_offset_pdf_split('./data/oss_test_256ms.txt', 0)

    # dd.draw_boxplot(0)
    # dd.draw_boxplot(1)
    # dd.draw_demo(3)
    # dd.draw_demo(4)

    # dd.draw_volinplot(3)
    dd.draw_1_gmRR_plot('oss_test.txt', 2)