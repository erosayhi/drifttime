import matplotlib.pyplot as plt
import txtfile_parser as tp
import get_data as gd
import seaborn as sns
from scipy.stats import norm
import scipy

# 绘制单个txt文件的offset的概率密度分布图
def draw_1_offset_pdf(filepath: str, topo_id :int):

    sync_records, delay_records = tp.parse_txtfile(filepath, topo_id)

    offset_list = gd.get_offset_list(sync_records, topo_id)

    sample_num = gd.get_min_sample_num(offset_list)

    draw_list = gd.generate_draw_list(1,sample_num,offset_list)

    device_num = gd.TOPO_MID_LIST[topo_id]

    mid_list = gd.generate_mid_list(device_num)

    fig, ax = plt.subplots()

    ax.hist(draw_list, label=mid_list, density=1, stacked=0, bins=100)

    ax.legend()
    ax.set_title('offset概率密度分布')
    plt.show()


# 绘制单个txt文件的gmRateRatio的变化趋势图
def draw_1_gmRR_plot(filepath: str, topo_id :int):

    sync_records, delay_records = tp.parse_txtfile(filepath, topo_id)

    gmRR_list = gd.get_gmRR_list(sync_records, topo_id)

    sample_num = gd.get_min_sample_num(gmRR_list)
    print(sample_num)
    draw_list = gd.generate_draw_list(1,sample_num,gmRR_list)

    device_num = gd.TOPO_MID_LIST[topo_id]

    mid_list = gd.generate_mid_list(device_num)

    fig, ax = plt.subplots()

    for index in range(0,device_num):
        if(len(draw_list[index])!=0):
            ax.plot(range(1, sample_num), draw_list[index], label = mid_list[index])


    ax.legend()
    ax.set_title('gmRateRatio')

    plt.show()


# 绘制单个txt文件的offset的变化趋势
def draw_1_offset_plot(filepath: str, topo_id :int):
    sync_records, delay_records = tp.parse_txtfile(filepath, topo_id)

    offset_list = gd.get_offset_list(sync_records, topo_id)

    sample_num = gd.get_min_sample_num(offset_list)

    draw_list = gd.generate_draw_list(1,sample_num,offset_list)

    device_num = gd.TOPO_MID_LIST[topo_id]

    mid_list = gd.generate_mid_list(device_num)

    fig, ax = plt.subplots()

    for index in range(0,device_num):
        if(len(draw_list[index])!=0):
            ax.plot(range(1, sample_num), draw_list[index], label = mid_list[index])


    ax.legend()
    ax.set_title('offset')
    plt.show()


# 绘制offset逆推的变化趋势
def draw_1_r_gmrr_offset_plot(filepath: str, topo_id :int):
    sync_records, delay_records = tp.parse_txtfile(filepath, topo_id)

    offset_list = gd.get_reverse_gmRR(sync_records, topo_id)

    sample_num = gd.get_min_sample_num(offset_list)
    sample_num = 100

    draw_list = gd.generate_draw_list(1,sample_num,offset_list)

    device_num = gd.TOPO_MID_LIST[topo_id]

    mid_list = gd.generate_mid_list(device_num)

    fig, ax = plt.subplots()

    for index in range(0,device_num):
        if(len(draw_list[index])!=0):
            ax.plot(range(1, sample_num), draw_list[index], label = mid_list[index])


    ax.legend()
    ax.set_title('gmRR caculated by offset')
    plt.show()


# 绘制邻居频比的图
def draw_1_neighbourRateRatio_plot(filepath: str, topo_id :int):
    sync_records, delay_records = tp.parse_txtfile(filepath, topo_id)
    nRR_list = gd.get_neighborRateRatio(delay_records,topo_id)

    sample_num = gd.get_min_sample_num(nRR_list)

    draw_list = gd.generate_draw_list(1,sample_num,nRR_list)

    link_num = len(gd.TOPO_LINK_LIST[topo_id])

    link_list = gd.generate_link_list(topo_id)

    fig, ax = plt.subplots()

    for index in range(0,link_num):
        if(len(draw_list[index])!=0):
            ax.plot(range(1, sample_num), draw_list[index], label = link_list[index])

    ax.legend()
    ax.set_title('Link NeighborRateRatio')
    plt.show()


