#!/usr/bin/python

from optparse import OptionParser
import netsnmp
import string
import sys

# Parsing argurments
parser = OptionParser()
parser.add_option("-H", dest="host", type="string",
                  help="Hostname/IP Address of device", metavar=' ')

parser.add_option("-c", dest="community", type="string",
                  help="Community string", metavar=' ')

parser.add_option("-t", dest="hostname", type="string",
                 help="Host name", metavar=' ', default='HCMPTEST')

(options, args) = parser.parse_args()

# OID

Rectifier_fail=         ".1.3.6.1.4.1.534.11.1.70.1.6.1"
Multi_rect=             ".1.3.6.1.4.1.534.11.1.70.1.6.2"
Comms_lost=             ".1.3.6.1.4.1.534.11.1.70.1.6.3"
Rect_temp=              ".1.3.6.1.4.1.534.11.1.70.1.6.4"
Fan_fail=               ".1.3.6.1.4.1.534.11.1.70.1.6.30"
AC_fail=                ".1.3.6.1.4.1.534.11.1.70.1.6.29"
Volt_sense=             ".1.3.6.1.4.1.534.11.1.70.1.6.31"
Batt_Test_active=       ".1.3.6.1.4.1.534.11.1.70.1.6.15"
Batt_Test_fail=         ".1.3.6.1.4.1.534.11.1.70.1.6.16"
Batt_Equalising=        ".1.3.6.1.4.1.534.11.1.70.1.6.17"
Batt_Fast_charge=       ".1.3.6.1.4.1.534.11.1.70.1.6.18"
Batt_disconnected=      ".1.3.6.1.4.1.534.11.1.70.1.6.20"
Batt_curr_limit=        ".1.3.6.1.4.1.534.11.1.40.31.0"
String_trip=            ".1.3.6.1.4.1.534.11.1.70.1.6.8"
String_fail=            ".1.3.6.1.4.1.534.11.1.70.1.6.9"
String_low=             ".1.3.6.1.4.1.534.11.1.70.1.6.10"
String_disconnected=    ".1.3.6.1.4.1.534.11.1.70.1.6.11"
Output_fail=            ".1.3.6.1.4.1.534.11.1.70.1.6.6"
Output_disconnected=    ".1.3.6.1.4.1.534.11.1.70.1.6.7"
Output_trip=            ".1.3.6.1.4.1.534.11.1.70.1.6.5"
Low_load=               ".1.3.6.1.4.1.534.11.1.70.1.6.21"
Low_float=              ".1.3.6.1.4.1.534.11.1.70.1.6.22"
High_float=             ".1.3.6.1.4.1.534.11.1.70.1.6.23"
High_load=              ".1.3.6.1.4.1.534.11.1.70.1.6.24"
Over_current=           ".1.3.6.1.4.1.534.11.1.70.1.6.25"
Over_load=              ".1.3.6.1.4.1.534.11.1.70.1.6.26"
Midpoint=               ".1.3.6.1.4.1.534.11.1.70.1.6.12"
Mains_fail=             ".1.3.6.1.4.1.534.11.1.70.1.6.28"
Batt_temp=              ".1.3.6.1.4.1.534.11.1.70.1.6.13"
Sensor_fail=            ".1.3.6.1.4.1.534.11.1.70.1.6.14"
Internal_temp=          ".1.3.6.1.4.1.534.11.1.70.1.6.27"
Dc_volt_output=         ".1.3.6.1.4.1.534.11.1.80.5.0"
LVD_Disconnect=         ".1.3.6.1.4.1.534.11.1.40.20.0"
LVD_Reconnect=          ".1.3.6.1.4.1.534.11.1.40.21.0"
LVD_Fail=               ".1.3.6.1.4.1.534.11.1.40.1.0"

# Query SNMP

if not options.host or not options.community:
    parser.print_help()
    sys.exit(3)
