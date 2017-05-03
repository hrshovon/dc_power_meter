import serial

try:
    s_handler=serial.Serial(port='COM3',baudrate=9600)
    while(True):
        rdln=s_handler.readline()
        rdln_split=rdln.split(",")
        print "Voltage:"+str(rdln_split[0])+"V Current:"+str(rdln_split[1])+str(rdln_split[2])+" Power:"+str(rdln_split[3])+str(rdln_split[4])
except:
    print "problem"
