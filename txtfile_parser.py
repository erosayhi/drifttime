# 文本文件的标志字符串，判断每行的内容
DEBUG_MSG = 'debug message'
SYNC_MSG = 'sync info'
DELAY_MSG = 'delay info'


# 每个设备参与同步的端口数量
TOPO_PORT_NUM_LIST = [(3,2,1,1,1),(1,2,1),(1,2,2,1)]


# 获取延时测量信息的MID以及测量周期数，格式如下
# delay info: hcp_mid = 3, serial_number = 1
def get_delay_info_mid(line: str):
    props = line.split(',')
    hcp_mid_str = props[0].split('=')
    serial_number_str = props[1].split('=')
    hcp_mid = int(hcp_mid_str[1].replace(" ",""))
    serial_number = int(serial_number_str[1].replace(" ",""))
    return hcp_mid,serial_number


# 解析端口的链路延时测量信息，格式如下
# port = 0, delay = 1916,sub_t1_t4=7640,sub_t2_t3=3808,neighbor_rate=0.0000000000,max_neighbor_rate=0.0000000000 
# t1 = 93 sec 706906832 ns, t2 = 93 sec 887089208 ns,t3 = 93 sec 887093016 ns,t4 = 93 sec 706914472 ns,last_t3 = 0 sec 0 ns,last_t4 = 0 sec 0 ns 
# port = 2, delay = 1916,sub_t1_t4=7640,sub_t2_t3=3808,neighbor_rate=0.0000000000,max_neighbor_rate=0.0000000000 
# t1 = 93 sec 706906832 ns, t2 = 93 sec 887089208 ns,t3 = 93 sec 887093016 ns,t4 = 93 sec 706914472 ns,last_t3 = 0 sec 0 ns,last_t4 = 0 sec 0 ns 
def port_delay_info_parse(line: str, hcp_mid, serial_number):
    props = line.split(',')
    record = [hcp_mid, serial_number]
    for prop in props:
        result = prop.split('=')
        result_1 = result[1].replace(" ","")
        record.append(result_1)
    return record


# 解析同步状态信息，格式如下
# sync info: hcp_mid = 1, serial_number=4 ,offset = -65,sync_flag = 0,count = 0,last_hop_cmRate=0,cur_hop_cmRate=2098042,rate_ratio= 1.0000009541,corr_fre=8.000008 
# TODO：sync报文中的时间戳和驻留延时
def sync_info_parse(line: str):
    props = line.split(',')
    record = []
    for prop in props:
        result = prop.split('=')
        result_1 = result[1].replace(" ","")
        record.append(result_1)
    return record



# 解析同步上报的txt文本文件，返回同步记录和链路延时测量记录
def parse_txtfile(filepath: str, topo_id):
    sync_records = []     #文本文件包含的同步信息
    delay_records = []    #文本文件包含的延时信息

    file = open(filepath)   #打开同步过程产生的文本文件
    line = file.readline()  #读取文件的第一行

    port_num_list = TOPO_PORT_NUM_LIST[topo_id]  #根据拓扑的ID确定每个设备参与同步的端口数量


    # 循环读取文本文件的下一行
    # 根据每一行的关键字信息进行不同的解析
    while line:
        if DEBUG_MSG in line:
            print("Debug msg")
        elif SYNC_MSG in line:
            sync_records.append(sync_info_parse(line))
        elif DELAY_MSG in line:
            hcp_mid, serial_number = get_delay_info_mid(line)
            port_num = port_num_list[hcp_mid]
            # 根据端口的数量继续读端口的状态
            for index in range(0,port_num):
                line1 = file.readline()
                line1 = line1.replace('\n','').replace('\r','')
                line2 = file.readline()
                line2 = line2.replace('\n','').replace('\r','')
                line1 = line1 + ',' + line2
                delay_records.append(port_delay_info_parse(line1, hcp_mid, serial_number))
        else:
            print("Exception Line")
            print(line)
        line = file.readline()
    # 读完文件并释放文件句柄
    file.close()
    return sync_records,delay_records