# 绘制offset分布图，每个设备单独一个子图
def draw_1_offset_pdf_split(filepath: str, topo_id :int):
    sync_records, delay_records = tp.parse_txtfile(filepath, topo_id)
    offset_list = gd.get_offset_list(sync_records,topo_id)

    sample_num = gd.get_min_sample_num(offset_list)

    draw_list = gd.generate_draw_list(1, sample_num, offset_list)

    mid_list = ['N0','N1','N2','N3','N4']

    fig, ax = plt.subplots(1,4)
    color = ['red','gray','green','blue','gold']
    count = 0
    for i in range(0,5):
        if len(draw_list[i]) != 0:
            ax[count].hist(draw_list[i], color = color[i], density=1, stacked=0, bins = 48, label = mid_list[i])
            sns.distplot(draw_list[i], hist=False, kde=False, fit = norm, fit_kws={'color':'black','linestyle':'-'},
                         ax=ax[count])
            # ax[count].set_xlim(-100,100)
            # ax[count].set_ylim(0,0.045)
            mean = round(scipy.mean(draw_list[i]),6)
            var = round(scipy.stats.tstd(draw_list[i]),6)
            name = '$\mu$=' + str(mean) + '  $\sigma$=' + str(var)
            ax[count].set_title(name,fontsize = 16)

            # print(mean,var)
            ax[count].tick_params(labelsize = 16)
            ax[count].legend(loc = 'upper right',fontsize = 16)
            count = count + 1
    plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=0.3, hspace=None)
    fig.set_size_inches(22,4)
    filepath = filepath.split('/')
    t = filepath[2].split('.')
    name = t[0] + '.png'
    plt.savefig(name)
    # plt.show()
    

def draw_boxplot(index):
    D = []
    color = ['red','gray','green','blue','gold']
    sync_records, delay_records = tp.parse_txtfile('./data/oss_test_64ms.txt', 0)
    offset_list = gd.get_offset_list(sync_records, 0)
    sample_num = gd.get_min_sample_num(offset_list)
    draw_list = gd.generate_draw_list(1, sample_num, offset_list)
    D.append(draw_list[index])

    sync_records, delay_records = tp.parse_txtfile('./data/oss_test_32ms.txt', 0)
    offset_list = gd.get_offset_list(sync_records, 0)
    sample_num = gd.get_min_sample_num(offset_list)
    draw_list = gd.generate_draw_list(1, sample_num, offset_list)
    D.append(draw_list[index])

    sync_records, delay_records = tp.parse_txtfile('./data/oss_test_128ms.txt', 0)
    offset_list = gd.get_offset_list(sync_records, 0)
    sample_num = gd.get_min_sample_num(offset_list)
    draw_list = gd.generate_draw_list(1, sample_num, offset_list)
    D.append(draw_list[index])

    sync_records, delay_records = tp.parse_txtfile('./data/oss_test_256ms.txt', 0)
    offset_list = gd.get_offset_list(sync_records, 0)
    sample_num = gd.get_min_sample_num(offset_list)
    draw_list = gd.generate_draw_list(1, sample_num, offset_list)
    D.append(draw_list[index])
    



    # plot
    fig, ax = plt.subplots()
    VP = ax.boxplot(D, positions=[2, 4, 6, 8], widths=1.5, patch_artist=True,
                    showmeans=True, showfliers=False,
                    medianprops={"color": "white", "linewidth": 1},
                    boxprops={"facecolor": color[index], "edgecolor": "white",
                            "linewidth": 0.5},
                    whiskerprops={"color": color[index], "linewidth": 1.5},
                    capprops={"color": color[index], "linewidth": 1.5})
    ax.set_xticklabels(['32ms', '64ms', '128ms', '256ms'])
    ax.tick_params(labelsize=16)

    name = str(index) + '.png'
    plt.savefig(name)
    # plt.show()


def draw_volinplot(index):
    D = []
    color = ['red','gray','green','blue','gold']
    sync_records, delay_records = tp.parse_txtfile('./data/oss_test_64ms.txt', 0)
    offset_list = gd.get_offset_list(sync_records, 0)
    sample_num = gd.get_min_sample_num(offset_list)
    draw_list = gd.generate_draw_list(1, sample_num, offset_list)
    D.append(draw_list[index])

    sync_records, delay_records = tp.parse_txtfile('./data/oss_test_32ms.txt', 0)
    offset_list = gd.get_offset_list(sync_records, 0)
    sample_num = gd.get_min_sample_num(offset_list)
    draw_list = gd.generate_draw_list(1, sample_num, offset_list)
    D.append(draw_list[index])

    sync_records, delay_records = tp.parse_txtfile('./data/oss_test_128ms.txt', 0)
    offset_list = gd.get_offset_list(sync_records, 0)
    sample_num = gd.get_min_sample_num(offset_list)
    draw_list = gd.generate_draw_list(1, sample_num, offset_list)
    D.append(draw_list[index])

    sync_records, delay_records = tp.parse_txtfile('./data/oss_test_256ms.txt', 0)
    offset_list = gd.get_offset_list(sync_records, 0)
    sample_num = gd.get_min_sample_num(offset_list)
    draw_list = gd.generate_draw_list(1, sample_num, offset_list)
    D.append(draw_list[index])


    fig, ax = plt.subplots()
    ax.violinplot(D, positions=[2, 4, 6, 8], widths=1.5, showmedians=True,points=20000)
    # ax.set_xticklabels(['32ms', '64ms', '128ms', '256ms'])
    plt.xticks(ticks=[2,4,6,8],labels=['32ms', '64ms', '128ms', '256ms'])
    ax.tick_params(labelsize=16)
    plt.show()