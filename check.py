import os
import requests

path = os.path.abspath(os.curdir)
odoo_version = "14.0"

def appendFile(module_name, upgradable):
    with open("./README.md", "a") as readme:
        if (upgradable[0] == "true"):
            readme.write("[%s](%s/) | %s | [%s](%s) \n"%(module_name, module_name, upgradable[0], module_name, upgradable[1]))
        else:
            readme.write("[%s](%s/) | %s | -- \n"%(module_name, module_name, upgradable[0]))

def listdirs(path):
    return [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]
    
def checkUpgrade(module_name, odoo_version):
    response = requests.get("https://apps.odoo.com/apps/modules/%s/%s/"%(odoo_version, module_name))
    if (response.status_code == 200):
        return "true", "https://apps.odoo.com/apps/modules/%s/%s/"%(odoo_version, module_name)
    elif (response.status_code == 404):
        return "false", "Not Found"

def deleteLines():
    with open("./README.md", "r") as input:
        with open("./README-temp.md", "w") as output:
            for line in input:
                if not line.strip("\n").startswith('['):
                    output.write(line)

print("Starting to check!")

deleteLines()
os.replace('./README-temp.md', './README.md')
modules = listdirs(path)
for module in modules:
    appendFile(module, checkUpgrade(module, odoo_version))

print("Finished checking!")
