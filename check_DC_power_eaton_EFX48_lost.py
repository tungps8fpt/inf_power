#!/usr/bin/python

from optparse import OptionParser
import netsnmp
import string
import sys
import time
import http.client
import os
#sys.exit(0)
# Parsing argurments
parser = OptionParser()
parser.add_option("-H", dest="host", type="string",
                  help="Hostname/IP Address of device", metavar=' ')

parser.add_option("-c", dest="community", type="string",
                  help="Community string", metavar=' ')

parser.add_option("-t", dest="hostname", type="string",
                  help="Host name", metavar=' ', default='HCMPxxx')


(options, args) = parser.parse_args()

# OID

AC_fail=                ".1.3.6.1.4.1.534.11.1.70.1.6.29"
Batt_Test_active=       ".1.3.6.1.4.1.534.11.1.70.1.6.15"
Gpip_Eaton_4 =          ".1.3.6.1.4.1.534.11.1.70.1.6.35"
Gpip_Eaton_5 =          ".1.3.6.1.4.1.534.11.1.70.1.6.36"
Ac_volt_input1=         ".1.3.6.1.4.1.534.11.1.30.1.4.1"
Ac_volt_input2=         ".1.3.6.1.4.1.534.11.1.30.1.4.2"
Dc_volt_output=         ".1.3.6.1.4.1.534.11.1.80.5.0"
Batt_curr1=             ".1.3.6.1.4.1.534.11.1.41.1.7.1"
Batt_curr2=             ".1.3.6.1.4.1.534.11.1.41.1.7.2"

# Query SNMP

if not options.host or not options.community:
    parser.print_help()
    sys.exit(3)
else:
    sess = netsnmp.Session(Version = 1, DestHost = options.host, Community = options.community, Timeout=1000000, Retries=1)
    # vars =  netsnmp.VarList(
    vars =  [
            AC_fail,                        #0
            Batt_Test_active,               #1
            Gpip_Eaton_4,                   #2
            Gpip_Eaton_5,                   #3
            Ac_volt_input1,                 #4
            Ac_volt_input2,                 #5
            Dc_volt_output,                 #6
            Batt_curr1,                     #7
            Batt_curr2                      #8
            ]

result =()
for i in vars :
    rst = sess.get(netsnmp.VarList(i))
    # print rst
    result += rst

# print result

status = ''
#status_code 0 ~ OK, 1 ~ WARNING, 2 ~ CRITICAL, 3 ~ UNKNOW
status_code = 0
msg =''
crit_msg=''

Ac_phase1_lost = int(result[0])
Batt_Test_active = int(result[1])
Relay_ac = int(result[2]) # Relay_AC
Relay_mpd = int(result[3]) # Relay_MPD
Ac_volt_input1 = float(result[4])/100
Ac_volt_input2 = float(result[5])/100
Dc_volt_output = float(result[6])/100
Batt_curr1 = float(result[7])
Batt_curr2 = float(result[8])

Batt_Curr = float(Batt_curr1 + Batt_curr2)/100

#GPIP4 dau truoc AC
#GPIP5 dau truoc MPD
#CO DIEN LUOI,KHONG CHAY MAY PHAT : ac_phase1_lost=0, relay_ac=0, relay_mpd=0
#CUP DIEN, CHAY BINH : ac_phase1_lost=1, relay_ac=1, relay_mpd=0
#CUP DIEN, DANG CHAY MAY PHAT : ac_phase1_lost=0, relay_ac=1, relay_mpd=1
#CO DIEN LUOI, DANG CHAY MAY PHAT : ac_phase1_lost=0, relay_ac=0, relay_mpd=1

if (Ac_phase1_lost == 1):
    status = status + 'CUP DIEN - CHAY BINH'
    status_code = 2

elif (Ac_phase1_lost == 0):
    if Batt_Test_active == 1:
        status = status + 'WARNING: Battery-Test'
        status_code = 1
    else:
        if Relay_ac == 0:
            if (Relay_mpd == 0):
                status = status + 'DANG CO DIEN LUOI AC'
                status_code = 0
            else : # (relay_mpd == '1')
                status = status + 'WARNING: KIEM TRA MAY PHAT'
                status_code = 1
        else : #(relay_ac == '1')
            if (Relay_mpd == 1):
                status = status + 'WARNING: CUP DIEN-DANG CHAY MAY PHAT'
                status_code = 1
            else : #(relay_mpd == '0')
                status = status + 'WARNING: Relay AC - Error'
                status_code = 1
else:
    status = status + 'Check-SNMP-AC-phase-lost'
    status_code = 3

msg = status + ' - AC-Input=' + str(Ac_volt_input1) + ', DC-Output=' + str(Dc_volt_output) + ', Batt-Curr=' + str(Batt_Curr)

print(msg)
sys.exit(status_code)
#Truyen du lieu qua inside :
#CUP DIEN - CHAY BINH -> 2
#DANG CO DIEN LUOI AC -> 0
#DANG CO DIEN LUOI-DANG CHAY MAY PHAT ->3
#CUP DIEN-DANG CHAY MAY PHAT -> 1
#Replay_AC hong



