#F0
#subir archivos:
#    barrios_medellin.txt MEDELLIN CALI BOGOTA BARRANQUILLA CARTAGENA SANTAMARTA
#    old_links.txt
#    old_tels.txt

from google.colab import files
import io
uploaded = files.upload()


# F1
import time
import sys
import csv
from datetime import date
from datetime import datetime
import datetime
import requests
import sys
import codecs
from lxml import html
from google.colab import files
 

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
ciudades = ['medellin']
#ciudades = ['medellin','bello','itagui','envigado','sabaneta','rionegro','sanjeronimo','copacabana']
#ciudades = ['cucuta','villadelrosario','lospatios','ibague','melgar','manizales','villamaria']
#ciudades = ['popayan','valledupar','quibdo','monteria','neiva','pitalito']
#ciudades = ['bogota','chia','funza','girardot','cajica','madrid','zipaquira','cota','fusagasuga','soacha','lacalera','sopo','facatativa']
#ciudades = ['cali','palmira','jamundi','tulua']
#ciudades = ['bogota', 'chia','funza','madrid','fusagasuga','zipaquira','soacha']
archivo_salida_links = "links_olx_"+ str(ciudades[0])+"_" + str(date.today()) + ".csv"

DataOut=open(archivo_salida_links,'w')
inicio = time.clock()  
numero_paginas = 1 #150 Ete es el numero de paginas a revisar (mejorar en el fututo)
links_depurado = []
links_depurados = []



for ciudad in ciudades:
  enlace =  'https://'+str(ciudad)+'.olx.com.co/apartamentos-casas-alquiler-cat-363'
  print(ciudad)
  print(enlace)
  page = download(enlace) 
  
  num_pag=1
  links = []  
  
  while num_pag <=numero_paginas:
    print(enlace+'-p-'+str(num_pag))
    page = download(enlace+'-p-'+str(num_pag))
    #print(page.content)
    tree = html.fromstring(page.content)
    #print(tree)
    try:
      text_contents = [el for el in tree.xpath('/html/body/div/div/main/div/section/div/div/div[4]/div[2]/div/div[2]/ul/li[1]/a/@href')]
    except:
      num_pag += 1
    #print(text_contents)
    date_contents = [el.text.replace("\n                ", "").replace("\n            ", "") for el in tree.xpath("/html/body/div/div/main/div/section/div/div/div[4]/div[2]/div/div[2]/ul/li[1]/a/div/div[2]/span[2]/span")]
    pauta_contents = [el.text for el in tree.xpath("/html/body/div/div/main/div/section/div/div/div[4]/div[2]/div/div[2]/ul/li[1]/a/div/div[1]/label/span")]
    
    for i in range(len(text_contents)):
      if date_contents[i].find("oy")>=0:
        try:
          links.append([text_contents[i],hoy(),pauta_contents[i]])
        except:
          links.append([text_contents[i],hoy(),"NO"])
      elif date_contents[i].find("yer")>=0:
        try:
          links.append([text_contents[i],ayer(),pauta_contents[i]])
        except:
          links.append([text_contents[i],ayer(),"NO"])
      else:
        try:
          links.append([text_contents[i],date_contents[i],pauta_contents[i]])
        except:
          links.append([text_contents[i],date_contents[i],"NO"])
     #print(links[i])
      DataOut.write(str(links[i][0])+","+str(links[i][1])+","+str(links[i][2]))
      DataOut.write('\n')    
    del text_contents
    del date_contents
    num_pag += 1

    for i in links:
       if i[0] not in links_depurado:
          links_depurado.append(i[0])
          links_depurados.append(i)
          #print(i)
          
  
#print(links_depurados)
final = time.clock()
tiempo_ejecucion = final-inicio
DataOut.write("Número registros leidos: " + str(len(links)))
print("Número registros leidos: " + str(len(links_depurados)))
DataOut.write('\n')
DataOut.write("Número registros únicos: " + str(len(links_depurado)))
DataOut.write('\n')
DataOut.write("Fecha ejecución: "+ str(date.today()))
DataOut.write('\n')
DataOut.write("Tiempo ejecución: " + str(tiempo_ejecucion) + " segundos")
DataOut.close()
print("Tiempo ejecución: " + str(tiempo_ejecucion))
files.download(archivo_salida_links)


