#############################################################################
'''
    This software is released under a variant of the MIT licence  

    Please note that imported libraries may have different licences
'''
#############################################################################
'''

 What this program does
    1. Accepts the following cmd line rguments
        -file [filename] (will prompt for filename of not provided.)
        -paper [A6|A5|A4|A3|A2|A1|A0|2A0|4A0] (Default A4 paper size)
        -maxw [n] (defaults as coded 800mm between motor centre)
        -maxh [n] (defaults as coded 960 to calibration point )
        -fname [True|False] (defaults to False. Plots the filename)
        -dist [True|False] (defaults to False. Plots the distance the pen moved if True)
        -time [True|False] (defaults to False. Plots the time taken to plot if True)

            (-fname, dist & time are plotted in that order
            at the bottom left of the drawing area/paper)
            
    3. Calibrates the plotter before each drawing (at the bottom and again
        at the origin, bottom left, of the drawing area.
        
    4. If the image is not portrait, then rotate it.
    
    5. The SVG/Gcode file from the images folder is scaled to 90% of the
        selected paper Size and motor step size to fit the entire image
        in the drawing area. I work arse about face with the step size,
        but that is how my head works. It is then:
        
    6. It is then Plotted in the centre of the MaxW & MaxH rectangle (portrait)
    
    7. If enabled, filename, distance moved and time taken are plotted
        at the origin (this is too small when using a sharpie/pencil,
        adjust the multiplier, scale, in the draw_str() function, or
        .upper() the text)
        
    8. The motors are released

    9. When run in ___debug___ mode the image is plotted using Turtle
        (you may need to adjust the scaling in the plot_pair function)
        svg files will be upside down
        
   10. When run with -O, output will be sent to the Motor Shield to plot

   11. There is very little bounds checking and almost no error trapping
       I will leave this to you as an exercise.


 A few points:
     1. This is an artistic exercise, not an engineering one.
     2. An image with a lot of small lines/dots is best suited to a printer, NOT a plotter.
     3. The best image for a PLOTTER is one with long continuous lines
     4. Long lines, especially those whe one motor has a small relative movement to the other,
          will curve. 
     5. Files created for CNC/Etching machines are rarely optimised for plotting,
          and a lot of drawing time can be saved by pre-processing the input file before
          sending it to the plotter. (https://github.com/alsliahona/gcode-optimizer
          is well worth casting an eye over.) 
 
 Due to the inherent insability of a suspended pen, the fewer segments
 in each line the better as the steppers are the running continuously rather
 than stopping and starting all the time (Intertia)

 There is far too much margin for error when
   setting up
   measuring
   always working on the diagonal
   rounding
   movement of the pen carriage
   vibration (stand, motor, belt ...)
   shake/sway/stretch in the belt/string
   having to drive motors individually1 step at a time (motor Hat/Bonnet)

 The best we can do is embrace inacuracy and reduce drift as much as we can!

 This is just not a high resolution device
 As resolution is reduced, so is detail. this is a good thing
     (for this device anyway)
 As counterintuitive as it may seem lower resolutions perform the better
 
 A LOT depends on how you are creating the images you are going to plot
 When using a pencil or sharpie if you think 1mm == 1 pixel and you should
 get fairly decent results.
 
 The key is to be patient and experiment taking a meticulous approach,
 otherwise you will end up frusrated with the seemingly random results

 Some Tips
    Busy images, and those with a lot of detail, do not translate well
    'flat', high contrast, low detail images work best
    'lines'/edges are created by sharp changes in colour.
     increasing the blur will reduce the number of contour lines
     A gradient will not give you a line.
     Pencil lines are lighter than you expect
     Everything takes longer than you expect
     If the pen carriage is not balanced, you wlill get small loops in lines
         (especially a long V lengths at the bottom of the drawing)
    Long horizontal or vertical lines will curve (Split them up)
    You can not start a stepper motor at full speed and expect it to run
     flawlessly. You need to ramp the speed up in steps.
    Don't underestimate the impact of a poor quality motor or trying to run
        a motor too fast. All ypu need is for it to choke once and everything
        from then onwards is offset.
    The slower you draw, the better the quality.
    Ink does not flow horizontally! Angle the pen sightly to keep the tip inked up

 Important
     1. This is not the best, vleanest or tidiest code out there. There are many
         opportunities for refactoring and simplifying. You will also find a bug
         or three. Don't criticise them, use them 
     2. When using code snippets to test and the app fails or is stopped, the motors
         will still be energised. This is not a good state to keep them in for any
         length of time.  (I just start the app again and ^C at the calibration prompt
         to release the motors when debugging)
     3. This Gcode will draw a clockwise square in the centre of the page
         up, right, down, left. put it in a file sq.ngc and plot that file on A5/A6   

             G00 X0 Y0
             G01 X0 Y1
             G01 X1 Y1
             G01 X1 Y0
             G01 X0 Y0

 Other Software/projects/Docs to look at
    1. bCNC - If you are doing anything with GCode, want to check a converted file,
        want to edit before you print, have a look at this. if is also much faster at
        converting SVG fies to G-Code (https://github.com/vlachoudis/bCNC)
    2. Inkscape - is also useful especially if you add in the Gcode pluginn
    3. Brachiograph - This is where it all started, I built this and then got
        carried away. (https://www.brachiograph.art/)
    4. LaserGRBL is a Windows GCode streamer for DIY Laser Engravers. It has a
        raster to gcode convertion that could be useful. http://lasergrbl.com/

Other useful sites
    https://homofaciens.de/technics-machines-v-plotter_en.htm
    https://www.raspberrypi.org/blog/plotter-made-from-scrap-computer-parts/
    https://www.lifewire.com/driving-stepper-motors-at-high-speed-818822
    http://www.polargraph.co.uk/
    http://www.makelangelo.com/
    http://www.practicalagile.uk
    
        

Bill Of Materials

 Raspberry Pi Zero (or other variant)
 Raspberry Pi motor bonnet (I should have used 2 'proper' drivers)
 Supporting software for the motor Bonnet/Hat
 2 x Nema 17 stepper Motors
 1 micro servo/solenoid
 gt2 gear 20 tooth 2mm pitch
 gt2 belt 6mm
 gt2 rol1ers
 2 x Motor Brackets
 
 Misc
     Blu Tack
     Frame to hold Motors (cardboard box, wood, shelving ...)
     Pen carriage (plastic takeaway box)
         weights (water filled balloons) with each weight being 1/2 that of the pen carriage
     Fridge (Magnetic drawing surface)
     Magnets to hold the paper onto the fridge
     Image manipulation software (various)

Time (Far more time than you think)
'''

#Imports

import time
import math
import json
import getopt
import argparse
import re

from sys import argv

from os import listdir, environ
from os.path import isfile, join
from datetime import datetime

import pigpio

