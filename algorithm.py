from scipy import ndimage
import cv2
import math 
import moviepy.editor as mv
import numpy as np
import wave
from os.path import exists



######################### GENERAL VARIABLES ##############################
file = "nba"
source_video = "Videos/"+file+".mp4"
source_audio = "Videos/"+file+".wav"
outputFile_path = "OutputsUltimate/"+file+".txt"

#Numbers od bytes to generate
byteNumber = 12500


############################### FUNCTIONS #################################
#Print iterations progress bar
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    if iteration == total: 
        print()
        
        
#Get R, G, B from igm 
def R(x, y, img):
    return img[y, x, 2]
def G(x, y, img):
    return img[y, x, 1]
def B(x, y, img):
    return img[y, x, 0]

#Generte color of x, y from img
def getColor(x, y, img):
    return (R(x, y, img) << 16) + (G(x, y, img)  << 8) + B(x, y, img) 


#Clear output file
outputFile = open(outputFile_path, 'w+')
with open(outputFile_path, 'r+') as f:
    f.truncate(0)
outputFile = open(outputFile_path, 'a')


############################## AUDIO ###############################
#Generate audio file from .mp4
file_exists = exists(source_audio)
if not file_exists:
    sound = mv.AudioFileClip(source_video)
    sound.write_audiofile(source_audio)    

#Get audio samples                                                                                       
ifile = wave.open(source_audio,'r')
audio_samples = ifile.getnframes()
audio = ifile.readframes(audio_samples)
audio_samples = np.frombuffer(audio,dtype=np.uint8)

#Cut leading zeros
i = 0
while(audio_samples[i] == 0):
    i+=1
audio_samples = audio_samples[i:]
    

############################# VIDEO ####################################
#Read video
vidcap = cv2.VideoCapture(source_video) 
fps = int(vidcap.get(cv2.CAP_PROP_FPS))

#Get frame and dimensions
success, image = vidcap.read()
height = image.shape[0]
width = image.shape[1]

#Center pixel cordinates
x_c = round(height/2)
y_c = round(width/2)

#Central pixel color
color_i = (getColor(x_c-1, y_c-1, image) + getColor(x_c-1, y_c, image) + getColor(x_c-1, y_c+1, image) + getColor(x_c, y_c-1, image) + getColor(x_c, y_c+1, image) + getColor(x_c+1, y_c-1, image) + getColor(x_c+1, y_c, image) + getColor(x_c+1, y_c+1, image) + getColor(x_c, y_c, image))/9

#Set tresholds
vidcap.set(1, fps*3)
success, image_3rd_second = vidcap.read()
vt = math.sqrt(ndimage.variance(image_3rd_second))
th = 100
watchdog = 0


############# MAIN LOOP ###################
#Parameters
R_1 = 0
G_1 = 0
B_1 = 0
R_2 = 0
G_2 = 0
B_2 = 0

frameDiscardFlag = False 
outputR = 0
outputG = 0
outputB = 0
bufor   = ''
buforG  = '' 
buforB  = ''

vidcap.set(1, 0)
bitCounter = 0
byteCounter = 0

#Aux audio variables
runct = 1
K = 500
soundbyte = 0

#Get pixel
x = round((color_i)%(width/2)+(width/4))
y = round((color_i)%(height/2)+(height/4))


while 1:
    success, image = vidcap.read()
    
    #Check if file not ended
    if(not success):
        break
    
    #Selecting pixel
    while 1:
        R = image[y, x, 2]
        G = image[y, x, 1]
        B = image[y, x, 0]
        if((R-R_1)**2 + (G-G_1)**2 + (B - B_1) ** 2 < vt):
            watchdog += 1
            x = (x+(R^G)+1)%width
            y = (y+(R^G)+1)%height
            if(watchdog > th):
                frameDiscardFlag = True
                break
        else: 
            break
    if(frameDiscardFlag):
        frameDiscardFlag = False
        continue


    if (byteCounter % 100 == 0):
        runct+=1
        
    #Getting audio based values
    binarySample = np.unpackbits(audio_samples[soundbyte])
    SN1 = binarySample[int((10 + (R*bitCounter+(G<<2)+B+runct)%(K/2))%8)]
    SN2 = binarySample[int((15 + (R*bitCounter+(G<<3)+B+runct)%(K/2))%8)]
    SN3 = binarySample[int((20 + (R*bitCounter+(G<<4)+B+runct)%(K/2))%8)]
    SN4 = binarySample[int((5 + (R*bitCounter+(G<<1)+B+runct)%(K/2))%8)]
    SN5 = binarySample[int((25 + (R*bitCounter+(G<<5)+B+runct)%(K/2))%8)]
    soundbyte += K
    
    #Getting random bit
    bufor += str(int(1 & (R ^ G ^ B ^ R_1 ^ R_2 ^ B_1 ^ B_2 ^ G_1 ^ G_2 ^ SN2 ^ SN2 ^ SN2 ^ SN2 ^ SN2)))

    #Changing next loop initial coords and previous R,G,B
    R_1 = R
    G_1 = G
    B_1 = B 
    x = (((R^x) << 4)^(G^y))%width
    y = (((G^x) << 4)^(B^y))%height

    #Printing 8-bit numbers to output file
    bitCounter += 1
    if(bitCounter > 7):
        R_2 = R
        G_2 = G
        B_2 = B
        outputFile.write(bufor+' ')
        bufor = ''
        byteCounter += 1
        printProgressBar(byteCounter, byteNumber, prefix = 'Progress:', suffix = 'Complete', length = 50)
        if(byteCounter >= byteNumber):
            break
        bitCounter = 0      
print("Completed")    
outputFile.close()
