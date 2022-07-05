import csv
import serial
from time import sleep
import sys
import getopt
import serial.tools.list_ports

global serialport
serialport = ''

def openserialport(serial_number):

	try:
		global serialport
		serialport = serial.Serial(serial_number, baudrate=9600, timeout=0.0)
		return

	except SerialPortError:
		print("Could not open serial port, use -h or --help")
		return

def csvloop(file):

	global serialport

	try:
		while true:

			with open(file) as patterncsv:
				pattern_csv_object = csv.reader(patterncsv, delimiter=';')

				for row in pattern_csv_object:
						count = 1
						for  chell in row:
							if count < 5:
								attenuation = row[(count)]
								command = "SET "+str((count))+" "+str(attenuation)
								serialport.write((command).encode())
								print(str(serialport.readline()).strip('\'b\\r\\n'))
								print(str(serialport.readline()).strip('\'b\\r\\n'))
							count += 1
						sleep(int(row[0])/1000)

	except FileNotFoundError:
		print("Could not find file, use -h or --help")
		return

def help():

		print(
"""usage:
\t-h --help\t\t\t\tshows this help

\t-p --port\t[serialport]\t\tpath to serial port the device is in
\t\t\t\t\t\tthis option is required for every function except help

\t-s --set_value\t[chain:attenuation]\tsets given chain to a given attenuation.
\t\t\t\t\t\tavailable chains: 1 2 3 4
\t\t\t\t\t\tattenuation needs to be between 0 and 95dB
\t\t\t\t\t\tthe resolution is 0.25dB

\t-s --set_all\t[attenuation]\tsets all chains to one given attenuation.
\t\t\t\t\t\tattenuation needs to be between 0 and 95dB
\t\t\t\t\t\tthe resolution is 0.25dB

\t-m --multiset\t[attenuation_chain1]:[attenuation_chain2]:[attenuation_chain3]:[attenuation_chain4]\tsets all chains to the given attenuation.
\t\t\t\t\t\tattenuation needs to be between 0 and 95dB
\t\t\t\t\t\tthe resolution is 0.25dB

\t-t --csv_table\t[path to csv file]
\t\t\t\t\t\tinstructs the attenuator to run an attenuation pattern
\t\t\t\t\t\twhen using this option the script needs to be terminated manually
\t\t\t\t\t\tsee in readme how the csv file needs to be filled

\t-i --info\t\t\t\treads out the status of the device

\t--portinfo\t\t\t\tshows list of connected serial devices


""")
		return

def info():

	global serialport

	serialport.write(("info").encode())
	output = serialport.readlines()
	print("")
	for line in output[1:]:
		print (str(line).strip('\'b\\r\\n'))
	serialport.close()
	return

def status():

	global serialport

	serialport.write(("status").encode())
	output = serialport.readlines()
	print("")
	for line in output[1:]:
		print (str(line).strip('\'b\\r\\n'))
	serialport.close()
	return

def setvalue(attenuation):

	global serialport

	par = attenuation.split(":")
	command = "SET "+str(par[0])+" "+str(par[1])
	serialport.write((command).encode())
	sleep(0.01)
	print(str(serialport.readline()).strip('\'b\\r\\n'))
	print(str(serialport.readline()).strip('\'b\\r\\n'))
	serialport.close()
	return

def setall(attenuation):

	global serialport

	command ="SAA "+str(attenuation)
	serialport.write((command).encode())
	sleep(0.01)
	print(str(serialport.readline()).strip('\'b\\r\\n'))
	print(str(serialport.readline()).strip('\'b\\r\\n'))
	serialport.close()
	return

def multiset(attenuation: str):

	global serialport

	par = attenuation.split(":")
	
	command = "SET 1 "+str(par[0])
	serialport.write((command).encode())
	sleep(0.01)
	print(str(serialport.readline()).strip('\'b\\r\\n'))
	print(str(serialport.readline()).strip('\'b\\r\\n'))

	command = "SET 2 "+str(par[1])
	serialport.write((command).encode())
	sleep(0.01)
	print(str(serialport.readline()).strip('\'b\\r\\n'))
	print(str(serialport.readline()).strip('\'b\\r\\n'))

	command = "SET 3 "+str(par[2])
	serialport.write((command).encode())
	sleep(0.01)
	print(str(serialport.readline()).strip('\'b\\r\\n'))
	print(str(serialport.readline()).strip('\'b\\r\\n'))

	command = "SET 4 "+str(par[3])
	serialport.write((command).encode())
	sleep(0.01)
	print(str(serialport.readline()).strip('\'b\\r\\n'))
	print(str(serialport.readline()).strip('\'b\\r\\n'))
	serialport.close()
	return


def portinfo():

	portlist = serial.tools.list_ports.comports()
	for port in portlist:
		print(port.description)

def argumentcheck():

	portopt = False
	argv = sys.argv[1:]

	try:
		opts, args = getopt.getopt(argv,"dhp:s:t:a:m:i",["help","port=","set_value=","set_all=","csv_table=","info","portinfo","multiset=","status"])
	except:
		print("""incorrect input, use -h or --help for a list of options""")
		sys.exit(2)

	for opt, arg in opts:

		if opt in ("-h","--help"):
			help()

		elif opt == "--portinfo":
			portinfo()

		elif opt in ("-p","--port"):
			openserialport(arg)
			portopt = True

		elif opt in ("-i","--info"):
			if portopt == True:
				info()
			else:
				print("no port was given")
				help()

		elif opt in ("-s","--set_value"):
			if portopt == True:
				setvalue(arg)
			else:
				print("no port was given")
				help()
			return

		elif opt in ("-m","--multiset"):
			if portopt == True:
				multiset(arg)
			else:
				print("no port was given")
				help()
			return

		elif opt in ("-a","--set_all"):
			if portopt == True:
				setall(arg)
			else:
				print("no port was given")
				help()
			return

		elif opt in ("-t","--csv_table"):
			if portopt == True:
				csvloop()
			else:
				print("no port was given")
				help()
			return

		elif opt == "--status":
			status()


		else:
			print("no options given, try -h or --help")


argumentcheck()

sys.exit(2)