# if no -O draw using turtle
if __debug__:
    import turtle
    if environ.get('DISPLAY','') == '':
        environ.__setitem__('DISPLAY', ':0.0')
else:
    
    from adafruit_motor import stepper as STEPPER
    from adafruit_motorkit import MotorKit

########################################################################
################################ CONFIG Start  #########################
#
'''
    THEORETICAL Maximum width and height of CANVAS/PLOTTER area (Portrait). You can't draw at this size,
        motors start to choke, belts/string starts slipping accuracy is reduced ... If you double the
        dimensions of the acual drawing area you will have no problems. 

    MaxW =  The horizontal distance between the two points at the top of the V. Unless you are using
            idler pulleys, this is the distance between centres of the motor spindles,

    MaxH =  The vertical distance from the point of the V to the horizintal line between the centres.
            This is also the ideal point for the centre of the Pen.
            if you can't mount the pen at this point mount the pen vertically below it, as close as possible
            Measure to the point of the V and NOT the Pen
'''
MaxW = 800
MaxH = 980


'''
    The area available for drawing and is in the centre of the canvas (Sizes in mm)
    The closer you are to the top the more things get skewed
    The Closer to the bottom the greater the problems experienced by the belt
        vibrating or the pen carriage swinging/shaking
    If you want to move or offset the drawing area on the overall canvas, adjust
        offsetx & offsety in calibrate()
'''
paper = {'A6':[105,148],'A5':[148,210], 'A4':[210,297], 'A3': [297,420], 'A2':[420,594],'A1':[594,841],'A0':[841,1190],'2A0':[1189,1682],'4A0':[1682,2378]}

'''
G2 pul1ey = 20 teeth at 2mm pitch = 40mm diameter meaning One rotation = 40mm
This give us 40/200 = mm/step for each stepstyle avilable on the Motor Hat/Bonnet
or
1/stepsize = steps per mm
    (I know this feels backwards, but that is how my brain works.
        divide to convert Coordinates to Steps
        multiply to convert Steps to Coordinates)

In reality there is no real advantage to using a smaller stepsize than Half steps
in this setup all it does is dramaticlly increase the time taken to draw anything.

obviously when coding/checking/testing, the larger the stepsize,
 the sooner you get there, but remember that generally, the larger the step, the lower the torque
'''
if not __debug__:
    #stepsize = [0.2,STEPPER.SINGLE]         # Single step 200/r
    #stepsize = [0.2,STEPPER.DOUBLE]         # Single step 200/r but more torque
    stepsize = [0.1,STEPPER.INTERLEAVE]     # Interleave (Half steps) 400/r also more torque
    #stepsize = [0.025,STEPPER.MICROSTEP]    # Microsteps 1600/r 
else:
    stepsize = [0.2,1]

#
################################ CONFIG END  #########################
######################################################################


'''
    Offset from the border to the canvas to the edges of the actual drawing area as well as
    the last length of each of the arms of the V.
    Dist =  The total distance the pen moves (includes Pen-up motion)
    drawing_width, drawing_height Drawing area width and height
'''
offsetx = 0
offsety = 0
lastlen = [0,0]
lastxy = [0,0]
Dist = 0
drawing_width = 0
drawing_height = 0

lastPenup = False

'''
    Create a default stepper motor object, no changes to I2C address or frequency
    If in debug mode, (not using python -O), we dont bother as we are going to use the turtle canvas.
'''
if not __debug__:
    kit = MotorKit()
else:
    s = turtle.getscreen()
    t = turtle.Turtle()

'''
    Set up the servo for the pen lifter.

    remember to 'sudo pigpiod'  or have it run at startup
    
    The pulse frequency should be no higher than 100Hz - higher values could (WILL) damage the servos
    This is the Broadcom gpio pin (18) we are using for the servo (pen lifter)
    this is deliberately set low!
'''
if not __debug__:
    rpi = pigpio.pi()
    rpi.set_PWM_frequency(18, 10)
                           
