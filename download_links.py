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
    archivo_salida_links = "links_olx_" + str(date.today()) + ".csv"
    DataOut = open(archivo_salida_links, 'a')
    inicio = time.clock()
    driver.get('https://www.olx.com.co/cali_g4069078/apartamentos-casas-arriendo_c363')
    cont = True
    while (cont):
        # driver.maximize_window()

        for x in range(1, 30):
            time.sleep(1)
            driver.execute_script( "window.scrollTo(0,document.body.scrollHeight)")

        

            time.sleep(5)
            driver.find_element_by_xpath(
                "/html/body/div[1]/div/main/div/section/div/div/div[5]/div[2]/div/div[3]/button").click()
        try:
            time.sleep(2)
            text_contents = [el.get_attribute('href') for el in driver.find_elements_by_xpath(
                "/html/body/div/div/main/div/section/div/div/div/div/div/div/ul/li/a")]
            date_contents = [(parsetoDate(el.text) + ' - ' + str(datetime.datetime.now().hour) + '-' + str(datetime.datetime.now().minute)) for el in driver.find_elements_by_xpath(
                "/html/body/div/div/main/div/section/div/div/div/div/div/div/ul/li/a/div/div/span/span")]
            pauta_contents = [el.text for el in driver.find_elements_by_xpath(
                "/html/body/div/div/main/div/section/div/div/div/div/div/div/ul/li/a/div/div/label/span")]
            post_contents = [el.text for el in driver.find_elements_by_xpath(
                '/html/body/div[1]/div/main/div/section/div/div/div[5]/div[2]/div/div[2]/ul/li/a/div/span[3]')]

            print(len(date_contents))
            print(len(post_contents))

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
            post_id = clean_id(clean_post_content(post_contents[i]) + date_contents[i])
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
	

#currentPath = os.getcwd() # current directory 2.7
#print(currentPath)

#files = []
#for i in listdir(currentPath):
#    if i.endswith('.csv'):
#        files.append(join(currentPath, i))
#print(files)

#f = open(files[0], "r")

#for x in f:
 #   print(x)
  #  print("***    ***")


##################################




def download(url):
    """Returns the HTML source code from the given URL
        :param url: URL to get the source from.
    """
    r = requests.get(url)
    if r.status_code != 200:
        sys.stderr.write("! Error {} retrieving url {}\n".format(r.status_code, url))
        return None

    return r
def mes_text(mes):
    meses = {
        1: "Ene",
        2: "Feb",
        3: "Mar",
        4: "Abr",
        5: "May",
        6: "Jun",
        7: "Jul",
        8: "Ago",
        9: "Sep",
        10: "Oct",
        11: "Nov",
        12: "Dec"
    }
    return meses.get(mes, "Mes Invalido")
    
def ayer():
    today=datetime.date.today() 
    oneday=datetime.timedelta(days=1)
    yesterday=today-oneday
    ayer = str(yesterday.day) + " " + str(mes_text(yesterday.month))
    return ayer
def hoy():
  today=datetime.date.today()
  hoy = str(today.day) + " " + str(mes_text(today.month))
  return hoy
def limpiar(texto):
    a=''
    for i in texto:
        if(i.isalpha() or i.isdigit() or i.isspace()):
            a=a+i
    a = a.replace('\n                        ','')
    a = a.replace('\n            ','')
    a = a.replace('\n        ','')
    a = a.replace('\n', ' ')
    a = a.replace('\n', ' ')
    return(a)

def sintilde(s):
    replacements = (
        ("á", "a"),
        ("é", "e"),
        ("í", "i"),
        ("ó", "o"),
        ("ú", "u"),
    )
    s = s.lower()
    for a, b in replacements:
        s = s.replace(a, b).replace(a.upper(), b.upper())
    return s

def limpiar_precio(precio):
    a=''
    for i in precio:
        if(i.isdigit()):
            a=a+i
    return(a)