#F3
from itertools import groupby
import time
import sys
import csv
from datetime import date
from __future__ import print_function
import pandas as pd #Nuevo
from google.colab import files

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

def ver_amoblado(publicacion,descripcion):
    if(publicacion.lower().find("amoblad") > -1 or descripcion.lower().find("amoblad") > -1):
        return("SI")
    else:
        return("NO")

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
    else:
        return("None")

def telefono_adicional(x,telefono):
    my_str = x
    lista1 = [int(''.join(i)) for is_digit, i in groupby(my_str, str.isdigit) if is_digit]
    my_str = x.replace(' ','')
    lista2 = [int(''.join(i)) for is_digit, i in groupby(my_str, str.isdigit) if is_digit]
    my_str = x.replace('_','')
    lista3 = [int(''.join(i)) for is_digit, i in groupby(my_str, str.isdigit) if is_digit]
    my_str = x.replace('-','')
    lista4 = [int(''.join(i)) for is_digit, i in groupby(my_str, str.isdigit) if is_digit]
    lista = lista1 +lista2 + lista3 + lista4
    #print(lista)
    for ll in lista:
        if (str(ll) != str(telefono) and len(str(ll)) == 10):
            print(str(ll))
            return(str(ll))
            
        
'''   
def comuna(descripcion):
    comunas = ["popular","santa cruz","manrique","aranjuez","castilla",
               "doce de octubre","12 de octubre","12 octubre","robledo","villa hermosa","buenos aires",
               "candelaria","laureles","estadio","américa","america",
               "san javier","poblado","guayabal","belén","belen","palmitas",
               "san cristóbal","san cristobal","altavista","san antonio de prado"]
    for comuna in comunas:
        if descripcion.lower().find(comuna) > -1:
            return(comuna)
''' 

with open('barrios.txt', 'r', encoding='utf-8', errors='ignore') as b:
      barrios = [linea.strip() for linea in b]
    
def barrio(descripcion,barrios):
    for barrio in barrios:
        if sintilde(descripcion).find(sintilde(barrio)) > -1:
            return barrio

#links1 = ['https://barranquilla.olx.com.co/habitacion-amoblada-en-arriendo-norte-iid-1062535112']          

links1 = links_depurados


inicio = time.clock()


time.sleep(1)
archivo_salida_info = 'inmuebles_olx_'+'_'+str(date.today())+'.csv'
contador = 1
Doc_errores = open('docu_errores.txt','a')
Doc_errores.write(str(date.today()))

'''CANON INFERIOR'''

list_fecha_adquisicion = []
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
list_negociable = []
list_parqueadero = []
list_cuartos = []
list_banos = []
list_enlaces = [] 

'''CANON SUPERIOR'''
list_fecha_adquisicion2 = []
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
list_negociable2 = []
list_parqueadero2 = []
list_cuartos2 = []
list_banos2 = []
list_enlaces2 = []


'''TODOS LOS INMUEBLES'''
list_fecha_adquisicion3 = []
list_fecha3 = []
list_tipo_vendedor3 = []
list_nombre_vendedor3 = []
list_publicacion3 = []
list_pauta3 = []
list_descripcion3 = [] 
list_tipo_inmueble3 = []
list_amoblado3 = []
list_barrio3 = []
list_telefono13 = []
list_telefono23 = []
list_metros23 = []
list_estrato3 = []
list_antiguedad3 = []
list_ubicacion3 = []
list_direccion3 = []
list_enlaces3 = []
list_precio3 = []
list_negociable3 = []
list_parqueadero3 = []
list_cuartos3 = []
list_banos3 = []
list_enlaces3 = [] 

pasaron = 0

