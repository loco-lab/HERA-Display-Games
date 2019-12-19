#!/usr/bin/env python3
#Author: Mickey Horn
#custom code testing for HERA LED model

import time
from neopixel import *
import argparse
import pandas as pd
import numpy as np
from datetime import datetime
import math
import random
import matplotlib.pyplot as plt
import matplotlib.colors as clr

parser = argparse.ArgumentParser()
parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
args = parser.parse_args()

# LED strip configuration:
LED_COUNT      = 320     # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 55     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

# antenna number : LED number
scheme = {
    0:10, 1:9, 2:8, 3:7, 4:6, 5:5, 6:4, 7:3, 8:2, 9:1, 10:0,
    11:11, 12:12, 13:13, 14:14, 15:15, 16:16, 17:17, 18:18, 19:19, 20:20, 21:21,
    22:119,
    23:32, 24:31, 25:30, 26:29, 27:28, 28:27, 29:26, 30:25, 31:24, 32:23, 33:22,
    34:118, 35:120,
    36:33, 37:34, 38:35, 39:36, 40:37, 41:38, 42:39, 43:40, 44:41, 45:42, 46:43,
    47:117, 48:121, 49:139,
    50:54, 51:53, 52:52, 53:51, 54:50, 55:49, 56:48, 57:47, 58:46, 59:45, 60:44,
    61:116, 62:122, 63:138, 64:140,
    65:55, 66:56, 67:57, 68:58, 69:59, 70:60, 71:61, 72:62, 73:63, 74:64, 75:65,
    76:115, 77:123, 78:137, 79:141, 80:159,
    81:76, 82:75, 83:74, 84:73, 85:72, 86:71, 87:70, 88:69, 89:68, 90:67, 91:66,
    92:114, 93:124, 94:136, 95:142, 96:158, 97:160,
    98:77, 99:78, 100:79, 101:80, 102:81, 103:82, 104:83, 105:84, 106:85, 107:86, 108:87,
    109:113, 110:125, 111:135, 112:143, 113:157, 114:161, 115:179,
    116:98, 117:97, 118:96, 119:95, 120:94, 121:93, 122:92, 123:91, 124:90, 125:89, 126:88,
    127:112, 128:126, 129:134, 130:144, 131:156, 132:162, 133:178, 134:180,
    135:99, 136:100, 137:101, 138:102, 139:103, 140:104, 141:105, 142:106, 143:107, 144:108, 145:109,
    146:111, 147:127, 148:133, 149:145, 150:155, 151:163, 152:177, 153:181, 154:199,
    155:309, 156:310, 157:311, 158:312, 159:313, 160:314, 161:315, 162:316, 163:317, 164:318, 165:319,
    166:110, 167:128, 168:132, 169:146, 170:154, 171:164, 172:176, 173:182, 174:198, 175:200,
    176:308, 177:307, 178:306, 179:305, 180:304, 181:303, 182:302, 183:301, 184:300, 185:299, 186:298,
    187:129, 188:131, 189:147, 190:153, 191:165, 192:175, 193:183, 194:197, 195:201,
    196:287, 197:288, 198:289, 199:290, 200:291, 201:292, 202:293, 203:294, 204:295, 205:296, 206:297,
    207:130, 208:148, 209:152, 210:166, 211:174, 212:184, 213:196, 214:202,
    215:286, 216:285, 217:284, 218:283, 219:282, 220:281, 221:280, 222:279, 223:278, 224:277, 225:276,
    226:149, 227:151, 228:167, 229:173, 230:185, 231:195, 232:203,
    233:265, 234:266, 235:267, 236:268, 237:269, 238:270, 239:271, 240:272, 241:273, 242:274, 243:275,
    244:150, 245:168, 246:172, 247:186, 248:194, 249:204,
    250:264, 251:263, 252:262, 253:261, 254:260, 255:259, 256:258, 257:257, 258:256, 259:255, 260:254,
    261:169, 262:171, 263:187, 264:193, 265:205,
    266:243, 267:244, 268:245, 269:246, 270:247, 271:248, 272:249, 273:250, 274:251, 275:252, 276:253,
    277:170, 278:188, 279:192, 280:206,
    281:242, 282:241, 283:240, 284:239, 285:238, 286:237, 287:236, 288:235, 289:234, 290:233, 291:232,
    292:189, 293:191, 294:207,
    295:221, 296:222, 297:223, 298:224, 299:225, 300:226, 301:227, 302:228, 303:229, 304:230, 305:231,
    306:190, 307:208,
    308:220, 309:219, 310:218, 311:217, 312:216, 313:215, 314:214, 315:213, 316:212, 317:211, 318:210,
    319:209
}

