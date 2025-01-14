import os
import numpy as np
import matplotlib.pyplot as plt
import numpy as np
import time

class AutoFocusMicroSpheres:
    def __init__(self,exposure=1, CCDMode='Normal'):
        self.exposure=exposure
        self.CCDMode=CCDMode
        zVal = []
        
    def MakeImageSweep(self, Zs, stg, showthem=True):
        zVal = []
        # Put the images in this array
        pics=[]
        
        from CamHamThread import CamHamThread
        cam=CamHamThread(exposure=0.5,SensitivityGain=4,CCDMode="NormalCCD")

        for i in range(0,len(Zs)):

            # Move stage
            stg.MoveToZ(Zs[i])

            #Snap a pic
            pics.append(cam.Snap(1)[0])
            print(Zs[i])
            time.sleep(1)
            
            zVal.append(Zs[i])
        self.zVal = zVal
        
        print (pics)
        print (len(pics)) 
        
        return pics

    def Autofocus(self, Zs, stg, showthem=True):
        Zs=Zs
        pics= self.MakeImageSweep(Zs, stg, showthem=True)
        
        
        print (len(pics))
        
        arrayMax = []
        arrayTenthLargestVal=[]
        arrayHundrethLargestVal =[]
        numarray=[]
        num =0

        for pic in pics:
            
            
            # create the histogram
            num+=1
            numarray.append(num)

            imarray = np.asarray(pic)
            imarray=imarray.flatten()
            plt.figure()

            maxValue=np.max(imarray)
            arrayMax.append(maxValue)
            minValue=np.min(imarray)
            xmax=maxValue
            xmin=minValue
            tenthLargestVal=np.partition(imarray, -10)[-10]
            optimize = tenthLargestVal
            arrayTenthLargestVal.append(optimize)
            hundrethLargestVal = np.partition(imarray, -100)[-100]
            arrayHundrethLargestVal.append(hundrethLargestVal)
            thousandthLargestVal = np.partition(imarray, -1000)[-1000]
            tenthousandthLargestVal = np.partition(imarray, -10000)[-10000]
            plt.axvline(x=xmax, ymin=0, ymax=1, color ='red', label="max")
            plt.axvline(x=xmin, ymin=0, ymax=1, color='blue',label = "min")
            plt.axvline(x=tenthLargestVal, ymin=0, ymax=1, color='green', label = "tenthLargestVal")
            plt.axvline(x=hundrethLargestVal, ymin=0, ymax=1, color='yellow', label = "hundrethLargestVal")
            plt.axvline(x=thousandthLargestVal, ymin=0, ymax=1, color='orange', Label = "thousandthLargestVal")
            plt.axvline(x=tenthousandthLargestVal, ymin=0, ymax=1, color='pink', label = "tenthousandthLargestVal")
            plt.legend(loc="upper left")

            (n, bins, patches) = plt.hist(imarray, bins=10**np.logspace(np.log10(.1),np.log10(5.0), 256), histtype='stepfilled')
            plt.yscale('symlog')
            plt.xscale('log')
            plt.title("Grayscale Histogram")
            plt.xlabel("grayscale value")
            plt.ylabel("pixels")
            plt.xlim(1000,100000)
            plt.ylim(1, 1000000)
            plt.savefig(r"C:\Users\ohs2758\Documents\plots"+ str(num))
            plt.close()

        plt.figure()
        plt.plot(numarray,arrayMax, color ='red',label="max")
        plt.plot(numarray,arrayTenthLargestVal, color ='green',label = "tenthLargestVal")
        plt.plot(numarray,arrayHundrethLargestVal, color ='yellow',label = "hundrethLargestVal")
        plt.title("Brightness per Image")
        plt.xlabel("Image number")
        plt.ylabel("Brightness Value")
        plt.legend(loc="upper left")
        plt.show()

        MaxTenthBrightestVal=np.max(arrayTenthLargestVal)
        indexTenthVal = arrayTenthLargestVal.index(MaxTenthBrightestVal)

        
        print("Sucessfully AutoFocused at ", self.zVal[indexTenthVal])
        return self.zVal[indexTenthVal]
