from msilib import Table
import tkinter as ktr
from tkinter import *
from tkinter import ttk
from tkinter import Tk
from tkinter import messagebox
from pandastable import Table, TableModel
from tkinter import filedialog
 

from selenium import webdriver 
import time 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import pandas as pd
import numpy as np
import pandastable as pt
import re


# Importar funciones necesarias para abrir y controlar chrome
from selenium.webdriver.chrome.service import Service as ChromeService  
from webdriver_manager.chrome import ChromeDriverManager

# Guardar las funciones en el objeto service
service = ChromeService(ChromeDriverManager().install())
 

##CREAR INTERFAZ##
root = Tk()
root.title('Whatsapp Mauster')
root.geometry('600x600')
 


def google():
    global driver
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()
        
def waplus():
    driver.get('https://chrome.google.com/webstore/detail/wa-web-plus-for-whatsapp/ekcgkejcjdcmonfpmnljobemcbpnkamh/related?hl=es/')
    time.sleep(2)
    boton =driver.find_element(By.XPATH, './/div[@class="g-c-R  webstore-test-button-label"]')
    boton.click()


def validarQR ():
    try:
        element = driver.find_element(By.TAG_NAME,'canvas')
    except: 
        return False
    return True

# Abrir whatsapp y autenticarse mediante QR
def abrirwhats ():
    driver.get('https://web.whatsapp.com/')
    time.sleep(10)
    
    QR = True
    
    while QR:
        print('Esperando autenticación')
        QR = validarQR()
        time.sleep(10)
        if QR == False:
            print('se autenticó')
            break
    #print('Ingreso a WhatssApp correcto')
    messagebox.showinfo(message=f"Ingreso a whatsApp correcto", title="Autenticación de usuario")


def aceptar():
    global chat_total
    try:
        chat_total = int(var_texto.get())  # Obtenemos el número de la StringVar
    except ValueError:            # Si lo ingresado no es un entero
        var_lbl.set(f"No escogiste un número válido")
    else:                         # Si lo ingresado es un entero
        var_lbl.set(f"Escogiste el número: {chat_total}")

def aceptar_NA():
    global numero_chats
    try:
        numero_chats = int(var_texto2.get())  # Obtenemos el número de la StringVar
    except ValueError:            # Si lo ingresado no es un entero
        var_lbl2.set(f"No escogiste un número válido")
    else:                         # Si lo ingresado es un entero
        var_lbl2.set(f"Escogiste el número: {numero_chats}")


var_texto = ktr.StringVar()
var_lbl = ktr.StringVar()
var_texto2 = ktr.StringVar()
var_lbl2 = ktr.StringVar()
var_texto3 = ktr.StringVar()
var_lbl3 = ktr.StringVar()


def entrada_fchats():
    # Crear una ventana secundaria.
    caja_1 = ktr.Toplevel()
    caja_1.title('Chats totales')
    caja_1.config(width=300, height=200)
    caja_1.grab_set()
    # Crear una etiqueta para la ventana secundaria
    var_lbl.set("Ingresa el número de chats totales (archivados y no archivados)") # Contenido inicial del Lable
    mi_label = ktr.Label(caja_1, textvariable=var_lbl)
    mi_label.place(width=260)   
    #Crear en Entry
    entry_1 = ktr.Entry(caja_1, textvariable=var_texto).place(x=20, y=20, width=260)
    #entry_1.grid(row=1, column=0, columnspan=2)
    #crear el boton dentro de caja_1
    bcerrar = Button(caja_1,text="Aceptar",command = caja_1.destroy).place(x=75, y=75)
    baceptar = Button(caja_1,text="Verificar numero", command = aceptar).place(x=170, y=75)

def cambiar_div():
    tamdiv = driver.find_element(By.XPATH,'//div[@class="pinUnlimitedChatsOptions"]')
    driver.execute_script("arguments[0].setAttribute('style', '1000000000000%')", tamdiv)


def prim_chat():
    # Buscar la barra de búsqueda de chats para poder desplazarnos a través de la lista de chats
    busqueda = driver.find_element(By.XPATH, '//div[@class = "_13NKt copyable-text selectable-text"]')
    busqueda.click()
    # Seleccionar el primer chat para poder recorrer toda la lista
    busqueda.send_keys(Keys.ARROW_DOWN)


#Función que busca el chat activo y espera a que esté cargado en el DOM
def fnumeros1 ():
    try:
        element1 = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//div[@aria-selected="true" and @role="row"]'))
        )
    except: 
        return False
    return True
# Función que busca los números dentro de los grupos y espera a que estén cargados en el DOM 
def fnumeros5 ():
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, './/span[@class="_2YPr_ i0jNr selectable-text copyable-text"]'))
        )
    except: 
        return False
    return True


def no_archi():
    global N_Grupos
    global Per
    global numero_grupos
    N_Grupos = []
    Per = []
    numero_grupos = 0
    while True:
        i = fnumeros1()
        if i == True:
            selected_contact =driver.find_element(By.XPATH, './/div[@aria-selected="true" and @role="row"] ')
            nombre = driver.find_element(By.XPATH, './/div[@class="_2rlF7"] ')
            N_Grupos.append(nombre.text)
        else:
            print(f'Nombre de grupo no encontrado, numero de chat: {numero_grupos}')
            N_Grupos.append(f'Nombre no encontrado, grupo: {numero_grupos}')
        f = fnumeros5()
        if f == True:
            integrantes = driver.find_element(By.XPATH, './/span[@class="_2YPr_ i0jNr selectable-text copyable-text"]')
            Per.append(integrantes.text)
        else:
            Per.append('No disponible')
            
        numero_grupos = numero_grupos + 1
        
        if numero_chats == numero_grupos:
            messagebox.showinfo(message=f"El número de chats contabilizado es {numero_grupos} grupos", title="Descarga terminada")
           #print(f'Descarga terminada, el numero de chats contabilizado es {numero_grupos} grupos')
            break

        selected_contact.send_keys(Keys.ARROW_DOWN)
        time.sleep(3.5)