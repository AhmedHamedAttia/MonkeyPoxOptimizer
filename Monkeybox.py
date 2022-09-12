import numpy as np
import math 

#########################################################
def cal_fitness(functype, x):
    
    if  functype == 1 :    
        return dixonprice(x)
    elif functype == 2 :  
         return LEVY(x)
    elif functype == 3 :  
         return  Sphere(x)  
    elif functype == 4 :  
         return  Rastrigin(x)
    elif functype == 5 :  
         return  sumpow(x)
     
    return 0
  
########################################################
def copy_gen(seq,functype):
    
     if  functype == 1 or functype == 2 :
        UpperLim = 10
        LomerLim = -10
     elif  functype == 3 or functype == 4 :
        UpperLim = 5.12
        LomerLim = -5.12
     elif  functype == 5 :
        UpperLim = 1
        LomerLim = -1
        
     n = len(seq) 
     minseq = np.zeros(n) 
     Arr = np.zeros(n)
     minseq[0:n] = seq[0:n]
     Arr[0:n] =  seq[0:n]
     
     minf = cal_fitness(functype, minseq) 
     #print("inside ",Arr,"  ",minseq)
     for i in range(n) :
        Arr[i] = np.random.uniform(low=LomerLim, high=UpperLim)
        ArrF =  cal_fitness(functype, Arr)
        #print(i,"  ",ArrF,"   ",minf)
        if ArrF < minf :
            minseq[0:len(Arr)] = Arr[0:len(Arr)]
            minf = ArrF
            #print("swap :",minseq)
        else :
            Arr[i] =  minseq[i]
                        
     #print(cal_fitness(functype,maxseq),"  ",minseq," \n")        
     return minseq
########################################################
def crossOver(seq1,seq2,functype):
    #print(seq1[0])
    n = len(seq1)
    Arr = np.zeros((2,n))
    crossover_point = int(n/2)
#    #print(crossover_point)
#    for i in range(n):
#      if i < crossover_point:
#        Arr[0, i] = seq1[i]
#        Arr[0, i] = seq2[i + crossover_point]
#        Arr[1, i] = seq2[i]
#        Arr[1, i] = seq1[i + crossover_point]
#        #print(i)
    Arr[0, 0:crossover_point] = seq1[0:crossover_point]
    Arr[0, crossover_point:] = seq2[crossover_point:]
    Arr[1, 0:crossover_point] = seq2[0:crossover_point]
    Arr[1, crossover_point:] = seq1[crossover_point:]
            
        
    if cal_fitness(functype, Arr[0,:]) < cal_fitness(functype, Arr[1,:]) and cal_fitness(functype, Arr[0,:]) < cal_fitness(functype, seq1) : 
        return Arr[0,:]
    elif cal_fitness(functype, Arr[1,:]) < cal_fitness(functype, Arr[0,:]) and cal_fitness(functype, Arr[1,:]) < cal_fitness(functype, seq1) :
      return Arr[1,:]
    else:
      return seq1
#######################################################
def dixonprice(x):
    return (x[0]-1)**2 + sum((i+1)*(2*x[i]**2-x[i-1])**2 for i in range(1, len(x)))

############################################
def Sphere(xx):
    d = len(xx)
    int_sum = 0
    for i in range(d):
        xi = xx[i]
        int_sum += xi ** 2
    return int_sum 
############################################    
def Rastrigin(chromosome):
	#### F5 Rastrigin's function multimodal, symmetric, separable
	fitness = 10*len(chromosome)
	for i in range(len(chromosome)):
		fitness += chromosome[i]**2 - (10*math.cos(2*math.pi*chromosome[i]))
	return fitness
##############################################
def sumpow(xx):
    d = len(xx);
    sumval = 0
    
    for ii in range(d):
         xi = xx[ii]
         new = (abs(xi))**(ii+2)
         sumval = sumval + new
     
    return sumval

####################################################
def LEVY(xx):
    
    d = len(xx)
    w = np.zeros(d) 

    for ii in range(d):
    	w[ii] = 1 + (xx[ii] - 1)/4;
    

    term1 = (math.sin(math.pi*w[0]))**2;
    term3 = (w[d-1]-1)**2 * (1+(math.sin(2*math.pi*w[d-1]))**2);

    sumval = 0;
    for ii in range(0,(d-1)):
         wi = w[ii] 
         new = (wi-1)**2 * (1+10 *(math.sin(math.pi*wi+1))**2)
         sumval = sumval + new

    return term1 + sumval + term3;