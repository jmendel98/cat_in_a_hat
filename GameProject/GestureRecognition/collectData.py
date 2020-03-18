#!/usr/bin/python
#
#   This program  reads the angles from the acceleromter, gyrscope
#   and mangnetometeron a BerryIMU connected to a Raspberry Pi.
#
#   Both the BerryIMUv1 and BerryIMUv2 are supported
#
#   BerryIMUv1 uses LSM9DS0 IMU
#   BerryIMUv2 uses LSM9DS1 IMU
#
#   This program includes a number of calculations to improve the 
#   values returned from BerryIMU. If this is new to you, it 
#   may be worthwhile first to look at berryIMU-simple.py, which 
#   has a much more simplified version of code which would be easier
#   to read.   
#
#   http://ozzmaker.com/

import time
import math
import IMU
import datetime
import os
import sys
import select
import pandas as pd
import os.path
import numpy as np
from os import path
import pickle
# If the IMU is upside down (Skull logo facing up), change this value to 1
IMU_UPSIDE_DOWN = 0

RAD_TO_DEG = 57.29578
M_PI = 3.14159265358979323846
G_GAIN = 0.070  # [deg/s/LSB]  If you change the dps for gyro, you need to update this value accordingly
AA =  0.40      # Complementary filter constant


################# Compass Calibration values ############
# Use calibrateBerryIMU.py to get calibration values 
# Calibrating the compass isnt mandatory, however a calibrated 
# compass will result in a more accurate heading value.

magXmin =  0
magYmin =  0
magZmin =  0
magXmax =  0
magYmax =  0
magZmax =  0


'''
Here is an example:
magXmin =  -1748
magYmin =  -1025
magZmin =  -1876
magXmax =  959
magYmax =  1651
magZmax =  708
Dont use the above values, these are just an example.
'''



#Kalman filter variables
Q_angle = 0.02
Q_gyro = 0.0015
R_angle = 0.005
y_bias = 0.0
x_bias = 0.0
XP_00 = 0.0
XP_01 = 0.0
XP_10 = 0.0
XP_11 = 0.0
YP_00 = 0.0
YP_01 = 0.0
YP_10 = 0.0
YP_11 = 0.0
KFangleX = 0.0
KFangleY = 0.0




def kalmanFilterY ( accAngle, gyroRate, DT):
    y=0.0
    S=0.0

    global KFangleY
    global Q_angle
    global Q_gyro
    global y_bias
    global YP_00
    global YP_01
    global YP_10
    global YP_11

    KFangleY = KFangleY + DT * (gyroRate - y_bias)

    YP_00 = YP_00 + ( - DT * (YP_10 + YP_01) + Q_angle * DT )
    YP_01 = YP_01 + ( - DT * YP_11 )
    YP_10 = YP_10 + ( - DT * YP_11 )
    YP_11 = YP_11 + ( + Q_gyro * DT )

    y = accAngle - KFangleY
    S = YP_00 + R_angle
    K_0 = YP_00 / S
    K_1 = YP_10 / S
    
    KFangleY = KFangleY + ( K_0 * y )
    y_bias = y_bias + ( K_1 * y )
    
    YP_00 = YP_00 - ( K_0 * YP_00 )
    YP_01 = YP_01 - ( K_0 * YP_01 )
    YP_10 = YP_10 - ( K_1 * YP_00 )
    YP_11 = YP_11 - ( K_1 * YP_01 )
    
    return KFangleY

def kalmanFilterX ( accAngle, gyroRate, DT):
    x=0.0
    S=0.0

    global KFangleX
    global Q_angle
    global Q_gyro
    global x_bias
    global XP_00
    global XP_01
    global XP_10
    global XP_11


    KFangleX = KFangleX + DT * (gyroRate - x_bias)

    XP_00 = XP_00 + ( - DT * (XP_10 + XP_01) + Q_angle * DT )
    XP_01 = XP_01 + ( - DT * XP_11 )
    XP_10 = XP_10 + ( - DT * XP_11 )
    XP_11 = XP_11 + ( + Q_gyro * DT )

    x = accAngle - KFangleX
    S = XP_00 + R_angle
    K_0 = XP_00 / S
    K_1 = XP_10 / S
    
    KFangleX = KFangleX + ( K_0 * x )
    x_bias = x_bias + ( K_1 * x )
    
    XP_00 = XP_00 - ( K_0 * XP_00 )
    XP_01 = XP_01 - ( K_0 * XP_01 )
    XP_10 = XP_10 - ( K_1 * XP_00 )
    XP_11 = XP_11 - ( K_1 * XP_01 )
    
    return KFangleX


IMU.detectIMU()     #Detect if BerryIMUv1 or BerryIMUv2 is connected.
IMU.initIMU()       #Initialise the accelerometer, gyroscope and compass

gyroXangle = 0.0
gyroYangle = 0.0
gyroZangle = 0.0
CFangleX = 0.0
CFangleY = 0.0
kalmanX = 0.0
kalmanY = 0.0

gesture_dict = {
    0:"none",
    1:"right twist",
    2:"thrust",
    3:"up",
    4:"circle",
}