for link in links1:
    negociable = ''
    precio = ''
    enlace = ''
    direccion = ''
    ubicacion = ''
    telefono = ''
    telefono1 = ''
    barrio = ''
    amoblado = ''
    descripcion = ''
    pauta = ''
    publicacion=''
    vendedor = ''
    fecha = ''
    tipo_inmueble = ''
    precio = 0
    url = "https:" + str(link[0])
    print(url)
    try:
      page = download(url)
      tree = html.fromstring(page.content)
    except:
      Doc_errores.write('\n')
      Doc_errores.write("error con direccion" + url + " " + direccion)

       
    try:
        publicacion = tree.xpath('/html/body/div[2]/div/main/article/div/section[1]/header/div[1]/h1/text()')
        publicacion = r"".join(publicacion)        
        publicacion = limpiar(publicacion)
    except:
        publicacion  = "None"        
    print("Publicacion: " + str(publicacion))
    
    try:
      tipo_inmueble = tipo_inmueble_fun(str(publicacion))          
    except:
      tipo_inmueble = "None"     
    print("Tipo de inmueble: " + tipo_inmueble)
    
    try:      
      vendedor = tree.xpath("//p[@class='name']/text()")
      vendedor = r"".join(vendedor)
      vendedor = limpiar(vendedor)
    except:
        vendedor = "None"        
    
    
    try:
      telefono = page.text[page.text[:].find("phone&quot;:&quot;")+18:page.text[:].find("phone&quot;:&quot;")+13+18]
      telefono = telefono.replace("&q","")
      telefono = telefono.replace("&","")
      telefono = telefono.replace("q","")
       
      if len(telefono)<=12:
        fijo1 = telefono[3:]
        telefono1 = limpiar(fijo1)        
        if telefono1 == "uot":
          telefono1 = "None"
      else:
        telefono1 = telefono[3:]
    except:
      telefono1 = ""
    try:
        fecha = str(link[1])
    except:
        fecha = "None"
        
    #print("Fecha: " + fecha)
    try:
      #print(str(link[2]))
      if str(link[2])=="Destacado":
        pauta = "SI"
      else:
        pauta = "NO"
    except:
        pauta = "NO"
        
    #print("Destacado: " + pauta)
    try:
      ubicacion = tree.xpath('/html/body/div[2]/div/main/article/div/section[1]/header/div[2]/p[1]/span/text()')
      ubicacion = r"".join(ubicacion)
      ubicacion = limpiar(ubicacion)
    except:
      ubicacion = "None"
    #print("Ubicación: " + ubicacion)
    
    try:
      precio_crudo = tree.xpath('/html/body/div[2]/div/main/article/div/section[1]/header/div[2]/p[2]/strong/text()')
      precio_crudo = r"".join(precio_crudo)
      precio = limpiar_precio(precio_crudo)
      print(precio)
    except:
      precio = 0
    
    if precio == "None":
      precio == 0
      
    if len(precio) == 0:
      precio = 0
    
    
      
      
    #print("Precio: " + precio)
    
    try:
      negociabletext = tree.xpath('/html/body/div[2]/div/main/article/div/section[1]/header/div[2]/p[2]/strong/em/text()')
      negociabletext = r"".join(negociabletext)
      negociabletext = limpiar(negociabletext)
      if negociabletext.find("egociable") > -1:
        negociable = "SI"
      else:
        negociable = "NO"
    except:
       negociable = "NO"
    
    
    try:
        descripcion = tree.xpath('/html/body/div[2]/div/main/article/div/section[1]/p/text()')
        descripcion = limpiar(r"".join(descripcion))
    except:
        descripcion = "None"
    #print("Descripcion: " + str(descripcion))
    
    try:
       amoblado = ver_amoblado(publicacion,descripcion)
    except:
       amoblado = "None"
    #print("Amoblado: " + amoblado)
    
    try:
      telefono2 = str(telefono_adicional(descripcion,telefono1))
      
    except:
      telefono2 = ""      
    
      
    if len(telefono1)<=9:
      if len(telefono2) >=10:
        telefono1 = telefono2
    elif len(telefono1) ==10:
      telefono1=telefono1    
            
   
     
    
    try:
        bar = barrio(descripcion,barrios)
    except:
        bar = ""
    print("Barrio: " + str(bar))
    
    try:
        tags = [el for el in tree.xpath("/html/body/div[2]/div/main/article/div/section[1]/ul/li/strong/text()")]
        text_contents = [el for el in tree.xpath("/html/body/div[2]/div/main/article/div/section[1]/ul/li/span/text()")]
        
        #array = []
        #for k in range(len(tags)):
        #  array.append([tags[k],text_contents[k]])
    except:
        l=0
    mt_cuadrados = "None"
    estrato = "None"
    tipo_vendedor = "None"
    parqueadero = "None"
    baños = "None"
    cuartos = "None"
    antiguedad = "None"
    for k in range(len(tags)):
        if tags[k].startswith("Metros Cuadrados Totales"):                   
            mt_cuadrados = text_contents[k]
        elif tags[k].startswith("Estrato") :
            estrato = text_contents[k]
        elif tags[k].startswith("Tipo de Vendedor") :
            tipo_vendedor = text_contents[k]
        elif tags[k].startswith("Parqueadero") :
            parqueadero = text_contents[k]
        elif tags[k].find("baño") > -1:
            baños = text_contents[k]
        elif tags[k].startswith("Cuartos") :
            cuartos = text_contents[k]
        elif tags[k].startswith("Antigüedad") :
            antiguedad = text_contents[k]
    
    try:
      if tipo_vendedor == "Dueño Directo":
        
        try:
          url_maps = tree.xpath('//a[@class="image"]/@href')
          url_maps = r"".join(url_maps)
          #print("url_maps: " + url_maps)
          page_maps = download(url_maps)
          tree_maps = html.fromstring(page_maps.content)
          direccion = tree_maps.xpath('/html/body/jsl/div[3]/div[7]/div[9]/div/div[1]/div/div/div[7]/div/div[1]/span[3]/span[3]/text()')
          direccion = limpiar(r"".join(direccion))
              
          
        except:
          direccion = url_maps
          Doc_errores.write('\n')
          Doc_errores.write("error con direccion" + url + " " + direccion)
      else:
        direccion = ""
        
    except:
       direccion = ""
    #print("Dirección: " + str(direccion))   
    try:
       Info_publicacion = [tipo_vendedor,vendedor,publicacion,pauta,descripcion,tipo_inmueble,amoblado,
                           telefono1,telefono2,mt_cuadrados,estrato,precio,parqueadero,
                           cuartos,baños,antiguedad,ubicacion,barrio,direccion,fecha,url]
       #print(Info_publicacion)
    except:
       print("********* error print ****")
      
            #Link="dfvfd"
            #print(text_contents)
    #def repetidos():
    with open('old_links.txt', 'r') as f:
      lineas = [linea.strip() for linea in f]
    for linea in lineas:
      us = lineas
    url_ = str(url)
    telefono1_ = telefono1
    links_repetidos = us.count(url_) #Encuentra el numero de veces que la url se repite en el texto, mediante el modulo count.
    
    with open('old_tels.txt', 'r', encoding='utf-8', errors='ignore') as t:
      lineas2 = [linea.strip() for linea in t]
    for linea in lineas2:
      ut = lineas2
    tel_usados = open('old_tels.txt', 'r+')
    
    tel_rep = ut.count(str(telefono1))
    print("Repetidos")
    print(tel_rep)
    
    print(tipo_vendedor)
    links_repetidos = links_repetidos
    
    if links_repetidos== 0:
      if tipo_vendedor== "Dueño Directo" and tel_rep == 0:
        pasaron += 1
        if (int(precio) <= 1200000):
          try:
            list_fecha_adquisicion.append(hoy())
            list_fecha.append(fecha)
            list_tipo_vendedor.append(tipo_vendedor)
            list_nombre_vendedor.append(vendedor)
            list_publicacion.append(publicacion)
            list_pauta.append(pauta)
            list_descripcion.append(descripcion)
            list_tipo_inmueble.append(tipo_inmueble)
            list_amoblado.append(amoblado)
            list_barrio.append(bar) 
            list_telefono1.append(telefono1)
            list_telefono2.append(telefono2)
            list_metros2.append(mt_cuadrados)
            list_estrato.append(estrato)
            list_precio.append(precio)
            list_negociable.append(negociable)
            list_parqueadero.append(parqueadero)
            list_cuartos.append(cuartos)
            list_banos.append(baños)
            list_antiguedad.append(antiguedad)
            list_ubicacion.append(ubicacion)         
            list_direccion.append(direccion)
            list_enlaces.append(url)


            links_usados = open('old_links.txt','a')
            links_usados.write(url)
            links_usados.write('\n')
            tel_usados = open('old_tels.txt', 'a')
            tel_usados.write(telefono1)
            tel_usados.write('\n') 
          except:
            print("******* error print ++++")
            Doc_errores.write('\n')
            Doc_errores.write("error guardar informacion" + url)
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
            list_barrio2.append(bar) 
            list_telefono12.append(telefono1)
            list_telefono22.append(telefono2)
            list_metros22.append(mt_cuadrados)
            list_estrato2.append(estrato)
            list_precio2.append(precio)
            list_negociable2.append(negociable)
            list_parqueadero2.append(parqueadero)
            list_cuartos2.append(cuartos)
            list_banos2.append(baños)
            list_antiguedad2.append(antiguedad)
            list_ubicacion2.append(ubicacion)         
            list_direccion2.append(direccion)
            list_enlaces2.append(url)


            links_usados = open('old_links.txt','a')
            links_usados.write(url)
            links_usados.write('\n')
            tel_usados = open('old_tels.txt', 'a')
            tel_usados.write(telefono1)
            tel_usados.write('\n') 

          except:
              print("******* error print ++++")
              Doc_errores.write('\n')
              Doc_errores.write("error guardar informacion" + url)
          

    else:
      try:
          list_fecha_adquisicion3.append(hoy())
          list_fecha3.append(fecha)
          list_tipo_vendedor3.append(tipo_vendedor)
          list_nombre_vendedor3.append(vendedor)
          list_publicacion3.append(publicacion)
          list_pauta3.append(pauta)
          list_descripcion3.append(descripcion)
          list_tipo_inmueble3.append(tipo_inmueble)
          list_amoblado3.append(amoblado)
          list_barrio3.append(bar) 
          list_telefono13.append(telefono1)
          list_telefono23.append(telefono2)
          list_metros23.append(mt_cuadrados)
          list_estrato3.append(estrato)
          list_precio3.append(precio)
          list_negociable3.append(negociable)
          list_parqueadero3.append(parqueadero)
          list_cuartos3.append(cuartos)
          list_banos3.append(baños)
          list_antiguedad3.append(antiguedad)
          list_ubicacion3.append(ubicacion)         
          list_direccion3.append(direccion)
          list_enlaces3.append(url)
          
          
          links_usados = open('old_links.txt','a')
          links_usados.write(url)
          links_usados.write('\n')
          tel_usados = open('old_tels.txt', 'a')
          tel_usados.write(telefono1)
          tel_usados.write('\n') 
          
      except:
          print("******* error print ++++")
          Doc_errores.write('\n')
          Doc_errores.write("error guardar informacion" + url)
   
    try:
          list_fecha_adquisicion3.append(hoy())
          list_fecha3.append(fecha)
          list_tipo_vendedor3.append(tipo_vendedor)
          list_nombre_vendedor3.append(vendedor)
          list_publicacion3.append(publicacion)
          list_pauta3.append(pauta)
          list_descripcion3.append(descripcion)
          list_tipo_inmueble3.append(tipo_inmueble)
          list_amoblado3.append(amoblado)
          list_barrio3.append(bar) 
          list_telefono13.append(telefono1)
          list_telefono23.append(telefono2)
          list_metros23.append(mt_cuadrados)
          list_estrato3.append(estrato)
          list_precio3.append(precio)
          list_negociable3.append(negociable)
          list_parqueadero3.append(parqueadero)
          list_cuartos3.append(cuartos)
          list_banos3.append(baños)
          list_antiguedad3.append(antiguedad)
          list_ubicacion3.append(ubicacion)         
          list_direccion3.append(direccion)
          list_enlaces3.append(url)
          
          
          links_usados = open('old_links.txt','a')
          links_usados.write(url)
          links_usados.write('\n')
          tel_usados = open('old_tels.txt', 'a')
          tel_usados.write(telefono1)
          tel_usados.write('\n') 
          
    except:
          print("******* error print ++++")
          Doc_errores.write('\n')
          Doc_errores.write("error guardar informacion" + url)
      
    print("*****************************************************************")
    print(contador)
    print("*****************************************************************")
    contador += 1  

    
