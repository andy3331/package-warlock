# -*- coding: utf-8 -*-

"""

Created on Tue Feb  4 09:20:45 2020

phase 1 is to allow steve to quickly build/package the coding references installer. will make it more dynamic to allow other packages as well.

 

pre requisite:

    run on package machine

   

    

1. Need to get product contents

2. Set to non read only attributes

3. backup the ism file

4. update the ism file with product version (product version via cmd line is not working...maybe can use the api at some point but havent done in python before)

5. send build command to installshield with updated ism

6. restore ism file to the installshield folder

 

lot of variables hard coded for now. will need to split out file locations/user info into config file/user input

will package via electron

 

@author: aconning

"""

 

# -*- coding: utf-8 -*-

"""

Created on Wed Jan 29 10:32:21 2020

 

@author: Andy

"""

 

import in_place
import subprocess
import os
import shutil
import sys
 

product_name = sys.argv[2]
#product_name = 'CodingReferences'
input_user = sys.argv[3]
input_password = sys.argv[4]
input_version =  sys.argv[5]

for i in sys.argv:
    print(i)
print("now variables")
print(input_user)
print(input_password)
print(input_version)
print(product_name)
text_to_search = 'ProductVersion'

#version does not need the v, gets appended by installer.
version = input_version
encoding = 'utf-8'
#product_name = 'kentucky'

#production variables
work_folder = 'e:\\builds\\webstrat\\' + product_name
#this is packaging machine installshield +kentucky
installshield_folder = 'e:\\installshield\\19\\webstrat\\'
installshield_folder_with_product = installshield_folder + product_name
ism_file = installshield_folder_with_product + '\\' + product_name + '.ism'
vault_exec = 'e:\\Program Files (x86)\\SourceGear\\Vault Client\\vault.exe'
build_executable = 'E:\\Program Files (x86)\\InstallShield\\2012SpringSP1 SAB\\System\\IsCmdBld.exe'
build_type = 'Single'

 
def error_message(msg):
    print("Error: " + msg)
    sys.stdout.flush()
    sys.exit(1)
    
def run_command(cmd, opt):
    if opt == 1:
        print('Get started')
    try:
        print(cmd)
        process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()
        output = output.decode(encoding)
    except:
        error_message("failure ")
        #should just end this to error function
        #sys.exit(1)
    if opt == 1:
        try:
            parse_results(output)
            print('Parse_results success')
        except:
            error_message("Failure in parse_results")
    else:
            print("Attribute success")

        #sys.exit(1)
def run_build(cmd):
    print('build started')
    try:
        print(cmd)
        subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
    except:
        error_message("failure ")
        #should just end this to error function
        #sys.exit(1)

def parse_results(output):
    if '<success>True</success>' in output:
        print(output)
    elif '<success>False</success>' in output:
        error_message("Parse_results was false.  Call was sent but unsuccessful")
    else:
        error_message('Unexpected response in parse_results: ' + output)

 
def backup_ism(product_name, ism_file, option):
    sys.stdout.flush()
    if option == 1 :
        print('Begin backup_ism' + product_name)
        if os.path.exists(ism_file):
            print('File exists' + ism_file)
            print(installshield_folder_with_product + '\\Backup')
            if not os.path.exists(installshield_folder_with_product + '\\Backup'):
                os.makedirs(installshield_folder_with_product + '\\Backup')
            try:
                shutil.copy(ism_file, installshield_folder_with_product + '\\Backup')
            except:
                error_message("Backup_ism failure.  Error copying file")
        else:
            error_message("Backup_ism failure.  ISM file not found:" + ism_file)
            #print('I cant find the .ism file for this product.' + ism_file)
            #sys.exit(1)
    else:
        try:
            print('Begin backup_ism (restore)' + product_name)
            shutil.copy(installshield_folder_with_product + '\\Backup\\' + product_name + '.ism', ism_file)
        except:
            error_message("Backup_ism failure (on Restore).  Error copying file: " + installshield_folder_with_product + '\\Backup\\' + product_name + '.ism')

def update_ism(ism_file):
    print('Begin update_ism')
    try:
        with in_place.InPlace(ism_file) as file:
            for line in file:
                if "ProductVersion" in line:
                    line=line.replace(line,'\t\t<row><td>ProductVersion</td><td>' +version + '</td><td/></row>\r')
                    file.write(line) 
                else:
                    file.write(line)
    except Exception as e:
        error_message("Update_ism failure. " + e)
        #sys.exit(1)



run_command(cmd = '\"' + vault_exec + '\"' + " GET -host dbsed1143 -user " + input_user + " -password " + input_password + " -repository CT40Packaging $/builds/WebStrat/CodingReferences -makewritable -setfiletime modification", opt=1)
sys.stdout.flush()
#i actually think i no longer need attribute change...seems like -makewritable will render this unnecessary!
#print("Running attribute change")
#run_command(cmd = "attrib -R -S " + work_folder + '\\* /S /D', opt=0)
backup_ism(product_name, ism_file, 1)
sys.stdout.flush()
update_ism(ism_file)
run_build(cmd = '\"' +  build_executable  + '\"' + " -p " + ism_file + " -r \"Single\"")
print('\"' + build_executable  + '\"' + " -p " + ism_file + " -r \"Single\"")
sys.stdout.flush()
backup_ism(product_name, ism_file, 0)
sys.stdout.flush()
