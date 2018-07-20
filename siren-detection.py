import essentia
import essentia.standard
from essentia.standard import *
import numpy as np
import math
import wave
import os
from sys import argv

from pylab import plot, show, figure, imshow
import matplotlib.pyplot as plt
plt.rcParams['figure.figsize'] = (16, 9)    # set plot to something larger than default

# 10 types of audio sample in the data set
audioSampleCategoryList = ["air_conditioner", "car_horn", "children_playing", "dog_bark", "drilling", "engine_idling", "gun_shot", "jackhammer", "siren", "street_music"];

siren_avg_high = -7.6
siren_max_low = 8.05


def min_(x, y):
    if x > y:
        return y
    else:
        return x

def max_(x, y):
    if x > y:
        return x
    else:
        return y

def sampleTest(fileName):
    loader = essentia.standard.MonoLoader(filename=fileName)
    audio = loader()

    plt.figure(1)
    plt.subplot(311)
    plt.plot(audio[1 * 44100: 2 * 44100])
    plt.title("Audio sample")

    plt.subplot(312)
    plt.plot(audio)
    plt.title("Before FFT")

    func = FFT()
    curr = func(loader())
    avg = math.log(abs(np.mean(curr)))
    maxim = math.log(abs(max(curr)))

    print("avg: " + str(avg))
    print("maxim: " + str(maxim))

    plt.subplot(313)
    plt.plot(curr)
    plt.title("After FFT")
    plt.show()

    if avg <= siren_avg_high and maxim >= siren_max_low:
        print "This is a siren!"
    else:
        print "This is not a siren."

def plotOriginalWavFile(filename):
    spf = wave.open(filename)
    # extract raw audio from wave file
    signal = spf.readframes(-1)
    signal = np.fromstring(signal, 'Int16')
    fs = spf.getframerate()

    print("len of signal: " + str(len(signal)))
    print("freq of signal: " + str(fs) + "Hz")
    Time = np.linspace(0, len(signal)/fs*2, num = len(signal))
    plt.figure(0)
    plt.title('Siren Signal Wave')
    plt.plot(Time, signal)
    plt.show()

def getAvgMaxFromWavFile(filePath):
    results = {}
    if not os.path.exists(filePath):
        print "Invalid file path!"
        return results

    for fileName in os.listdir(filePath):
        absoluteFileName = filePath + "/" + fileName
        if not absoluteFileName.endswith('.wav') and not absoluteFileName.endswith('.mp3'):
            print "Invalid wav or mp3 file"
            continue
        #print absoluteFileName
        loader = essentia.standard.MonoLoader(filename=absoluteFileName)
        audio = loader()
        audioLen = len(audio)
        if (audioLen % 2) == 1:
            audio = audio[1:]
        func = FFT()
        curr = func(audio)
        avg = math.log(abs(np.mean(curr)))
        maxim = math.log(abs(max(curr)))
        result = (avg, maxim)
        results[fileName] = result

    return results

def getIndex(string):
    index = -1
    if not string:
        return category
    startIndex = string.find('-')
    endIndex = string.find('-', startIndex + 1)
    if startIndex == -1 or endIndex == -1 or startIndex >= endIndex:
        return index
    element = string[startIndex+1 : endIndex]
    #print element
    index = int(element)
    return index

def getMinMaxForEachCatory(results):
    avgMinDict     = [float('inf')] * len(audioSampleCategoryList)
    avgMaxDict     = [float('-inf')] * len(audioSampleCategoryList)
    maximMinDict   = [float('inf')] * len(audioSampleCategoryList)
    maximMaxDict   = [float('-inf')] * len(audioSampleCategoryList)

    for key, val in results.items():
        index = getIndex(key)
        if index == -1:
            print "Invalid index for " + key
            continue

        avg = val[0]
        avgMinDict[index] = min_(avg, avgMinDict[index])
        avgMaxDict[index] = max_(avg, avgMinDict[index])

        maxim = val[1]
        maximMinDict[index] = min_(maxim, maximMinDict[index])
        maximMaxDict[index] = max_(maxim, maximMaxDict[index])
        #print avgMinDict[index], avgMaxDict[index], maximMinDict[index], maximMaxDict[index]


    resultsList = [avgMinDict, avgMaxDict, maximMinDict, maximMaxDict]
    return resultsList


def printDict(results):
    print "file:            avg:            maxim:"
    for key, val in results.items():
        print key, " => ", (val[0], val[1])

def printDictPair(resultsList):
    avgMinDict = resultsList[0]
    avgMaxDict = resultsList[1]
    maximMinDict = resultsList[2]
    maximMaxDict = resultsList[3]
    index = 0
    print "file:            avg: (min - max)        maxim: (min - max)"
    for key in audioSampleCategoryList:
        print key, " => ", "avg: [", avgMinDict[index], avgMaxDict[index], "]   maxim: [", maximMinDict[index], maximMaxDict[index], "]"
        index += 1

def main():
    """
    filePath = './SirenTones'
    results = getAvgMaxFromWavFile(filePath)
    printDict(results)
    """
    filePath = '/home/yunpengx/Documents/SirenDetection/UrbanSound8K/audio/fold1'
    #filePath = '/home/yunpengx/Documents/SirenDetection/UrbanSound8K/audio/test'
    results = getAvgMaxFromWavFile(filePath)
    printDict(results)

    resultsList = getMinMaxForEachCatory(results)
    printDictPair(resultsList)

    #sampleTest(argv[1])

if __name__ == "__main__":
    main()

# --------------------- CODE USED FOR TESTING ---------------------

#import matplotlib.pyplot as plt

#loader1 = essentia.standard.MonoLoader(filename='siren-short.mp3')
#loader2 = essentia.standard.MonoLoader(filename='siren-long.mp3')
#loader3 = essentia.standard.MonoLoader(filename='audio-siren.mp3')
#loader4 = essentia.standard.MonoLoader(filename='siren2-short.mp3')
#loader5 = essentia.standard.MonoLoader(filename='siren2-long.mp3')
#loader6 = essentia.standard.MonoLoader(filename='antidote.mp3')
#loader7 = essentia.standard.MonoLoader(filename='beep13.mp3')
#loader8 = essentia.standard.MonoLoader(filename='vacuum.mp3')

#loaders = [loader1(), loader2(), loader3(), loader4(),
    #loader5(), loader6(), loader7(), loader8()]

#func = FFT()
#curr = func(loader8())
#plt.plot(curr)
#plt.show()
#print math.log(abs(np.mean(curr)))
#print math.log(abs(max(curr)))

#for loader in loaders:
    #curr = func(loader)
    #avg = math.log(abs(np.mean(curr)))
    #maxim = math.log(abs(max(curr)))

    #if avg <= siren_avg_high and maxim >= siren_max_low:
        #print "this is a siren!"
    #else:
        #print "NOPE!"

#file.write(func(loader2()))

#file.write(func(loader7()))
#file.write("\n")
#file.write(func(loader8()))

#file.close()

#def arrayToFile(fName, ldr):
    #func = FFT()
    #arr = func(ldr)

    #fle = open(fName, 'w')

    #for item in arr:
        #print >> fle, item

    #fle.close()
