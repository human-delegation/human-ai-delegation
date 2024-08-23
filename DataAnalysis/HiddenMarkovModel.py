# Created at 2/8/2020

# Enter feature description here

# Enter Scenario herer: This code is used for HMM model with general number of hidden states: state_n>=2

# Enter steps here:
# 1. The code will get input data from 2-KPI-summary-with-weather folder
# 2. The input data is the initial values of emission related factors and transition related factors
#### 2.1 To deliver the best fit, different initial values should be used for the best MLE
# 3. BFGS fitting is implemented to fit the data with MLE maximization (-log MLE minimization)
# 4. The fitting result is stored in the Coefficients_estimation table and output


import os
import numpy as np
from scipy.optimize import minimize
import csv
import pandas as pd


###
state_n=3
######
# This is the sample code that generates the 3-hidden state.
def logit(x):
    return 1 / (1 + np.exp(-1*x))

def emi(i, o, x, emi_coef):  # emission function: emi(state=i,observation=o,factors=x,coefficients=emi_coef)
    xnum = len(x)  # dimension of factors
    return np.exp(-(o[0] - emi_coef[i]-emi_coef[3] - np.array(emi_coef[state_n+1+i*xnum:state_n+1+(i+1)*xnum]).dot(x)) ** 2)

def q(i, j, trans_coef,x):  # transition unit transition probability (q=(current state=i,next state=j,coefficient=trans_coef,factor=x))
    xnum = len(x)
    if i==0 and j==0:
        return logit(trans_coef[0]+trans_coef[6] + np.array(trans_coef[7:7+xnum]).dot(x))+logit(trans_coef[1]+trans_coef[6]+np.array(trans_coef[7:7+xnum]).dot(x))-1
    if i==0 and j==1:
        return 1-logit(trans_coef[0]+trans_coef[6]+np.array(trans_coef[7:7+xnum]).dot(x))
    if i==0 and j==2:
        return 1-logit(trans_coef[1]+trans_coef[6]+np.array(trans_coef[7:7+xnum]).dot(x))

    if i==1 and j==0:
        return logit(trans_coef[2]+trans_coef[6]+np.array(trans_coef[7+xnum:7+2*xnum]).dot(x))
    if i==1 and j==2:
        return 1-logit(trans_coef[3]+trans_coef[6]+np.array(trans_coef[7+xnum:7+2*xnum]).dot(x))
    if i==1 and j==1:
        return logit(trans_coef[3]+trans_coef[6]+np.array(trans_coef[7+xnum:7+2*xnum]).dot(x))-logit(trans_coef[2]+trans_coef[6]+np.array(trans_coef[7+xnum:7+2*xnum]).dot(x))

    if i==2 and j==0:
        return logit(trans_coef[4]+trans_coef[6]+np.array(trans_coef[7+2*xnum:7+3*xnum]).dot(x))
    if i==2 and j==1:
        return logit(trans_coef[5]+trans_coef[6]+np.array(trans_coef[7+2*xnum:7+3*xnum]).dot(x))
    if i==2 and j==2:
        return 1-logit(trans_coef[4]+trans_coef[6]+np.array(trans_coef[7+2*xnum:7+3*xnum]).dot(x))-logit(trans_coef[5]+trans_coef[6]+np.array(trans_coef[7+2*xnum:7+3*xnum]).dot(x))

# def emi
def sigmoid(params):
    trans_coef = [params[k] for k in range(7+3*num_xtrans)]
    emi_coef = [params[k] for k in range(7+3*num_xtrans, 7+3*num_xtrans+state_n+state_n*num_xemi+1)]

    forward = {}
    for s in range(state_n): # get period 0 state distribution
        forward[s]=1/state_n*sum([q(ss, s, trans_coef, xtrans[0]) for ss in range(state_n)])

    for t in range(1, len(ydata)):
        this_forward = [forward[s] for s in range(state_n)]
        for s in range(state_n):
            forward[s]=sum([this_forward[s0]*q(s0, s, trans_coef, xtrans[t]) * emi(s, ydata[t], xemi[t], emi_coef) for s0 in range(state_n)])
    # Calculate negative log likelihood
    LL = sum([forward[s] for s in range(state_n)])
    LL = -1*np.log(LL)
    for i in range(len(params)):
        LL=LL+0.001*params[i]*params[i]

    return LL



transition_factors = ['sale_improvement','Manager_outperform','outperform_area']

emission_factors = ['period', 'period_square','BadWeather','Holiday']

para_description=['mu12', 'mu13', 'mu21', 'mu23', 'mu31', 'mu32','tra_fix',
                  'L1 sale_improvement', 'L1 Manager_outperform', 'L1 outperform_area',
                  'L2 sale_improvement', 'L2 Manager_outperform', 'L2 outperform_area',
                  'L3 sale_improvement', 'L3 Manager_outperform', 'L3 outperform_area',
                  'emicoef_1', 'emicoef_2', 'emicoef_3','emi_fix',
                  'L1 period', 'L1 period_square','L1 weather','L1 Holiday',
                  'L2 period', 'L2 period_square','L2 weather','L2 Holiday',
                  'L3 period', 'L3 period_square','L3 weather','L3 Holiday']

num_xtrans = len(transition_factors)
num_xemi = len(emission_factors)

Aggregate_table=open('Coefficients_estimation_State_'+str(state_n)+'.csv','w')
Aggregate_table_writer=csv.writer(Aggregate_table)
Aggregate_table_writer.writerow(['store_id'] + para_description + ['likelyhood'])

current_loc = 0

reader=csv.reader(open('Initial_parameters.csv', 'r'))
a=next(reader)
for row in reader:
    initParams=[float(rows) for rows in row]

initParams = np.array(initParams, dtype=np.float128)

current_loc = 0

file_list = os.listdir('../DataProcessing/2-KPI-summary-with-weather')
file_list.sort()

# for file in file_list:
file=file_list[0]
if '.csv' in file:
    store_id = file.split('.')[0]

    Inputfile1_transform = pd.read_csv('../DataProcessing/2-KPI-summary-with-weather/' + file)

    ydata = Inputfile1_transform[['DelegationDecision']].values
    if len(ydata)>=30:
        print(store_id)
        xtrans = Inputfile1_transform[transition_factors].values
        Inputfile1_transform['period']=[i for i in range(len(ydata))]
        Inputfile1_transform['period'] = Inputfile1_transform['period'] / Inputfile1_transform['period'].max()

        Inputfile1_transform['period_square']=Inputfile1_transform['period']*Inputfile1_transform['period']
        xemi = Inputfile1_transform[emission_factors].values

        results = minimize(sigmoid, initParams, method='BFGS')

        print(store_id, results.message,results.fun,results.x.tolist())
        Aggregate_table_writer.writerow([store_id] + results.x.tolist() + [results.fun])

Aggregate_table.close()