print(list_fecha_adquisicion3)    
print(list_fecha3)
print(list_tipo_vendedor3)
print(list_nombre_vendedor3)
print(list_publicacion)
print(list_pauta)
print(list_descripcion)
print(list_tipo_inmueble)
print(list_amoblado)
print(list_barrio)
print(list_telefono1)
print(list_telefono2)
print(list_metros2)
print(list_estrato)
print(list_negociable)
print(list_parqueadero)
print(list_cuartos)
print(list_banos)
print(list_antiguedad)
print(list_ubicacion)
print(list_direccion)
print(list_enlaces)

print(pasaron)

archivo_salida_info = 'inmuebles_olx_'+ str(ciudades[0])+"_"+ str(ciudad)+"_"+str(date.today())+'.csv'
cannon_inferior = 'Depurado_OLX_CANNON_INFERIOR_'+ str(ciudades[0])+"_"+str(date.today())+'.csv'
cannon_superior = 'Depurado_OLX_CANNON_SUPERIOR_'+ str(ciudades[0])+"_"+str(date.today())+'.csv'

mi_df = pd.DataFrame({'Fecha Adquisición':list_fecha_adquisicion, 'Fecha': list_fecha,'Nombre Vendedor': list_nombre_vendedor,'Telefono1': list_telefono1,
                      'Telefono2': list_telefono2,'Tipo Inmueble': list_tipo_inmueble, 'Amoblado': list_amoblado,'Tipo Vendededor': list_tipo_vendedor,  'Barrio': list_barrio, 
                      'Ubicación': list_ubicacion, 'Precio': list_precio,'Estrato': list_estrato, 'Metros Cuadrados': list_metros2,'Habitaciones': list_cuartos,
                      'Baños': list_banos,  'Parqueadero': list_parqueadero,  'Antiguedad': list_antiguedad,'Publicación': list_publicacion,'Descripción': list_descripcion,
                      'Link':list_enlaces,'Pauta': list_pauta, 'Dirección': list_direccion})