#
################################ Global END  #########################
######################################################################
def drawngc(thisfile):
    '''
    A few assumptions are made about the Gcode
        The unit of measure is mm
        Absolute coordinate mode is used
        Only G00, G01, G02, G03, M3 & M5 are acted on. ALL other commands are ignored
        G0 is always Pen Up, all others draw
            Unless Explicit Laser OFF (M03)/ON (M05) are taken as Pen UP/DOWN
        All movement commands must include both X & Y, even if it is 0
        Z (Depth) is always ignored
        Only I,J curves are plotted. (the most common)
            K is ignored as we are plotting on the X&Y plane
        All Arc (G02 & G03) command must include an end-point
        Gcode ORIGIN is bottom left (you may end up with morrored/inverted drawings)
    '''    
    global offsetx, offsety
    global drawing_width, drawing_height
    global lastlen
    
    print ("Drawing-",thisfile)

    # empty list of commands
    Lines=[]
    try:
        #file1 = open(thisfile, 'r')
        with open(thisfile) as fp:
            print ("Reading file...")
            # parse the lines and include those we are interested in
            for cnt, line in enumerate(fp):
                line = parse_line(line)
                if line:
                    Lines.append(line)
               
    except (OSError, IOError) as e:
        print ("File open error")
        print (e)
        hardware_reset()
        exit()
        
    fp.close()
    '''
        run through the file and find the largest & smallest x & y
        (image width and height)
        This really should be done when we are parsing the file
        but I will leave this to you to refactor
    '''
    image_width = 0.0
    image_height = 0.0
    sw = 0.0
    sh = 0.0
    
    print ("Finding GCODE drawing extents...")
    for line in Lines:
        for p in line:
            pkey = p[:1]
            #pval = float(p[1:])
            if pkey == "X":
                pval = float(p[1:])
                if pval > image_width: image_width =  pval
                if pval < sw: sw =  pval
            elif pkey == "Y":
                pval = float(p[1:])
                if pval > image_height: image_height =  pval
                if pval < sh: sh =  pval
    
    # get correct image size.
    sw = abs(sw)
    sh = abs(sh)
    image_width = image_width + sw
    image_height = image_height + sh
    
    image_width = image_width / stepsize[0]  #   drawing width in steps
    image_height = image_height / stepsize[0]  #   drawing height in steps

    if (drawing_width == 0) or (drawing_height == 0):
        print ("One or more drawing extents is zero")
        exit()
 
    # Image MUST be portrait.  scale to fit drawing area
    if drawing_width/image_width < drawing_height/image_height:
        image_ratio = float(drawing_width / image_width)
    else:
        image_ratio = float(drawing_height / image_height)


    # centre image on drawing area
    offsetx=int((MaxW-(image_width*image_ratio))/2)
    offsety=int((MaxH-(image_height*image_ratio))/2)
    
    if __debug__:
        print ("         draw-X", drawing_width)
        print ("         draw-Y", drawing_height)
        print ("        draw-sw", sw)
        print ("        draw-sh", sh)
        print ("        Image-X", image_width * stepsize[0])
        print ("        Image-Y", image_height * stepsize[0])
        print ("    Image ratio", image_ratio)
        print (" Scaled-image-X", image_width*image_ratio)
        print (" Scaled-image-Y", image_height*image_ratio)
        print ("Scaled-offset-X", offsetx)
        print ("Scaled-offset-Y", offsety)         

    # plot each drawable line
    x = 0.0
    y = 0.0
    #z = 0.0
    #r = 0.0
    i = 0.0
    j = 0.0
    lastx = 0.0
    lasty = 0.0

    print ("Starting to draw...")
    
    for line in Lines:
        if __debug__ == True:
            print ("Line", line)
            
        # parse the parameters in the line and extract the available values
        # we add in sw & sh to move the origin so all X & Y axis values are positive.)
        got_xy = 0
        for p in line:
            pkey = p[:1]
            #pval = float(p[1:])
            if pkey == "X":           
                x = (float(p[1:]) + sw) * image_ratio / stepsize[0]
                got_xy += 1
            elif pkey == "Y":
                y = (float(p[1:]) + sh) * image_ratio  / stepsize[0]
                got_xy += 1
            elif pkey == "I":
                i = float(p[1:]) * image_ratio  / stepsize[0]      # x offset to center
            elif pkey == "J":
                j = float(p[1:]) * image_ratio  / stepsize[0]     # y offset to centre
            #elif pkey == "R":
            #    r = float(p[1:]) * image_ratio       # radius of arc


        # we need at least x & Y for all "G" codes otherwise we just skip the line
        if line[0][:1] == "G":
            if got_xy < 2:
                if __debug__:
                    print ("Skipped", line)
                    continue
             
        '''
        The pen is UP for moves/fast traverse, othewise it is drawing
        Depending on how/where the G-Code was created, this sometimes adds
        unwanted lines to the drawing. It is worth checking.
        Explicit Laser OFF/ON are taken as Explicit Pen UP/DOWN
        '''
        if line[0] in("G00", "M05"):    # Jog or explicit laser OFF
            PenUp=True
        elif line[0] == "M03":         # Explicit laser ON
            PenUp=False
        else:
            PenUp=False

        set_pen_up(PenUp)

        # ????
        #print (line)
        
        # Nice simple move to new position  (straight line)       
        if line[0] in ("G00", "G01"):
            plot_pair(x,y)
            
        # An Arc, Clockwise or Anti-clockwise. We only draw a single arc up to 360 degrees
        if line[0] in ("G02", "G03"): 
            # only cater for I & J curves (they are also the most common)
            if i == 0 and j == 0:
                print ("Unable to process line", line)
                plot_pair(x,y)
                continue

            #remember I,J are the centre of the circle/arc.
            converted =  G0203(line[0], x, y, i, j, r, lastx, lasty)

            for G01 in converted:
                xy = G01.split(",")
                plot_pair(float(xy[0]),float(xy[1]))

        # Remember where we ended on the last move so we can draw an arc if needed.
        lastx = x
        lasty = y             

    # al1 the lines done
    return()
        
def parse_line(line):
    '''
    Parse the GCODE and return those commands we are interested in
    
    '''
    # extract letter-digit pattern
    g_pattern = "([A-Z][-+]?[0-9.]+)"
        
    # add leading zeros to commands
    two_digit_commands = "[GMN][0-9]([A-Z]|$)"
    
    # white spaces and comments start with ';' and in '()'
    clean_pattern = "\s+|\(.*?\)|;.*"

    line = line.upper()
    line = re.sub(clean_pattern, '', line)
    if len(line) == 0:
        return None
    if line[0] == '%':
        return None
    if line[0] == '(':
        return None
        
    line = re.sub(two_digit_commands, lambda x: x.group(0)[0] + '0' + x.group(0)[1:], line)
    m = re.findall(g_pattern,line)
        
    # The only commands we are going to use  
    if m[0] in ("G00", "G01", "G02", "G03", "M03", "M05"):
        return (m)
    else:
        return None

def getangle(start, end, centre, clockwise):
    '''
        Get the angle from centre to start and end points
        This is more resilient to 'creative' G-Code than using sin or cos

              360/0
                |
                |
                |
       270------+-------90
                |
                |
                |
               180
                
    '''

    u = start[0]- centre[0],start[1] - centre[1]
    v = end[0]- centre[0],end[1] - centre[1]

    angle1 = math.atan2(u[0], u[1])
    angle2 = math.atan2(v[0], v[1])

    if (angle1 < 0): angle1 += 2*math.pi
    if (angle2 < 0): angle2 += 2*math.pi
    
    return (angle1, angle2)

def angle_between(start,end,cw):
    twopi = math.pi + math.pi
    diff = 0
    
    td = end - start

    if td <0:
        diff = td + twopi
    else:
        diff = td
    if cw == -1:
        diff =twopi - td
        if diff > twopi:
            diff -= twopi
            
    return (diff)

def G0203(cmd,x,y,i,j,r,xp,yp):
    '''

    Takes an arc an converts it to a series of lines along the circumference.

    x, y = destination
    xp,yp = start point if arc (previous end position)
    i, j relative x & y offset from the start point to the center of the arc

    Defining an arc’s center with IJ
    This arc starts at X0Y2 and finishes at X2Y0.
    It’s center is at X0Y0. We could specify it in g-code like this:
    (Clockwise arc mode)
    G02 X2 Y0 I0 J-2.0
 

    '''
    
    #print ("cmd {} x{} y{} i{} j{} r{} xp{} yp{}".format(cmd,x,y,i,j,r,xp,yp))

    # Empty the list of commands
    G01 =[]

    '''
    Dont bother with very small distances just go to the endpoint
    if you have a drawing with a lot of small circles (4mm or less) you will
    end up with small dashes instead
    
    remember this has already been scaled to fit the drawing area
    '''
    if math.hypot(xp - x, yp - y) < 5:
        G01.append("{},{}".format(x,y) )
        return G01
    
    if cmd=="G02":      CW = 1
    else:               CW = -1

    originx = i + xp 
    originy = j + yp

    # We now calculate the radius
    r = myround(math.sqrt((i**2) + (j**2)))

    if CW == 1:
        sang, eang = getangle((xp,yp), (x,y), (originx,originy), True)
    else:
        sang, eang = getangle((xp,yp), (x,y), (originx,originy), False)

    angle = angle_between(sang,eang,CW)
    arclen = r * math.pi * angle
    move_angle = 20 / math.pi / r
    '''
    if __debug__:
        print ("cmd {} x{} y{} i{} j{} r{} xp{} yp{}".format(cmd,x,y,i,j,r,xp,yp))
        print ("ang to start",sang, math.degrees(sang))
        print ("  ang to end",eang, math.degrees(eang))
        print (" arc (angle)",angle, math.degrees(angle))
        print ("Step (angle)",move_angle, math.degrees(move_angle))
        print ("     Origin x,y",originx,originy)
        print ("      Start x,y",xp,yp)
        print ("        End x,y",x,y)
        print ("         Radius",r)
    '''
    
    # make sure we start at the start of the arc
    G01.append("{},{}".format(xp,yp))
    sub_angle = move_angle
 
    # move between points on circumference of the arc
    while sub_angle < angle:
        newangle = sang + (sub_angle * CW)
        nx = originx + (r * math.sin(newangle))
        ny = originy + (r * math.cos(newangle)) 
        G01.append("{},{}".format(nx,ny))
        sub_angle = sub_angle +  move_angle

    # and finish at the endpoint (that is sometimes NOT at the end of the arc.)
    G01.append("{},{}".format(x,y))
    
    return G01

