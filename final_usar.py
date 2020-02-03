#-----Importing packages------
import tkinter as tk
import tkinter.filedialog
from PIL import Image, ImageTk
import os
from pathlib import Path
import numpy as np
from tkinter import ttk
import scipy.stats as st
import warnings
import matplotlib.pyplot as plt
import random as rd
from scipy.stats import norm
import os.path
from tkinter import messagebox
#------------------------------

warnings.filterwarnings("ignore") #taking out warnings

class MainWindow: #defining class

    def __init__(self, master):  #initializing function

        #-----Declaring main variables-----

        self.Arquivo_de_Dados="Vazio"  
        self.master = master
        self.frame = tk.Frame(self.master)
        self.master.title('Calculadora de Tamanho Amostral Bayesiana')

        #----------------------------------

        #getting directory of the file
        dir=os.getcwd() 

        #----------------------------------

        #Loading image of the programm---
        file_image='bayes.jfif'  
        image = Image.open(file_image) 
        photo = ImageTk.PhotoImage(image)

        #--------------------------------

        #Modeling main interface of the software
        self.label1= tk.Label(self.frame, image=photo)        
        self.label1.image=photo
        self.label1.pack()
        self.frame.pack()
        menubar = tk.Menu(self.master) #creating menubar
        self.master.config(menu=menubar) #configuring menu bar
        fileMenu = tk.Menu(menubar) #adding menu bar

        #------Creating commands in the menu bar--------

        fileMenu.add_command(label="Aplicar Algoritmo ...", underline=0, command=self.Algoritmo) #Calling algoritmo function
        menubar.add_cascade(label="Novo Tamanho Amostral", underline=0, menu=fileMenu)

        #------------------------------------------------

        #---Taking out maximize button (it's not necessary)---

        master.resizable(0,0)
        
        #-----------------------------------------------------
    
    #------------Algoritmo Function------------#
    def Algoritmo(self):

        initialdir = os.getcwd() # Getting the directory of the file
        filename = tkinter.filedialog.askopenfilename(initialdir = initialdir, title = "Escolha a amostra",filetypes = [("Arquivos extensão .txt","*.txt")]) #Window for getting
        #the file in a navigator

        #----Defining error function (verify if some script gives an error)----

        def iserror(func, *args, **kw):
            try:
                func(*args, **kw)
                return False 
            except Exception:
                return True

        #----------------------------------------------------------------------

        #---------Verifying if the something was chosen-----------
        # If it wanst, it just returns to the main window

        if os.path.isfile(filename)==False:
            return      

        #---------------------------------------------------------

        #-------Using the error function to verify if the .txt is valid--------#

        if iserror(np.loadtxt, filename) == True:
            messagebox.showinfo("Erro", "Foi escolhido um arquivo .txt inválido.")
            return

        #----------------------------------------------------------------------#

        #--If no error is found--#
        if iserror(np.loadtxt, filename) == False:

            self.Arquivo_de_Dados=filename #Get the directory of the .txt
            
            #-----Opening and modeling the window of parameters-----#

            master = tk.Tk() #declaring master
            window = tk.Canvas(master, width = 400, height = 300) #creating canvas
            window.pack()
            master.title("Parâmetros - "+Path(self.Arquivo_de_Dados).resolve().stem) #title of the window
            master.resizable(0,0) #taking out maximize button

            #--------------------------------------------------------

            #---Creating and modeling entry fields---#

            #Width field----
            label1 = tk.Label(master, text='Espessura nominal do tubo [mm]')
            window.create_window(200, 25, window=label1)
            #---------------

            #Confidence field---
            label2 = tk.Label(master, text='Nível de confiança:')
            window.create_window(200,100 , window=label2)
            #-------------------

            self.width = tk.Entry (master) #geting values and giving to the width variable
            window.create_window(200, 50, window=self.width)
            
            self.conf = tk.Entry(master) #geting values and giving to the width variable
            window.create_window(200, 125, window=self.conf)
            
            #-----Verify function: Verifies if the given values are ok-----

            def verify():
                if iserror (float, self.width.get()) == True:
                    messagebox.showinfo("Erro", "O valor dado para a espessura não é válido.\nVerifique o padrão dos números.") 
                    return
                elif iserror(float, self.conf.get())==True: 
                    messagebox.showinfo("Erro", "O valor dado para a confiabilidade estatística não é válido.\nVerifique o padrão dos números.")
                    return
                elif float(self.width.get())<0:
                    messagebox.showinfo("Erro", "O valor dado para a espessura é menor que um.\nVerifique o valor real da espessura dos tubos ensaiados.")
                    return
                elif float(self.conf.get())<=0:
                    messagebox.showinfo("Erro", "O valor da confiabilidade é menor ou igual a zero.\nEste valor deve estar presente em um intervalo aberto de 0 a 1.")
                    return                    
                elif float(self.conf.get())>0.999999999999999:
                    messagebox.showinfo("Erro", "O valor da confiabilidade informado é demasiadamente alto.")
                    return

                #If no problems are found, the code executs the compute function.
                else:
                    compute()

            #---------------------------------------------------------------    

            #------Bayesian Sample Size Estimator Algorithm---------#

            def compute():
                
                #----Getting variables-----#

                conf = float(self.conf.get())
                width = float(self.width.get())
                path = str(self.Arquivo_de_Dados)
                sample_pure = np.array(np.loadtxt(fname = path))

                #---------------------------

                #----Defining some algorithm and statistical parameters----#

                Accurate = 150 #How many times the algorithm is going to run
                sample_data = sorted(width - sample_pure) #defining sample by loss
                N=len(sample_data) 
                alpha = 1 - conf #Getting the significance 
                conf_level = 1 - (alpha/2)
                z_score = norm.ppf(conf_level) #Normal inverse of the confidence level
                std_pop = np.std(sample_data)
                MOE_acc = 0.01 #Margin of error acceptable
                n=30 #initial sample size

                #-----------------------------------------------------------

                # Algorithm
                n_updated = []
                for i in range(0, Accurate):
                    n_bayesian = 0
                    while n_bayesian-n != 0:
                        data_al = rd.choices(sample_data, k=n)
                        std_sample = np.std(data_al, ddof=1)
                        sigma2L = (((std_sample**2)*(std_pop**2))/((std_sample**2)+(std_pop**2)))**0.5
                        n_bayesian = round(((z_score*(sigma2L/MOE_acc))**2)/(1+(((z_score*(sigma2L/MOE_acc))**2)/N)))
                        n=n+1
                        if n == N:
                            n = 30
                    n_updated.append(n_bayesian)

                n_bayesian_final = int(round(np.mean(n_updated))) #final result

                #-----------------------------------------------------------

                #------Modeling window of results and buttons-----#

                master.title("Resultados - "+Path(self.Arquivo_de_Dados).resolve().stem)
                
                label3 = tk.Label(master, text= 'O novo tamanho amostral obtido é de {} observações.'.format(n_bayesian_final),font=('helvetica', 10, 'bold'))
                window.create_window(200, 210, window=label3)

                label4 = tk.Label(master, text= 'Você deseja computar um novo tamanho amostral?',font=('helvetica', 10))
                window.create_window(200, 250, window=label4)

                label5 = tk.Button(master, text= 'Sim',command = self.Algoritmo, font=('helvetica', 10)) #button to run the Algoritmo function again
                window.create_window(170, 280, window=label5)

                label6 = tk.Button(master, text= 'Não, sair',command = master.quit,font=('helvetica', 10)) #button to quit
                window.create_window(230, 280, window=label6)

                #----------------------------------------------------
        
            button = tk.Button(master, text='Computar novo tamanho amostral', command=verify, bg='brown', fg='white', font=('helvetica', 9, 'bold'))
            window.create_window(200, 180, window=button)

        #----If any error occur, it will return to the main window-----#     

        else:
            messagebox.showinfo("Erro", "Foi escolhido um arquivo .txt inexistente.")
            return          

        #--------------------------------------------------------------#
        
        tk.mainloop()

def main(): 
    root = tk.Tk()
    MainWindow(root)
    root.mainloop()

if __name__ == '__main__':
    main()        



