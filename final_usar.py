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


warnings.filterwarnings("ignore")

class MainWindow:

    def __init__(self, master):
        self.Arquivo_de_Dados="Vazio"
        self.master = master
        self.frame = tk.Frame(self.master)
        self.master.title('Calculadora de Tamanho Amostral Bayesiana')
        dir=os.getcwd()
        file_image=r'D:\Iago Lemos\Área de trabalho\IC Petrobrás\Petrobras Codes\Bayesian Estimator\bayes.jfif'
        image = Image.open(file_image)
        photo = ImageTk.PhotoImage(image)
        self.label1= tk.Label(self.frame, image=photo)        
        self.label1.image=photo
        self.label1.pack()
        self.frame.pack()
        menubar = tk.Menu(self.master)
        self.master.config(menu=menubar)
        fileMenu = tk.Menu(menubar)
        fileMenu.add_command(label="Aplicar Algoritmo ...", underline=0, command=self.Algoritmo) 
        menubar.add_cascade(label="Novo Tamanho Amostral", underline=0, menu=fileMenu)
        master.resizable(0,0)
    
    def Algoritmo(self):
        initialdir = 'D:\Iago Lemos\Área de trabalho\IC Petrobrás\Petrobras Codes\Bayesian Estimator'
        filename = tkinter.filedialog.askopenfilename(initialdir = initialdir, title = "Escolha a amostra",filetypes = [("Arquivos extensão .txt","*.txt")])

        def iserror(func, *args, **kw):
            try:
                func(*args, **kw)
                return False
            except Exception:
                return True

        if os.path.isfile(filename)==False:
            return      

        if iserror(np.loadtxt, filename) == True:
            messagebox.showinfo("Erro", "Foi escolhido um arquivo .txt inválido.")
            return

        if iserror(np.loadtxt, filename) == False:
            self.Arquivo_de_Dados=filename 
            
            master = tk.Tk()
            window = tk.Canvas(master, width = 400, height = 300)
            window.pack()
            master.title("Parâmetros - "+Path(self.Arquivo_de_Dados).resolve().stem)
            master.resizable(0,0)

            label1 = tk.Label(master, text='Espessura nominal do tubo [mm]')
            window.create_window(200, 25, window=label1)

            label2 = tk.Label(master, text='Nível de confiança:')
            window.create_window(200,100 , window=label2)

            self.width = tk.Entry (master) 
            window.create_window(200, 50, window=self.width)
            
            self.conf = tk.Entry(master)
            window.create_window(200, 125, window=self.conf)
            
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
                else:
                    compute()

            def compute():
            
                conf = float(self.conf.get())
                width = float(self.width.get())
                path = str(self.Arquivo_de_Dados)
                sample_pure = np.array(np.loadtxt(fname = path))

                # Defining Data
                Accurate = 150
                sample_data = sorted(width - sample_pure)

                # Statistical definitions
                N=len(sample_data)

                alpha = 1 - conf
                conf_level = 1 - (alpha/2)
                z_score = norm.ppf(conf_level)
                std_pop = np.std(sample_data)
                MOE_acc = 0.01
                n=30

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

                n_bayesian_final = int(round(np.mean(n_updated)))
                
                master.title("Resultados - "+Path(self.Arquivo_de_Dados).resolve().stem)
                
                label3 = tk.Label(master, text= 'O novo tamanho amostral obtido é de {} observações.'.format(n_bayesian_final),font=('helvetica', 10, 'bold'))
                window.create_window(200, 210, window=label3)

                label4 = tk.Label(master, text= 'Você deseja computar um novo tamanho amostral?',font=('helvetica', 10))
                window.create_window(200, 250, window=label4)

                label5 = tk.Button(master, text= 'Sim',command = self.Algoritmo, font=('helvetica', 10))
                window.create_window(170, 280, window=label5)

                label6 = tk.Button(master, text= 'Não, sair',command = master.quit,font=('helvetica', 10))
                window.create_window(230, 280, window=label6)

            button = tk.Button(master, text='Computar novo tamanho amostral', command=verify, bg='brown', fg='white', font=('helvetica', 9, 'bold'))
            window.create_window(200, 180, window=button)
        else:
            messagebox.showinfo("Erro", "Foi escolhido um arquivo .txt inexistente.")
            return                                                                                          
        tk.mainloop()

def main(): 
    root = tk.Tk()
    MainWindow(root)
    root.mainloop()

if __name__ == '__main__':
    main()        



