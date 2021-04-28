import os
import sys
import xbmcaddon
import xbmcgui
import xbmc
import time
from random import seed
from random import random
from platform import system
import hashlib
import multiprocessing
import socket
import statistics
import threading
import urllib.request

Addon = xbmcaddon.Addon('script.screensaver.ducominer')

__scriptname__ = Addon.getAddonInfo('name')
__path__ = Addon.getAddonInfo('path')

class Screensaver(xbmcgui.WindowXMLDialog):

	class ExitMonitor(xbmc.Monitor):

		def __init__(self, exit_callback):
			self.exit_callback = exit_callback

		def onScreensaverDeactivated(self):
			print ('3 ExitMonitor: sending exit_callback')
			self.exit_callback()

	def onInit(self):
		print ('2 Screensaver: onInit')
		self.monitor = self.ExitMonitor(self.exit)

	def exit(self):
		print ('4 Screensaver: Exit requested')
		self.close()

miningLog = dict()
miningLog['line1']=''
miningLog['line2']=''
miningLog['line3']=''
miningLog['line4']=''
global infoLine
global platformID
global MaxCores
global username
global countconnections
countconnections=0
MaxCores=1

def addLog(news):
	#insert new
	#print('..in addLog')
	infoLine = makeInfoLine()
	miningLog['line1']=miningLog['line2']
	miningLog['line2']=miningLog['line3']
	miningLog['line3']=miningLog['line4']
	miningLog['line4']=infoLine+news
	#window1.show()
	print('debug_line1:'+miningLog['line1'])
	

def makeInfoLine():
	#print('..in makeInfoline')
	platformID=system()
	#print('debug_platformID: '+platformID)

	cpuTemp = xbmc.getInfoLabel('System.CPUTemperature')

	cpuFrequenz = xbmc.getInfoLabel('System.CpuFrequency')

	if( xbmc.getInfoLabel('System.HasCoreId(8)')==True ):
		MaxCores=8
	elif ( xbmc.getInfoLabel('System.HasCoreId(7)')==True ):
		MaxCores=7
	elif ( xbmc.getInfoLabel('System.HasCoreId(6)')==True ):
		MaxCores=6
	elif ( xbmc.getInfoLabel('System.HasCoreId(5)')==True ):
		MaxCores=5
	elif ( xbmc.getInfoLabel('System.HasCoreId(4)')==True ):
		MaxCores=4
	elif ( xbmc.getInfoLabel('System.HasCoreId(3)')==True ):
		MaxCores=3
	elif ( xbmc.getInfoLabel('System.HasCoreId(2)')==True ):
		MaxCores=2
	else:
		MaxCores=1
	print('debug:MaxCores is:'+str(MaxCores))
	if (platformID == "Windows"):
		return(str(countconnections) + ' ' + platformID + ' | ' + str(MaxCores) + 'Core(s)@' + str(cpuFrequenz) + ' -->')
	else:
		return(str(countconnections) + ' ' + platformID + ' | ' + str(MaxCores) + 'Core(s)@' + str(cpuFrequenz) + str(cpuTemp) + ' -->')

def retrieve_server_ip():
	#print("..in retrieve_server_ip")
	print("> Retrieving Pool Address And Port")
	pool_obtained = False
	while not pool_obtained:
		try:
			serverip = ("https://raw.githubusercontent.com/"
							+ "revoxhere/"
							+ "duino-coin/gh-pages/"
							+ "serverip.txt")
			with urllib.request.urlopen(serverip) as content:
				# Read content and split into lines
				content = content.read().decode().splitlines()
			global pool_address, pool_port
			# Line 1 = IP
			pool_address = content[0]
			# Line 2 = port
			pool_port = content[1]
			pool_obtained =  True
		except:
			print("> Failed to retrieve Pool Address and Port, Retrying.")
			continue

	