def tipo_inmueble_fun(publicacion):
  if(publicacion.lower().find("casafinca") > -1 ):
    return("Casafinca")
  elif(publicacion.lower().find("casa") > -1 ):
    return("Casa")
  elif(publicacion.lower().find("apartaestudio") > -1 ):
    return("Apartaestudio")
  elif(publicacion.lower().find("aparta") > -1 ):
    return("Apartamento")
  elif(publicacion.lower().find("apto") > -1 ):
    return("Apartamento")
  elif(publicacion.lower().find("habitacion") > -1 or publicacion.lower().find("habitación") > -1 ):
    return("Habitación")
  elif (publicacion.lower().find("estudio") > -1):
    return('Apartaestudio')
  elif (publicacion.lower().find("habitacion") > -1):
    return('Habitacion')
  elif (publicacion.lower().find("abitacion") > -1):
    return('Habitacion')
  elif (publicacion.lower().find("pieza") > -1):
    return('Habitacion')  
  elif (publicacion.lower().find("cuarto") > -1):
    return('Habitacion')
  else:
    return("None")



def type_seller(nombre_vendedor):
  if(nombre_vendedor.lower().find("inmobiliaria") > -1 ):  
    return  "Inmobiliaria"
  elif(nombre_vendedor.lower().find("propiedad") > -1 ):
    return  "Inmobiliaria"
  elif(nombre_vendedor.lower().find("arrendamientos") > -1 ):
    return  "Inmobiliaria"
  elif(nombre_vendedor.lower().find("bienes") > -1 ):
    return  "Inmobiliaria"
  elif(nombre_vendedor.lower().find("inversión") > -1 ):
    return  "Inmobiliaria"
  else:
    return 'None'

def mt_cuadrados_fun():
  try:
    label_metros_cuadrados = tree.xpath('/html/body/div/div/main/div/div/div[4]/section[1]/div/div/div[1]/div/div[4]/div/span[1]//text()')
    label_metros_cuadrados = r"".join(label_metros_cuadrados)
    if label_metros_cuadrados.lower() == 'metros cuadrados totales':
      mt_cuadrados = tree.xpath('/html/body/div/div/main/div/div/div[4]/section[1]/div/div/div[1]/div/div[4]/div/span[2]//text()')
      mt_cuadrados = r"".join(mt_cuadrados)
      mt_cuadrados = limpiar(mt_cuadrados)
      return mt_cuadrados
    else:
      try:
        label_metros_cuadrados = tree.xpath('/html/body/div/div/main/div/div/div[4]/section[1]/div/div/div[1]/div/div[3]/div/span[1]//text()')
        label_metros_cuadrados = r"".join(label_metros_cuadrados)
        if label_metros_cuadrados.lower() == 'metros cuadrados totales':
          mt_cuadrados = tree.xpath('/html/body/div/div/main/div/div/div[4]/section[1]/div/div/div[1]/div/div[3]/div/span[2]//text()')
          mt_cuadrados = r"".join(mt_cuadrados)
          mt_cuadrados = limpiar(mt_cuadrados)
          return mt_cuadrado
        else:
          return 'None'
      except:
        return 'None'
  except:
    return "None"  
  
    
inicio = time.clock()
archivo_salida_info = 'inmuebles_olx_'+'_'+str(date.today())+'.csv'
contador = 1
Doc_errores = open('docu_errores.txt','a')
Doc_errores.write(str(date.today()))
'''
#CANON INFERIOR
list_fecha = []
list_tipo_vendedor = []
list_nombre_vendedor = []
list_publicacion = []
list_pauta = []
list_descripcion = [] 
list_tipo_inmueble = []
list_amoblado = []
list_barrio = []
list_telefono1 = []
list_telefono2 = []
list_metros2 = []
list_estrato = []
list_antiguedad = []
list_ubicacion = []
list_direccion = []
list_enlaces = []
list_precio = []
list_parqueadero = []
list_cuartos = []
list_banos = []
list_enlaces = [] 

#CANON SUPERIOR

list_fecha2 = []
list_tipo_vendedor2 = []
list_nombre_vendedor2 = []
list_publicacion2 = []
list_pauta2 = []
list_descripcion2 = []
list_tipo_inmueble2 = []
list_amoblado2 = []
list_barrio2 = []
list_telefono12 = []
list_telefono22 = []
list_metros22 = []
list_estrato2 = []
list_antiguedad2 = []
list_ubicacion2 = []
list_direccion2 = []
list_enlaces2 = []
list_precio2 = []
list_parqueadero2 = []
list_cuartos2 = []
list_banos2 = []
list_enlaces2 = []

'''
#TODOS LOS INMUEBLES

