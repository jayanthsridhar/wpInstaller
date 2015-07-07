#!/usr/bin/python

import os, sys, random, string, urllib2, MySQLdb, optparse
from wpconfig import config

def printHelp():
	#Print Help
	print "Ohh la la\n"

def createDatabase (databaseName, databaseUser, databasePassword) :
	db = MySQLdb.connect("localhost",databaseUser,databasePassword)
	cursor = db.cursor()
	cursor.execute("CREATE DATABASE %s"%databaseName)
	db.close()
	return databaseName

def secureInstall(targetDir) :
	#Remove unnecessary files from install
	for fileName in ['license.txt', 'readme.html', 'wp-config-sample.php'] :
		if os.path.exists("%s/%s"%(targetDir, fileName)) :
			os.system("rm %s/%s"%(targetDir, fileName))

def tidyUp(projectName) :
	#Remove wp archive and temp dir
	os.system("rm latest.tar.gz")
	os.system("rm -rf %s"%projectName)

def createDirectory(dirPath) :
	#Check and create directories
	if not os.path.exists(dirPath) :
		os.system("mkdir %s"%dirPath)
	else :
		os.system("rm -rf %s/"%dirPath)
		os.system("mkdir %s"%dirPath)

def wpInstall(projectName, targetDir) :
	#Get latest wordpress archive
	os.system("wget -q https://wordpress.org/latest.tar.gz")

	#Create a temporary directory with projectName to extract
	createDirectory(projectName)
	os.system("tar -xzf latest.tar.gz -C %s"%projectName)

	#Get Database Details
	siteDatabase = raw_input("Enter Database Name:\nTo create one, press enter ")
	if siteDatabase == "\n" :
		#Create a new database with projectName
		siteDatabase = createDatabase(projectName, siteDBUser, siteDBPass)
	siteDBUser = raw_input("Enter Database Username: ")
	siteDBPass = raw_input("Enter Database Password: ")

	#Generate table prefix
	siteTBLPrefix = "".join(random.choice(string.lowercase) for x in range(4))
	siteTBLPrefix = "swp_"+siteTBLPrefix+"_"

	#Get keys and sald from WP API
	response = urllib2.urlopen("https://api.wordpress.org/secret-key/1.1/salt/")
	siteSalt = response.read()

	#Generate new config file
	configFile = open("%s/wordpress/wp-config.php"%projectName,"w")
	configString = config["wp_config"]%(siteDatabase, siteDBUser, siteDBPass, siteTBLPrefix, siteSalt)
	configFile.write(configString)
	configFile.close()

	#Create target directory and move the install over
	createDirectory(targetDir)
	os.system("mv %s/wordpress/* %s"%(projectName,targetDir))

	#Secure the install
	secureInstall(targetDir)

	#General clean up of the base dir and temp
	tidyUp(projectName)

def main(argv):
	parser = optparse.OptionParser()
	parser.add_option('-p', dest='projectName', action='store')
	parser.add_option('-t', dest='targetDir', action='store')
	parser.add_option('-i', action="callback", callback=wpInstall)
	parser.add_option('--help', action="callback", callback=printHelp)
	parser.parse_args()


if __name__ == "__main__":
	sys.exit(main(sys.argv[1:]))
