import os, sys, random, string, urllib2
from wpconfig import config

def secureInstall(targetDir) :
	for fileName in ['license.txt', 'readme.html', 'wp-config-sample.php'] :
		if os.path.exists("%s/%s"%(targetDir, fileName)) :
			os.system("rm %s/%s"%(targetDir, fileName))


def tidyUp(projectName) :
	os.system("rm latest.tar.gz")
	os.system("rm -rf %s"%projectName)

def createDirectory(dirPath) :
	if not os.path.exists(dirPath) :
		os.system("mkdir %s"%dirPath)
	else :
		os.system("rm -rf %s/"%dirPath)
		os.system("mkdir %s"%dirPath)

def wpInstall(projectName, targetDir) :
	os.system("wget -q https://wordpress.org/latest.tar.gz")
	createDirectory(projectName)
	os.system("tar -xzf latest.tar.gz -C %s"%projectName)
	os.system("cd %s/wordpress/"%projectName)
	#os.system("mv %s/wordpress/wp-config-sample.php %s/wordpress/wp-config.php"%(projectName,projectName))
	siteDatabase = raw_input("Enter Database Name:\n To create one, press enter ")
	siteDBUser = raw_input("Enter Database Username: ")
	siteDBPass = raw_input("Enter Database Password: ")
	siteTBLPrefix = "".join(random.choice(string.lowercase) for x in range(4))
	siteTBLPrefix = "wp_"+siteTBLPrefix+"_"

	response = urllib2.urlopen("https://api.wordpress.org/secret-key/1.1/salt/")
	siteSalt = response.read()
	configFile = open("%s/wordpress/wp-config.php"%projectName,"w")
	configString = config["wp_config"]%(siteDatabase, siteDBUser, siteDBPass, siteTBLPrefix, siteSalt)
	configFile.write(configString)
	configFile.close()
	createDirectory(targetDir)
	os.system("mv %s/wordpress/* %s"%(projectName,targetDir))
	secureInstall(targetDir)
	tidyUp(projectName)

def main(argv):
	projectName = argv[0]
	targetDir = argv[1]
	wpInstall(projectName, targetDir)


if __name__ == "__main__":
	sys.exit(main(sys.argv[1:]))
