#!/usr/bin/python

from optparse import OptionParser
import netsnmp
import sys, os
import commands

# Exit statuses recognized by Nagios
OK = 0
WARNING = 1
CRITICAL = 2
UNKNOWN = 3

sysDesrc = ''
Eaton_Descr_Oid = "iso.3.6.1.2.1.1.1"

# Parsing argurments
parser = OptionParser()

parser.add_option("-H", dest="host", type="string",
                  help="Hostname/IP Address of device", metavar=' ')

parser.add_option("-c", "-C", dest="community", type="string",
                  help="Community string", metavar=' ')

parser.add_option("-v", "-V", dest="version", type="int", default=1,
                  help="Community version", metavar=' ')

parser.add_option("--mode", dest="mode", type="string",
                  help="Mode: status or lost", metavar=' ')

parser.add_option("-t", dest="hostname", type="string",
                  help="Host name", metavar=' ', default='HCMPxxx')

(options, args) = parser.parse_args()

version_fw = ".1.3.6.1.4.1.21940.1.5.1.0"
        # NT1 new = 65

# Check for required options
for option in ('host', 'community'):
    if not getattr(options, option):
        print 'Option %s not specified' % option
        parser.print_help()
        sys.exit(3)

plugin = ''
plugin_option = ' -H ' + options.host + ' -c ' + options.community + ' -t ' + options.hostname

# Create session with smnp version 1
sess = netsnmp.Session(Version = 1, DestHost = options.host, Community = options.community, Timeout=1000000, Retries=3)

# Get sysDes ENATEL
var1 = sess.get(netsnmp.VarList('sysDescr.0'))

# Get sysDes EATON
if (var1 == None):
    var1 = sess.get(netsnmp.VarList(Eaton_Descr_Oid))

# Get fw VERSION ENATEL
var2 = sess.get(netsnmp.VarList(version_fw))

result = var1 + var2

if result[0] == None:
        # Create session with smnp version 2
        sess = netsnmp.Session(Version = 2, DestHost = options.host, Community = options.community, Timeout=1000000, Retries=1)
        var = netsnmp.VarList('sysDescr.0')
        result = sess.get(var)
#       print result
        if result[0] == None:
                print 'UNKNOW: Host not responding to SNMP request'
                sys.exit(3)
        else:
                sysDescr = result[0]
else:
        sysDescr = result[0]

try:
        version_fw = int(result[1])
except Exception as e:
        version_fw = 14

if (sysDescr == 'SC200 Controller - software version 3.10') or (sysDescr == 'SC200 Controller - software version 3.14') or (sysDescr == 'SC200 Controller - software version 4.02') or (sysDescr == 'SC200 Controller - software version 4.04'):
        plugin = 'check_DC_power_eaton'
elif sysDescr == 'Eaton EFX48' :
        plugin = 'check_DC_power_eaton_EFX48'
elif sysDescr == 'Enatel SM32 SNMP Agent' and version_fw == 65 :
        plugin = 'check_DC_power_enatelSM32_NT1'
elif sysDescr == 'Enatel SM32 SNMP Agent' and version_fw == 112 :
        plugin = 'check_DC_power_enatelSM32_NT1'
elif sysDescr == 'Enatel SM32 SNMP Agent' and version_fw == 118 :
        plugin = 'check_DC_power_enatelSM32_NT1'
elif sysDescr == 'Enatel SM32 SNMP Agent' :
        plugin = 'check_DC_power_enatelSM32_NT'
elif sysDescr == 'Enatel SM3X NT2 SNMP Agent':
        plugin = 'check_DC_power_enatelSM32_NT2'
elif sysDescr == 'Enatel SM22 SNMP Agent':
        plugin = 'check_DC_power_enatelSM22'
elif sysDescr == 'SWPR VER2.2':
        plugin = 'check_fts_power_dongah'
elif 'Linux ES_Controller' in sysDescr:
        plugin = 'check_DC_power_vertiv'
else:
        print 'UNKNOW: Unknown power type ' + sysDescr
        sys.exit(3)

if options.mode:
        if options.mode == 'lost':
                plugin += '_lost.py'
        elif options.mode == 'alarm':
                plugin += '_alarm.py'
        else:
                print 'Unknown mode'
                sys.exit(3)
else:
        plugin += '.py'

#status, output = commands.getstatusoutput('/usr/bin/python /usr/local/nagios/libexec/' + plugin + plugin_option)
status, output = commands.getstatusoutput('/usr/bin/python ' + plugin + plugin_option)

status = status / 256

if (status not in (OK, WARNING, CRITICAL, UNKNOWN)) or ('Traceback' in output):
        print "Unknown return status from plugin:" + str(status)
        print output
        sys.exit(3)
else:
        print output
        sys.exit(status)

