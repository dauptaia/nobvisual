"""

Browse a circlify object with tkinter
=====================================
"""


from pprint import pprint as pp
import circlify as circ
import tkinter

SIZE = 800
BKGD = "white"


__all__ = ["tkcirclify"]


def tkcirclify(circlify, holder=None, color="#777777",shade=0.2, legend=None, title=None):
    """Generate a Circlify in a Tkinter canvas.
    
    :param circlify: a ciclify object, list of Circles objects.
    :param color: hex coloer, for background of circles.
    :param shade: shading, making nested levels lighter (>0) or darker (<0)
        in range of floats [-0.5, 0.5]

    No returns
    ----------

    Interrupt the process with a tkinter canvas.
    """

    can = create_window(holder=holder)
    
    for circle in circlify:
        draw_circle(can, circle, base_color=color, shade=shade)

    if title is not None:
        draw_title(can, title)

    if legend is not None:
        draw_legend(can, legend)
    tkinter.mainloop()


def draw_title(can, title):
    """Draw the tiutle"""
    x_pix = int(0.5*SIZE)
    y_pix = int(0.02*SIZE)
    can.create_text(x_pix,y_pix, text=title, anchor="n", justify="center")    

def draw_legend(can, legend):
    """Draw a legend on the canvas"""

    unit = int(0.03*SIZE)

    x_pix =  2*unit
    y_pix =  5*unit
    
    for labl in legend:
        can.create_oval(
            x_pix-0.5*unit,
            y_pix-0.5*unit,
            x_pix+0.5*unit,
            y_pix+0.5*unit,
            fill = labl[1],
            outline=color_shade(labl[1],-0.2),
            )
        can.create_text(x_pix+0.81*unit,y_pix, text=labl[0], anchor="w")
        y_pix += 1.62* unit



def create_window(holder=None):
    """Create general window"""
    if holder == None:
        holder = tkinter.Tk()
    can = tkinter.Canvas(
        holder,
        width=SIZE,
        height=SIZE,
        bg=BKGD)

    can.pack(side="bottom", fill="x")
    return can


def draw_circle(can, circle, base_color, shade=0.1):
    """Draw the circle"""
    x__, y__, r__ = circle.circle
    smaller = 0.90

    x_center = SIZE*0.5
    y_center = SIZE*(0.5 + 0.4*(1-smaller))
    
    xpix = x_center + x__ * SIZE * 0.5 *smaller
    ypix = y_center + y__ * SIZE * 0.5 *smaller
    rpix = r__ * SIZE*0.5*smaller
    
    color = base_color
    for _ in range(circle.level):
        color =  color_shade(color, shade)
    
    tag= None

    anchor = None
            
    if circle.ex is not None:
        if "id" in circle.ex:
            list_ = circle.ex["id"].split("|")
            tag=list_[0]
            for item in list_:
                if item.startswith("COLOR"):
                    custom_color = item.split("=")[-1]
                    if custom_color =="default":
                        pass
                    else:
                        color = custom_color
                if item.startswith("ANCHOR"):
                    anchor = item.split("=")[-1]
    
    item = can.create_oval(
        (xpix-rpix, ypix-rpix, xpix+rpix, ypix+rpix),
        fill=color,
        outline=color_shade(color,-0.2),
    )

    if anchor is not None:
        can.create_text(
            (xpix, ypix),
            text=anchor,
        )
    
    can.tag_bind(item, "<Enter>", lambda event, arg=tag: enter_tag(event,arg))
    can.tag_bind(item, "<Leave>", lambda event, arg=tag: leave_tag())
    
    def enter_tag(event,tag):
        hilitext(can, tag, event.x-30, event.y+60, tags="hover")
        
    def leave_tag():
        can.delete("hover")


def hilitext(can, text, xpix, ypix,tags=None):
    """Highcontrast text"""
    can.create_text(xpix+1, ypix+1, text=text, tags=tags, fill="white")
    can.create_text(xpix+1, ypix-1, text=text, tags=tags, fill="white")
    can.create_text(xpix-1, ypix+1, text=text, tags=tags, fill="white")
    can.create_text(xpix-1, ypix-1, text=text, tags=tags, fill="white")
    can.create_text(xpix, ypix, text=text, tags=tags, fill="black")
    

def color_shade(color, adjust):
    """ alter a color to ligther or darker tone
    Parameters :
    ------------
    color : tuple (r,g,b) from (0,0,0) to (255,255,255)
    adjust : float from -1 (blakest) to 1 (whitest)

    Returns:
    --------
    shaded : tuple of the color, shaded
    """
    colorrgb = hex2rgb(color)

    shaded = []
    for col in colorrgb:
        if adjust > 0:
            out = 1 * adjust + float(col) * (1-adjust)
        else:
            out = float(col) * (1-abs(adjust))
        shaded.append(int(out))
    
    colorout = rgb2hex(shaded)
    return colorout


def rgb2hex(list_rgb):
    """Convert rgb list to hex"""
    return '#{:02x}{:02x}{:02x}'.format(
        int(list_rgb[0]), 
        int(list_rgb[1]), 
        int(list_rgb[2]))

def hex2rgb(str_rgb):
    """Convert hexadecimal color to rgb"""
    try:
        rgb = str_rgb[1:]

        if len(rgb) == 6:
            red, grn, blu = rgb[0:2], rgb[2:4], rgb[4:6]
        elif len(rgb) == 9:
            red, grn, blu = rgb[0:3], rgb[3:6], rgb[6:9]
        elif len(rgb) == 3:
            red, grn, blu = rgb[0] * 2, rgb[1] * 2, rgb[2] * 2
        else:
            raise ValueError()
    except:
        raise ValueError("Invalid value %r provided for rgb color." % str_rgb)

    return tuple(int(val, 16) for val in (red, grn, blu))

#test_tkinter_circlify()