# by LED number
# lights divided into the 3 diamond pieces
bot_third = list(range(0,110))
top_third = list(range(210,320))
side_third = list(range(110,210))
thirds = [bot_third,top_third,side_third]

# lights divided into 6 pieces
bot_r_sixth = [0,1,2,3,4,5,6,7,8,9,10,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,61,62,63,64,65,66,67,68,69,85,86,87,88,89,109]
bot_l_sixth = [11,31,32,33,34,35,51,52,53,54,55,56,57,58,59,60,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,90,91,92,93,94,95,96,97,98,99,100,101,102,103,104,105,106,107,108]
top_l_sixth = [220,221,222,240,241,242,243,244,245,246,260,261,262,263,264,265,266,267,268,269,270,271,279,280,281,282,283,284,285,286,287,288,289,290,291,292,293,294,295,299,300,301,302,303,304,305,306,307,308,309,310,311,312,313,314,315,316,317,318,319]
top_r_sixth = [210,211,212,213,214,215,216,217,218,219,223,224,225,226,227,228,229,230,231,232,233,234,235,236,237,238,239,247,248,249,250,251,252,253,254,255,256,257,258,259,272,273,274,275,276,277,278,296,297,298]
side_t_sixth = [209,208,190,207,191,189,206,192,188,170,205,193,187,171,169,204,194,186,172,168,150,203,195,185,173,167,151,149,202,196,184,174,166,152,148,130,201,197,183,175,165,153,147,131,129,200,198,182,176,164]
side_b_sixth = [119,118,120,117,121,139,116,122,138,140,115,123,137,141,159,114,124,136,142,158,160,113,125,135,143,157,161,179,112,126,134,144,156,162,178,180,111,127,133,145,155,163,177,181,199,110,128,132,146,154]
sixths = [bot_r_sixth,bot_l_sixth,top_l_sixth,top_r_sixth,side_t_sixth,side_b_sixth]

# lights in concentric rings
ring1 = [109,110,319]
ring2 = [108,89,88,111,128,129,298,299,318]
ring3 = [107,90,85,86,87,112,127,132,131,130,297,296,295,300,317]
ring4 = [106,91,84,69,68,67,66,113,126,133,146,147,148,149,276,277,278,279,294,301,316]
ring5 = [105,92,83,70,61,62,63,64,65,114,125,134,145,154,153,152,151,150,275,274,273,272,271,280,293,302,315]
ring6 = [104,93,82,71,60,49,48,47,46,45,44,115,124,135,144,155,164,165,166,167,168,169,254,255,256,257,258,259,270,281,292,303,314]
ring7 = [103,94,81,72,59,50,37,38,39,40,41,42,43,116,123,136,143,156,163,176,175,174,173,172,171,170,253,252,251,250,249,248,247,260,269,282,291,304,313]
ring8 = [102,95,80,73,58,51,36,29,28,27,26,25,24,23,22,117,122,137,142,157,162,177,182,183,184,185,186,187,188,189,232,233,234,235,236,237,238,239,246,261,268,283,290,305,312]
ring9 = [101,96,79,74,57,52,35,30,13,14,15,16,17,18,19,20,21,118,121,138,141,158,161,178,181,198,197,196,195,194,193,192,191,190,231,230,229,228,227,226,225,224,223,240,245,262,267,284,289,306,311]
ring10 = [100,97,78,75,56,53,34,31,12,9,8,7,6,5,4,3,2,1,0,119,120,139,140,159,160,179,180,199,200,201,202,203,204,205,206,207,208,209,210,211,212,213,214,215,216,217,218,219,222,241,244,263,266,285,288,307,310]
ring11 = [99,98,77,76,55,54,33,32,11,10,220,221,242,243,264,265,286,287,308,309]
rings = [ring1,ring2,ring3,ring4,ring5,ring6,ring7,ring8,ring9,ring10,ring11]