gesture_num = input("Enter the gesture number: ")
try:
    gesture_num = int(gesture_num)
except(ValueError):
    gesture_num = 0

if gesture_num not in gesture_dict:
    gesture_num = 0


a = datetime.datetime.now()


if not path.exists("gesture_data2.csv"):
    df = pd.DataFrame()
    df.to_csv('gesture_data2.csv')
else:
    df = pd.read_csv('gesture_data2.csv')

if not path.exists("gesture_data.pkl"):
    df_full = pd.DataFrame()
    df_full.to_pickle('gesture_data.pkl')
else:
    df_full = pd.read_pickle('gesture_data.pkl')




while True:
    outputs = {
        'ACCxs': [[]],
        'ACCys': [[]],
        'ACCzs': [[]],
        'GYRxs' : [[]],
        'GYRys' : [[]],
        'GYRzs' : [[]],
        'MAGxs' : [[]],
        'MAGys' : [[]],
        'MAGzs' : [[]],
        'times': [[]],
        'pitchs' : [[]],
        'rolls' : [[]],
        'AccXangles': [[]],       
        'AccYangles': [[]],
        'gyroXangles': [[]],
        'gyroYangles': [[]],
        'CFangleXs': [[]],
        'CFangleYs': [[]],
        'headings': [[]],
        'tiltCompensatedHeadings': [[]],
        'kalmanXs': [[]],
        'kalmanYs': [[]],
        'pitchs': [[]],
        'rolls': [[]],
        'sr': [0],
        'gesture_num': [gesture_num],
    }
    while True:
        if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
            line = input()
            a0 = datetime.datetime.now()
            break

    while True:
        #Read the accelerometer,gyroscope and magnetometer values
        ACCx = IMU.readACCx()
        ACCy = IMU.readACCy()
        ACCz = IMU.readACCz()
        GYRx = IMU.readGYRx()
        GYRy = IMU.readGYRy()
        GYRz = IMU.readGYRz()
        MAGx = IMU.readMAGx()
        MAGy = IMU.readMAGy()
        MAGz = IMU.readMAGz()
        
        outputs['ACCxs'][0].append(ACCx)
        outputs['ACCys'][0].append(ACCy)
        outputs['ACCzs'][0].append(ACCz)
        outputs['GYRxs'][0].append(GYRx)
        outputs['GYRys'][0].append(GYRy)
        outputs['GYRzs'][0].append(GYRz)

        #Apply compass calibration    
        MAGx -= (magXmin + magXmax) /2 
        MAGy -= (magYmin + magYmax) /2 
        MAGz -= (magZmin + magZmax) /2 

        outputs['MAGxs'][0].append(MAGx)
        outputs['MAGys'][0].append(MAGy)
        outputs['MAGzs'][0].append(MAGz)        
        ##Calculate loop Period(LP). How long between Gyro Reads
        b = datetime.datetime.now() - a
        a = datetime.datetime.now()
        LP = b.microseconds/(1000000*1.0)
        print("Loop Time %5.2f " % ( LP ), end=' ')
        m_time = (a-a0).seconds+((a-a0).microseconds)/(1000000*1.0)
        outputs['times'][0].append(m_time)

        #Convert Gyro raw to degrees per second
        rate_gyr_x =  GYRx * G_GAIN
        rate_gyr_y =  GYRy * G_GAIN
        rate_gyr_z =  GYRz * G_GAIN


        #Calculate the angles from the gyro. 
        gyroXangle+=rate_gyr_x*LP
        gyroYangle+=rate_gyr_y*LP
        gyroZangle+=rate_gyr_z*LP

        #Convert Accelerometer values to degrees

        if not IMU_UPSIDE_DOWN:
            # If the IMU is up the correct way (Skull logo facing down), use these calculations
            AccXangle =  (math.atan2(ACCy,ACCz)*RAD_TO_DEG)
            AccYangle =  (math.atan2(ACCz,ACCx)+M_PI)*RAD_TO_DEG
        else:
            #Us these four lines when the IMU is upside down. Skull logo is facing up
            AccXangle =  (math.atan2(-ACCy,-ACCz)*RAD_TO_DEG)
            AccYangle =  (math.atan2(-ACCz,-ACCx)+M_PI)*RAD_TO_DEG



        #Change the rotation value of the accelerometer to -/+ 180 and
        #move the Y axis '0' point to up.  This makes it easier to read.
        if AccYangle > 90:
            AccYangle -= 270.0
        else:
            AccYangle += 90.0



        #Complementary filter used to combine the accelerometer and gyro values.
        CFangleX=AA*(CFangleX+rate_gyr_x*LP) +(1 - AA) * AccXangle
        CFangleY=AA*(CFangleY+rate_gyr_y*LP) +(1 - AA) * AccYangle

        #Kalman filter used to combine the accelerometer and gyro values.
        kalmanY = kalmanFilterY(AccYangle, rate_gyr_y,LP)
        kalmanX = kalmanFilterX(AccXangle, rate_gyr_x,LP)

        if IMU_UPSIDE_DOWN:
            MAGy = -MAGy      #If IMU is upside down, this is needed to get correct heading.
        #Calculate heading
        heading = 180 * math.atan2(MAGy,MAGx)/M_PI

        #Only have our heading between 0 and 360
        if heading < 0:
            heading += 360



        ####################################################################
        ###################Tilt compensated heading#########################
        ####################################################################
        #Normalize accelerometer raw values.
        if not IMU_UPSIDE_DOWN:        
            #Use these two lines when the IMU is up the right way. Skull logo is facing down
            accXnorm = ACCx/math.sqrt(ACCx * ACCx + ACCy * ACCy + ACCz * ACCz)
            accYnorm = ACCy/math.sqrt(ACCx * ACCx + ACCy * ACCy + ACCz * ACCz)
        else:
            #Us these four lines when the IMU is upside down. Skull logo is facing up
            accXnorm = -ACCx/math.sqrt(ACCx * ACCx + ACCy * ACCy + ACCz * ACCz)
            accYnorm = ACCy/math.sqrt(ACCx * ACCx + ACCy * ACCy + ACCz * ACCz)

        #Calculate pitch and roll

        pitch = math.asin(accXnorm)
        roll = -math.asin(accYnorm/math.cos(pitch))


        #Calculate the new tilt compensated values
        magXcomp = MAGx*math.cos(pitch)+MAGz*math.sin(pitch)
     
        #The compass and accelerometer are orientated differently on the LSM9DS0 and LSM9DS1 and the Z axis on the compass
        #is also reversed. This needs to be taken into consideration when performing the calculations
        if(IMU.LSM9DS0):
            magYcomp = MAGx*math.sin(roll)*math.sin(pitch)+MAGy*math.cos(roll)-MAGz*math.sin(roll)*math.cos(pitch)   #LSM9DS0
        else:
            magYcomp = MAGx*math.sin(roll)*math.sin(pitch)+MAGy*math.cos(roll)+MAGz*math.sin(roll)*math.cos(pitch)   #LSM9DS1




        #Calculate tilt compensated heading
        tiltCompensatedHeading = 180 * math.atan2(magYcomp,magXcomp)/M_PI

        if tiltCompensatedHeading < 0:
                    tiltCompensatedHeading += 360

        ############################ END ##################################


        if 1:           #Change to '0' to stop showing the angles from the accelerometer
            print(("# ACCX Angle %5.2f ACCY Angle %5.2f #  " % (AccXangle, AccYangle)), end=' ')

        if 1:           #Change to '0' to stop  showing the angles from the gyro
            print(("\t# GRYX Angle %5.2f  GYRY Angle %5.2f  GYRZ Angle %5.2f # " % (gyroXangle,gyroYangle,gyroZangle)), end=' ')

        if 1:           #Change to '0' to stop  showing the angles from the complementary filter
            print(("\t# CFangleX Angle %5.2f   CFangleY Angle %5.2f #" % (CFangleX,CFangleY)), end=' ')
            
        if 1:           #Change to '0' to stop  showing the heading
            print(("\t# HEADING %5.2f  tiltCompensatedHeading %5.2f #" % (heading,tiltCompensatedHeading)), end=' ')
            
        if 1:           #Change to '0' to stop  showing the angles from the Kalman filter
            print(("# kalmanX %5.2f   kalmanY %5.2f #" % (kalmanX,kalmanY)), end=' ')


        outputs['AccXangles'][0].append(AccXangle)       
        outputs['AccYangles'][0].append(AccYangle)
        outputs['gyroXangles'][0].append(gyroXangle)
        outputs['gyroYangles'][0].append(gyroYangle)
        outputs['CFangleXs'][0].append(CFangleX)
        outputs['CFangleYs'][0].append(CFangleY)
        outputs['headings'][0].append(heading)
        outputs['tiltCompensatedHeadings'][0].append(tiltCompensatedHeading)
        outputs['kalmanXs'][0].append(kalmanX)
        outputs['kalmanYs'][0].append(kalmanY)
        outputs['pitchs'][0].append(pitch)
        outputs['rolls'][0].append(roll)
        #print a new line
        print("")  


        #slow program down a bit, makes the output more readable
        time.sleep(0.03)
        if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
            line = input()
            break
    # print(ACCxs)
    # print(GYRxs)
    # print(times)
    

    time_arr = np.asarray(outputs['times'])
    time_diffs = np.diff(time_arr)
    mean_period = np.mean(time_diffs)
    sr = 1/mean_period
    outputs['sr'] = sr
    #df = pd.DataFrame.from_dict(outputs)
    outputs_mean = {k:[np.mean(np.array(v))] for k,v in list(outputs.items())}
    #print(outputs_mean)
    #df2 = pd.DataFrame.from_dict(outputs_mean)
   # print(df2)
   # df = pd.concat([df,df2])
   # df.append(outputs_mean,ignore_index=True)
    #print(df)
    df_full2 = pd.DataFrame.from_dict(outputs)
    df_full = pd.concat([df_full,df_full2])
    print("Saving")
    df.to_csv('gesture_data2.csv')
    df_full.to_pickle('gesture_data.pkl')
    print("Done Saving")
    print(df_full2)
    print(df_full2.shape)
  #  print(df_full)
    print(df_full.shape)