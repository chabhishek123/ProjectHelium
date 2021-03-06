from bluetooth import *
import subprocess
import os
import sys
import struct
import bluetooth._bluetooth as bluez
import socket
import thread

video = 0
target_address = "00:1A:75:C2:61:CE"
#target_address = "00:1A:89:3A:6B:FF"
###############################################################
def device_inquiry_with_with_rssi(sock):
    # save current filter
    old_filter = sock.getsockopt( bluez.SOL_HCI, bluez.HCI_FILTER, 14)

    # perform a device inquiry on bluetooth device #0
    # The inquiry should last 8 * 1.28 = 10.24 seconds
    # before the inquiry is performed, bluez should flush its cache of
    # previously discovered devices
    flt = bluez.hci_filter_new()
    bluez.hci_filter_all_events(flt)
    bluez.hci_filter_set_ptype(flt, bluez.HCI_EVENT_PKT)
    sock.setsockopt( bluez.SOL_HCI, bluez.HCI_FILTER, flt )

    duration = 8
    max_responses = 255
    cmd_pkt = struct.pack("BBBBB", 0x33, 0x8b, 0x9e, duration, max_responses)
    bluez.hci_send_cmd(sock, bluez.OGF_LINK_CTL, bluez.OCF_INQUIRY, cmd_pkt)

    results = []
    
    pkt = sock.recv(255)
    ptype, event, plen = struct.unpack("BBB", pkt[:3])
    
    done = False
    xil = 0
    while not done:
        pkt = sock.recv(255)
        ptype, event, plen = struct.unpack("BBB", pkt[:3])
        if event == bluez.EVT_INQUIRY_RESULT_WITH_RSSI:
            pkt = pkt[3:]
            nrsp = struct.unpack("B", pkt[0])[0]
            
            for i in range(nrsp):
                addr = bluez.ba2str( pkt[1+6*i:1+6*i+6] )
                rssi = struct.unpack("b", pkt[1+13*nrsp+i])[0]
               
                
                if addr == target_address :
              	 	xil = xil + 1
              	 	print " [%s] [%d]" % (addr,xil)
              	 	results.append( ( addr, rssi ) )
               		
                		
                
            if xil > 0 :
            	break
            
                #print "[%s] RSSI: [%d]" % (addr, rssi)
        elif event == bluez.EVT_INQUIRY_COMPLETE:
            done = True
        elif event == bluez.EVT_CMD_STATUS:
            status, ncmd, opcode = struct.unpack("BBH", pkt[3:7])
            
            if status != 0:
            #   print "uh oh..."
            #   printpacket(pkt[3:7])
                done = True
                
        else:
            print "unrecognized packet type 0x%02x" % ptype
    
    
    # restore old filter
    sock.setsockopt( bluez.SOL_HCI, bluez.HCI_FILTER, old_filter )


    if len(results) == 0 :
    	return 0
    else :
    	return 100+results[0][1]
#####################################################
def check_signal_strength () :
	dev_id = 0
	
	try:
    		sock = bluez.hci_open_dev(dev_id)
	except:	
    		print "error accessing bluetooth device..."
    		sys.exit(1)

	i=0
	
	while i<3 :
	
		rssi_results = device_inquiry_with_with_rssi(sock)
		i = i+1
		
		if rssi_results:
			break

	
	sock.close()
	
	return rssi_results
###################################	
def launch_vlc(arg):
	subprocess.call("vlc -vvv /windows/d/songs/Echoes.mp3 --sout '#transcode{vcodec=mp2v,vb=800,scale=1,acodec=mpga,ab=128,channels=2}:duplicate{dst=display,dst=rtp{dst=10.42.43.10,mux=ts,port=1234}}' --rc-host localhost:45002",shell=True)
	sleep(2)

##################################
def initialize():
	
	flag1 = 0

	while flag1 == 0 :
	
		nearby_devices = discover_devices(duration=8)
	
		if(len(nearby_devices) != 0) :
		
			for address in nearby_devices :
			
				if address == target_address :
				
					flag1 = 1
	
	print "Device Found! Launching your music..."
	
	#subprocess.call("vlc /home/nitin/play.m3u --rc-host localhost:45123",shell=True)
	#vlc -vvv /windows/d/songs/Echoes.mp3 --sout '#transcode{vcodec=mp2v,vb=800,scale=1,acodec=mpga,ab=128,channels=2}:duplicate{dst=display,dst=rtp{dst=172.17.9.58,mux=ts,port=1234}}' --rc-host localhost:45123

	#thread.start_new_thread(launch_vlc,(0,))
	#sleep(2)
	#launch_vlc
	#subprocess.Popen(['vlc','-vvv','/windows/d/songs/Echoes.mp3','--sout','\'#transcode{vcodec=mp2v,vb=800,scale=1,acodec=mpga,ab=128,channels=2}:duplicate{dst=display,dst=rtp{dst=localhost,mux=ts,port=1234}}\'','-I','rc','--rc-host="localhost:45123"'])
	
	#subprocess.Popen(['vlc','/windows/d/songs/Echoes.mp3','-vvv','--sout','\'#transcode{vcodec=mp2v,vb=800,scale=1,acodec=mpga,ab=128,channels=2}:duplicate{dst=display,dst=rtp{dst=172.17.9.58,mux=ts,port=1234}}\'','--rc-host','localhost:45123'])	
	
	#stream_text = (['vlc','/windows/d/songs/Echoes.mp3','-vvv','--sout','\'#transcode{vcodec=mp2v,vb=800,scale=1,acodec=mpga,ab=128,channels=2}:duplicate{dst=display,dst=rtp{dst=172.17.9.58,mux=ts,port=1234}}\'','--rc-host','localhost:45123'])
	
		
	subprocess.Popen("vlc -vvv /home/nitin/cats.mp3 --sout '#transcode{vcodec=mp2v,vb=800,scale=1,acodec=mpga,ab=128,channels=2}:duplicate{dst=display,dst=rtp{dst=172.17.9.58,mux=ts,port=1234}}' --rc-host localhost:45123",shell=True)
	#subprocess.Popen(['vlc','/windows/d/songs/Echoes.mp3','-vvv','--sout',stream_text,'--rc-host','localhost:45123'])
	
	return
#################################

def vlc_controller(command):

	# create a socket
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	# connect to server
	host = 'localhost' # server address
	port = 45123 # server port
	s.connect((host, port))
	
	
	if command == 'logout' :
	  	sys.exit(0)
  	
	command = command + '\n'
	sent = s.send(command)
	

	s.close()

##################################

initialize()

while 1:

	in_range = 1
	
	while in_range == 1:
		print "Device in range!"
		res = check_signal_strength()
		print "%d strength" % res
		if res == 0:
			in_range = 0
			print "Device left range!"
	
	vlc_controller('volume 1')
	vlc_controller('voldown')
	
	while in_range == 0:
		print "Device still out of reach!"
		res = check_signal_strength()
		
		if res:
		
			in_range = 1
			print "Device coming back in range...!"
			
	vlc_controller('volume 120')