# pumpkin for Halloween
pumpkin_face = [301,302,303,292,293,315,316,317,281, 149,151,130,148,152,131,147,129,150, 157,143,162,96,80,79,74,73,72,69,68,57,58,59,61,62,63,65,52,51,35,36,37,40,41,42,43,44,45,46,47,48,49,50,29,25,24,23,22,115,116,117,122,123,137,142,136,124,114]
pumpkin_stem = [213,214,215,227,228]

# clock hands
hourhand01 = [319,298,297,276,275,254,253,232,231]
hourhand02 = [110,131,152,173,194]
hourhand03 = [110,128,132,146,154,164,176,182,198]
hourhand04 = [110,127,134,143,158]
hourhand05 = [110,111,112,113,114,115,116,117,118]
hourhand06 = [109,86,63,40,17]
hourhand07 = [109,89,85,69,61,49,37,29,13]
hourhand08 = [109,90,83,72,57]
hourhand09 = [109,108,107,106,105,104,103,102,101,100]
hourhand10 = [319,300,293,282,267]
hourhand11 = [319,299,295,279,271,259,247,239,223]
hourhand12 = [319,296,273,250,227]
hourhands = [hourhand01,hourhand02,hourhand03,hourhand04,hourhand05,hourhand06,hourhand07,hourhand08,hourhand09,hourhand10,hourhand11,hourhand12]

sec_ring = [214,213,212,211,210,209,208,207,206,205,204,203,202,201,200,199,180,179,160,159,140,139,120,119,0,1,2,3,4,5,6,7,8,9,10,11,32,33,54,55,76,77,98,99,309,308,287,286,265,264,243,242,221,220,219,218,217,216,215]

hours_dict = { # correlates the hour with the hour hand position
    '00':hourhand12, '12':hourhand12,
    '01':hourhand01, '13':hourhand01,
    '02':hourhand02, '14':hourhand02,
    '03':hourhand03, '15':hourhand03,
    '04':hourhand04, '16':hourhand04,
    '05':hourhand05, '17':hourhand05,
    '06':hourhand06, '18':hourhand06,
    '07':hourhand07, '19':hourhand07,
    '08':hourhand08, '20':hourhand08,
    '09':hourhand09, '21':hourhand09,
    '10':hourhand10, '22':hourhand10,
    '11':hourhand11, '23':hourhand11
}

mins_dict = { # correlates the minute with the hour/minute hand position
    '00':hourhand12, '01':hourhand12, '02':hourhand12, '03':hourhand12, '04':hourhand12,
    '05':hourhand01, '06':hourhand01, '07':hourhand01, '08':hourhand01, '09':hourhand01,
    '10':hourhand02, '11':hourhand02, '12':hourhand02, '13':hourhand02, '14':hourhand02,
    '15':hourhand03, '16':hourhand03, '17':hourhand03, '18':hourhand03, '19':hourhand03,
    '20':hourhand04, '21':hourhand04, '22':hourhand04, '23':hourhand04, '24':hourhand04,
    '25':hourhand05, '26':hourhand05, '27':hourhand05, '28':hourhand05, '29':hourhand05,
    '30':hourhand06, '31':hourhand06, '32':hourhand06, '33':hourhand06, '34':hourhand06,
    '35':hourhand07, '36':hourhand07, '37':hourhand07, '38':hourhand07, '39':hourhand07,
    '40':hourhand08, '41':hourhand08, '42':hourhand08, '43':hourhand08, '44':hourhand08,
    '45':hourhand09, '46':hourhand09, '47':hourhand09, '48':hourhand09, '49':hourhand09,
    '50':hourhand10, '51':hourhand10, '52':hourhand10, '53':hourhand10, '54':hourhand10,
    '55':hourhand11, '56':hourhand11, '57':hourhand11, '58':hourhand11, '59':hourhand11
}

