#!/usr/bin/python3
# imports to allow running of shell commands
#
from __future__ import print_function
import os
import subprocess
import re



# terminal colour text codes (found via a so page)
class bcolors:
    GREEN = '\033[92m'
    ORANGE = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    vmTag = ''

def pingItem(pinginput):
  pingResult = subprocess.run(['ping', '-c 2', pinginput], capture_output=True, text=True)
  if (pingResult.stderr != ""):
    return pingResult.stderr
  else:
    return pingResult.stdout

def main():
  if (os.path.isfile('ping.txt')):
    ip4Regex = re.compile(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")
    os.system('clear')
    print("################################")
    print("## Preparing initial results ...")

    # need to declare arrays here to allow comparison with previous info
    resolving = []
    resolvingTo = []
    notResolving = []    
    bcolorsTag = [] 
    i = 0
    while (i < 5):

      with open('ping.txt') as items:
        allItems = items.readlines()
        itemsCount = len(allItems)
 

        #print("%s" % allItems[itemsCount-1])



        for item in allItems:
          pingResult = pingItem(item.rstrip())
          for pingResultLine in pingResult.splitlines():
            if ("bytes" in pingResultLine):
              for word in pingResultLine.split():
                cleanWord = word.strip("()")
                if (ip4Regex.match(cleanWord)):
                  #print("## %s resolving to: %s " %(item.rstrip(), cleanWord))
                  resolving.append(item.rstrip())
                  resolvingTo.append(cleanWord)
                  notResolving.append("empty")

                  if (i > 0):
                    print(resolvingTo[(i * itemsCount)-itemsCount])
                    print(cleanWord)
                    if (resolvingTo[(i * itemsCount)-itemsCount] == cleanWord):
                      bcolorsTag.append("\033[93m")
                    else:
                      bcolorsTag.append("\033[92m")
                  else:
                    bcolorsTag.append("\033[93m")

            elif ("not known" in pingResultLine):
              #print("## %s not resolving " %item.rstrip())
              # append to all arrays to keep index in sync
              notResolving.append(item.rstrip())
              resolving.append("empty")
              resolvingTo.append("empty")
              bcolorsTag.append("\033[93m")
        
        # clear screen each time just before printing latest info
        #os.system('clear')
        # set default colour for the list of VMs to amber
        bcolors.vmTag='\033[93m'
        print("################################")
        print("##     Pinging %s devices " %str(itemsCount))
        # only print the last results info
        for x in range(i*itemsCount, len(resolving)):
          if (not "empty" in resolving[x]):
            print("## %s resolving to: %s %s %s %s" %(resolving[x], bcolorsTag[x], resolvingTo[x], bcolors.END, x))
          else:
            print("## %s is not resolving %s " %(notResolving[x], i))
      
      i+=1

  
  else:
    print("Please ensure ping.txt exists in this scripts folder.")



if __name__ == '__main__':
    main()