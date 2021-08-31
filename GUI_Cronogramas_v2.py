# -*- coding: utf-8 -*-
"""
Project: Cronogramas de Auditoría
Created on Wed Aug 25 07:20:27 2021

 - Validation button working on Thurs Aug 26 16:04:27 2021

@author: ksastoque
"""
# ======================================================================
# # Importamos los módulos con los que vamos a trabajar
# ======================================================================
from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter.ttk import Progressbar

# Data manipulation
import pandas as pd
import numpy as np

import string
import random
import time

# Visualization
from IPython.display import HTML
import seaborn as sns
#import altair as alt
import matplotlib.pyplot as plt

# Math
from math import ceil
from collections import Counter

# Misc
import os

# =======================================================================
# # Definimos la interfaz para la ventana principal
# =======================================================================

class main_Window():

    def __init__(self, main_):

# # =====================================================================
#      # Botones de carga de archivo de excel
# # =====================================================================
        
        self.top = Label(main_, 
                         text='Seleccione enfermedad y'\
                             +' cargue el archivo para continuar')
        self.top.grid(row=0, column=0)# self.top.pack()
        
        self.disease = StringVar()
        self.disease.set("Seleccione la enfermedad") # Valor defecto
        DISEASE_OPTIONS = ['CANCER', 'ERC', 'HEMOFILIA', 'VIH',
                            'Duplicados (cualquier enfermedad)']

        self.dropdownList = OptionMenu(main_, 
                                       self.disease, 
                                       *DISEASE_OPTIONS)
        self.dropdownList.grid(row=0, column=1)
        # self.dropdownList.pack()
  
        
        self.loadFile_button = Button(main_, 
                                 text="Cargar Archivo",
                                 width=70,
                                 command=self.UploadAction,
                                 fg="blue")
        self.loadFile_button.grid(row=1, columnspan=20)
        # self.b_loadFile.pack(expand=TRUE, fill=X)
        
        self.answer_load = StringVar()
        self.answer_load.set("Cargue un archivo .xlsx o .xlsm")
        # self.answer_load.grid(row=3, columnspan=3)
        # self.answer_color = StringVar()
        # self.answer_color.set('black')
        
        # self.pb1 = Progressbar(main_, 
        #                       orient=HORIZONTAL, 
        #                       length=300, mode='determinate')
        # self.pb1.grid(row=2, columnspan=2)# self.pb1.pack()
        
        self.check_load = Label(main_, 
                               text = self.answer_load.get(), 
                               textvariable=self.answer_load)
                               # foreground=self.answer_color.get())
        self.check_load.grid(row=3, columnspan=3)
        # self.check_load.pack(expand=TRUE, fill=X)
        
# ======================================================================
#      # Parte 2
#      # Genera espacios para ingresar los datos 
#      # de parametrización del cronograma 
# ======================================================================

