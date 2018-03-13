#!/usr/bin/python3

import os
import sys
import openpyxl
import re

print('This is the name of the script:', sys.argv[0])
print('Number of arguments:', len(sys.argv))
print('The arguments are:', str(sys.argv))

#excel_sheet_filename = str(sys.argv[1])
excel_sheet_filename = str('Apalis_iMX6.xlsx')
#excel_sheet_filename = str('Colibri_iMX7_512MB.xlsx')

wb = openpyxl.load_workbook(excel_sheet_filename)
ws1 = wb.active

print(excel_sheet_filename)
tmp_str = re.split('[_.]', excel_sheet_filename)
result_file_name = tmp_str[0] + '_' + tmp_str[1] + '_' + tmp_str[2] + str('.conf')

# Open a new text file and write the contents of countyData to it.
print('Writing results...')
resultFile = open(result_file_name, 'w')

resultFile.write('# Toradex ' + tmp_str[0] + ' ' + tmp_str[1] + ' Computer On Module.' + '\r\n')
resultFile.write('# http://developer.toradex.com/products/' + tmp_str[0].lower() + '-' + tmp_str[1].lower() + '\r\n\n')

resultFile.write('[board]' + '\r\n')
resultFile.write('dtfile = /proc/device-tree/model' + '\r\n')
resultFile.write('model = Toradex ' + tmp_str[0] + ' ' + tmp_str[1] + ' on ' + tmp_str[0] + ' Evaluation Board' + '\r\n\n')

resultFile.write('[GPIO]' + '\r\n')
resultFile.write('###' + tmp_str[0] + ' ' + tmp_str[1].upper() + ' SODIMM number to GPIO number mapping' + '\r\n\n')

#column_port_heading = str()

#if tmp_str[1].lower() == 'imx7':
#    column_port_heading = (tmp_str[1] + '_' + tmp_str[2] + str(' Function')).lower()
#elif tmp_str[1].lower() == 'vf50':
#    column_port_heading = str('VF50 Note2')

column_pin_heading = input('Enter sodimm pin column name where only pin number is specified:')
column_port_heading = input('Enter gpio port information column heading name:')

column_port = int(1)
column_pin = int(1)

for tmp in range(1, ws1.max_column):
    column_str = ws1.cell(1, tmp).value
    if column_str.lower() == column_pin_heading.lower():
        column_pin = tmp
    if column_str.lower() == column_port_heading.lower():
        column_port = tmp

pin_name = str()

if tmp_str[0].lower() == str('colibri'):
    pin_name = str('SODIMM_')
elif tmp_str[0].lower() == str('apalis'):
    pin_name = str('MXM3_')

print('Reading rows...')
for row in range(2, ws1.max_row + 1):
        # Each row in the spreadsheet has data for one census tract.

    sodimm_number= ws1.cell(row, column_pin).value
    gpio_str = ws1.cell(row, column_port).value

    #This is less time consuming option, dut don't know how to use it
    #s = [int(s) for s in gpioStr.split() if s.isdigit()]

#   print(gpio_str)
    gpio_str_split = re.findall('\d+', gpio_str)
#   print(gpio_str_split)

    bank_number = int(gpio_str_split[0])
    offset_number = int(gpio_str_split[1])
    gpio_number = bank_number * 32 + offset_number

#   print(bank_number, offset_number, gpio_number)

    gpio_number_str = str(gpio_number)
    sodimm_number_str = pin_name + str(sodimm_number)

    resultFile.write(sodimm_number_str + ' = ' + gpio_number_str + '\n')
#   print(sodimm_number_str + '=' + gpio_number_str)

    if(gpio_str_split.__len__() == 4):
        bank_number = int(gpio_str_split[2])
        offset_number = int(gpio_str_split[3])
        gpio_number = (bank_number - 1) * 32 + offset_number
        gpio_number_str = str(gpio_number)
        sodimm_number_str += "#"
        resultFile.write(sodimm_number_str + ' = ' + gpio_number_str + '\n')
#       print(sodimm_number_str + '=' + gpio_number_str)

resultFile.close()
print('Done.')