secs_dict = { # correlates the second with a point on the edge
    '00':214, '01':213, '02':212, '03':211, '04':210,
    '05':209, '06':208, '07':207, '08':206, '09':205,
    '10':204, '11':203, '12':202, '13':201, '14':200,
    '15':199, '16':180, '17':179, '18':160, '19':159,
    '20':140, '21':139, '22':120, '23':119, '24':0,
    '25':1, '26':2, '27':3, '28':4, '29':5,
    '30':6, '31':7, '32':8, '33':9, '34':10,
    '35':11, '36':32, '37':33, '38':54, '39':55,
    '40':76, '41':77, '42':98, '43':99, '44':309,
    '45':308, '46':287, '47':286, '48':265, '49':264,
    '50':243, '51':242, '52':221, '53':220, '54':219,
    '55':218, '56':217, '57':216, '58':215, '59':215
}

hera_h = [288,311,101,78,312,313,290,103,80]
hera_e = [293,294,295,316,317,106,83,84,85]
hera_r = [149,131,127,113,151,152,153,146,133,134,135]
hera_a = [195,184,175,164,156,196,197,198,180,176,182]
hera_text = [hera_h,hera_e,hera_r,hera_a]

# colors
red = [255,0,0]
orange = [255,127,0]
yellow = [255,255,0]
lime = [127,255,0]
green = [0,255,0]
turq = [0,255,127]
cyan = [0,255,255]
teal = [0,127,255]
blue = [0,0,255]
indigo = [127,0,255]
purple = [255,0,255]
pink = [255,0,127]
white = [255,255,255]
off = [0,0,0]
rgbcolors = [red,green,blue]
rainbowcolors = [red,orange,yellow,green,blue,purple]
ringcolors = [red,orange,yellow,lime,green,turq,cyan,blue,indigo,purple,pink]

def clear():
# Turns off all LEDs.
    for i in range(LED_COUNT): strip.setPixelColorRGB(i,0,0,0)
    strip.show()

def pulse(lights,r,g,b,scale):
# Makes a list of lights "breathe".
    for i in list(reversed(np.arange(scale))) + list(np.arange(scale)):
        for j in lights: strip.setPixelColorRGB(j,int(r*(i/float(scale))),int(g*(i/float(scale))),int(b*(i/float(scale))))
        strip.show()
    time.sleep(1)

def flash(lights,r,g,b,ontime,offtime):
# Makes a list of lights turn off and on rapidly.
    for i in lights: strip.setPixelColorRGB(i,r,g,b)
    strip.show()
    time.sleep(ontime)
    for i in lights: strip.setPixelColorRGB(i,0,0,0)
    strip.show()
    time.sleep(offtime)

def next_shape(shapes,colors,direction):
# Takes in a list of "shapes" (lists of LED indices) and a list of colors, and rotates the colors to the next shape once.
# The direction should be 1 or -1, and simply controls which way the colors progress.
# The list of shapes and the list of colors must be the same length.
    for i in range(LED_COUNT):
        for j,k in enumerate(shapes):
            if i in k: strip.setPixelColorRGB(i,colors[j][0],colors[j][1],colors[j][2])
    strip.show()
    colors = colors[direction::] + colors[:direction:]
    return colors

def moving_shapes(shapes,colors,direction,waittime):
# Takes in a list of shapes and a list of colors and cycles the colors through the shapes repeatedly.
# See next_shape() for more detail.
    print('Displaying Moving Shapes')
    for i in range(len(colors)):
        print('Position '+str(i+1))
        colors = next_shape(shapes,colors,direction)
        time.sleep(waittime)

def pumpkin(waittime):
# Displays a Jack-O-Lantern face, spooky!
    print('Displaying Pumpkin')
    for i in range(LED_COUNT):
        if i in pumpkin_face: strip.setPixelColorRGB(i,25,25,25)
        elif i in pumpkin_stem: strip.setPixelColorRGB(i,0,255,0)
        else: strip.setPixelColorRGB(i,255,65,0)
    strip.show()
    time.sleep(waittime)