#######################################################
#       # Seleccionar un número      
        self.meta = Label(main_, 
                   text='Meta completa (casos a auditar diarios): ')\
            .grid(row=5, column=0)# self.meta.pack(side=LEFT)
        self.goal = Spinbox(main_, from_ = 1, to = 100)
        self.goal.grid(row=5, column=1)# self.goal.pack(side=LEFT)      
        
        self.dias = Label(main_, 
                   text='Días máximos para auditar: ')\
            .grid(row=6, column=0)
        self.total_days = Spinbox(main_, from_ = 1, to = 50)
        self.total_days.grid(row=6, column=1)
        
        self.dia1 = Label(main_, 
                   text='Casos de adaptación (dia 1): ')\
            .grid(row=7, column=0)
        self.adap1 = Spinbox(main_, from_ = 1, to = 50)
        self.adap1.grid(row=7, column=1)
        
        self.dia2 = Label(main_, 
                   text='Casos de adaptación (dia 2): ')\
            .grid(row=8, column=0)
        self.adap2 = Spinbox(main_, from_ = 1, to = 50)
        self.adap2.grid(row=8, column=1)

        self.dia3 = Label(main_, 
                   text='Casos de adaptación (dia 3): ')\
            .grid(row=9, column=0)
        self.adap3 = Spinbox(main_, from_ = 1, to = 50)
        self.adap3.grid(row=9, column=1)
        
        # MEDICIONES_LIST = df['Medicion'].unique()
        # self.medicionesList = OptionMenu(main_, 
        #                               'Mediciones (sel mulitple)', 
        #                                *MEDICIONES_LIST)
        # self.medicionesList.grid(row=9, column=0)
        # self.dropdownList.pack()
        
        self.validation_button = Button(main_, 
                                    text=' Validar parámetros', 
                                    width=40,
                                    # fg ='red',
                                    command=self.getParameters)
        self.validation_button.grid(row=18, column=1)
        # self.button_close.pack()        

        self.answer_processing = StringVar()
        self.answer_processing.set("Resultados de los parámetros")
        # self.answer_load.grid(row=3, columnspan=3)
        # self.answer_color = StringVar()
        # self.answer_color.set('black')
        
        # self.pb1 = Progressbar(main_, 
        #                        orient=HORIZONTAL, 
        #                        length=300, mode='determinate')
        # self.pb1.grid(row=2, columnspan=2)# self.pb1.pack()
        
        self.check_processing = Label(main_, 
                                     text = self.answer_processing.get(), 
                                     textvariable=self.answer_processing)
                                     # foreground=self.answer_color.get())
        self.check_processing.grid(row=19, columnspan=3)
        # self.check_load.pack(expand=TRUE, fill=X)

        
# # ========================================================================
#      # Botón para cerrar la ventana de la app
# # ========================================================================
        
        self.close_button = Button(main_, 
                                    text=' Terminar/Cancelar', 
                                    width=20,
                                    # fg ='red',
                                    command=main_.destroy)
        self.close_button.grid(row=25, column=1)# self.button_close.pack()


