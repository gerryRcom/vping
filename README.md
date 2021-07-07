# vping
Visual Ping, a python utility to monitor multiple ping results

The requirement for this stems for some work we had to do with some internal sites, needed to monitor a large amount of CNAME changes and take certain actions as they resolved to their new address.

The idea is for future such sessions we can have the script running against the list of sites and have it dynamically change as the changes take effect.

* add list of items to be pinged to the `ping.txt` file.
* run the `vping.py` script.
* terminal output will keep updating as the devices resolve.
* `ctrl + c` to quit out of.


Screenshot (once it exists)