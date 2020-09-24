# This module is derived from https://github.com/LingDong-/linedraw, by
# Lingdong Huang.

from random import *
import math
import argparse
import json
import time

from PIL import Image, ImageDraw, ImageOps

# file settings
export_path = "images/out.svg"
svg_folder = "images/"

#Image Sizes
paper = {'A6':[105,148],'A5':[148,210], 'A4':[210,297], 'A3': [297,420], 'A2':[420,594],'A1':[594,841],'A0':[841,1190],'2A0':[1189,1682],'4A0':[1682,2378]}

import numpy as np
import cv2

# -------------- output functions --------------


def makesvg(lines, commentlines=""):
    print("generating svg file...")
    width = math.ceil(max([max([p[0]*0.5 for p in l]) for l in lines]))
    height = math.ceil(max([max([p[1]*0.5 for p in l]) for l in lines]))

    out = '<svg xmlns="http://www.w3.org/2000/svg" height="%spx" width="%spx" version="1.1">' % (height, width)
    out += '<annotation encoding="UTF-8">'
    out += commentlines
    out += '</annotation>'
    for l in lines:
        l = ",".join([str(p[0]*0.5)+","+str(p[1]*0.5) for p in l])
        out += '\n<polyline points="'+l+'" stroke="black" stroke-width="1" fill="none" />'
    out += '\n</svg>'
    return out

# -------------- conversion control --------------

def vectorise(
    image_filename, resolution='A0',
    draw_contours=False, repeat_contours=1,
    draw_hatch=False, repeat_hatch=1, 
    cannymin=50, cannymax=200, blur=0,setgrey=True,
    ):

    image = None
    possible = [
        image_filename,
        "images/"+image_filename,
        "images/"+image_filename+".jpg",
        "images/"+image_filename+".png",
        "images/"+image_filename+".tif"
    ]

    for p in possible:
        try:
            image = Image.open(p)
            break
        except:
            pass

    image = crop_and_resize(image,resolution)
    
    w,h = image.size

    # convert the image to greyscale & Adjust contrast
    if setgrey == True:
        image = image.convert("L")
    image=ImageOps.autocontrast(image)
    image.save(svg_folder + image_filename + "-grey.jpg")
    
    lines = []

    if draw_contours and repeat_contours:
        contours = sortlines(getcontours(
            image.resize((int(w/draw_contours), int(h/draw_contours))),
            draw_contours, cannymin, cannymax, blur
        ))
        for r in range(repeat_contours):
            lines += contours

    if draw_hatch and repeat_hatch:
        hatches = sortlines(
            hatch(
                image.resize((int(w/draw_hatch), int(h/draw_hatch))),
                #image,
                draw_hatch,cannymin, cannymax, random=False
        ))
        for r in range(repeat_hatch):
            lines += hatches
            
    cmnt = "\n    image_filename: " + image_filename + ",\n"
    cmnt += "    resolution: " + resolution + ",\n"
    cmnt += "    draw_contours: " + str(draw_contours) + ",\n"
    cmnt += "    repeat_contours: " + str(repeat_contours) + ",\n"
    cmnt += "    draw_hatch: " + str(draw_hatch) + ",\n"
    cmnt += "    repeat_hatch: " + str(repeat_hatch) + ",\n"
    cmnt += "    cannymin: " + str(cannymin) + ",\n"
    cmnt += "    cannymax: " + str(cannymax) + ",\n"
    cmnt += "    blur: " + str(blur) + ",\n"
    cmnt += "    setgrey: " + str(setgrey) + ",\n"
  
    f = open(svg_folder + image_filename + ".svg", 'w')
    f.write(makesvg(lines,cmnt))
    f.close()

    segments = 0
    for line in lines:
        segments = segments + len(line)
    print(len(lines), "strokes,", segments, "points.")
    print("done.")
    return


# -------------- vectorisation options --------------