# ==========================================================================
# # # # Functions  
# ==========================================================================
    def UploadAction(self):
        
        global check_cols
        global MEDICIONES_LIST
        global grupo
        global df
        
        filepath = askopenfilename(filetypes=[('Excel Files', 
                                            '*.xlsx *.xlsm')])
            
        file_ = filepath.split('/')[-1]
        df = pd.read_excel(filepath, dtype=str)
        
        self.check_load.config(fg='black')
        self.answer_load.set('Validando {}'.format(file_))
                
        # for i in range(5):
        #     main_.update_idletasks()
        #     self.pb1['value'] += 20
        #     time.sleep(1)
        # self.pb1.destroy()
        # self.pb1.__init__()
        
        check_cols = ['idAuditing', 'tipoID', 'Identificacion', 
                  'idEPS', 'Medicion', 'idDuplicado']
        # print(df.columns)
        # print('Getting selected item: ', disease.get())
        if self.disease.get() == 'CANCER':
            check_cols = check_cols + ['Agrupador']
    
        if sorted(df.columns) == sorted(check_cols):
            self.check_load.config(fg='green')            
            self.answer_load.set('Archivo {}\n'\
                                 +'\n ¡¡¡Cargado exitosamente!!! \n'\
                            .format(file_)\
                            +'\nCantidad de registros: {} \n Columnas: {}'\
                                .format(
                                df.shape[0],
                                df.shape[1]))
                
            MEDICIONES_LIST = df['Medicion'].unique()

            
            self.middle = Label(main_, 
                         text='Seleccione las mediciones a trabajar')\
                        .grid(row=4, column=0)
            self.medicionesList = Listbox(main_,
                                        selectmode='multiple',
                                        yscrollcommand=Scrollbar(main_))
            for each_item in range(len(MEDICIONES_LIST)):
      
                self.medicionesList.insert(END, 
                                           MEDICIONES_LIST[each_item])
                self.medicionesList.itemconfig(each_item, 
                                               bg = "lime")
                
            self.medicionesList.grid(row=4, column=1)
            
            # grupo = list(self.medicionesList.get())
            # grupo = []
            # curr_sel = self.medicionesList.curselection()
            # for i in curr_sel:
            #     op = self.medicionesList.get(i)
            #     grupo.append(op)

        else:
            self.check_load.config(fg='red')
            self.answer_load.set(
                'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n'\
                +'Los nombres de las columnas no coinciden.\n'\
                +'Por favor valide que los nombres de las '\
                    +'columnas contengan: \n'\
                              +'\n {}'.format(check_cols))
            
            
    def getParameters(self):
        
        global df
        global goal
        global grupo
        global MEDICIONES_LIST
        global perc_adp1
        global perc_adp2
        global perc_adp3
        global total_days

        self.answer_processing.set('Validando parámetros')
        
        goal = int(self.goal.get())
        print('Meta seleccionada: ', goal)
        
        total_days = int(self.total_days.get())
        print('Dias maximos: ', total_days)
        
        perc_adp1 = round( (goal - int(self.adap1.get())) / goal, 2)
        print('Porcentaje adaptacion 1:', perc_adp1)
        
        perc_adp2 = round( (goal - int(self.adap2.get())) / goal, 2)
        print('Porcentaje adaptacion 2:', perc_adp2)
        
        perc_adp3 = round( (goal - int(self.adap3.get())) / goal, 2)
        print('Porcentaje adaptacion 2:', perc_adp3)  

        print('Tamaño de la base de datos: ', df.shape)
        
        # grupo = list(self.medicionesList.get())
        grupo = []
        curr_sel = self.medicionesList.curselection()
        for i in curr_sel:
            op = self.medicionesList.get(i)
            grupo.append(op)        
        print('Selección mediciones   ', grupo)
        
        fail1 = goal < int(self.adap1.get())
        fail2 = goal < int(self.adap2.get())
        fail3 = goal < int(self.adap3.get())
                
        if len(grupo) == 0 or fail1 or fail2 or fail3:
            self.check_processing.config(fg='red')
            self.answer_processing\
                .set('xXxXxXxXxXxXxX \n'\
                    +'Por favor valide que: \n '\
                +'- Haya seleccionado medicion(es) para el cronograma\n'\
                    +'- La meta de casos a auditar por día no sea menor'\
                    +' a la de los casos de adaptación...')
        else:
            self.check_processing.config(fg='green')
            self.answer_processing\
                .set('Parámetros de generación de cronograma para '\
                    +'auditar {} registros. \n \n'.format(
                        df['Identificacion'].count())\
                    +' Meta de casos a auditar por día: {}'.format(goal)\
                    +'\n Días máximos de auditoría: {}'.format(total_days)\
                    +'\n Porcentajes de adaptación:  \n'\
                    +'    Día 1: {} \n'.format(perc_adp1)\
                    +'    Día 2: {} \n'.format(perc_adp2)\
                    +'    Día 3: {} \n'.format(perc_adp3)
                    )
        

# # ========================================================================
# # # Botón para cerrar la ventana de la app
# # ========================================================================
# button_close = Button(main_, 
#                     text=' Cerrar', 
#                     width=20,
#                     # fg ='red',
#                     command=main_.destroy)

# button_close.pack()

# ==========================================================================
# # Crea y lanza la ventana principal
# ==========================================================================
main_ = Tk(screenName=None, 
              baseName=None, 
              className=' Cronogramas Auditoría CAC ', 
              useTk=1)

# # # Funcion para refrescar la ventana principal
# def refresh(self):
#     self.__init__()

w = main_Window(main_)

# ===========================================================================
# # Finalizar
# ===========================================================================
main_.mainloop()

print(df)


# duplicados anteriores 3.413 registros inician el martes
# tengan o no tengan bot .... 20 auditores
# inicia el día 33 o 34 
# meta 80 casos todos los dias
# anteriores en seguimiento 
# lineas unicas 8.985 registros
# 41 auditores, meta 120
# dia 38 septiembre 6  