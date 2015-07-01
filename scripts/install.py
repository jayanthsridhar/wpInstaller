import os, sys

def writeConfig(fileName, findText, replaceText) :
	tempFile = open( fileName, 'r+' )
	for line in fileinput.input( fileName ):
    		if findText in line :
        		tempFile.write( line.replace( findText, replaceText ) )
	tempFile.close()

def wpInstall(projectName, targetDir) :
	#os.system("wget -q https://wordpress.org/latest.tar.gz")
	os.system("mkdir %s"%projectName)
	os.system("tar -xzvf latest.tar.gz -C %s"%projectName)
	#os.system("cd %s/wordpress/"%projectName)
	os.system("mv %s/wordpress/wp-config-sample.php %s/wordpress/wp-config.php"%(projectName,projectName))
	siteTitle = raw_input("Enter Site Title: ")	
	siteURL = raw_input("Enter Site URL: ")
	siteDatabase = raw_input("Enter Database Name:\n To create one, press enter ")
	siteDBUser = raw_input("Enter Database Username: ");
	siteDBPass = raw_input("Enter Database Password: ");

	print siteTitle;
	os.system("mv %s/wordpress/* %s"%(projectName,targetDir))


def main(argv):
	projectName = argv[0]
	targetDir = argv[1]
	wpInstall(projectName, targetDir)


if __name__ == "__main__":
	sys.exit(main(sys.argv[1:]))