else:
    sess = netsnmp.Session(Version = 1, DestHost = options.host, Community = options.community, Timeout=1000000, Retries=1)
    # vars =  netsnmp.VarList(
    vars =  [
                    Rectifier_fail,                     #0
                    Multi_rect,                         #1
                    Comms_lost,                         #2
                    Rect_temp,                          #3
                    Fan_fail,                           #4
                    AC_fail,                            #5
                    Volt_sense,                         #6
                    Dc_volt_output,                     #7
                    Batt_Test_active,                   #8
                    Batt_Test_fail,                     #9
                    Batt_Equalising,                    #10
                    Batt_Fast_charge,                   #11
                    Batt_disconnected,                  #12
                    Batt_curr_limit,                    #13
                    String_trip,                        #14
                    String_fail,                        #15
                    String_low,                         #16
                    String_disconnected,                #17
                    Output_fail,                        #18
                    Output_disconnected,                #19
                    Output_trip,                        #20
                    Low_load,                           #21
                    Low_float,                          #22
                    High_float,                         #23
                    High_load,                          #24
                    Over_current,                       #25
                    Over_load,                          #26
                    Midpoint,                           #27
                    Mains_fail,                         #28
                    Batt_temp,                          #29
                    Sensor_fail,                        #30
                    Internal_temp,                      #31
                    LVD_Disconnect,                     #32
                    LVD_Reconnect,                      #33
                    LVD_Fail                            #34
                ]
    # vars = netsnmp.VarList(Rectifier_fail,Multi_rect)
result =()
for i in vars :
    rst = sess.get(netsnmp.VarList(i))
    # print rst
    result += rst
# print result
# result = sess.get(vars)
# print result, 'result'


status = ''
#status_code 0 ~ OK, 1 ~ WARNING, 2 ~ CRITICAL, 3 ~ UNKNOW
status_code = 0
msg =''
crit_msg = ''
crit_msg_detail = ''
warn_msg = ''
warn_msg_detail = ''

Rectifier_fail = int(result[0])
Multi_rect = int(result[1])
Comms_lost = int(result[2])
Rect_temp = int(result[3])
Fan_fail = int(result[4])
AC_fail = int(result[5])
Volt_sense = int(result[6])
Dc_volt_output = int(result[7])
Batt_Test_active = int(result[8])
Batt_Test_fail = int(result[9])
Batt_Equalising = int(result[10])
Batt_Fast_charge = int(result[11])
Batt_disconnected = int(result[12])
Batt_curr_limit = int(result[13])
String_trip = int(result[14])
String_fail = int(result[15])
String_low = int(result[16])
String_disconnected = int(result[17])
Output_fail = int(result[18])
Output_disconnected = int(result[19])
Output_trip = int(result[20])
Low_load = int(result[21])
Low_float = int(result[22])
High_float = int(result[23])
High_load = int(result[24])
Over_current = int(result[25])
Over_load = int(result[26])
Midpoint = int(result[27])
Mains_fail = int(result[28])
Batt_temp = int(result[29])
Sensor_fail = int(result[30])
Internal_temp = int(result[31])
LVD_Disconnect = int(result[32])/100
LVD_Reconnect = int(result[33])/100
LVD_Fail = int(result[34])


#Alarm WARNING
if Batt_Test_active >0:
    status_code = 1;
    warn_msg = "WARNING: "
    warn_msg_detail = warn_msg_detail + " Batt_Test_active;"
if Batt_Equalising >0:
    status_code = 1;
    warn_msg = "WARNING: "
    warn_msg_detail = warn_msg_detail + " Batt_Equalising;"
if Batt_Fast_charge >0:
    status_code = 1;
    warn_msg = "WARNING: "
    warn_msg_detail = warn_msg_detail + " Batt_Fast_charge;"
if Batt_disconnected >0:
    status_code = 1;
    warn_msg = "WARNING: "
    warn_msg_detail = warn_msg_detail + " Batt_disconnected;"
if String_low >0:
    status_code = 1;
    warn_msg = "WARNING: "
    warn_msg_detail = warn_msg_detail + " String_low;"
if String_disconnected >0:
    status_code = 1;
    warn_msg = "WARNING: "
    warn_msg_detail = warn_msg_detail + " String_disconnected;"
if Output_disconnected >0:
    status_code = 1;
    warn_msg = "WARNING: "
    warn_msg_detail = warn_msg_detail + " Output_disconnected;"
if Low_load >0:
    status_code = 1;
    warn_msg = "WARNING: "
    warn_msg_detail = warn_msg_detail + " Low_load;"
if Low_float >0:
    status_code = 1;
    warn_msg = "WARNING: "
    warn_msg_detail = warn_msg_detail + " Low_float;"
