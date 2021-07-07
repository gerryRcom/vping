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
    print("################################")
    print("## Preparing initial results ...")

    i = 0
    while (i < 5):

      with open('ping.txt') as items:
        allItems = items.readlines()
        itemsCount = len(allItems)
        resolving = []
        resolvingTo = []
        notResolving = []      

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

            elif ("not known" in pingResultLine):
              #print("## %s not resolving " %item.rstrip())
              notResolving.append(item.rstrip())
              resolving.append("empty")
              resolvingTo.append("empty")
        
        os.system('clear')
        print("################################")
        print("##     Pinging %s devices " %str(itemsCount))
        for x in range(len(resolving)):
          if (not "empty" in resolving[x]):
            print("## %s resolving to: %s %s" %(resolving[x], resolvingTo[x], x))
          else:
            print("## %s is not resolving %s " %(notResolving[x], i))
      
      i+=1

  
  else:
    print("Please ensure ping.txt exists in this scripts folder.")



if __name__ == '__main__':
    main()