def random_colors():
# Sets each antenna to a random color.
    for i in range(LED_COUNT): strip.setPixelColorRGB(i,random.randrange(0,255,1),random.randrange(0,255,1),random.randrange(0,255,1))
    strip.show()
    time.sleep(2)

def ant_sequence():
# Loops through all lights in antenna order and sets them to R>G>B.
    print('Displaying Antenna Sequences')
    clear()
    print('Loop 1')
    for i in range(LED_COUNT):
        strip.setPixelColorRGB(scheme[i],255,0,0)
        strip.show()
    print('Loop 2')
    for i in range(LED_COUNT):
        strip.setPixelColorRGB(scheme[i],0,255,0)
        strip.show()
    print('Loop 3')
    for i in range(LED_COUNT):
        strip.setPixelColorRGB(scheme[i],0,0,255)
        strip.show()

def ant_status_ew(pulses):
# Reads the live antenna status csv from HERAnow and outputs appropriate colors for each EW antenna.
    print('Displaying Live EW Antenna Status')
    red_lights = []
    status = np.array(pd.read_csv('http://heranow.reionization.org/ant_stats.csv', header=0, names=['Ant','Auto','PAM','ADC','ADC RMS','FEM T','FEM P','EQ']))
    for i in status:
        antname = i[0]
        antnum = int(antname[2:len(antname)-1])
        antdir = antname[len(antname)-1:len(antname)]
        if antdir=='e' and -1<antnum<320:
            if pd.isnull(i[1])==True: strip.setPixelColorRGB(scheme[antnum],255,127,0) # weird nan, orange
            elif i[1]=='CONST': strip.setPixelColorRGB(scheme[antnum],80,0,255) # offline, blue
            elif i[1]=='OFF' : strip.setPixelColorRGB(scheme[antnum],0,0,0) # not built, off
            else:
                if int(float(i[1]))>=15: strip.setPixelColorRGB(scheme[antnum],0,255,0) # good, green
                elif int(float(i[1]))<15:
                    strip.setPixelColorRGB(scheme[antnum],255,50,0) # bad, red
                    red_lights.append(scheme[antnum])
                else: strip.setPixelColorRGB(scheme[antnum],0,0,0) # not in csv, off
    print('Initial Color')
    strip.show()
    counter = 0
    #while counter<pulses:
    #    print('Pulse '+str(counter+1))
    #    pulse(red_lights,125,25,0,50)
    #    counter += 1
    time.sleep(5)

def ant_status_ns(pulses):
# Reads the live antenna status csv from HERAnow and outputs appropriate colors for each NS antenna.
    print('Displaying Live NS Antenna Status')
    red_lights = []
    status = np.array(pd.read_csv('http://heranow.reionization.org/ant_stats.csv', header=0, names=['Ant','Auto','PAM','ADC','ADC RMS','FEM T','FEM P','EQ']))
    for i in status:
        antname = i[0]
        antnum = int(antname[2:len(antname)-1])
        antdir = antname[len(antname)-1:len(antname)]
        if antdir=='n' and -1<antnum<320:
            if pd.isnull(i[1])==True: strip.setPixelColorRGB(scheme[antnum],255,127,0) # weird nan, orange
            elif i[1]=='CONST': strip.setPixelColorRGB(scheme[antnum],80,0,255) # offline, blue
            elif i[1]=='OFF' : strip.setPixelColorRGB(scheme[antnum],0,0,0) # not built, off
            else:
                if int(float(i[1]))>=15: strip.setPixelColorRGB(scheme[antnum],0,255,0) # good, green
                elif int(float(i[1]))<15:
                    strip.setPixelColorRGB(scheme[antnum],255,50,0) # bad, red
                    red_lights.append(scheme[antnum])
                else: strip.setPixelColorRGB(scheme[antnum],0,0,0) # not in csv, off
    print('Initial Color')
    strip.show()
    counter = 0
    #while counter<pulses:
    #    print('Pulse '+str(counter+1))
    #    pulse(red_lights,125,25,0,50)
    #    counter += 1
    time.sleep(5)

