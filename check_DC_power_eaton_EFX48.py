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
                  help="Host name", metavar=' ', default='FPTABC')

(options, args) = parser.parse_args()

# OID
Ac_volt_input1=     ".1.3.6.1.4.1.534.11.1.30.1.4.1"
Ac_volt_input2=     ".1.3.6.1.4.1.534.11.1.30.1.4.2"
Dc_volt_output=     ".1.3.6.1.4.1.534.11.1.80.5.0"
System_curr1=       ".1.3.6.1.4.1.534.11.1.30.1.3.1"
System_curr2=       ".1.3.6.1.4.1.534.11.1.30.1.3.2"
Load_curr1=         ".1.3.6.1.4.1.534.11.1.46.1.6.1"
Load_curr2=         ".1.3.6.1.4.1.534.11.1.46.1.6.2"
Load_curr3=         ".1.3.6.1.4.1.534.11.1.46.1.6.3"
Load_curr4=         ".1.3.6.1.4.1.534.11.1.46.1.6.4"
Load_curr5=         ".1.3.6.1.4.1.534.11.1.46.1.6.5"
Load_curr6=         ".1.3.6.1.4.1.534.11.1.46.1.6.6"
Batt_curr1=         ".1.3.6.1.4.1.534.11.1.41.1.7.1"
Batt_curr2=         ".1.3.6.1.4.1.534.11.1.41.1.7.2"
Batt_curr_limit=    ".1.3.6.1.4.1.534.11.1.40.31.0"
Batt_temp=          ".1.3.6.1.4.1.534.11.1.40.85.0"
Internal_temp=      ".1.3.6.1.4.1.534.11.1.80.7.0"
Serial_Rect1=       ".1.3.6.1.4.1.534.11.1.30.1.2.1"
Serial_Rect2=       ".1.3.6.1.4.1.534.11.1.30.1.2.2"


# Query SNMP

if not options.host or not options.community:
    parser.print_help()
    sys.exit(3)
else:
    sess = netsnmp.Session(Version = 1, DestHost = options.host, Community = options.community, Timeout=1000000, Retries=1)
    # vars =  netsnmp.VarList(
    vars =  [
            Ac_volt_input1,             #0
            Ac_volt_input2,             #1
            Dc_volt_output,             #2
            System_curr1,               #3
            System_curr2,               #4
            Load_curr1,                 #5
            Load_curr2,                 #6
            Load_curr3,                 #7
            Load_curr4,                 #8
            Load_curr5,                 #9
            Load_curr6,                 #10
            Batt_curr1,                 #11
            Batt_curr2,                 #12
            Batt_curr_limit,            #13
            Batt_temp,                  #14
            Internal_temp,              #15
            Serial_Rect1,               #16
            Serial_Rect2                #17
                ]
result =()
for i in vars :
    rst = sess.get(netsnmp.VarList(i))
    # print rst
    result += rst
# print result
# result = sess.get(vars)
# print result

if result[0] == None:
    print('UNKNOW: Host not responding to SNMP request or wrong frimware version !')
    sys.exit(3)
#print result

msg =''
crit_msg=''

Ac_volt_input1 =    float((result[0])/100)
Ac_volt_input2 =    float((result[1])/100)
Dc_volt_output =    float((result[2])/100)
System_curr1 =      float((result[3])/100)
System_curr2 =      float((result[4])/100)
Load_curr1 =        float((result[5]))
Load_curr2 =        float((result[6]))
Load_curr3 =        float((result[7]))
Load_curr4 =        float((result[8]))
Load_curr5 =        float((result[9]))
Load_curr6 =        float((result[10]))
Batt_curr1 =        float((result[11]))
Batt_curr2 =        float((result[12]))
Batt_curr_limit =   float((result[13]))
Batt_temp =         float((result[14])/10)
Internal_temp =     float((result[15])/10)
Serial_Rect1 =      int(result[16])
Serial_Rect2 =      int(result[17])

#Calculation
#-----------#
#1. AC Vol
Ac_volt_input = 0

if Ac_volt_input1 > 0:
    Ac_volt_input = Ac_volt_input1

elif Ac_volt_input2 > 0:
    Ac_volt_input = Ac_volt_input2


#2. Load DC
Load_curr = float((Load_curr1 + Load_curr2 + Load_curr3 + Load_curr4 + Load_curr5 + Load_curr6)/100)


#3. Rectifiers
Number_rect = 0
if Serial_Rect1 > 0 and Serial_Rect2 > 0:
    Number_rect = 2

elif Serial_Rect1 > 0 or Serial_Rect2 > 0:
    Number_rect = 1

else:
    Number_rect = 0

#4. System
if Number_rect > 0:
    System_curr = float((System_curr1 + System_curr2) / Number_rect)


# Compose result message
msg = 'AC-Input=' + str(Ac_volt_input) + ', DC-Output=' + str(Dc_volt_output) + ', System-Curr=' + str(System_curr) + ', Load-Curr=' + str(Load_curr) + ', Batt-Curr-1=' + str(Batt_curr1/100) + ', Batt-Curr-2=' + str(Batt_curr2/100) + ', Batt-Remain=#N/A' + ', Batt-Temp=' + str(Batt_temp) + ', Internal_Temp=' + str(Internal_temp) + ', Rectnumber=' + str(Number_rect) + ', Battery_Type=#N/A' + ', Batt-Curr-Limit= ' + str(Batt_curr_limit)
print(msg)