if High_float >0:
    status_code = 1;
    warn_msg = "WARNING: "
    warn_msg_detail = warn_msg_detail + " High_float;"
if High_load >0:
    status_code = 1;
    warn_msg = "WARNING: "
    warn_msg_detail = warn_msg_detail + " High_load;"
if Midpoint >0:
    status_code = 1;
    warn_msg = "WARNING: "
    warn_msg_detail = warn_msg_detail + " Midpoint;"
if Mains_fail >0:
    status_code = 1;
    warn_msg = "WARNING: "
    warn_msg_detail = warn_msg_detail + " Mains_fail;"
if Batt_temp >0:
    status_code = 1;
    warn_msg = "WARNING: "
    warn_msg_detail = warn_msg_detail + " Batt_temp;"
if Sensor_fail >0:
    status_code = 1;
    warn_msg = "WARNING: "
    warn_msg_detail = warn_msg_detail + " Sensor_fail;"
if Internal_temp >0:
    status_code = 1;
    warn_msg = "WARNING: "
    warn_msg_detail = warn_msg_detail + " Internal_temp;"
if LVD_Disconnect >48:
    status_code = 1;
    warn_msg = "WARNING: "
    warn_msg_detail = warn_msg_detail + " Check-LVD-Disconnect-Setpoint-Config: " + str(LVD_Disconnect) + ";"
if LVD_Reconnect >48:
    status_code = 1;
    warn_msg = "WARNING: "
    warn_msg_detail = warn_msg_detail + " Check-LVD-Reconnect-Setpoint-Config: " + str(LVD_Reconnect) + ";"

#Alarm CRITICAL
if (Rectifier_fail >0) and (AC_fail >0):
    status_code = 2;
    crit_msg = 'CRITICAL: '
    crit_msg_detail = crit_msg_detail + " Rectifier-Failed;"
if (Multi_rect >0) and (AC_fail >0):
    status_code = 2;
    crit_msg = 'CRITICAL: '
    crit_msg_detail = crit_msg_detail + " Multi_rect;"
if (Comms_lost >0) and (AC_fail >0):
    status_code = 2;
    crit_msg = 'CRITICAL: '
    crit_msg_detail = crit_msg_detail + " Comms_lost;"
if (Rect_temp >0) and (AC_fail >0):
    status_code = 2;
    crit_msg = 'CRITICAL: '
    crit_msg_detail = crit_msg_detail + " Rect_temp;"
if (Fan_fail >0) and (AC_fail >0):
    status_code = 2;
    crit_msg = 'CRITICAL: '
    crit_msg_detail = crit_msg_detail + " Rect-Fan-fail;"
if (Volt_sense >0) and (AC_fail >0):
    status_code = 2;
    crit_msg = 'CRITICAL: '
    crit_msg_detail = crit_msg_detail + " Volt_sense;"
if (Batt_Test_fail >0):
    status_code = 2;
    crit_msg = 'CRITICAL: '
    crit_msg_detail = crit_msg_detail + " Battery-Test-Fail;"
if (Batt_curr_limit >10):
    status_code = 2;
    crit_msg = 'CRITICAL: '
    crit_msg_detail = crit_msg_detail + " Battery-Charge-Current-High;"
if (Batt_curr_limit <5)
    status_code = 2;
    crit_msg = 'CRITICAL: '
    crit_msg_detail = crit_msg_detail + " Battery-Charge-Current-Low;"
if (String_trip >0):
    status_code = 2;
    crit_msg = 'CRITICAL: '
    crit_msg_detail = crit_msg_detail + " String-Trip;"
if (String_fail >0):
    status_code = 2;
    crit_msg = 'CRITICAL: '
    crit_msg_detail = crit_msg_detail + " String-Fail;"
if (Output_fail >0):
    status_code = 2;
    crit_msg = 'CRITICAL: '
    crit_msg_detail = crit_msg_detail + " Output-Fail;"
if (Output_trip >0):
    status_code = 2;
    crit_msg = 'CRITICAL: '
    crit_msg_detail = crit_msg_detail + " Output-Trip;"
if (Over_current >0):
    status_code = 2;
    crit_msg = 'CRITICAL: '
    crit_msg_detail = crit_msg_detail + " Over-Current;"
if (Over_load >0):
    status_code = 2;
    crit_msg = 'CRITICAL: '
    crit_msg_detail = crit_msg_detail + " Over-Load;"