def ant_status():
# Reads the live antenna status csv from HERAnow and outputs appropriate colors for each antenna. The worst dipole is always shown.
    print('Displaying Live Antenna Status')
    status = np.array(pd.read_csv('http://heranow.reionization.org/ant_stats.csv', header=0, names=['Ant','Auto','PAM','ADC','ADC RMS','FEM T','FEM P','EQ']))
    e_status = np.empty((0,8))
    n_status = np.empty((0,8))
    for i in status:
        antname = i[0]
        antnum = int(antname[2:len(antname)-1])
        antdir = antname[len(antname)-1:len(antname)]
        if antdir=='e' and -1<antnum<320: e_status = np.append(e_status,[i],axis=0)
        elif antdir=='n' and -1<antnum<320: n_status = np.append(n_status,[i],axis=0)
    for j in range(320):
        if pd.isnull(e_status[j][1])==True or pd.isnull(n_status[j][1])==True: strip.setPixelColorRGB(scheme[j],255,127,0) # weird nan, orange
        elif e_status[j][1]=='CONST' or n_status[j][1]=='CONST': strip.setPixelColorRGB(scheme[j],80,0,255) # offline, blue
        elif e_status[j][1]=='OFF' or n_status[j][1]=='OFF': strip.setPixelColorRGB(scheme[j],0,0,0) # not built, off
        else:
            if int(float(e_status[j][1]))>=15 and int(float(n_status[j][1]))>=15: strip.setPixelColorRGB(scheme[j],0,255,0) # good, green
            elif int(float(e_status[j][1]))<15 or int(float(n_status[j][1]))<15: strip.setPixelColorRGB(scheme[j],255,50,0) # bad, red
            else: strip.setPixelColorRGB(scheme[j],0,0,0) # not in csv, off
    strip.show()
    time.sleep(120)

def colorscale(mag,cmin,cmax):
# Returns a tuple of floats between 0 and 255 for RGB, scaling from green to yellow.
    try: x = float(mag-cmin)/(cmax-cmin) # scales from 0 to 1
    except ZeroDivisionError: x=0.5 # cmax==cmin
    r = int(x*255)
    g = 255
    b = int(75-(x*75))
    return r,g,b

def ant_status_scaling():
# Reads the live antenna status csv from HERAnow and outputs appropriate colors for each antenna. The worst dipole is always shown.
    print('Displaying Live Antenna Status')
    status = np.array(pd.read_csv('http://heranow.reionization.org/ant_stats.csv', header=0, names=['Ant','Auto','PAM','ADC','ADC RMS','FEM T','FEM P','EQ']))
    e_status = np.empty((0,8))
    n_status = np.empty((0,8))
    for i in status:
        antname = i[0]
        antnum = int(antname[2:len(antname)-1])
        antdir = antname[len(antname)-1:len(antname)]
        if antdir=='e' and -1<antnum<320: e_status = np.append(e_status,[i],axis=0)
        elif antdir=='n' and -1<antnum<320: n_status = np.append(n_status,[i],axis=0)
    for j in range(320):
        e_autocorr = e_status[j][1]
        n_autocorr = n_status[j][1]
        if pd.isnull(e_autocorr)==True or pd.isnull(n_autocorr)==True: strip.setPixelColorRGB(scheme[j],255,127,0) # weird nan, orange
        elif e_autocorr=='CONST' or n_autocorr=='CONST': strip.setPixelColorRGB(scheme[j],80,0,255) # offline, blue
        elif e_autocorr=='OFF' or n_autocorr=='OFF': strip.setPixelColorRGB(scheme[j],0,0,0) # not built, off
        else:
            if int(float(e_autocorr))>=10 and int(float(n_autocorr))>=10:
                avg_autocorr = (float(e_autocorr)+float(n_autocorr))/2
                r,g,b = colorscale(avg_autocorr,10,23)
                strip.setPixelColorRGB(scheme[j],r,g,b) #good, scaled green to yellow
            elif int(float(e_autocorr))<10 or int(float(n_autocorr))<10: strip.setPixelColorRGB(scheme[j],255,50,0) # bad, red
            else: strip.setPixelColorRGB(scheme[j],0,0,0) # not in csv, off
    strip.show()
    time.sleep(120)

