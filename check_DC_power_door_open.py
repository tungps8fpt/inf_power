#!/usr/bin/python

from optparse import OptionParser
import netsnmp
import string
import sys, os
import httplib


# Parsing argurments
parser = OptionParser()
parser.add_option("-H", dest="host", type="string",
                  help="Hostname/IP Address of device", metavar=' ')

parser.add_option("-c", "-C", dest="community", type="string",
                  help="Community string", metavar=' ')

(options, args) = parser.parse_args()

for option in ('host', 'community'):
    if not getattr(options, option):
        print 'Option %s not specified' % option
        parser.print_help()
        sys.exit(3)

sess = netsnmp.Session(Version = 1, DestHost = options.host, Community = options.community,     Timeout=10000000, Retries=3)

var = netsnmp.VarList(".1.3.6.1.2.1.1.1.0")
#var = netsnmp.VarList('sysDescr.0')


result = sess.get(var)
# print result,'result_door'

if result[0] == None:
        print 'UNKNOW: Host not responding to SNMP request (sysDecr)'
        sys.exit(3)
else:
        sysDescr = result[0]
        #print sysDescr

GPIP6 = 0

if sysDescr == 'SC200 Controller - software version 3.10' or sysDescr == 'SC200 Controller - software version 3.14' or sysDescr == 'SC200 Controller - software version 4.02' or sysDescr == 'SC200 Controller - software version 4.04':
        Gpip_Eaton = ".1.3.6.1.4.1.1918.2.13.10.90.40.1.20.6"  #eaton
        result = sess.get(netsnmp.VarList(Gpip_Eaton))
        GPIP6 = int(result[0])

#update Eaton 1U
elif sysDescr =='Eaton EFX48':
        Gpip_Eaton_2 = ".1.3.6.1.4.1.534.11.1.70.1.6.33"
        Gpip_Eaton_3 = ".1.3.6.1.4.1.534.11.1.70.1.6.34"
        var1 = sess.get(netsnmp.VarList(Gpip_Eaton_2))
        var2 = sess.get(netsnmp.VarList(Gpip_Eaton_3))
        result = var1 + var2
        if int(result[0] == 1):
            GPIP6 = int(result[0])
        elif int(result[1] == 1):
            GPIP6 = int(result[1])
        else:
            status = 'OK'

elif sysDescr =='Enatel SM32 SNMP Agent' :
        version_fw = ".1.3.6.1.4.1.21940.1.5.1.0" # NT1 old <> 65
        var1 = sess.get(netsnmp.VarList(version_fw))
        if (var1[0] == '') or (var1[0] == None) :
            Gpip6_Enatel = ".1.3.6.1.4.1.21940.2.2.2.5"
            Gpip2_Enatel = ".1.3.6.1.4.1.21940.2.2.2.1"
            Gpip3_Enatel = ".1.3.6.1.4.1.21940.2.2.2.2"
            var2 = sess.get(netsnmp.VarList(Gpip6_Enatel))
            var3 = sess.get(netsnmp.VarList(Gpip2_Enatel))
            var4 = sess.get(netsnmp.VarList(Gpip3_Enatel))
            result = var2 + var3 + var4
            if (int(result[0]) == 1):
                GPIP6 = int(result[0])
            elif (int(result[1]) == 1) :
                GPIP6 = int(result[1])
            elif (int(result[2]) == 1):
                GPIP6 = int(result[2])
            else:
                status = 'OK'
        else : # <> None
                Check_Enatel = int(var1[0])
                if (Check_Enatel == 65 or Check_Enatel == 112 or Check_Enatel == 118) :
                        Gpip_Enatel_NT = ".1.3.6.1.4.1.21940.2.11.1.0" #
                        result = sess.get(netsnmp.VarList(Gpip_Enatel_NT))
                        GPIP6 = int(result[0])
                else :
                        print 'UNKNOW: Check software version !'
                        sys.exit(3)


elif sysDescr =='Enatel SM3X NT2 SNMP Agent':
        Gpip_Enatel_NT2 = ".1.3.6.1.4.1.21940.2.11.1.0" #
        result = sess.get(netsnmp.VarList(Gpip_Enatel_NT2))
        GPIP6 = int(result[0])

elif sysDescr =='Enatel SM22 SNMP Agent':
        Gpip_Enatel_SM22 = ".1.3.6.1.4.1.21940.1.2.1.27.0" #
        result = sess.get(netsnmp.VarList(Gpip_Enatel_SM22))
        GPIP6 = int(result[0])
else:
        print 'UNKNOW: Unknown switch type ' + sysDesrc
        sys.exit(3)

status = 'OK'
status_code = 0
#status_code 0 ung voi OK, 1 voi WARNING, 2 voi CRITICAL, 3 voi UNKNOW
msg =''
crit_msg=''

if (GPIP6 == 1): status = "Open-Door" ; status_code = 1;
elif (GPIP6 & 32) : status = "Open-Door" ; status_code = 1;
elif (GPIP6 & 6) : status = "Open-Door" ; status_code = 1;
elif (GPIP6 & 4) : status = "Open-Door" ; status_code = 1;
elif (GPIP6 & 2) : status = "Open-Door" ; status_code = 1;
else:
        status = "OK" ;
msg = status
print msg
sys.exit(status_code)