list_id_scrappin3 = []
list_fecha_anuncio3 = []
list_nombre_completo3 = []
list_cedula3 = []
list_email3 = []
list_telefono3 = []
list_fuente3 = []
list_demostracion_ingresos3 = []
list_carta_laboral3 = []
list_fiador_solvente3 = []
list_fiador_finca_raiz3 = []
list_tipo_propiedad3 = []
list_publicacion3 = []
list_descripcion3 = [] 
list_departamento3 = []
list_ciudad3 = []
list_barrio3 = []
list_direccion3 = []
list_estrato3 = []
list_precio3 = []
list_amoblado3 = []
list_area3 = []
list_banios3 = []
list_habitaciones3 = []
list_cocina3 = []
list_mascotas3 = []
list_conjunto_cerrado3 = []
list_parqueadero3 = []
list_enlace_fuente3 = []
list_titulo_publicacion_externa3 = []
list_descripcion_externa3 = []
list_tipo_vendedor3 = []


pasaron = 0
 
currentPath = os.getcwd() # current directory 2.7
print(currentPath)

filess = []
for ii in listdir(currentPath):
    if ii.endswith('.csv'):
        filess.append(join(currentPath, ii))
print(filess)

# f = open(files[0], "r")

# with open(filess[0], encoding='utf8', errors='replace') as File:  

# with open('/var/www/html/python_test/links_olx_2020-01-14.csv', "r") as File:  
# with open(filess[0], "r") as File:  