def drawsvg(thisfile):

    # SVG origin is TOP left

    global offsetx, offsety
    global drawing_width, drawing_height

    try:
        file1 = open(thisfile, 'r')
    except (OSError, IOError) as e:
        print ("File open error")
        print (e)
        hardware_reset()
        exit()
        
    Lines = file1.readlines()   #Read ENTIRE File
    file1.close()

    print ("Drawing-",thisfile)
    # Badly Parse the file  for width and height
    for line in Lines:
        line = line.upper().replace('"',"").replace( "'","")
        whflag = 0
        if " WIDTH=" in line:
            tmp=line.split(" WIDTH=")
            if " WIDTH=" in tmp[0]:
                tn = (tmp[0])
            else:
                tn = (tmp[1])
            for C in range(1,len(tn)):
                if tn[:C].isnumeric():
                    image_width =  (tn[:C])
                    whflag += 1
                else:
                    break
            
        if " HEIGHT=" in line:
            tmp=line.split(" HEIGHT=")
            if " HEIGHT=" in tmp[0]:
                tn = (tmp[0])
            else:
                tn = (tmp[1])
            for C in range(1,len(tn)):
                if tn[:C].isnumeric():
                    image_height =  (tn[:C])
                    whflag += 1
                else:
                    break
                
        # got both width and height so stop going through the file
        if whflag == 2: break

    image_width=(int(image_width) / stepsize[0])  #   input image width in steps
    fliph = int(image_height)
    image_height =(int(image_height) / stepsize[0])  #   input image height in steps
    
    #Image MUST be portrait. scale to fit drawing area
    if drawing_width/image_width < drawing_height/image_height:
        image_ratio = float(drawing_width / image_width)
    else:
        image_ratio = float(drawing_height /image_height)
     

    # centre Scaled image on drawing area
    offsetx=int((MaxW-(image_width*image_ratio))/2)
    offsety=int((MaxH-(image_height*image_ratio))/2)
    
    if __debug__:
        print ("    Image ratio", image_ratio)
        print ("        image X", image_width * stepsize[0])
        print ("        image Y", image_height * stepsize[0])
        print (" Scaled-image X", image_width * image_ratio * stepsize[0])
        print (" Scaled-image Y", image_height * image_ratio * stepsize[0])
        print ("Scaled-offset X", offsetx)
        print ("Scaled-offset Y", offsety)     
    
    for line in Lines:
        coords=line.split('"')              #split line into segments
        if 'polyline points' in coords[0] : #only draws poly line elements
            if __debug__ == True:
                print ("Line", line)
            set_pen_up(True)                    # Lift pen before moving to start of line
            
            PointPair = 0
            points=coords[1].split(',')     # the 2nd segment is the points so split that
            
            for pt in points:
                if PointPair==0:            # get a pair of points
                    px=(float(pt)/stepsize[0]*image_ratio)
                    PointPair +=1
                else:
                    # SVG origin is TOP left, so flip y to move origin to bottom left.
                    py=(float(fliph-float(pt))/stepsize[0]*image_ratio)
                    # We now have a pair of points to plot
                    plot_pair(px,py)
                    PointPair=0
                    # Drop the pen for subsequent points in the polyline
                    set_pen_up(False)
    
    # al1 the lines done
    return()


def adjust_speed(this_step,thisleg,step_delay,line_segment=False):
    '''
    This is really rough, but it helps with the speed of the drawing,
    the pen carrige swinging round and also helps prevent the motor choking.

    One single motor Choke destroys the rest of the drawing!

    We make the assumption that the length of a single segment is long
        enough to get to slow down speed.

    We effectively end up running at the pace of the fastest stepper with the
    extra steps in the long leg making sure the the short leg doesn't choke

    If the motor starts to shudder or not move, reduce the acceleration by
      either increasing the delay initially passed in, or the number of steps
      beween reductions in the delay time.
    You may need to adjust this depending on your stepsize[1]

    TBH though, a global delay of 0.015 is probably just as good
    if the motor shart 'Chocking' or skipping steps, you are probably trying
    to accelerate too quickly.
        Either incease the initial delay in plot_pair() or
        increase the # steps between increments (this_step % ?? == 0:) below

    One of the motors I have, chokes quicker than the other, but this seems
        to be OK for me with interleave steps. (higher torque) 
    '''
    
    wMin = 0.013        # shortest sleep, fastest movement
    wMax = 0.020
  
    if line_segment == False:
        # start slowing down near the end, reducing the speed every 3rd step
        if this_step > (thisleg - 70):
            if step_delay < wMax:
                if this_step % 3 == 0:   
                    step_delay /=  0.98

    else:
        # accelerate to the Maximum speed, a little slower than we slow down (every 4th step)
        if step_delay > wMin:
            if this_step % 4 == 0:            
                step_delay *=  0.98

    return(step_delay)
  

