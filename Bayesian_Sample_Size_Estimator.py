import numpy as np
from scipy.stats import norm
import random as rd
import subprocess, platform

def bayesian_sample_size_estimator():
    #Cleaning the terminal depending on the OS
    if platform.system()=="Windows":
        subprocess.Popen("cls", shell=True).communicate()
    else: #Linux and Mac
        print("\033c", end="")

    # Defining Data
    file = str(input('Input the path of the .txt data file and its name: '))
    width = float(input('Input the width of the tubes in analysis: '))
    sample_pure = np.array(np.loadtxt(fname=file))
    sample_data = sorted(width - sample_pure)

    # Statistical definitions
    N=len(sample_data)
    conf = float(input('Input the confidence level: '))
    Accurate = int(input('Input how many times you want that the algorithm compute the sample size before getting the final result (usually 100 times is enough):'))-1
    alpha = 1 - conf
    conf_level = 1 - (alpha/2)
    z_score = norm.ppf(conf_level)
    print(z_score)
    std_pop = np.std(sample_data)
    MOE_acc = 0.02
    n=30

    print('Wait until the algorithm converges.')

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
    n_bayesian_final = round(np.mean(n_updated))

    print('The initial sample size is {N}. The sample size estimated by the algorithm is {n_b}.'.format(N=N, n_b=n_bayesian_final))

    restart = str(input('Would you like to restart this program? (yes or no)'))
    if restart == 'yes' or restart == 'y':
        bayesian_sample_size_estimator()
    if restart == 'n' or restart == 'no':
        print ('Finishing Script.')
        input('Press enter to quit. ')

bayesian_sample_size_estimator()