with open('/var/www/html/python_test/links_olx_2020-01-14.csv', "r") as File:  
    
    links = csv.reader(File,delimiter=',')
    for l in links:

      id_scrappin = ''
      fecha_anuncio = ''
      nombre_completo = '',
      cedula = '|'
      email = '|'
      telefono = '|'
      demostracion_ingresos = '|'
      carta_laboral = '|'
      fiador_solvente = '|' 
      fiador_finca_raiz = '|' 
      tipo_propiedad = ''
      descripcion= '|' 
      departamento = 'Valle del Cauca' 
      ciudad = 'Cali'
      barrio = ''
      direccion = '|' 
      estrato = ''
      precio = 0
      amoblado = ''
      area = ''
      banios = '' 
      habitaciones = '' 
      cocina = '|'
      mascotas = '|' 
      conjunto_cerrado = '|'  
      parqueadero = ''
      fuente = 'OLX'
      enlace_fuente = '' 
      titulo_publicacion_externa = ''  
      descripcion_externa = ''  
           
      print(l[1])

      #----------------------------

      try:
        page = download(l[1])
        tree = html.fromstring(page.content)
      except:
        print('error')
        Doc_errores.write('\n')
        Doc_errores.write('error con direccion' + l[1] + " " + direccion)

      #------------------------------------

      try:
        nombre_completo = tree.xpath('/html/body/div/div/main/div/div/div[5]/div[2]/div/div/div[2]/div/a/div//text()')
        nombre_completo = r"".join(nombre_completo)
        nombre_completo = limpiar(nombre_completo)
      except:
        nombre_completo = "None" 
        
      print('Nombre Completo: '+ nombre_completo)

      #------------------------------------------

      try:
        label_tipo_inmueble = tree.xpath('/html/body/div/div/main/div/div/div[4]/section[1]/div/div/div[1]/div/div[1]/div/span[1]//text()')
        label_tipo_inmueble = r"".join(label_tipo_inmueble)
        if label_tipo_inmueble.lower() == 'tipo':
          tipo_propiedad = tree.xpath('/html/body/div/div/main/div/div/div[4]/section[1]/div/div/div[1]/div/div[1]/div/span[2]//text()')
          tipo_propiedad  = r"".join(tipo_propiedad)        
        else:
          tipo_propiedad = tipo_inmueble_fun(tipo_propiedad)  
      except:
        tipo_propiedad = tipo_inmueble_fun(tipo_propiedad) 

      print("Tipo de inmueble: " + tipo_propiedad)
      #------------------------------------------

      try:
        barrio = tree.xpath('/html/body/div/div/main/div/div/div[5]/div[1]/div/section/div/div[1]/div/span//text()')
        barrio = r"".join(barrio)
        barrio = limpiar(barrio)
      except:
        barrio = "None"
      print("Ubicación: "+barrio)

      #----------------------------

      try:
        label_estrato = tree.xpath('/html/body/div/div/main/div/div/div[4]/section[1]/div/div/div[1]/div/div[7]/div/span[1]//text()')
        label_estrato = r"".join(label_estrato)
        if label_estrato.lower() == 'estrato':
          estrato = tree.xpath("/html/body/div/div/main/div/div/div[4]/section[1]/div/div/div[1]/div/div[7]/div/span[2]//text()")
          estrato = r"".join(estrato)
          estrato = limpiar(estrato)
        else:
          label_estrato = tree.xpath('/html/body/div/div/main/div/div/div[4]/section[1]/div/div/div[1]/div/div[5]/div/span[1]//text()')
          label_estrato = r"".join(label_estrato)
          if label_estrato.lower() == 'estrato':
            estrato = tree.xpath("/html/body/div/div/main/div/div/div[4]/section[1]/div/div/div[1]/div/div[5]/div/span[2]//text()")
            estrato = r"".join(estrato)
            estrato = limpiar(estrato)
          else:
            label_estrato = tree.xpath('/html/body/div/div/main/div/div/div[4]/section[1]/div/div/div[1]/div/div[6]/div/span[1]//text()')
            label_estrato = r"".join(label_estrato)
            if label_estrato.lower() == 'estrato':
              estrato = tree.xpath("/html/body/div/div/main/div/div/div[4]/section[1]/div/div/div[1]/div/div[6]/div/span[2]//text()")
              estrato = r"".join(estrato)
              estrato = limpiar(estrato)

      except:
        mt_cuadrados = 'None'
      print('estrato: '+ estrato)

      #----------------------------------

      try:
        precio_crudo = tree.xpath('/html/body/div/div/main/div/div/div[5]/div[1]/div/section/span[1]//text()')
        precio_crudo = r"".join(precio_crudo)
        precio = limpiar_precio(precio_crudo)
      except:
        precio = 0   
      if precio == "None":
        precio == 0      
      elif len(precio) == 0:
        precio = 0
      
      print("Precio: " + str(precio))

      #-----------------------------------------

      try:
        label_amoblado = tree.xpath('/html/body/div/div/main/div/div/div[4]/section[1]/div/div/div[1]/div/div[2]/div/span[1]//text()')
        label_amoblado = r"".join(label_amoblado)
        if label_amoblado.lower() == 'amueblado':
          amoblado = tree.xpath('/html/body/div/div/main/div/div/div[4]/section/div/div/div[1]/div/div[2]/div/span[2]//text()')
          amoblado = r"".join(amoblado)
        else:
          amoblado = 'No'
      except:
       amoblado = "No"
      print("Amoblado: " + amoblado)

      #-----------------------------------------

      try:
        label_metros_cuadrados = tree.xpath('/html/body/div/div/main/div/div/div[4]/section[1]/div/div/div[1]/div/div[5]/div/span[1]//text()')
        label_metros_cuadrados = r"".join(label_metros_cuadrados)
        if label_metros_cuadrados.lower() == 'metros cuadrados totales':
          area = tree.xpath("/html/body/div/div/main/div/div/div[4]/section/div/div/div[1]/div/div[5]/div/span[2]//text()")
          area = r"".join(area)
          area = limpiar(area)
        else:
          area = mt_cuadrados_fun()
      except:
        area = mt_cuadrados_fun()

      print('mt_cuadrados: '+ area)

      #-----------------------------------------
      
      try:
        banios = tree.xpath("/html/body/div/div/main/div/div/div[4]/section/div/div/div[1]/div/div[4]/div/span[2]//text()")
        banios = r"".join(banios)
      except:
        banios = "None"
      print('Baños: '+ banios)

      #----------------------------------------
      
      try:
        habitaciones = tree.xpath("/html/body/div/div/main/div/div/div[4]/section/div/div/div[1]/div/div[3]/div/span[2]//text()")
        habitaciones = r"".join(habitaciones)
      except:
        habitaciones = "None"
      
      print('Habitaciones: '+ habitaciones)

      # ----------------------------------------

      try:
        parqueadero = tree.xpath("/html/body/div/div/main/div/div/div[4]/section/div/div/div[1]/div/div[8]/div/span[2]//text()")
        parqueadero = r"".join(parqueadero)
      except:
        parqueadero = "None"
      print('parqueadero: '+ parqueadero)

      # ----------------------------------------

      try:
        titulo_publicacion_externa = tree.xpath('/html/body/div/div/main/div/div/div[5]/div[1]/div/section/h1//text()')
        titulo_publicacion_externa = r"".join(titulo_publicacion_externa)        
        titulo_publicacion_externa = limpiar(titulo_publicacion_externa)
      except:
        titulo_publicacion_externa  = "None" 

      print("Publicacion: " + str(titulo_publicacion_externa))
      
      # ----------------------------------------      
      
      
      try:
        descripcion_externa = tree.xpath('/html/body/div/div/main/div/div/div[4]/section/div/div/div[2]/p/text()')
        descripcion_externa = limpiar(r"".join(descripcion_externa))
      except:
        descripcion_externa = "None"
      
      print("Descripcion: " + str(descripcion_externa))
      
     
      
      

      
      '''
      try:
        tipo_vendedor = tree.xpath("/html/body/div/div/main/div/div/div[4]/section/div/div/div[1]/div/div[10]/div/span[2]//text()")
        tipo_vendedor = r"".join(tipo_vendedor)
        if tipo_vendedor == '':
          tipo_vendedor = type_seller(vendedor)
        if tipo_vendedor.isdigit():
          tipo_vendedor = type_seller(vendedor)
      except:
        tipo_vendedor = type_seller(vendedor)
      
      print('tipo_vendedor: '+ tipo_vendedor)
      '''
     


      try:
        list_id_scrappin3.append(l[0])
        list_fecha_anuncio3.append(l[2])
        list_nombre_completo3.append(nombre_completo)
        list_cedula3.append(cedula)
        list_email3.append(email)
        list_telefono3.append(telefono)
        list_fuente3.append(fuente)
        list_demostracion_ingresos3.append(demostracion_ingresos)
        list_carta_laboral3.append(carta_laboral)
        list_fiador_solvente3.append(fiador_solvente)
        list_fiador_finca_raiz3.append(fiador_finca_raiz)
        list_tipo_propiedad3.append(tipo_propiedad)
        list_descripcion3.append(descripcion)
        list_departamento3.append(departamento)
        list_ciudad3.append(ciudad)
        list_barrio3.append(barrio)
        list_direccion3.append(direccion)
        list_estrato3.append(estrato)
        list_precio3.append(precio)
        list_amoblado3.append(amoblado)
        list_area3.append(area)
        list_banios3.append(banios)
        list_habitaciones3.append(habitaciones)
        list_cocina3.append(cocina)
        list_mascotas3.append(conjunto_cerrado)
        list_conjunto_cerrado3.append(conjunto_cerrado)
        list_parqueadero3.append(parqueadero)
        list_enlace_fuente3.append(l[1])
        list_titulo_publicacion_externa3.append(titulo_publicacion_externa)
        list_descripcion_externa3.append(descripcion_externa)
        
            
      except:
        print("******* error print ++++")
        Doc_errores.write('\n')
        Doc_errores.write("error guardar informacion" + l[0])
    
            
      print("*****************************************************************")
      print(contador)
      print("*****************************************************************")
      contador += 1

      #with open('old_links.txt', 'r') as f:
        #lineas = [linea.strip() for linea in f]
      #for linea in lineas:
        #us = lineas
      #url_ = str(l[0])
      #telefono1_ = telefono1
      #links_repetidos = us.count(url_) #Encuentra el numero de veces que la url se repite en el texto, mediante el modulo count.
      #print('Repetidos: '+ str(links_repetidos))
      
      #with open('old_tels.txt', 'r', encoding='utf-8', errors='ignore') as t:
        #lineas2 = [linea.strip() for linea in t]
      #for linea in lineas2:
        #ut = lineas2
      #tel_usados = open('old_tels.txt', 'r+')
      
      #tel_rep = ut.count(str(telefono1))
      #print("tel Repetidos : "+ str(tel_rep))
      #print(tel_rep)
      '''
      if tipo_vendedor== "Dueño Directo":
        pasaron += 1
        if (int(precio) <= 1200000):
          print('CANON INFERIOR')
          try:
            print('hola')
            list_fecha_adquisicion.append(hoy())
            list_fecha.append(fecha)
            list_tipo_vendedor.append(tipo_vendedor)
            list_nombre_vendedor.append(vendedor)
            list_publicacion.append(publicacion)
            list_pauta.append(pauta)
            list_descripcion.append(descripcion)
            list_tipo_inmueble.append(tipo_inmueble)
            list_amoblado.append(amoblado)
            list_metros2.append(mt_cuadrados)
            list_estrato.append(estrato)
            list_precio.append(precio)
            list_parqueadero.append(parqueadero)
            list_cuartos.append(cuartos)
            list_banos.append(baños)
            list_antiguedad.append(antiguedad)
            list_ubicacion.append(ubicacion)
            list_enlaces.append(l[0])
          except:
            print("******* error print ++++")
            Doc_errores.write('\n')
            Doc_errores.write("error guardar informacion" + l[0])
        else:
          try:
            list_fecha_adquisicion2.append(hoy())
            list_fecha2.append(fecha)
            list_tipo_vendedor2.append(tipo_vendedor)
            list_nombre_vendedor2.append(vendedor)
            list_publicacion2.append(publicacion)
            list_pauta2.append(pauta)
            list_descripcion2.append(descripcion)
            list_tipo_inmueble2.append(tipo_inmueble)
            list_amoblado2.append(amoblado)
            list_metros22.append(mt_cuadrados)
            list_estrato2.append(estrato)
            list_precio2.append(precio)
            list_parqueadero2.append(parqueadero)
            list_cuartos2.append(cuartos)
            list_banos2.append(baños)
            list_antiguedad2.append(antiguedad)
            list_ubicacion2.append(ubicacion)
            list_enlaces2.append(l[0])
          except:
            print("******* error print ++++")
            Doc_errores.write('\n')
            Doc_errores.write("error guardar informacion" + l[0])
            '''

      


