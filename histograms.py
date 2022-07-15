import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import scipy.stats as sp 

#File name to proccess
file="msza"  
argument="OutputsUltimate/"+file+".txt" 

#Calculates uint8 values from 8-bit binary number
def analyze(input):
  weights = [128, 64, 32, 16, 8, 4, 2, 1]
  currWeight = 0
  currNumber = 0
  data = []
  
  with open(input) as inputFile:
    for line in inputFile:
      for currBit in line:
        if(currBit == ' '):
          currWeight = 0
          data.append(currNumber)
          currNumber = 0
        else: 
          currNumber += weights[currWeight]*int(currBit)
          currWeight += 1
  return data
        
        
#Calculates entropy of given data array       
def entropy(data):
  pd_series = pd.Series(data)
  counts = pd_series.value_counts()
  return sp.entropy(counts, base=2)

#Prints histograms of R,G,B components from R,G,B arrays    
def histograms(arrayR,arrayG,arrayB):
  #Weights of numbers
  w = np.ones_like(arrayR) / float(len(arrayR))
  
  #Histogram aux
  fig, axs = plt.subplots(3, 1,tight_layout=True, figsize=(10,6))
  
  #Text-box properties
  props= dict(boxstyle='round',facecolor='wheat',alpha=0.5)
  
  #Entropy label
  textR = "E="+str(round(entropy(arrayR),5)) 
  textG = "E="+str(round(entropy(arrayG),5)) 
  textB = "E="+str(round(entropy(arrayB),5)) 
  
  axs[0].hist(arrayR, bins=np.amax(arrayR)+1,weights=w)
  axs[1].hist(arrayG, bins=np.amax(arrayG)+1,weights=w)
  axs[2].hist(arrayB, bins=np.amax(arrayB)+1,weights=w)
  axs[0].set_title("R")
  axs[1].set_title("G")
  axs[2].set_title("B")
  axs[0].text(0.85,0.95,textR,transform=axs[0].transAxes,fontsize=10,verticalalignment='top',bbox=props)
  axs[1].text(0.85,0.95,textG,transform=axs[1].transAxes,fontsize=10,verticalalignment='top',bbox=props)
  axs[2].text(0.85,0.95,textB,transform=axs[2].transAxes,fontsize=10,verticalalignment='top',bbox=props)
    
  fig.suptitle("Histograms of R, G, B components")
  plt.show() 
  
 #Prints histogram from one array 
def histogram(array):
  #Weights of numbers
  w = np.ones_like(array) / float(len(array))
  
  #Histogram aux
  fig, ax = plt.subplots(tight_layout=True, figsize=(10,6))
  
  #Text-box properties
  props= dict(boxstyle='round',facecolor='wheat',alpha=0.5)
  
  #Entropy label
  textR = "E="+str(round(entropy(array),5)) 
  
  ax.hist(array, bins=np.amax(array)+1,weights=w)
  ax.text(0.85,0.95,textR,transform=ax.transAxes,fontsize=10,verticalalignment='top',bbox=props)
  string="Histogram of "+file+" sequence"
  fig.suptitle(string)
  plt.show() 
  
  
#Displays histograms of given file/files  
def display(*args):
  """
  If you want to get a single histogram, provide only one argument. 
  If you want to get histograms of R,G,B components provide 3 .txt files, separated with coma
  """
  
  match len(args):
    case 3:
      inputPath_R = args[0]
      inputPath_G = args[1]
      inputPath_B = args[2]
    
      data_r = analyze(inputPath_R)
      data_g = analyze(inputPath_G)
      data_b = analyze(inputPath_B)
    
      histograms(data_r, data_g, data_b) 
      
    case 1:
      inputPath = args[0]
      data = analyze(inputPath)
      histogram(data) 
      
    case _:
      print("Valid amount of arguments is either 1 or 3. For more type help(histograms.display)")
    
#Call function 
display(argument)