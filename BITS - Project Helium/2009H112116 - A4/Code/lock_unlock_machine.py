from bluetooth import *
import subprocess

target_name = "NJ's Cellphone"
       
target_address = "00:1A:75:C2:61:CE"
#target_address = "00:1A:89:3A:6B:FF"
flag = 0
flag1 = 0

while flag1 == 0 :
	
	nearby_devices = discover_devices(duration=4)
	
	if(len(nearby_devices) != 0) :
		
		for address in nearby_devices :
			
			if address == target_address :
				
				flag1 = 1
		
				
		
print "Device Found" 
print nearby_devices

while 1:
	in_range = 1

	while in_range == 1:

		nearby_devices = discover_devices(duration=4)
	
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

		nearby_devices = discover_devices(duration=4)
	
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
    	subprocess.call("gnome-screensaver; gnome-screensaver-command -d",shell=True)
                                                               

