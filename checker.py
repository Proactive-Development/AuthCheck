import re
import sys
from colorama import Fore, Back, Style
def get_ip(file):
    try:
        with open(file) as fh:
            fstring = fh.readlines()
    except FileNotFoundError:
        print("AuthChecker: The file "+file+" Cant be found")
        exit()
    pattern = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')
    lst=[]
    for line in fstring:
        if str(pattern.search(line)) == "None":
            continue
        else:
            #i know this is a weird extraction method
            ip = str(pattern.search(line)).replace("<re.Match object; span=(","").replace("), match=","").replace("'>","")
            lst.append(ip[ip.find("'")+1:])
    lst = list(dict.fromkeys(lst))
    return lst
def get_auth_failures(file): 
    with open(file) as fh:
        fstring = fh.read()
    return fstring.split().count("Failed")
def get_auth_successful(file): 
    with open(file) as fh:
        fstring = fh.read()
    return fstring.split().count("Accepted")
if __name__ == "__main__":
    auth_file = "/var/log/auth.log"
    for i in sys.argv:
        if i.startswith("--file="):
            auth_file = i.replace("--file=","")
    for i in sys.argv:
        if i == "-l":
            for i in get_ip(auth_file):
                print(i)
        if i == "-n":
            ln = 0
            for i in get_ip(auth_file):
                print(str(ln)+"|"+i)
                ln = ln + 1
        if i == "-s":
            ln = 0
            for i in get_ip(auth_file):
                ln = ln + 1
            if ln <= 10:
                print(Fore.GREEN+"There are "+str(ln)+" Unique IP addresses in "+auth_file+Style.RESET_ALL)
            elif ln <= 50:
                print(Fore.YELLOW+"There are "+str(ln)+" Unique IP addresses in "+auth_file+Style.RESET_ALL)
            elif ln <= 100:
                print(Fore.RED+"There are "+str(ln)+" Unique IP addresses in "+auth_file+Style.RESET_ALL)
                print("Checking firewall and auth.log is recommended")
            else:
                print(Fore.WHITE+Back.RED+"There are "+str(ln)+" Unique IP addresses in "+auth_file+Style.RESET_ALL)
                print("Checking firewall and auth.log is recommended")
            fail = get_auth_failures(auth_file)
            if fail <= 5:
                print(Fore.GREEN+"There are "+str(fail)+" Authentication failures reported "+auth_file+Style.RESET_ALL)
            elif fail <= 10:
                print(Fore.YELLOW+"There are "+str(fail)+" Authentication failures reported "+auth_file+Style.RESET_ALL)
            elif fail <= 30:
                print(Fore.RED+"There are "+str(fail)+" Authentication failures reported "+auth_file+Style.RESET_ALL)
                print("Checking firewall and auth.log is recommended")
            else:
                print(Fore.WHITE+Back.RED+"There are "+str(fail)+" Authentication failures reported "+auth_file+Style.RESET_ALL)
                print("Checking firewall and auth.log is recommanded")
            print("The system has accepted "+str(get_auth_successful(auth_file))+" logins")