def plot_pair(x, y,line_segment=False,max_dist=0,step_delay=0.02):
    '''

    By the time we get here, everthing should be in stepper motor steps.
    
    Convert the X,Y coordinates to the change in the length of each diagonal (l1,l2)
    and then use bresenham's line algorithm to syncronise the movement of the motors

    Long paths are broken down into segments while drawing. This means that long
        diagonals, off-centre, vertical or horizontal lines don't curve as much.
        
    Think about it.
             
      <--------w------->      
  m1> O                O <m2  ^ 
       \              /       |
        \            /        | 
         \          /         |
       l1 \        /l2        |
           \      /           |
            \    /            h
             \  /             |           
              \/              |
      <----x-->^              |
               y              |
               |              |
               v              v
     ^-Origin (0,0)
     
    '''
        
    global stepsize
    global offsetx, offsety
    global lastlen, lastxy, Dist

    # Turtle draw if in debug
    if __debug__:
        a,b = s.screensize()
        x = x / 2
        y = y / 2
        x,y = x - (a/4), y - (b/4)
        t.goto(x,y)
        lastxy = (x,y)
        return()
    

    dx = x - lastxy[0]      
    dy = y - lastxy[1]
    longest_move = max(abs(dx),abs(dy))
    '''
    break the line down into maximum horizontal or vertical segments
        of 30 mm to reduce curve for long lines.
    '''
    if max_dist == 0:
        max_dist = 30 / stepsize[0]     # 30 mm into steps. 
        num_segments = int(longest_move / max_dist) + 1
        max_dist = int(longest_move / num_segments)
    
        if max_dist < longest_move:
            # Work from the origin of the original line, not the start of this segment
            oxy = lastxy
            line_angle = math.atan2(dy,dx)
            if dx > 0: multx = 1
            else: multx = -1
            if dy > 0: multy = 1
            else: multy = -1
            if abs(dx) > abs(dy):
                for i in range (1,num_segments):        
                    newx = (oxy[0] + (max_dist * multx * i))
                    newy = (newx - oxy[0]) * math.tan(line_angle) 
                    newy = (oxy[1]) + newy
                    step_delay = plot_pair(newx, newy,True,max_dist,step_delay)
            else:
                for i in range (1,num_segments):
                    newy = (oxy[1] + (max_dist * multy * i))
                    newx = (newy -  oxy[1])/ math.tan(line_angle)
                    newx = (oxy[0] ) + newx
                    step_delay = plot_pair(newx, newy,True,max_dist,step_delay)

    # We fall through for the last segment of the line and slow down to the end.

    # Turtle draw and return if in debug
    if __debug__:
        a,b = s.screensize()
        x = x / 2
        y = y / 2
        x,y = x - (a/4), y - (b/4)
        t.goto(x,y)
        lastxy = (x,y)
        return()
    
    # get the new length for each side with the offset applied
    l1 = int(myround(math.sqrt(((x + offsetx)**2) + ((MaxH - y - offsety)**2))))
    l2 = int(myround(math.sqrt(((MaxW-x-offsetx)**2) + ((MaxH - y - offsety)**2))))

    # calculate the change from where we are now
    move1 = lastlen[0] - l1         # steps to move left length 
    move2 = lastlen[1] - l2         # steps to move Right length

    # the steps we have travelled for the original line passed in
    if line_segment == False:
        Dist = Dist + math.hypot(dx, dy) 

        
    #####################################################################
    # Replace this section if you use drivers other than the motor hat
    #vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
    if move1 >= 0:
        dir1 = STEPPER.FORWARD
    else:
        dir1 = STEPPER.BACKWARD

    if move2 >= 0:
        dir2 = STEPPER.BACKWARD
    else:
        dir2 = STEPPER.FORWARD

    # Steps to move for each motor.
    move1 = abs(move1)
    move2 = abs(move2)  
   
    # bresenham's line algorithm https://en.wikipedia.org/wiki/Bresenham%27s_line_algorithm
    if move1 > move2:
        over = move1 / 2
        for steps in range(move1):
            kit.stepper1.onestep(direction=dir1, style=stepsize[1])
            step_delay = adjust_speed(steps,move1,step_delay,line_segment)
            over += move2
            if(over>=move1):
                over -= move1
                kit.stepper2.onestep(direction=dir2, style=stepsize[1])
            time.sleep(step_delay)
    else:
        over = move2 / 2;
        for steps in range(move2):
            kit.stepper2.onestep(direction=dir2, style=stepsize[1])
            step_delay = adjust_speed(steps,move2,step_delay,line_segment)
            over += move1
            if(over >= move2):
                over -= move2
                kit.stepper1.onestep(direction=dir1, style=stepsize[1])
            time.sleep(step_delay)
                   
    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # Replace this section if you use drivers other than the motor hat
    #####################################################################
    
    '''
    Save the length of each leg we were at in preparation for next move.
    This helps reduce drift as we a moving from the last position
    we go to, rather than where we should have gone. 
    '''
    lastlen[0] = l1
    lastlen[1] = l2
   
    lastxy = (x,y)

    # return the most recent step delay, so we can maintain the speed between line segments    
    return (step_delay)


def myround(x):
    #round to the size of the step we are taking.  (our maximum accuracy.)
    return round (int(x/stepsize[0])* stepsize[0],3)

def calibrate():
    
    global MaxW, MaxH
    global drawing_width, drawing_height
    global offsetx, offsety
    global lastlen
    
    if (drawing_width>=MaxW) or (drawing_height>=MaxH):
        print ("")
        print ("ERROR Drawing area larger than canvas!")
        print ("")
        print ("Please correct")
        print ("")
        exit()
        
    '''
        This could be changed to calibarte at the drawing origin,
        but I prefer this.
    '''    
    print ("+----------------------------------------------+")
    print ("|  Move point of V to centre (between motors)  |")
    print ("|      and ", MaxH ,"mm  below motor axis           |")
    print ("+----------------------------------------------+")
    if not __debug__:    input("Press 'Enter' to Accept ")
    print ("")
    print ("CALIBRATED. (at",stepsize[0], "mm/step)")
    
    # move everything to steps to reduce creeping, rounding, drift problems.
    # NOT to improve accuracy.
    MaxW = myround(MaxW / stepsize[0])
    MaxH = myround(MaxH / stepsize[0])
    drawing_width = myround(drawing_width / stepsize[0])
    drawing_height = myround(drawing_height / stepsize[0])
    
    '''
    0,0 is bottom left of the entire Canvas
    Place the drawing area or page in the centre of the theoretical canvas
    adjust these offsets if you need to move the actual drawing area on the canvas.
    but try to keep it as central as possible
    '''
    offsetx=int((MaxW-drawing_width)/2)
    offsety=int((MaxH-drawing_height)/2)
    
    # the length of the diagonals at the calibration point. (MaxH & half way between motors)
    lastlen[0]=int(myround(math.sqrt(((MaxW/2)**2) + (MaxH**2))))
    lastlen[1]=lastlen[0]

    if __debug__:
        s.screensize(drawing_width,drawing_height)
        #draw_protractor()
        print ("")
        print ("Max-Width-", MaxW)
        print ("Max-Height", MaxH)
        print ("Diagonal--", lastlen[0])
        print ("")
        print ("Drawing-Width", drawing_width)
        print ("Drawing-height", drawing_height)
        print ("Offset-X", offsetx)
        print ("Offset-Y", offsety)

        print ("")
    
    print ("+----------------------------------------------+")
    print ("|    Moving to bottom left of drawing area.    |")
    print ("+----------------------------------------------+")
    plot_pair(0,0,True)
    
    print ("Now at bottom left of drawing area")
    print ("")
    if not __debug__:    input ("Press ENTER to start drawing..")

def init():
    hardware_reset()
    calibrate()
    
