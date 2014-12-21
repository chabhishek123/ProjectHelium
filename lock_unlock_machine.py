import bluetooth
import subprocess
target_name = "GT N7000"
       
target_address = "9C:E6:E7:1A:E3:7B"
#target_address = "00:1A:89:3A:6B:FF"
flag = 0
flag1 = 0

while flag1 == 0 :
	
	nearby_devices = bluetooth.discover_devices()
	
	if(len(nearby_devices) != 0) :
		
		for address in nearby_devices :
			
			if address == target_address :
				
				flag1 = 1
		
				
		
print "Device Found" 
print nearby_devices

while 1:
	in_range = 1

	while in_range == 1:

		nearby_devices = bluetooth.discover_devices()
	
		if(len(nearby_devices) != 0) :
	
			for address in nearby_devices :
			
				if address == target_address :
				
					in_range = 1
					break
					
				else :
		
					in_range = 0
		else :
			in_range = 0
	
		
	subprocess.call("gnome-screensaver; gnome-screensaver-command -l",shell=True)

	in_range = 0

	while in_range == 0:

		nearby_devices = bluetooth.discover_devices()
	
		if(len(nearby_devices) != 0) :
	
			for address in nearby_devices :
			
				if address == target_address :
				
					in_range = 1
					break
				
				else :
		
					in_range = 0
		else :
			in_range = 0
		
		         
	if in_range == 1 :
		    	print "Device back in range, unlocking..."
			subprocess.call("gnome-screensaver", shell = True)
		    	subprocess.call("gnome-screensaver-command -d && xdotool type ball && xdotool key Return",shell=True)
                                                             