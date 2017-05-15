import serial
str_file=""
set_c_unit="mA"
set_p_unit="mW"
try:
    s_handler=serial.Serial(port='COM8',baudrate=9600)
    while(True):
        try:
            rdln=s_handler.readline()
            rdln_split=rdln.split(",")
            print "Voltage:"+str(rdln_split[0])+"V Current:"+str(rdln_split[1])+str(rdln_split[2])+" Power:"+str(rdln_split[3])+str(rdln_split[4])
            try:
                voltage=float(str(rdln_split[0]))
                current=float(str(rdln_split[1]))
                curr_unit=rdln_split[2]
                power=float(str(rdln_split[3]))
                p_unit=rdln_split[4][0:len(rdln_split[4])-2]
                if set_c_unit=="mA":
                    if curr_unit=="A":
                        current=current*1000
                else:
                    if curr_unit=="mA":
                        current=current/1000

                if set_p_unit=="mW":
                    if p_unit=="W":
                        power=power*1000
                else:
                    if p_unit=="mW":
                        power=power/1000
                
            except:
                pass
            str_file=str_file+str(voltage)+","+str(current)+","+str(curr_unit)+","+str(power)+","+str(p_unit)+chr(13)    
        except KeyboardInterrupt:
            break
    #print str_file
    with open("testdata.csv","w") as file_obj:
        file_obj.write(str_file)
    print "done"
except:
    print "problem"