def hardware_reset():
    '''
    Make sure the pen is up so that is it does not bleed onto the paper,
    also
    release the motors so that they are not energised.
    The motors should cope with being energised for a long time,
        but  if there is no need ....
    It also allows you to move them and reposition the pen carriage,
        something you can't do while they are energised.
    '''
    set_pen_up(True)
    if not __debug__:
        kit.stepper1.release()
        kit.stepper2.release()

def set_pen_up(PenUp=True):
    '''
        Dont underestimate how violent these servos are, they throw the
        pen carriage all over the place. The difficulty is balancing the
        unwanted movement and the time taken to lift or drop the pen,
        especially with a busy drawing (not a good idea anyway)

        You are much better off moving the pen rather than the entire carriage

        The idea is to keep the movement (difference between up and down)
        as small as possible and dampen it if we can

        if you are lifting the pen rather than the  carriage, the loop could
        probably be sped up a little
    '''
    global lastPenup
    if lastPenup == PenUp:
        return()
    else:
        lastPenup = PenUp
    
    up = 1800      
    down = 1450
    gpio_pin=18
    transition_time = 0.02
    
    if PenUp == True:
        if __debug__:
            t.penup()
            return()
        for i in range(down,up+20,20):
            time.sleep(transition_time)
            rpi.set_servo_pulsewidth(gpio_pin, up)
            
    else:
        if __debug__:
            t.pendown()
            return()
        for i in range(up,down-20,-20):
            time.sleep(transition_time)
            rpi.set_servo_pulsewidth(gpio_pin, down)


