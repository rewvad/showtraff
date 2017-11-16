#!/usr/bin/env python

import commands
import time

from prettytable import PrettyTable

#Get intarfaces names
ifaceNames = commands.getstatusoutput("netstat -i |  tail -n +3 | awk '{print $1 }'")[1].split()

#Get list of interfaces in bond
bondInfo = commands.getstatusoutput("cat /proc/net/bonding/* | grep 'Slave Interface' | awk '{print $3}'")[1].split()


ifaceLoad = commands.getstatusoutput("ifconfig | grep 'RX bytes' | sed 's/:/ /g' | awk '{print $3 \"--\" $8}'")[1].split()

RXload1 = [i.split('--')[0] for i in ifaceLoad]
TXload1 = [i.split('--')[1] for i in ifaceLoad]

RX1 = commands.getstatusoutput("netstat -i |  tail -n +3 | awk '{print $4 }'")[1].split()
TX1 = commands.getstatusoutput("netstat -i |  tail -n +3 | awk '{print $8 }'")[1].split()

time.sleep(1)

ifaceLoad = commands.getstatusoutput("ifconfig | grep 'RX bytes' | sed 's/:/ /g' | awk '{print $3 \"--\" $8}'")[1].split()

RXload2 = [i.split('--')[0] for i in ifaceLoad]
TXload2 = [i.split('--')[1] for i in ifaceLoad]

RX2 = commands.getstatusoutput("netstat -i |  tail -n +3 | awk '{print $4 }'")[1].split()
TX2 = commands.getstatusoutput("netstat -i |  tail -n +3 | awk '{print $8 }'")[1].split()

table = PrettyTable(["iface", "Incoming rates Mbit/s", "Incoming pkts/s", "Outgoing rates Mbit/s", "Outgoing pkts/s"])
table.padding_width = 1

RXload_total = 0.0
TXload_total = 0.0
RX_total = 0
TX_total = 0
i = 0
j = 0

for iface in ifaceNames:
        #If interface in bond, skip it
        if iface in bondInfo:
                j+=1
                i+=1
                continue
        try:
                RXload = round(((float(RXload2[j]) - float(RXload1[j]))*8)/(1024*1024),3)
                TXload = round(((float(TXload2[j]) - float(TXload1[j]))*8)/(1024*1024),3)
                RX_out = int(RX2[i]) - int(RX1[i])
                TX_out = int(TX2[i]) - int(TX1[i])
                RXload_total = RXload_total + RXload
                TXload_total = TXload_total + TXload
                RX_total += RX_out
                TX_total += TX_out
                table.add_row([iface, RXload, RX_out, TXload, TX_out])
        except:
                table.add_row([iface, "not supported", "not supported", "not supported", "not supported"])
                i+=1
                continue
        i+=1
        j+=1
print table
print "--------------------------------------------------"

print "total Incoming: " + str( RXload_total) + " Mbit/s " + str(RX_total) + " pkts/s,\tOutgoing: " + str(TXload_total) + " Mbit/s " + str(RX_total)+ " pkts/s"