def getcontours(image, draw_contours=2, cannymin=50, cannymax=200, blur=3):
    print("generating contours...")
    image = find_edges(image, cannymin, cannymax, blur)

    image.save("images/snapshot-lines.jpg")
    
    IM1 = image.copy()
    IM2 = image.rotate(-90,expand=True).transpose(Image.FLIP_LEFT_RIGHT)
    dots1 = getdots(IM1)
    contours1 = connectdots(dots1)
    dots2 = getdots(IM2)
    contours2 = connectdots(dots2)

    for i in range(len(contours2)):
        contours2[i] = [(c[1],c[0]) for c in contours2[i]]
    contours = contours1+contours2

    for i in range(len(contours)):
        for j in range(len(contours)):
            if len(contours[i]) > 0 and len(contours[j])>0:
                if distsum(contours[j][0],contours[i][-1]) < 8:
                    contours[i] = contours[i]+contours[j]
                    contours[j] = []

    for i in range(len(contours)):
        contours[i] = [contours[i][j] for j in range(0,len(contours[i]),8)]


    contours = [c for c in contours if len(c) > 1]

    for i in range(0,len(contours)):
        contours[i] = [(v[0]*draw_contours,v[1]*draw_contours) for v in contours[i]]

    return contours


# improved, faster and easier to understand hatching (ppl)
def hatch(image, draw_hatch=16, cannymin=50, cannymax=200, random=False):

    t0 = time.time()

    print("hatching using hatch()...")
    pixels = image.load()
    w, h = image.size
    lg1 = []
    lg2 = []
    lg3 = []
    lg4 = []
    lg5 = []
    lg6 = []
    
    d2=draw_hatch/2
    #print ("draw_hatch ", draw_hatch)
    #print ("image size w,h",w,h)

    split = int((cannymax-cannymin)/8)
    #print("split",split)
    
    for x0 in range(w):
        x = (x0 * draw_hatch) 
        #print("reading x0,x", x0,x)
        for y0 in range(h):
            # print("    reading y", x0)
            #x = (x0 * draw_hatch) #+ draw_hatch
            y = (y0 * draw_hatch) 
            #if x == 0:
            #    print("reading y0,y", y0,y)
                
            # introduce some randomness or not
            if random:
                r=randint(0,3)-1
            else:
                r=0
          
                       
            # ppl new hatch (6 rather than 3 levels)
            #   132 104 79  56  35  9
            
            if pixels[x0, y0] < 128:
            #if pixels[x0, y0] < cannymax-(split * 2):
                lg1.append([(x,y),(x+draw_hatch,r+y+draw_hatch)]) # right diagonal
 
            if pixels[x0, y0] < 105:
            #if pixels[x0, y0] < cannymax-(split * 3):
                lg2.append([(x+draw_hatch,y+r),(x,y+draw_hatch)]) # left diagonall
                
            if pixels[x0, y0] < 84:
            #if pixels[x0, y0] < cannymax-(split * 4):
                lg3.append([(x-d2,y),(x+d2,r+y+draw_hatch)]) # 2nd right diagonal

            if pixels[x0, y0] < 62:
            #if pixels[x0, y0] < cannymax-(split * 5):
               lg4.append([(x+d2,y+r),(x-d2,y+draw_hatch)]) # 2nd left diagonall
                
            if pixels[x0, y0] <40:     #40
            #if pixels[x0, y0] < cannymax-(split * 6):
                lg5.append([(x,y+d2),(x+draw_hatch,r+y+d2)])  # horizontal lines

            if pixels[x0, y0] < 18:
            #if pixels[x0, y0] < cannymax-(split * 7):
                lg6.append([(x+d2,y),(x+d2,y+draw_hatch)])  # Vertical lines     
                        

    t1 = time.time()

    print("wrangling points...")

    # Make segments into lines
    line_groups = [lg1, lg2, lg3, lg4, lg5, lg6]

    for line_group in line_groups:
        for lines in line_group:
            for lines2 in line_group:

                # do items exist in both?
                if lines and lines2:
                    # if the last point of first is the same as the first point of of the second
                    if lines[-1] == lines2[0]:
                        # then extend the first with all the rest of the points of the second
                        lines.extend(lines2[1:])
                        # and empty the second list
                        lines2.clear()

        # in each line group keep any non-empty lines
        saved_lines = [[line[0], line[-1]] for line in line_group if line]
        line_group.clear()
        line_group.extend(saved_lines)

    lines = [item for group in line_groups for item in group]

    t2 = time.time()

    print("hatching   : ", t1 - t0)
    print("wrangling:   ", t2 - t1)
    print("total:       ", t2 - t0)

    return lines


