# coding=utf-8
 
import os
from os import listdir
from os.path import isfile, join
import datetime
import random
import time
from datetime import date
from selenium import webdriver

#####
from itertools import groupby
from datetime import datetime
import time
import datetime
import requests
from lxml import html
import time
import sys
import csv
# from __future__ import print_function
import pandas as pd #Nuevo
#from google.colab import files


#####


def mes_text(mes):
    if mes == 1:
        return ("Ene")
    elif mes == 2:
        return ("Feb")
    elif mes == 3:
        return ("Mar")
    elif mes == 4:
        return ("Abr")
    elif mes == 5:
        return ("May")
    elif mes == 6:
        return ("Jun")
    elif mes == 7:
        return ("Jul")
    elif mes == 8:
        return ("Ago")
    elif mes == 9:
        return ("Sep")
    elif mes == 10:
        return ("Oct")
    elif mes == 11:
        return ("Nov")
    elif mes == 12:
        return ("Dic")


# def ayer():
#     today = datetime.date.today()
#     oneday = datetime.timedelta(days=1)
#     yesterday = today - oneday
#     ayer = str(yesterday.day) + "-" + str(yesterday.month) + "-" + str(yesterday.year)
#     return ayer

#hoy = datetime.datetime.now()


def parsetoDate(dat):
    if dat.lower() == 'hoy':
        day_temp = str(datetime.datetime.now().year) + "-" + \
            str(datetime.datetime.now().month) + \
            "-" + str(datetime.datetime.now().day)
    elif dat.lower() == 'ayer':
        today = datetime.date.today()
        oneday = datetime.timedelta(days=1)
        yesterday = today - oneday
        day_temp = str(yesterday.year) + "-" + \
            str(yesterday.month) + "-" + str(yesterday.day)
    elif dat.find('HACE') >= 0 or dat.find('Hace') >= 0:
        d = int(dat[5:6])
        today = datetime.date.today()
        oneday = datetime.timedelta(days=d)
        anyday = today-oneday
        day_temp = str(anyday.year) + "-" + \
            str(anyday.month) + "-" + str(anyday.day)
    else:
        d = int(dat[:1])
        today = datetime.date.today()
        oneday = datetime.timedelta(days=d)
        anyday = today-oneday
        day_temp = str(anyday.year) + "-" + \
            str(anyday.month) + "-" + str(anyday.day)

    return day_temp

def clean_post_content(content):
    replacements = {
        "á": "a",
        "é": "e",
        "í": "i",
        "ó": "o",
        "ú": "u",
        'ñ': 'ni'
    }
   # print(content)
    content = content.encode('utf-8').strip()
    content = str(content).lower().replace('ñ', 'ni').replace(' ', '')
   # print('********')
   # print(content)
   
    # print('********')
    # print(content)
    # print('********')
    chars = ['_', '.', ',', '-', '/', '$', '1',
             '2', '3', '4', '5', '6', '7', '8', '9', '0']
    vocals = ['á', 'é', 'í', 'ó', 'ú']
    for vocal in vocals:
        content = content.replace(vocal, replacements.get(vocal, 'error'))
    for char in content:
        if char in chars:
            content = content.replace(char, '')
    return content


def clean_id(id):
    id = id.replace('-', '').replace(' ', '')
    return id

# def hoy():
#     today = datetime.date.today()
#     hoy = str(today.day) + " " + str(mes_text(today.month))
#     return hoy


def lectura():
   # options = webdriver.ChromeOptions() #webdriver.Chrome()# webdriver.Firefox()
    
    # driver.get('https://'+ciudad+'.olx.com.co/apartamentos-casas-alquiler-cat-363')
    # driver.get('https://www.olx.com.co/antioquia_g2007002/apartamentos-casas-arriendo_c363')

   # driver = webdriver.Chrome()# webdriver.Firefox()
  #  options.add_argument("--start-maximized")
   # driver = webdriver.Chrome(chrome_options=options)

    driver = webdriver.Firefox()
    driver.maximize_window()

    links = []
    links_depurado = []
    links_depurados = []
    archivo_salida_links = "links_olx_cats_" + str(date.today()) + ".csv"
    DataOut = open(archivo_salida_links, 'a')
    inicio = time.clock()
    # driver.get('https://www.olx.com.co/cali_g4069078/apartamentos-casas-arriendo_c363')
    driver.get('https://www.olx.com.co/items/q-perros')

    cont = True
    while (cont):
        # driver.maximize_window()

        for x in range(1, 2):
            time.sleep(1)
            driver.execute_script( "window.scrollTo(0,document.body.scrollHeight)")

            time.sleep(5)
            driver.find_element_by_xpath(
                "/html/body/div/div/main/div/section/div/div/div[4]/div[2]/div/div[3]/button").click()
        try:
            time.sleep(2)
            text_contents = [el.get_attribute('href') for el in driver.find_elements_by_xpath(
                "/html/body/div/div/main/div/section/div/div/div/div/div/div/ul/li/a")]
            date_contents = [(parsetoDate(el.text) + ' - ' + str(datetime.datetime.now().hour) + '-' + str(datetime.datetime.now().minute)) for el in driver.find_elements_by_xpath(
                "/html/body/div/div/main/div/section/div/div/div/div/div/div/ul/li/a/div/div/span/span")]
            pauta_contents = [el.text for el in driver.find_elements_by_xpath(
                "/html/body/div/div/main/div/section/div/div/div/div/div/div/ul/li/a/div/div/label/span")]
            post_contents = [el.text for el in driver.find_elements_by_xpath(
                '/html/body/div/div/main/div/section/div/div/div[4]/div[2]/div/div[2]/ul/li/a/div/span[2]')]
                
            print(len(date_contents))
            print(len(post_contents))
            print(len(text_contents))
            
            print(post_contents)

            cont += 1
        except:
            print('Error')
        time.sleep(1)

        m = len(text_contents)
        print('***')
        print(m)
        print('***')
        if m == 600:
            cont = False

        for i in range(len(text_contents)):
            #post_id = clean_id(clean_post_content(post_contents[i]) + date_contents[i])
            post_id = 123#clean_id(clean_post_content(post_contents[i]))
            try:
                links.append([post_id, text_contents[i],
                              date_contents[i][0:9], pauta_contents[i]])
            except:
                links.append([post_id, text_contents[i],
                              date_contents[i][0:9], "NO"])
             # print(links[i])

            DataOut.write(str(links[i][0]) + "," + str(links[i][1]) + "," + str(links[i][2]))
            DataOut.write('\n')

        for i in links:
            if i[0] not in links_depurado:
                links_depurado.append(i[0])
                links_depurados.append(i)
                # print(i)

    # print('inmuebles: ' + str(len(links_depurados)))
    # print('clicks: '+ str(cont))
    # print(links)
    final = time.clock()
    tiempo_ejecucion = final - inicio
    print("Número registros leidos: " + str(len(links)))
    print("Número registros únicos: " + str(len(links_depurado)))
    print("Fecha ejecución: " + str(date.today()))
    print("Tiempo ejecución: " + str(tiempo_ejecucion) + " segundos")
    DataOut.close()
    driver.quit()

    return links_depurados


lectura()

time.sleep(20)

##############################
	

# currentPath = os.getcwd() # current directory 2.7
# print(currentPath)

# files = []
# for i in listdir(currentPath):
#    if i.endswith('.csv'):
#        files.append(join(currentPath, i))
# print(files)

# f = open(files[0], "r")

# for x in f:
#    print(x)
#    print("***    ***")


##################################


