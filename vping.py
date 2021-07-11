#!/usr/bin/python3
# script contains some Linux specific commands
# run the script from a folder containing ping.txt which should contain list of items/ FQDNs to ping
# imports to allow running of shell commands, file access and regex check
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

# ping the name and return the results for parsing
def pingItem(pinginput):
  pingResult = subprocess.run(['ping', '-c 2', pinginput], capture_output=True, text=True)
  if (pingResult.stderr != ""):
    return pingResult.stderr
  else:
    return pingResult.stdout

def main():
  if (os.path.isfile('ping.txt')):
    # ipv4 regex check
    ip4Regex = re.compile(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")
    os.system('clear')
    print("################################")
    print("## Preparing initial results ...")

    # need to declare arrays here to allow comparison with previous info
    resolving = []
    resolvingTo = []
    notResolving = []    
    bcolorsTag = []
    changeCount = []

    # can set a failsafe to prevent indefinite running of the script
    # for my use case ctrl+c will be used to quit once propagation has complete
    i = 0
    while (i < 100):

      with open('ping.txt') as items:
        allItems = items.readlines()
        itemsCount = len(allItems)
        
        # setup a counter to use to refer back to previous run
        w=0
 
        for item in allItems:
          pingResult = pingItem(item.rstrip())
          for pingResultLine in pingResult.splitlines():
            if ("bytes" in pingResultLine):
              
              for word in pingResultLine.split():
                cleanWord = word.strip("()")
                if (ip4Regex.match(cleanWord)):
                  resolving.append(item.rstrip())
                  resolvingTo.append(cleanWord)
                  notResolving.append("empty")

                  # skip check on first run and set colour to amber
                  if (i > 0):
                    # compare previous run IP to current IP
                    if (resolvingTo[(i * itemsCount)-itemsCount+w] == cleanWord):
                      # if IPs match set colour the same as previous run
                      bcolorsTag.append(bcolorsTag[(i * itemsCount)-itemsCount+w])
                      changeCount.append(0 + int(changeCount[(i * itemsCount)-itemsCount+w]))
                    else:
                      # if IPs differ set colout to green
                      bcolorsTag.append("\033[92m")
                      changeCount.append(1 + int(changeCount[(i * itemsCount)-itemsCount+w]))
                  else:
                    bcolorsTag.append("\033[93m")
                    changeCount.append(0)

            elif ("not known" in pingResultLine):
              # append to all arrays to keep index in sync
              notResolving.append(item.rstrip())
              resolving.append("empty")
              resolvingTo.append("empty")
              bcolorsTag.append("\033[93m")
              changeCount.append(0)

          # increment counter used to refer back to previous run 
          w+=1         
        # clear screen each time just before printing latest info
        os.system('clear')
        # set default colour for the list of VMs to amber
        bcolors.vmTag='\033[93m'
        print("################################")
        print("##     Pinging %s devices " %str(itemsCount))
        # only print the last results info
        for x in range(i*itemsCount, len(resolving)):
          if (not "empty" in resolving[x]):
            print("## %s resolving to: %s %s %s - (%s)" %(resolving[x], bcolorsTag[x], resolvingTo[x], bcolors.END, changeCount[x]))
          else:
            print("## %s is not resolving!" %notResolving[x])
      
      # increment counter used to control amount of runs
      i+=1
    print(changeCounter)
  else:
    print("Please ensure ping.txt exists in this scripts folder.")

if __name__ == '__main__':
    main()