def draw_str(this_str):
    global stepsize
    #Position [n][0] is info only. Reference this as 'ord(character) - 32'
    simplex = [[" ",16,],
        ["!",10,5,21,5,7,-1,-1,5,2,4,1,5,0,6,1,5,2],
        ['"',16,4,21,4,14,-1,-1,12,21,12,14],
        ["#",21,11,25,4,-7,-1,-1,17,25,10,-7,-1,-1,4,12,18,12,-1,-1,3,6,17,6],
        ["$",20,8,25,8,-4,-1,-1,12,25,12,-4,-1,-1,17,18,15,20,12,21,8,21,5,20,3,18,3,16,4,14,5,13,7,12,13,10,15,9,16,8,17,6,17,3,15,1,12,0,8,0,5,1,3,3],
        ["%",24,21,21,3,0,-1,-1,8,21,10,19,10,17,9,15,7,14,5,14,3,16,3,18,4,20,6,21,8,21,10,20,13,19,16,19,19,20,21,21,-1,-1,17,7,15,6,14,4,14,2,16,0,18,0,20,1,21,3,21,5,19,7,17,7],
        ["&",26,23,12,23,13,22,14,21,14,20,13,19,11,17,6,15,3,13,1,11,0,7,0,5,1,4,2,3,4,3,6,4,8,5,9,12,13,13,14,14,16,14,18,13,20,11,21,9,20,8,18,8,16,9,13,11,10,16,3,18,1,20,0,22,0,23,1,23,2],
        [ "'",10,5,19,4,20,5,21,6,20,6,18,5,16,4,15],
        ["(",14,11,25,9,23,7,20,5,16,4,11,4,7,5,2,7,-2,9,-5,11,-7],
        [")",14,3,25,5,23,7,20,9,16,10,11,10,7,9,2,7,-2,5,-5,3,-7],
        ["*",16,8,21,8,9,-1,-1,3,18,13,12,-1,-1,13,18,3,12],
        ["+",26,13,18,13,0,-1,-1,4,9,22,9],
        [",",10,6,1,5,0,4,1,5,2,6,1,6,-1,5,-3,4,-4],
        ["-",26,4,9,22,9],
        [".",10,5,2,4,1,5,0,6,1,5,2],
        ["/",22,20,25,2,-7],
        ["0",20,9,21,6,20,4,17,3,12,3,9,4,4,6,1,9,0,11,0,14,1,16,4,17,9,17,12,16,17,14,20,11,21,9,21],
        ["1",20,6,17,8,18,11,21,11,0],
        ["2",20,4,16,4,17,5,19,6,20,8,21,12,21,14,20,15,19,16,17,16,15,15,13,13,10,3,0,17,0],
        ["3",20,5,21,16,21,10,13,13,13,15,12,16,11,17,8,17,6,16,3,14,1,11,0,8,0,5,1,4,2,3,4],
        ["4",20,13,21,3,7,18,7,-1,-1,13,21,13,0],
        ["5",20,15,21,5,21,4,12,5,13,8,14,11,14,14,13,16,11,17,8,17,6,16,3,14,1,11,0,8,0,5,1,4,2,3,4],
        ["6",20,16,18,15,20,12,21,10,21,7,20,5,17,4,12,4,7,5,3,7,1,10,0,11,0,14,1,16,3,17,6,17,7,16,10,14,12,11,13,10,13,7,12,5,10,4,7],
        ["7",20,17,21,7,0,-1,-1,3,21,17,21],
        ["8",20,8,21,5,20,4,18,4,16,5,14,7,13,11,12,14,11,16,9,17,7,17,4,16,2,15,1,12,0,8,0,5,1,4,2,3,4,3,7,4,9,6,11,9,12,13,13,15,14,16,16,16,18,15,20,12,21,8,21],
        ["9",20,16,14,15,11,13,9,10,8,9,8,6,9,4,11,3,14,3,15,4,18,6,20,9,21,10,21,13,20,15,18,16,14,16,9,15,4,13,1,10,0,8,0,5,1,4,3],
        [":",10,5,14,4,13,5,12,6,13,5,14,-1,-1,5,2,4,1,5,0,6,1,5,2],
        [";",10,5,14,4,13,5,12,6,13,5,14,-1,-1,6,1,5,0,4,1,5,2,6,1,6,-1,5,-3,4,-4],
        ["<",24,20,18,4,9,20,0],
        ["=",26,4,12,22,12,-1,-1,4,6,22,6],
        [">",24,4,18,20,9,4,0],
        ["?",18,3,16,3,17,4,19,5,20,7,21,11,21,13,20,14,19,15,17,15,15,14,13,13,12,9,10,9,7,-1,-1,9,2,8,1,9,0,10,1,9,2],
        ["@",27,18,13,17,15,15,16,12,16,10,15,9,14,8,11,8,8,9,6,11,5,14,5,16,6,17,8,-1,-1,12,16,10,14,9,11,9,8,10,6,11,5,-1,-1,18,16,17,8,17,6,19,5,21,5,23,7,24,10,24,12,23,15,22,17,20,19,18,20,15,21,12,21,9,20,7,19,5,17,4,15,3,12,3,9,4,6,5,4,7,2,9,1,12,0,15,0,18,1,20,2,21,3,-1,-1,19,16,18,8,18,6,19,5],
        ["A",18,9,21,1,0,-1,-1,9,21,17,0,-1,-1,4,7,14,7],
        ["B",21,4,21,4,0,-1,-1,4,21,13,21,16,20,17,19,18,17,18,15,17,13,16,12,13,11,-1,-1,4,11,13,11,16,10,17,9,18,7,18,4,17,2,16,1,13,0,4,0],
        ["C",21,18,16,17,18,15,20,13,21,9,21,7,20,5,18,4,16,3,13,3,8,4,5,5,3,7,1,9,0,13,0,15,1,17,3,18,5],
        ["D",21,4,21,4,0,-1,-1,4,21,11,21,14,20,16,18,17,16,18,13,18,8,17,5,16,3,14,1,11,0,4,0],
        ["E",19,4,21,4,0,-1,-1,4,21,17,21,-1,-1,4,11,12,11,-1,-1,4,0,17,0],
        ["F",18,4,21,4,0,-1,-1,4,21,17,21,-1,-1,4,11,12,11],
        ["G",21,18,16,17,18,15,20,13,21,9,21,7,20,5,18,4,16,3,13,3,8,4,5,5,3,7,1,9,0,13,0,15,1,17,3,18,5,18,8,-1,-1,13,8,18,8],
        ["H",22,4,21,4,0,-1,-1,18,21,18,0,-1,-1,4,11,18,11],
        ["I",8,4,21,4,0],
        ["J",16,12,21,12,5,11,2,10,1,8,0,6,0,4,1,3,2,2,5,2,7],
        ["K",21,4,21,4,0,-1,-1,18,21,4,7,-1,-1,9,12,18,0],
        ["L",17,4,21,4,0,-1,-1,4,0,16,0],
        ["M",24,4,21,4,0,-1,-1,4,21,12,0,-1,-1,20,21,12,0,-1,-1,20,21,20,0],
        ["N",22,4,21,4,0,-1,-1,4,21,18,0,-1,-1,18,21,18,0],
        ["O",22,9,21,7,20,5,18,4,16,3,13,3,8,4,5,5,3,7,1,9,0,13,0,15,1,17,3,18,5,19,8,19,13,18,16,17,18,15,20,13,21,9,21],
        ["P",21,4,21,4,0,-1,-1,4,21,13,21,16,20,17,19,18,17,18,14,17,12,16,11,13,10,4,10],
        ["Q",22,9,21,7,20,5,18,4,16,3,13,3,8,4,5,5,3,7,1,9,0,13,0,15,1,17,3,18,5,19,8,19,13,18,16,17,18,15,20,13,21,9,21,-1,-1,12,4,18,-2],
        ["R",21,4,21,4,0,-1,-1,4,21,13,21,16,20,17,19,18,17,18,15,17,13,16,12,13,11,4,11,-1,-1,11,11,18,0],
        ["S",20,17,18,15,20,12,21,8,21,5,20,3,18,3,16,4,14,5,13,7,12,13,10,15,9,16,8,17,6,17,3,15,1,12,0,8,0,5,1,3,3],
        ["T",16,8,21,8,0,-1,-1,1,21,15,21],
        ["U",22,4,21,4,6,5,3,7,1,10,0,12,0,15,1,17,3,18,6,18,21],
        ["V",18,1,21,9,0,-1,-1,17,21,9,0],
        ["W",24,2,21,7,0,-1,-1,12,21,7,0,-1,-1,12,21,17,0,-1,-1,22,21,17,0],
        ["X",20,3,21,17,0,-1,-1,17,21,3,0],
        ["Y",18,1,21,9,11,9,0,-1,-1,17,21,9,11],
        ["Z",20,17,21,3,0,-1,-1,3,21,17,21,-1,-1,3,0,17,0],
        ["[",14,4,25,4,-7,-1,-1,5,25,5,-7,-1,-1,4,25,11,25,-1,-1,4,-7,11,-7],
        ["\\",14,0,21,14,-3],
        ["]",14,9,25,9,-7,-1,-1,10,25,10,-7,-1,-1,3,25,10,25,-1,-1,3,-7,10,-7],
        ["^",16,6,15,8,18,10,15,-1,-1,3,12,8,17,13,12],
        ["_",16,0,-2,16,-2],
        ["`",10,6,21,5,20,4,18,4,16,5,15,6,16,5,17],
        ["a",19,15,14,15,0,-1,-1,15,11,13,13,11,14,8,14,6,13,4,11,3,8,3,6,4,3,6,1,8,0,11,0,13,1,15,3],
        ["b",19,4,21,4,0,-1,-1,4,11,6,13,8,14,11,14,13,13,15,11,16,8,16,6,15,3,13,1,11,0,8,0,6,1,4,3],
        ["c",18,15,11,13,13,11,14,8,14,6,13,4,11,3,8,3,6,4,3,6,1,8,0,11,0,13,1,15,3],
        ["d",19,15,21,15,0,-1,-1,15,11,13,13,11,14,8,14,6,13,4,11,3,8,3,6,4,3,6,1,8,0,11,0,13,1,15,3],
        ["e",18,3,8,15,8,15,10,14,12,13,13,11,14,8,14,6,13,4,11,3,8,3,6,4,3,6,1,8,0,11,0,13,1,15,3],
        ["f",12,10,21,8,21,6,20,5,17,5,0,-1,-1,2,14,9,14],
        ["g",19,15,14,15,-2,14,-5,13,-6,11,-7,8,-7,6,-6,-1,-1,15,11,13,13,11,14,8,14,6,13,4,11,3,8,3,6,4,3,6,1,8,0,11,0,13,1,15,3],
        ["h",19,4,21,4,0,-1,-1,4,10,7,13,9,14,12,14,14,13,15,10,15,0],
        ["i",8,3,21,4,20,5,21,4,22,3,21,-1,-1,4,14,4,0],
        ["j",10,5,21,6,20,7,21,6,22,5,21,-1,-1,6,14,6,-3,5,-6,3,-7,1,-7],
        ["k",17,4,21,4,0,-1,-1,14,14,4,4,-1,-1,8,8,15,0],
        ["l",8,4,21,4,0],
        ["m",30,4,14,4,0,-1,-1,4,10,7,13,9,14,12,14,14,13,15,10,15,0,-1,-1,15,10,18,13,20,14,23,14,25,13,26,10,26,0],
        ["n",19,4,14,4,0,-1,-1,4,10,7,13,9,14,12,14,14,13,15,10,15,0],
        ["o",19,8,14,6,13,4,11,3,8,3,6,4,3,6,1,8,0,11,0,13,1,15,3,16,6,16,8,15,11,13,13,11,14,8,14],
        ["p",19,4,14,4,-7,-1,-1,4,11,6,13,8,14,11,14,13,13,15,11,16,8,16,6,15,3,13,1,11,0,8,0,6,1,4,3],
        ["q",19,15,14,15,-7,-1,-1,15,11,13,13,11,14,8,14,6,13,4,11,3,8,3,6,4,3,6,1,8,0,11,0,13,1,15,3],
        ["r",13,4,14,4,0,-1,-1,4,8,5,11,7,13,9,14,12,14,],
        ["s",17,14,11,13,13,10,14,7,14,4,13,3,11,4,9,6,8,11,7,13,6,14,4,14,3,13,1,10,0,7,0,4,1,3,3],
        ["t",12,5,21,5,4,6,1,8,0,10,0,-1,-1,2,14,9,14],
        ["u",19,4,14,4,4,5,1,7,0,10,0,12,1,15,4,-1,-1,15,14,15,0],
        ["v",16,2,14,8,0,-1,-1,14,14,8,0],
        ["w",22,3,14,7,0,-1,-1,11,14,7,0,-1,-1,11,14,15,0,-1,-1,19,14,15,0],
        ["x",17,3,14,14,0,-1,-1,14,14,3,0],
        ["y",16,2,14,8,0,-1,-1,14,14,8,0,6,-4,4,-6,2,-7,1,-7],
        ["z",17,14,14,3,0,-1,-1,3,14,14,14,-1,-1,3,0,14,0],
        ["{",14,9,25,7,24,6,23,5,21,5,19,6,17,7,16,8,14,8,12,6,10,-1,-1,7,24,6,22,6,20,7,18,8,17,9,15,9,13,8,11,4,9,8,7,9,5,9,3,8,1,7,0,6,-2,6,-4,7,-6,-1,-1,6,8,8,6,8,4,7,2,6,1,5,-1,5,-3,6,-5,7,-6,9,-7],
        ["|",8,4,25,4,-7],
        ["}",14,5,25,7,24,8,23,9,21,9,19,8,17,7,16,6,14,6,12,8,10,-1,-1,7,24,8,22,8,20,7,18,6,17,5,15,5,13,6,11,10,9,6,7,5,5,5,3,6,1,7,0,8,-2,8,-4,7,-6,-1,-1,8,8,6,6,6,4,7,2,8,1,9,-1,9,-3,8,-5,7,-6,5,-7],
        ["~",24,3,6,3,8,4,11,6,12,8,12,10,11,14,8,16,7,18,7,20,8,21,10,-1,-1,3,8,4,10,6,11,8,11,10,10,14,7,16,6,18,6,20,7,21,10,21,12]    ]
    
  
    # we are just negating stepsize here. (multiply by 2 to double the size)
    scale = stepsize[0] * 10 * 1
    
    xpos = 0
    for ch in this_str:
        gotpair = ord (ch)
        if gotpair < 32 or gotpair > 126:  #ASCII 32 (Space) -> 126 (~)
            gotpair = 32
        char = simplex[gotpair - 32]
        width = char[1] * scale 
        xy = [0,0]
        gotpair = 0
        set_pen_up(True)
        for pair in char:
            gotpair +=1
            if gotpair %2 == 0:
                xy[1] = pair
                if gotpair > 3:
                    if xy == [-1,-1]:
                        set_pen_up(True)
                    else:
                        plot_pair(xpos+(xy[0]*scale),xy[1]*scale)
                        time.sleep(0.15)
                        set_pen_up(False)
            else:
                xy[0] = pair

        xpos += width 
        
