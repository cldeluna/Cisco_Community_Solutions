#!/usr/bin/python -tt
# Project: netmiko38
# Filename: ccom
# claudia
# PyCharm

from __future__ import absolute_import, division, print_function

__author__ = "Claudia de Luna (claudia@indigowire.net)"
__version__ = ": 1.0 $"
__date__ = "9/29/20"
__copyright__ = "Copyright (c) 2018 Claudia"
__license__ = "Python"

import argparse
import pandas as pd
import netmiko
import os
import json
from getpass import getpass

## Cisco Community Example

def main():

    os.environ["NET_TEXTFSM"] = "./ntc-templates/templates"

    password = getpass()
    hostname = "10.1.10.216"
    net_connect = netmiko.Netmiko(host=hostname, username='cisco', password=password, device_type='cisco_ios')
    mac_table = net_connect.send_command("show mac address-table", use_textfsm=True)
    print(mac_table)
    print(len(mac_table))
    for line in mac_table:
        print(json.dumps(line, indent=4))
    mac_data = {'mac': [entry['destination_address'] for entry in mac_table],
                'interface': [entry['destination_port'] for entry in mac_table],
                'vlan': [entry['vlan'] for entry in mac_table]
                }

    df = pd.DataFrame(mac_data, columns=list(mac_data.keys()))
    print(df.head())

    df.to_excel('mac_table.xlsx')

    # Saving to a specific Excel Sheet or Tab

    # First create a Pandas Excel Writer "object"
    xlwriter_object = pd.ExcelWriter('MAC_TABLES.xlsx')

    # Save the data frame to a specific tab or sheet in your writer object
    df.to_excel(xlwriter_object, hostname)

    # Save the object to a file
    xlwriter_object.save()


# Standard call to the main() function.
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Script Description",
                                     epilog="Usage: ' python ccom' ")
    arguments = parser.parse_args()
    main()