print(len(list_id_scrappin3))
print(len(list_fecha_anuncio3))
print(len(list_nombre_completo3))
print(len(list_cedula3))
print(len(list_email3))
print(len(list_telefono3))
print(len(list_demostracion_ingresos3))
print(len(list_carta_laboral3))
print(len(list_fiador_solvente3))
print(len(list_fiador_finca_raiz3))
print(len(list_tipo_propiedad3))
print(len(list_descripcion3))

print(len(list_departamento3))
print(len(list_ciudad3))
print(len(list_barrio3))
print(len(list_direccion3))
print(len(list_estrato3))
print(len(list_precio3))
print(len(list_amoblado3))
print(len(list_area3))
print(len(list_banios3))
print(len(list_habitaciones3))
print(len(list_cocina3))
print(len(list_mascotas3))

print(len(list_conjunto_cerrado3))
print(len(list_parqueadero3))
print(len(list_fuente3))
print(len(list_enlace_fuente3))
print(len(list_titulo_publicacion_externa3))
print(len(list_descripcion_externa3))




archivo_salida_info = 'inmuebles_olx_Cal_'+str(date.today())+'.csv'
#cannon_inferior = 'Depurado_OLX_CANNON_INFERIOR_Cal_'+str(date.today())+'.csv'
#cannon_superior = 'Depurado_OLX_CANNON_SUPERIOR_Cal_'+str(date.today())+'.csv'
'''
mi_df = pd.DataFrame({'Fecha Adquisición':list_fecha_adquisicion, 'Fecha': list_fecha,'Nombre Vendedor': list_nombre_vendedor,
                      'Tipo Inmueble': list_tipo_inmueble, 'Amoblado': list_amoblado,'Tipo Vendededor': list_tipo_vendedor,
                      'Ubicación': list_ubicacion,  'Precio': list_precio,'Estrato': list_estrato, 'Metros Cuadrados': list_metros2,
                      'Habitaciones': list_cuartos,'Baños': list_banos,  'Parqueadero': list_parqueadero, 'Antiguedad': list_antiguedad,
                      'Publicación': list_publicacion,'Descripción': list_descripcion,'Link':list_enlaces,'Pauta': list_pauta})
mi_df.to_csv(cannon_inferior, mode='w', index=False, header=True,sep=',',decimal=',')

mi_df2 = pd.DataFrame({'Fecha Adquisición':list_fecha_adquisicion2, 'Fecha': list_fecha2,'Nombre Vendedor': list_nombre_vendedor2,
                       'Tipo Inmueble': list_tipo_inmueble2, 'Amoblado': list_amoblado2,'Tipo Vendededor': list_tipo_vendedor2, 
                      'Ubicación': list_ubicacion2, 'Precio': list_precio2,'Estrato': list_estrato2, 'Metros Cuadrados': list_metros22,
                       'Habitaciones': list_cuartos2,'Baños': list_banos2,  'Parqueadero': list_parqueadero2,  'Antiguedad': list_antiguedad2,
                       'Publicación': list_publicacion2,'Descripción': list_descripcion2,'Link':list_enlaces2,'Pauta': list_pauta2})
mi_df2.to_csv(cannon_superior, mode='w', index=False, header=True,sep=',',decimal=',')

 
'''
mi_df3 = pd.DataFrame({'scrapind_id': list_id_scrappin3, 'fecha_anuncio': list_fecha_anuncio3,'nombre_completo': list_nombre_completo3,
                       'cedula': list_cedula3, 'correo_electronico': list_email3, 'telefono': list_telefono3, 'demostracion_ingresos': list_demostracion_ingresos3,
                       'carta_laboral': list_carta_laboral3, 'fiador_solvente': list_fiador_solvente3,'fiador_finca_raiz': list_fiador_finca_raiz3,
                       'tipo_propiedad': list_tipo_propiedad3, 'descripcion': list_descripcion3, 'departamento': list_departamento3, 'ciudad': list_ciudad3,
                       'barrio': list_barrio3, 'direccion': list_direccion3, 'estrato': list_estrato3, 'precio':list_precio3, 'amoblado': list_amoblado3,
                       'area':list_area3, 'banios': list_banios3, 'habitaciones': list_habitaciones3, 'cocina': list_cocina3, 
                       'mascotas': list_mascotas3, 'conjunto_cerrado': list_conjunto_cerrado3, 'parqueadero': list_parqueadero3,
                       'fuente': list_fuente3, 'enlace_fuente': list_enlace_fuente3, 'titulo_publicacion_externa': list_titulo_publicacion_externa3,
                       'descripcion_externa': list_descripcion_externa3})
mi_df3.to_csv(archivo_salida_info, mode='w', index=False, header=True,sep=',',decimal=',')

try:
  fin = time.clock()
  tiempo_ejecucion = fin-inicio
  print(tiempo_ejecucion)
except:
   r=0

#files.download(depurado)

Doc_errores.close()