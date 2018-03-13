#!/usr/bin/python3

import os
import sys
import openpyxl
import re

wb = openpyxl.load_workbook('/home/raja/ToradexModules/Colibri_iMX7_512MB.xlsx')
ws1 = wb.active

# Open a new text file and write the contents of countyData to it.
print('Writing results...')
resultFile = open('/home/raja/Colibri_iMX7_512MB.conf', 'w')

resultFile.write('# Toradex Colibri iMX7 ComputerOn Module' + '\r\n')
resultFile.write('# http://developer.toradex.com/products/colibri-imx7' + '\r\n\n')

resultFile.write('[board]' + '\r\n')
resultFile.write('dtfile = /proc/device-tree/model' + '\r\n')
resultFile.write('model = Toradex Colibri iMX7 on Colibri Evaluation Board' + '\r\n\n')

resultFile.write('[GPIO]' + '\r\n')
resultFile.write('### Colibri IMX7 SODIMM number to GPIO number mapping' + '\r\n\n')

print('Reading rows...')
for row in range(2, ws1.max_row + 1):
        # Each row in the spreadsheet has data for one census tract.
         sodimmNo = ws1['B' + str(row)].value
         gpioStr = ws1['D' + str(row)].value

         #This is less time consuming option, dut don't know how to use it
         #s = [int(s) for s in gpioStr.split() if s.isdigit()]

         print(gpioStr)
         gpioStr1 = re.findall('\d+', gpioStr)
         print(gpioStr1)

         firstNumber = int(gpioStr1[0])
         secondNumber = int(gpioStr1[1])
         gpioNo = (firstNumber -1) * 32 + secondNumber

         print(firstNumber, secondNumber, gpioNo)

         gpioStr = str(gpioNo)
         sodimmStr = str('SODIMM_') + str(sodimmNo)

         resultFile.write(sodimmStr + ' = ' + gpioStr + '\n')
         print(sodimmStr + '=' + gpioStr)

resultFile.close()
print('Done.')