if (LVD_Fail >0):
    status_code = 2;
    crit_msg = 'CRITICAL: '
    crit_msg_detail = crit_msg_detail + " LVD-Fail;"

#Check alarm
if (crit_msg != '') and (warn_msg != ''):
    status = crit_msg + crit_msg_detail + ' -- ' + warn_msg + warn_msg_detail
if (crit_msg != '') and (warn_msg == ''):
    status = crit_msg + crit_msg_detail
if (crit_msg == '') and (warn_msg != ''):
        status = warn_msg + warn_msg_detail
if (crit_msg == '') and (warn_msg == ''):
    status = "OK"

# Compose result message
msg = status
print(msg)
sys.exit(status_code)


## Battery-Charge-Current-High  	CRITICAL	Ngưỡng dòng sạc cài lớn hơn 10A.
## Battery-Charge-Current-Low	    CRITICAL	Ngưỡng dòng sạc cài nhỏ hơn 5A.
## Battery-Test-Fail	            CRITICAL	Test ắc quy bị lỗi.
## Comms lost	                    CRITICAL	Khi Rect mất kết nối nối với bộ giám sát của nguồn thì cảnh báo sẽ được kích hoạt
## LVD-Fail	                        CRITICAL	Ngưỡng LVD thấp/Điện áp Accu/Pin Lithium xuống thấp hơn ngưỡng LVD.
## Multi rect	                    CRITICAL	Một hoặc nhiều Rect ở trạng thái Failed.
## Output-Fail	                    CRITICAL	Khi ouput trạng thái tắt và dòng đi.ện đo được lớn hơn 3A thì cảnh báo lỗi tải được raise lên
## Output-Trip	                    CRITICAL	Khi bất cứ ngỏ ra nào ở trạng thái quá dòng đỉnh.
## Over-Current	                    CRITICAL	Dòng của nguồn quá 55A trong vòng 20s
## Over-Load	                    CRITICAL	Khi công suất cấp ra bởi module nguồn lớn hơn công suất cài đặt.
## Rect temp                        CRITICAL	Rect bị quá nhiệt.
## Rect-Fan-fail	                CRITICAL	Quạt Rectifier hỏng.
## Rectifier-Failed	                CRITICAL	Rectifier nguồn hỏng.
## String-Fail	                    CRITICAL	Lỗi sạc, ngỏ kết nối bình disconnect, nhưng vẫn có dòng +-3A.
## String-Trip	                    CRITICAL	Lỗi dòng của Accu/Pin vượt ngưỡng Trip tức thời.
## Volt sense	                    CRITICAL	Lỗi module đọc điện áp của nguồn
## Batt disconnected	                 WARNING	Pin/Accu mất kết nối với nguồn
## Batt Equalising                       WARNING	Cảnh báo không cân bằng các tổ accu
## Batt Fast charge	                     WARNING	Cảnh báo chức năng sạc nhanh accu đang kích hoạt
## Batt temp	                         WARNING	Cảnh báo nhiệt độ quá giới hạn trên và dưới theo ngưỡng cài đặt
## Batt Test active	                     WARNING	Cảnh báo trạnh thái Test Accu đang thực hiện
## Check LVD Disconnect Setpoint Config	 WARNING	Cảnh báo cài đặt sai ngưỡng LVD
## Check LVD Reconnect Setpoint Config	 WARNING	Cảnh báo cài đặt sai ngưỡng LVD
## High float	                         WARNING	Điện áp nguồn lớn hơn ngưỡng High Float
## High load	                         WARNING	Điện áp nguồn lớn hơn ngưỡng High Load
## Internal temp	                     WARNING	Cảnh báo quá nhiệt bên trong nguồn
## Low float	                         WARNING	Điện áp nguồn thấp hơn ngưỡng Low float
## Low load	                             WARNING	Điện áp nguồn thấp hơn ngưỡng Low Load
## Mains fail	                         WARNING	Lỗi nguồn AC delay
## Midpoint	                             WARNING
## Output disconnected	                 WARNING	Mất kết nối với output
## Sensor fail	                         WARNING	Lỗi sensor nhiệt độ Bình
## String disconnected	                 WARNING	Battery ngắt kết nối
## String low	                         WARNING	Điện áp bình nhỏ hơn ngưỡng LVD Disconnect