if __name__ == '__main__':
	xbmc.log(msg='Ducominer started.', level=xbmc.LOGDEBUG)
	print ('1 Python Screensaver Started')
	#config lesen
	print ('1.a Read Config')
	miningUserWalletID=Addon.getSetting('EnterWalletID')
	xbmc.log(msg='Ducominer UserWalletID is:'+miningUserWalletID, level=xbmc.LOGDEBUG)
	miningCharity=Addon.getSetting('setting_charity')
	xbmc.log(msg='Ducominer CharityWalletID is:'+miningCharity, level=xbmc.LOGDEBUG)
	charity_percentage=Addon.getSetting('setting_charity_percentage')
	xbmc.log(msg='Ducominer charity_percentage is:'+charity_percentage, level=xbmc.LOGDEBUG)
	dev_percentage=Addon.getSetting('setting_dev_percentage')
	xbmc.log(msg='Ducominer dev_percentage is:'+dev_percentage, level=xbmc.LOGDEBUG)
	powerMining=Addon.getSetting('setting_powermining')
	xbmc.log(msg='Ducominer setting_powermining is:'+powerMining, level=xbmc.LOGDEBUG)

	#hintergrund schön machen
	window1 = xbmcgui.Window()
	image1 = xbmcgui.ControlImage(0, 0, 1280, 720, filename=Addon.getAddonInfo('path')+'/resources/skins/default/media/background1280x720.png') 
	textbox1 = xbmcgui.ControlTextBox(50, 600, 1180, 25, textColor='0xFFFFFFFF')
	textbox2 = xbmcgui.ControlTextBox(50, 625, 1180, 25, textColor='0xFFFFFFFF')
	textbox3 = xbmcgui.ControlTextBox(50, 650, 1180, 25, textColor='0xFFFFFFFF')
	textbox4 = xbmcgui.ControlTextBox(50, 675, 1180, 25, textColor='0xFFFFFFFF')
	textbox1.setText(miningLog['line1'])
	textbox2.setText(miningLog['line2'])
	textbox3.setText(miningLog['line3'])
	textbox4.setText(miningLog['line4'])
	window1.addControls([image1, textbox1, textbox2, textbox3, textbox4])
	#anzeigen
	window1.show()
	
	# hauptminer einfügen
	addLog('Starte KodiSmartTVMinerSingleCoreV0.1')

	username = 'sanduhrgucker'  # Edit this to your username, mind the quotes
	#UseLowerDiff = True  # Set it to True to mine with lower difficulty
	UseLowerDiff = False  # Set it to True to mine with lower difficulty


	
	retrieve_server_ip()

	while True:
		# This section connects and logs user to the server
		soc = socket.socket()
		soc.settimeout(30)
		soc.connect((str(pool_address), int(pool_port)))
		countconnections=countconnections+1
		server_version = soc.recv(3).decode()  # Get server version
		print("Server is on version "+str( server_version))

		# Mining section
		#print("..in loopTry")	
		#print('debug_username:'+username)	
		jobrequestRaw=( "JOB," + str(username) + ",MEDIUM")
		print('debug_jobrequest (raw) is:'+jobrequestRaw)	
		
		if UseLowerDiff:
			# Send job request for lower diff
			soc.send(bytes(
				"JOB,"
				+ str(username)
				+ ",MEDIUM",
				encoding="utf8"))
		else:
			# Send job request
			soc.send(bytes(
				"JOB,"
				+ str(username),
				encoding="utf8"))

		#print("..in loopTry_sended jobrequest")
		# Receive work
		
		job = soc.recv(1024).decode().rstrip("\n")
		#print(type(job))
		print("..in loopTry_jobdecoded Job is :"+job)			
		# Split received data to job and difficulty
		job = job.split(",")
		difficulty = job[2]
		#print('debug_diff:'+str(difficulty))
		hashingStartTime = time.time()
		base_hash = hashlib.sha1(str(job[0]).encode('ascii'))
		temp_hash = None

		#print(job[0])			
		#print(job[1])			
		#print(job[2])			
		#print("..in loopTry_getjob completed, now searching for hash")			
		for result in range(100 * int(difficulty) + 1):
			#print('debug_diff_in_loop:'+str(difficulty))			
			# Calculate hash with difficulty
			temp_hash =  base_hash.copy()
			temp_hash.update(str(result).encode('ascii'))
			ducos1 = temp_hash.hexdigest()

			# If hash is even with expected hash result
			if job[1] == ducos1:
				#print('debug_hashes sind gleich1')				
				hashingStopTime = time.time()
				timeDifference = hashingStopTime - hashingStartTime
				hashrate = result / timeDifference

				# Send numeric result to the server 'Minimal_PC_Miner' vs 'KodiSmartTVMinerSingleCoreV0.1'
				print('debug_calculated_result is: '+str(result))
				soc.send(bytes(
					str(result)
					+ ","
					+ str(hashrate)
					+ ",KodiSmartTVMinerSingleCoreV0.1",
					encoding="utf8"))

				# Get feedback about the result
				feedback = soc.recv(1024).decode().rstrip("\n")
				print('debug_feedback is: '+feedback)
				# If result was good
				if feedback == "GOOD":
					#print("Accepted share",result,"Hashrate",int(hashrate/1000),"kH/s","Difficulty",difficulty)
					print(' Accepted share' + str(result) + ' | Hashrate ' + str(int(hashrate/1000)) + ' kH/s | Diff: ' + difficulty)
					addLog(' Accepted share' + str(result) + ' | Hashrate ' + str(int(hashrate/1000)) + ' kH/s | Diff: ' + difficulty)
					break
				# If result was incorrect
				elif feedback == "BAD":
					#print("Rejected share",result,"Hashrate",int(hashrate/1000),"kH/s","Difficulty",difficulty)
					print(' Rejected share' + str(result) + ' | Hashrate' + str(int(hashrate/1000)) + ' kH/s | Diff: ' + difficulty)
					addLog(' Rejected share' + str(result) + ' | Hashrate' + str(int(hashrate/1000)) + ' kH/s | Diff: ' + difficulty)
					break
		
		textbox1.setText(miningLog['line1'])
		textbox2.setText(miningLog['line2'])
		textbox3.setText(miningLog['line3'])
		textbox4.setText(miningLog['line4'])
		soc.close()	
		#time.sleep(30)
	
#hier miner verlassen
print ('5 Python Screensaver Exited')

del window1
sys.modules.clear()
xbmc.log(msg='Ducominer stopped.', level=xbmc.LOGDEBUG)