# -------------- supporting functions for drawing contours --------------
# simplified find edges that works better (ppl)
def find_edges(image, cannymin, cannymax, blur):
    print("finding edges...")

    im = np.array(image)
    if blur > 0:
        im = cv2.GaussianBlur(im,(blur,blur),0)
    im = cv2.Canny(im,cannymin,cannymax)
    image = Image.fromarray(im)

    return ImageOps.invert(image)

def crop_and_resize(image,resolution):

    # Make orientation Portrait
    c_width, c_height = image.size
    #print ("0Wide-", c_width)
    #print ("0High-", c_height)


    if c_width > c_height:
        image = image.rotate(90,expand=True)
        c_width, c_height = image.size
        #print ("rWide-", c_width)
        #print ("rHigh-", c_height)

    t_width = int(paper[resolution][0] * 0.9)
    t_height = int(paper[resolution][1] * 0.9)

    #print ("tWide-", t_width)
    #print ("tHigh-", t_width)

    wr, hr = t_width / c_width, t_height / c_height


    #Image MUST be portrait. scale to fit drawing area
    if t_width/c_width < t_height/t_height:
        ir = float(t_width / c_width)
    else:
        ir = float(t_height /c_height)
        
    target = int(c_width*ir), int(c_height*ir)
 
        
    #print ("Target-",target)
    image_r = image.resize(target, Image.ANTIALIAS)
    
    return image_r


def getdots(IM):
    print("getting contour points1...")
    PX = IM.load()
    dots = []
    w,h = IM.size
    for y in range(h-1):
        row = []
        for x in range(1,w):
            if PX[x,y] == 255:
                if len(row) > 0:
                    if x-row[-1][0] == row[-1][-1]+1:
                        row[-1] = (row[-1][0],row[-1][-1]+1)
                    else:
                        row.append((x,0))
                else:
                    row.append((x,0))
        dots.append(row)
    return dots

def connectdots(dots):
    print("connecting contour points2...")
    contours = []
    for y in range(len(dots)):
        for x,v in dots[y]:
            if v > -1:
                if y == 0:
                    contours.append([(x,y)])
                else:
                    closest = -1
                    cdist = 100
                    for x0,v0 in dots[y-1]:
                        if abs(x0-x) < cdist:
                            cdist = abs(x0-x)
                            closest = x0

                    if cdist > 3:
                        contours.append([(x,y)])
                    else:
                        found = 0
                        for i in range(len(contours)):
                            if contours[i][-1] == (closest,y-1):
                                contours[i].append((x,y,))
                                found = 1
                                break
                        if found == 0:
                            contours.append([(x,y)])
        for c in contours:
            if c[-1][1] < y-1 and len(c)<4:
                contours.remove(c)
    return contours


# -------------- optimisation for pen movement --------------

def sortlines(lines):
    print("optimizing stroke sequence...")
    clines = lines[:]
    slines = [clines.pop(0)]

    while clines != []:
        x,s,r = None,1000000,False
        for l in clines:
            d = distsum(l[0],slines[-1][-1])
            dr = distsum(l[-1],slines[-1][-1])
            if d < s:
                x,s,r = l[:],d,False
            if dr < s:
                x,s,r = l[:],s,True

        clines.remove(x)
        if r == True:
            x = x[::-1]
        slines.append(x)
    return slines


# -------------- helper functions --------------

def midpt(*args):
    xs,ys = 0,0
    for p in args:
        xs += p[0]
        ys += p[1]
    return xs/len(args),ys/len(args)


def distsum(*args):
    return sum([ ((args[i][0]-args[i-1][0])**2 + (args[i][1]-args[i-1][1])**2)**0.5 for i in range(1,len(args))])


