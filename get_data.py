TOPO_MID_LIST = [5,3,4]
TOPO_LINK_LIST = [[(0,0),(0,1),(0,3),(2,0),(4,0),(3,0),(1,3),(1,0)],[(0,0),(1,0),(1,1),(2,0)],[(1,0),(1,1)]]


# 统计offset数据
def get_offset_list(sync_records: list, topo_id):
    offset_list = []
    
    for item in range(0,TOPO_MID_LIST[topo_id]):
        offset_list_item = []
        offset_list.append(offset_list_item)

    for record in sync_records:
        index = int(record[0])
        offset_list[index].append(int(record[2]))

    return offset_list


# 统计gmRateRatio数据
def get_gmRR_list(sync_records: list, topo_id):
    gmRR_list = []

    for item in range(0,TOPO_MID_LIST[topo_id]):
        gmRR_list_item = []
        gmRR_list.append(gmRR_list_item)

    for record in sync_records:
        index = int(record[0])
        gmRR_list[index].append(float(record[7]))

    return gmRR_list


# 统计链路延时测量的数据
def get_linkdelay_list(delay_records: list, topo_id):
    link_delay_list = []

    for index in range(0, len(TOPO_LINK_LIST[topo_id])):
        link_delay_list_item = []
        link_delay_list.append(link_delay_list_item)

    topo_link = TOPO_LINK_LIST[topo_id]

    for record in delay_records:
        link_begin = record[0]
        port = int(record[2])
        link = (link_begin,port)
        for index in range(0, len(TOPO_LINK_LIST[topo_id])):
            if topo_link[index] == link:
                link_delay_list[index].append(int(record[3]))

    return link_delay_list

# 统计链路的邻居频比
def get_linkdelay_nrr_list(delay_records: list, topo_id):
    link_delay_list = []

    for index in range(0, len(TOPO_LINK_LIST[topo_id])):
        link_delay_list_item = []
        link_delay_list.append(link_delay_list_item)

    topo_link = TOPO_LINK_LIST[topo_id]

    for record in delay_records:
        link_begin = record[0]
        port = int(record[2])
        link = (link_begin,port)
        for index in range(0, len(TOPO_LINK_LIST[topo_id])):
            if topo_link[index] == link:
                link_delay_list[index].append(float(record[6]))

    return link_delay_list


# 生成需要要画图的样本列表
def generate_draw_list(begin: int, sample_num: int, src_list):
    re_list = []
    for temp in src_list:
        l = temp[begin:sample_num]
        re_list.append(l)
    return re_list


# 找到样本数量的最小值
def get_min_sample_num(src_list):
    min = 99999999
    for item in src_list:
        if len(item) < min and len(item) != 0:
            min = len(item)
    return min


# 生成MID的标号列表
def generate_mid_list(device_num: int):
    mid_list = []
    for index in range(0,device_num):
        str_temp = 'MID_' + str(index)
        mid_list.append(str_temp)
    return mid_list

# 生成LINK的标号列表
def generate_link_list(topo_id):
    mid_list = []
    links = TOPO_LINK_LIST[topo_id]
    for index in range(0,len(links)):
        link = links[index]
        str_temp = 'LINK_' + str(link[0]) + '_' + str(link[1])
        mid_list.append(str_temp)
    return mid_list


# offset反推gmRR
def get_reverse_gmRR(sync_records: list, topo_id):
    offset_list = []
    
    for item in range(0,TOPO_MID_LIST[topo_id]):
        offset_list_item = []
        offset_list.append(offset_list_item)

    for record in sync_records:
        index = int(record[0])
        offset_list[index].append(1/(1-float(record[2])/128000000))

    return offset_list

# 将链路延时测量的时间戳字符串转化为int型变量
# 93sec706906832ns
def delay_ts_2_int(timestamp: str):
    temp = timestamp.split('sec')
    second = int(temp[0])
    nanosecond = int(temp[1].split('ns')[0])
    return (second,nanosecond)

# 计算时间戳的差值
def calculate_ts_minus(timestamp1, timestamp2):
    ts1 = delay_ts_2_int(timestamp1)
    ts2 = delay_ts_2_int(timestamp2)
    return (ts1[0]*1000000000 + ts1[0])-(ts2[0]*1000000000 + ts2[0])


# 获取每条链路的邻居频比
def get_neighborRateRatio(delay_records: list, topo_id):
    nRR_list = []

    link_num = len(TOPO_LINK_LIST[topo_id])
    links = TOPO_LINK_LIST[topo_id]

    for i in range(0,link_num):
        nRR_list_item = []
        nRR_list.append(nRR_list_item)
    
    for record in delay_records:
        mid = record[0]
        port = int(record[2])
        for index in range(0,link_num):
            if (mid, port) == links[index]:
                nRR_list[index].append(abs(float(record[6])-1))
    
    return nRR_list


# 获取每条链路的链路延时
def get_link_delay(delay_records: list, topo_id):
    ld_list = []

    link_num = len(TOPO_LINK_LIST[topo_id])
    links = TOPO_LINK_LIST[topo_id]

    for i in range(0,link_num):
        ld_list_item = []
        ld_list.append(ld_list_item)
    
    for record in delay_records:
        mid = record[0]
        port = int(record[2])
        for index in range(0,link_num):
            if (mid, port) == links[index]:
                ld_list[index].append(int(record[3]))  
    return ld_list