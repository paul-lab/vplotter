
 What this program does:
    1. Accepts the following cmd line rguments
        -file [filename] (will prompt for filename if not provided.)
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
    
    5. The SVG/NGC file from the images folder is scaled to 90% of the
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
