#! /usr/bin/python
# -*- coding:utf-8 -*-
# Filename: writecsv.py
# Author: xiaobing
# E-mail: xiaobingzhang29@gmail.com
# Date: 2013-11-02
# Description:
import configparser
import csv
import os

aaid = 'aaid'
ametlin = 'ametlin'
blmass = 'blmass'
ename = 'ename'
hformula = 'fformula'
fgcas = 'fgcas'
kegg = 'fhegg'
gxms = 'gams'
gcollisionenergy_value = 'gcollisionenergyvalue'
gh_mode = 'ghmode'
xy = 'xy'

#写入excel
def save(dict_writer,rows):
        # 多行写入
        dict_writer.writerows(rows)


def saverow(dict_writer, oneline):
    # 多行写入
    dict_writer.writerow(oneline)

#创建excel
def creatCvs(csvFile):
    fieldnames = {ametlin: 'METLIN ID', blmass: 'Mass', ename: 'Name', hformula: 'Formula', fgcas: 'CAS',
                  kegg: 'KEGG', gxms: 'MS/MS', gcollisionenergy_value: 'collision_energy', gh_mode: 'Mode',
                  xy:'x和y'
                  }
    if os.path.isfile(csvFile):
        csvfile = open(csvFile, 'a+', newline='',encoding='utf-8')
        dict_writer = csv.writer(csvfile)
    else:
        csvfile = open(csvFile, 'a+', newline='', encoding='utf-8')
        dict_writer = csv.writer(csvfile)
    return dict_writer

def getLastIndexAndAddOne():
    csvFile = 'american.csv'
    with open(csvFile, newline='',encoding='utf-8') as f:
        reader = csv.reader(f)
        # for row in reader:
        #     print(row)
        # column = [row[0] for row in reader]
        for row in reader:
            if len(row) > 0:
                column = row[0]
                if column and len(column) > 0:
                    str = column[-1]
                    print('最后一个index是:%s'% str)
                    index = 1
                    if str:
                        index = int(str) + 1
                    return index
                else:
                    return 1
            else:
                return 1

if __name__ == "__main__":
    csvFile = 'american.csv'
    # dict_writer = creatCvs(csvFile)
    # rows = [{ametlin: 'METLIN ID', blmass: 'Mass', ename: 'Name', hformula: 'Formula', fgcas: 'CAS', kegg: 'KEGG',
    #  gxperimental: 'Experimental'
    #  }]
    # dict_writer.writerows(rows)
    # save(dict_writer, rows)
    # spamwriter = creatCvs(csvFile)
    # spamwriter.writerow(['Spam'] * 5 + ['Baked Beans'])
    # spamwriter.writerow(['Spam', 'Lovely Spam', 'Wonderful Spam'])
    with open(csvFile, newline='') as f:
        reader = csv.reader(f)
        # for row in reader:
        #     print(row)
        column = [row[0] for row in reader]
        print(type(column))
        str = column[-1]
        print(str)
        print(type(str))
        index = int(str) + 1
        print(index)