def adopt_antenna():
# A fun outreach demo, let kids choose and color an antenna to make a collage by the end!
    print(' ')
    print('It is time to adopt your very own HERA antenna!')
    antenna = int(input('Which antenna would you like? Pick any number between 0 and 319: '))
    while antenna<0 or antenna>319: antenna = int(input('Oops! Which antenna would you like? Pick any number between 0 and 319: '))
    red = int(input('How much red do you want? Enter a number between 0 (no red) and 255 (max red): '))
    while red<0 or red>255: red = int(input('Oops! How much red do you want? Enter a number between 0 (no red) and 255 (max red): '))
    green = int(input('How much green do you want? Enter a number between 0 and 255: '))
    while green<0 or green>255: green = int(input('Oops! How much green do you want? Enter a number between 0 and 255: '))
    blue = int(input('How much blue do you want? Enter a number between 0 and 255: '))
    while blue<0 or blue>255: blue = int(input('Oops! How much blue do you want? Enter a number between 0 and 255: '))
    strip.setPixelColorRGB(scheme[antenna],red,green,blue)
    strip.show()
    print('Your antenna is on! Can you find it?')
    print('-------------------------')
    time.sleep(10)

def clock():
# A real time analog clock, with 3 hands!
    print('Displaying Clock')
    nowtime = str(datetime.now().time()) #format is hh:mm:ss.ssssss
    hours = nowtime[0:2]
    minutes = nowtime[3:5]
    seconds = nowtime[6:8]
    print('It is currently '+hours+':'+minutes+':'+seconds)
    clear()
    minutehand = mins_dict[minutes]
    for i in minutehand: strip.setPixelColorRGB(i,0,255,0)
    hourhand = hours_dict[hours][:int(round(len(hours_dict[hours])/2)+1)]
    for i in hourhand: strip.setPixelColorRGB(i,0,0,255)
    for i in sec_ring[:len(sec_ring)-(59-int(seconds))]: strip.setPixelColorRGB(i,255,0,0) # enable this line for cumulative seconds ring
    #strip.setPixelColorRGB(secs_dict[seconds],255,0,0) # enable this line for 1 second dot at a time
    strip.show()
    time.sleep(.97)

def hera():
# Displays the text "HERA".
    print('Displaying HERA')
    for i in range(LED_COUNT):
        if i in hera_h: strip.setPixelColorRGB(i,0,0,255)
        elif i in hera_e: strip.setPixelColorRGB(i,255,0,0)
        elif i in hera_r: strip.setPixelColorRGB(i,0,255,0)
        elif i in hera_a: strip.setPixelColorRGB(i,255,255,0)
        else: strip.setPixelColorRGB(i,0,0,0)
    strip.show()
    time.sleep(10)

def image_mapper(file):
    image_map = np.array(pd.read_csv(file, header=0, names=['r','g','b']))
    for i in range(len(image_map)): strip.setPixelColorRGB(i,int(image_map[i][0]),int(image_map[i][1]),int(image_map[i][2]))
    strip.show()
    time.sleep(60)


# main code
print('Starting')
strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
strip.begin()

try:
    while True:
        #moving_shapes(sixths,rainbowcolors,-1,.1)
        #moving_shapes(sixths,rainbowcolors,-1,.1)

        #moving_shapes(rings,ringcolors,1,.1)
        #moving_shapes(rings,ringcolors,-1,.1)

        #pumpkin(30)

        #random_colors()

        #ant_sequence()

        #ant_status_ew(3)
        #ant_status_ns(3)
        ant_status_scaling()

        #adopt_antenna()

        #clock()
        #time.sleep(5)

        #hera()

        #image_mapper('treergb')

except KeyboardInterrupt:
    if args.clear:
        print('Clear')
        clear()
