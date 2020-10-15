#!/usr/bin/python -tt
# Project: netmiko38
# Filename: test
# claudia
# PyCharm

from __future__ import absolute_import, division, print_function

__author__ = "Claudia de Luna (claudia@indigowire.net)"
__version__ = ": 1.0 $"
__date__ = "4/20/20"
__copyright__ = "Copyright (c) 2018 Claudia"
__license__ = "Python"

import argparse
import netmiko
import os
import save2xl_tabs
import datetime



def main():
    """
    Basic Netmiko script showing how to connect to a device and save the output.
    """


    user = 'admin'
    pwd = 'Admin_1234!'
    sec = 'Admin_1234!'

    # dev = {
    #     'device_type': 'cisco_nxos',
    #     'ip' : 'sbx-nxos-mgmt.cisco.com',
    #     'username' : user,
    #     'password' : pwd,
    #     'secret' : sec,
    #     'port' : 8181
    #
    # }
    #
    # dev_asa = {
    #     'device_type': 'cisco_asa',
    #     'ip' : '10.1.10.27',
    #     'username' : 'cisco',
    #     'password' : 'cisco',
    #     'secret' : 'cisco',
    #     'port' : 22
    #
    # }

    user = 'root'
    pwd = 'D_Vay!_10&'
    sec = 'D_Vay!_10&'
    #
    dev = {
        'device_type': 'cisco_ios',
        'ip' : 'ios-xe-mgmt.cisco.com',
        'username' : user,
        'password' : pwd,
        'secret' : sec,
        'port' : '8181'
    }


    # RAW Parsing with Python
    print(f"\n===============  Get Show Command with Netmiko  ===============")
    try:
        # Get today's date to use in filenames
        datestamp = datetime.date.today()

        # Connect to Device
        dev_conn = netmiko.ConnectHandler(**dev)
        dev_conn.enable()
        response = dev_conn.send_command('show version')
        print(f"\nResponse is of type {type(response)}\nRaw Response is:\n{response}")

        # because the response is a string we need to do some string manipulation
        # first we need to split the string into lines
        resp = response.splitlines()

        with open(f"{dev['ip']}_{datestamp}.txt", 'w') as sample_file:
            sample_file.write(response)

        # Save Raw Out put to a Tab in an Exel

        # Define an Excel Workbook filename
        xlfilename = f"{dev['ip']}_{datestamp}.xlsx"

        # Create an Excl Workbook Object
        xobj = save2xl_tabs.create_xlwkbk()

        # Add a Tab to the Excel Workbook Ojbect
        tab_name = "RAW_OUTPUT"
        save2xl_tabs.create_xltab(xobj, tab_name)

        print(f"===== Saving to Excel file {xlfilename} on Tab {tab_name} ====")

        # Add a Tab to the Excel Workbook to save the splitline Output
        tab_name = "SPLITLINE_OUTPUT"
        save2xl_tabs.create_xltab(xobj, tab_name)

        print(f"===== Saving to Excel file {xlfilename} on Tab {tab_name} ====")


        # Save the Excel Workbook Object to Disk
        res, filepath = save2xl_tabs.save_xlwkbk(xobj, xlfilename)

        print(f"===== Saving the Excel file with tabs {xobj.sheetnames} to path {filepath} ====")

        # Open the Excel file and list the Tabs
        wkbk = save2xl_tabs.open_xlwkbk(filepath)
        print(wkbk.sheetnames)


    except Exception as e:
        print(e)


# Standard call to the main() function.
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Script Description",
                                     epilog="Usage: ' python test' ")

    #parser.add_argument('all', help='Execute all exercises in week 4 assignment')
    parser.add_argument('-a', '--all', help='Execute all exercises in week 4 assignment', action='store_true',
                        default=False)
    arguments = parser.parse_args()
    main()
