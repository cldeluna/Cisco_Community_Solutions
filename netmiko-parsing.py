#!/usr/bin/python -tt
# Project: Cisco_Community_Solutions
# Filename: netmiko-parsing
# claudia
# PyCharm

from __future__ import absolute_import, division, print_function

__author__ = "Claudia de Luna (claudia@indigowire.net)"
__version__ = ": 1.0 $"
__date__ = "10/15/20"
__copyright__ = "Copyright (c) 2020 Claudia"
__license__ = "Python"

import argparse
import netmiko
import os


def main():
    """
    Basic Netmiko script showing how to connect to a device and save the output.
    The first section only shows how to get raw output.
    The second section shows how to use TextFMS to parse the raw output into structured data.

    """

    # Set the environment variable NET_TEXTFSM to point to the ntc-templates directory
    os.environ["NET_TEXTFSM"] = "./ntc-templates/templates"

    # Dictionary of device dictionaries for Netmiko
    devices_dict = {
        'nxos': {
            'device_type': 'cisco_nxos',
            'ip': 'sbx-nxos-mgmt.cisco.com',
            'username': 'admin',
            'password': 'Admin_1234!',
            'secret': 'Admin_1234!',
            'port': 8181
        },
        'asa': {
            'device_type': 'cisco_asa',
            'ip': '10.1.10.27',
            'username': 'cisco',
            'password': 'cisco',
            'secret': 'cisco',
            'port': 22
        },

        'ios': {
            'device_type': 'cisco_ios',
            'ip' : 'ios-xe-mgmt.cisco.com',
            'username' : 'root',
            'password' : 'D_Vay!_10&',
            'secret' : 'D_Vay!_10&',
            'port' : '8181'
        }
    }


    # RAW Parsing with Python
    print(f"\n===============  Netmiko ONLY ===============")
    try:
        dev_conn = netmiko.ConnectHandler(**devices_dict['nxos'])
        dev_conn.enable()
        response = dev_conn.send_command('show version')
        print(f"\nResponse is of type {type(response)}\n")
        print(response)
        # because the response is a string we need to do some string manipulation
        # first we need to split the string into lines
        resp = response.splitlines()

        with open('test.txt', 'w') as sample_file:
            sample_file.write(response)

        # now we should have a list in the variable resp over which we can iterate
        print(f"\nSplit Response is of type {type(resp)}\n")
        print(resp)
        find_string = "NXOS: version"
        # look
        for line in resp:
            if find_string in line:
                print(f"******** FOUND LINE! ******\n{line}\n")

    except Exception as e:
        print(e)

    # Parsing with Netmiko's support of TEXTFSM and the NTC Template library
    print(f"\n===============  Netmiko with TEXTFSM OPTION  ===============")
    try:
        dev_conn = netmiko.ConnectHandler(**devices_dict['nxos'])
        dev_conn.enable()
        response = dev_conn.send_command('show interface', use_textfsm=True)
        print(f"\nResponse is of type {type(response)}\n")
        print(response)
        print(f"\n== Pick out specific information from the response!")
        print(f"The OS is {response[0]['os']}")
        print(f"The Platform is {response[0]['platform']}")
        print(f"The boot image is {response[0]['boot_image']}")

    except Exception as e:
        print(e)


# Standard call to the main() function.
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Script Description",
                                     epilog="Usage: ' python netmiko-parsing.py' ")
    arguments = parser.parse_args()
    main()