def draw_protractor():
    orig = 0,0
    radius = 250
    steps = 30

    t.pencolor("lightblue")
    
    for angle in range (0,360,steps):
        t.penup()
        t.goto(orig)
        t.pendown()
        ang = math.radians(angle)
     
        x,y = orig[0] + (radius * math.sin(ang)),orig[1] + (radius * math.cos(ang))
        t.goto(x,y)
        t.write(round(math.degrees(ang)))
   
    t.pencolor("black")
    t.penup()

def main():
    global MaxW,MaxH
    global drawing_width,drawing_height,offsetx,offsety

    hardware_reset()
    set_pen_up(False)
    set_pen_up(True)
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-file')
    parser.add_argument('-paper')
    parser.add_argument('-maxw')
    parser.add_argument('-maxh')
    parser.add_argument('-dist')
    parser.add_argument('-time')
    parser.add_argument('-fname')
     
    args = parser.parse_args()

    mypath = "images/"
    if args.file:
        thisfile = args.file
    else:
        onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath,f))]
        print (onlyfiles)
        thisfile = input ("Which file? ")
        
    # make sure there is a border (stops the pen/lifter from snagging)
    if args.paper:   
        drawing_width = int(paper[args.paper][0] * 0.9)  
        drawing_height = int(paper[args.paper][1] * 0.9)
    else:
        drawing_width = int(paper['A4'][0] * 0.9)
        drawing_height = int(paper['A4'][1] * 0.9)

    if args.maxw:
        MaxW = int(args.maxw)

    if args.maxh:
        MaxH = int(args.maxh)

    if args.fname:
        if args.fname == "True":
            plotfname = True
        else:
            plotfname = False
    else:
        plotfname = False
        
    if args.dist:
        if args.dist == "True":
            plotdist = True
        else:
            plotdist = False
    else:
        plotdist = False

    if args.time:
        if args.time == "True":
            plottime = True
        else:
            plottime = False
    else:
        plottime = False
             
         
    init()
    starttime = datetime.now()
    oox = offsetx
    ooy = offsety

    if thisfile[-3:].upper() == "SVG":
        drawsvg(thisfile = mypath + thisfile)   
    elif thisfile[-3:].upper() in("NGC",".NC","ODE"):
        drawngc(thisfile = mypath + thisfile)
    else:
        print("")
        print("Missing/incorrect file ({})".format(mypath + thisfile))
        print("Selected 'svg' or 'nc,ngc,gcode' files only")
        return()
    
    # bottom of page, not the drawing
    offsetx = oox
    offsety = ooy 
    
    endtime = datetime.now()

    drawstr = ""
    if plotfname:
        drawstr += "File: " + thisfile + "    "

    if plotdist:
        drawstr += "Distance: " + str(round(Dist * stepsize[0] / 1000,3))+ "m" + "    "

    if plottime:
        tm = str((endtime  - starttime)).split(".")
        drawstr += "Time taken: " + str(tm[0])

    if len(drawstr) > 0:
        draw_str(drawstr)

    set_pen_up(True)
    plot_pair(0,0)
    hardware_reset()

    print ("Distance moved {}m".format(round(Dist * stepsize[0] / 1000,3)))
    print ("    Time Taken",endtime  - starttime)
    print ("  Time Started",starttime)
    print ("Time Completed",endtime)

if __name__ == "__main__":
    #   REMEMBER TO RELEASE THE MOTOR AND LIFT THE PEN WHEN NEEDED
    #main()

    try:
        main()
        pass
    except () as e:
        # Make sure the motors are not energised if the code fails,
        # or we stop it with a ^C.
        #
        # When coding or debugging,you obviously need to have only one main()
        # outside the try: block but
        print (e)
        hardware_reset()
