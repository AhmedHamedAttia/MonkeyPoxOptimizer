import numpy as np
import Monkeybox
import random
import pandas as pd
import csv
from xlsxwriter import Workbook

# Function Type 
################# dixonprice 
functype = 5
# Number of the weights we are looking to optimize.
num_weights = 75    ## or d 

if  functype == 1 or functype == 2 :
        UpperLim = 10
        LomerLim = -10
elif  functype == 3 or functype == 4 :
        UpperLim = 5.12
        LomerLim = -5.12
elif  functype == 5 :
        UpperLim = 1
        LomerLim = -1


maxGen = 50 #50
maxItr = 1

x = np.arange(0, maxGen, 1)
results = pd.DataFrame([],columns = {'Fitness'})
serResults = pd.Series(data=[0.0],index={'Fitness'})

convCurve = pd.DataFrame([],columns = x)
serCurve = pd.Series(data=np.arange(0.0, maxGen, 1),index=x)
#BsFitness = 0.0


limpop = 100   ### num of virus
delPre = 20
BestPre =  50

count = 0
while(count<maxItr):
  print("Iteration number: ", count)

  """
  ############### MO exploration step ###################
  """
  cell = np.random.uniform(low=LomerLim, high=UpperLim, size= num_weights)
  CFitness = Monkeybox.cal_fitness(functype, cell)
  #print("CFitness ",CFitness)
  c = 0  
  
  Attack = np.zeros(num_weights) 
  Attack[0:num_weights] = cell[0:num_weights] 

  while 1 :

      for i in range(num_weights) :
          #print(Attack[i],"   ",(Attack[i] - 0.2))
          if (Attack[i] - 0.01) >  LomerLim : 
              Attack[i] = Attack[i] - 0.01

      AtFitness=Monkeybox.cal_fitness(functype, Attack)
      #print("Attack :: ",Attack)
      #print(c," Attack  F :: ",AtFitness)
      c = c + 1
      if AtFitness < CFitness : 
          break;
      if c == 10000 :
          Attack[0:num_weights] = cell[0:num_weights] 
          break;



  """
  ########## MO Exploitation step  #######################
  """
  pop2 = np.arange(0.0, num_weights+1, 1)
  x = np.arange(0, num_weights+1, 1)
  #print(Attack)

  for k in range(num_weights):
    pop2[k] = Attack[k]

  pop2[num_weights] = Monkeybox.cal_fitness(functype,pop2[0:num_weights]) 
  pop2.resize(num_weights+1)
  #print("pop2  ",pop2)
  ser = pd.Series(data=pop2,index=x)
  #ser[num_weight] = Monkeybox.cal_fitnessArr(equation_inputs,pop[0])
  #print(" ser  ",ser)
  df = pd.DataFrame()
  df = ser.to_frame()
  df = pd.DataFrame([],columns = x)
  df = df.append(ser,ignore_index=True)
  #print(" df ",df.iloc[0,:])

  popInd = 1

  for i in range(maxGen):
    
      df = df.sort_values(num_weights,ascending=True)

      delInd = int(np.floor(len(df)*delPre/100))
      if delInd>10:
        df = df.drop(df.tail(delInd).index)
      BestLen = int(np.ceil(len(df)*BestPre/100))
      otherLen = len(df) - BestLen

      df.reset_index(inplace = True)
      del df["index"]
      #print("\n   ",i,"   ",df,"\n")
      #print(" BLen",BestLen,"   OLen",otherLen)


        ####### copy best 
      for j in range(BestLen):
          #print(" BLen",BestLen)
          copym = Monkeybox.copy_gen(df.iloc[j,0:num_weights],functype)
          #print("\n *** ",copym)
          if not((copym == df.iloc[j,0:num_weights]).all().any()):
            for k in range(num_weights):
              pop2[k] = copym[k]
            pop2[num_weights] = Monkeybox.cal_fitness(functype,pop2[0:num_weights]) 
            ser = pd.Series(data=pop2,index=x)
            df = df.append(ser,ignore_index=True)
  #
  #    ###### crossOver other 
      ind = []
      for j in range(BestLen+1,BestLen+otherLen) :
          rindx = random.randint(0,BestLen-1)
          #print(df.iloc[j,0:num_weights])
          #print(df.iloc[rindx,0:num_weights])
          crossm = Monkeybox.crossOver(df.iloc[j,0:num_weights],df.iloc[rindx,0:num_weights],functype)
          #print("crossm :: ",crossm)
          if not((crossm == df.iloc[j,0:num_weights]).all().any()):
            for k in range(num_weights):
                pop2[k] = crossm[k]
            pop2[num_weights] = Monkeybox.cal_fitness(functype,pop2[0:num_weights]) 
            ser = pd.Series(data=pop2,index=x)
            if not((df == ser).all(1).any()):
              df.iloc[j,:] = ser
      serCurve[i] = df.iloc[0,num_weights]
  convCurve = convCurve.append(serCurve,ignore_index=True)
# Then return the index of that solution corresponding to the best fitness.
  df = df.sort_values(num_weights,ascending=True)
  df.reset_index(inplace = True)
  del df["index"]

  #print("Best solution : \n", df.head(20))
  #serCurve[i] = 
  serResults[0] = df.iloc[0,num_weights]
  print("Best value", serResults[0])
  results = results.append(serResults,ignore_index=True)
  count += 1
  
#convCurve = convCurve.iloc[convCurve.iloc[:,num_weights].idxmax(),:]
results.describe()
mx = results.idxmax()

writer =  pd.ExcelWriter('ConvCurve.xlsx', engine='xlsxwriter') #SONout.xlse
convCurve.iloc[mx,:].to_excel(writer, sheet_name='ConvCurve', index=False) # welocme -> sheet sheet_name
writer.save()