mi_df.to_csv(cannon_inferior, mode='w', index=False, header=True,sep=',',decimal=',')

mi_df2 = pd.DataFrame({'Fecha Adquisición':list_fecha_adquisicion2, 'Fecha': list_fecha2,'Nombre Vendedor': list_nombre_vendedor2,'Telefono1': list_telefono12,
                      'Telefono2': list_telefono22,'Tipo Inmueble': list_tipo_inmueble2, 'Amoblado': list_amoblado2,'Tipo Vendededor': list_tipo_vendedor2,  'Barrio': list_barrio2, 
                      'Ubicación': list_ubicacion2, 'Precio': list_precio2,'Estrato': list_estrato2, 'Metros Cuadrados': list_metros22,'Habitaciones': list_cuartos2,
                      'Baños': list_banos2,  'Parqueadero': list_parqueadero2,  'Antiguedad': list_antiguedad2,'Publicación': list_publicacion2,'Descripción': list_descripcion2,
                      'Link':list_enlaces2,'Pauta': list_pauta2, 'Dirección': list_direccion2})
mi_df2.to_csv(cannon_superior, mode='w', index=False, header=True,sep=',',decimal=',')

mi_df3 = pd.DataFrame({'Fecha Adquisición':list_fecha_adquisicion3, 'Fecha': list_fecha3,'Nombre Vendedor': list_nombre_vendedor3,'Telefono1': list_telefono13,
                      'Telefono2': list_telefono23,'Tipo Inmueble': list_tipo_inmueble3, 'Amoblado': list_amoblado3,'Tipo Vendededor': list_tipo_vendedor3,  'Barrio': list_barrio3, 
                      'Ubicación': list_ubicacion3, 'Precio': list_precio3,'Estrato': list_estrato3, 'Metros Cuadrados': list_metros23,'Habitaciones': list_cuartos3,
                      'Baños': list_banos3,  'Parqueadero': list_parqueadero3,  'Antiguedad': list_antiguedad3,'Publicación': list_publicacion3,'Descripción': list_descripcion3,
                      'Link':list_enlaces3,'Pauta': list_pauta3, 'Dirección': list_direccion3})
mi_df3.to_csv(archivo_salida_info, mode='w', index=False, header=True,sep=',',decimal=',')

try:
  fin = time.clock()
  tiempo_ejecucion = fin-inicio
  print(tiempo_ejecucion)
except:
   r=0

#files.download(depurado)

Doc_errores.close()



f.close()
t.close()


#F5
from google.colab import files

files.download(cannon_inferior)
files.download(cannon_superior)
files.download(archivo_salida_links)
files.download(archivo_salida_info)
#files.download('old_links.txt')
#files.download('old_tels.txt')
