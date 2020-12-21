"""module to browse a circlify object with tkinter"""


from pprint import pprint as pp
import circlify as circ
import tkinter

SIZE = 600
BKGD = "white"


__all__ = ["tkcirclify"]

def test_tkinter_circlify():
    """show off"""

    data = [
        0.05, 
        {'id': 'a2', 'datum': 0.05},
        {'id': 'a0', 'datum': 0.8, 'children': [
            0.3, 0.2, 0.2, 0.1
            ], 
        },
        {'id': 'a1', 'datum': 0.1, 'children': [
            {
                'id': 'a1_1', 'datum': 0.05
            }, 
            {
                'datum': 0.04
            },
            0.01
            ],
        },
    ]
    circles = circ.circlify(data, show_enclosure=True)
    #circles = circ.circlify([19, 17, 13, 11, 7, 5, 3, 2, 1], show_enclosure=True)
    pp(circles)
    #circ.bubbles(circles)
    tkinter_circlify(circles)



def tkcirclify(circlify, holder=None, color="#777777",shade=0.2):
    """Generate a Circlify in aTkinter canvas"""

    can = create_window(holder=holder)
    
    for circle in circlify:
        draw_circle(can, circle, base_color=color, shade=shade)

    tkinter.mainloop()

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
    xpix = (1+x__) * SIZE*0.5
    ypix = (1+ y__) * SIZE*0.5
    rpix = r__ * SIZE*0.5
    
    color = hex2rgb(base_color)
    tag= None

    if circle.ex is not None:
        if "id" in circle.ex:
            list_ = circle.ex["id"].split("|")
            tag=list_[0]
            for item in list_:
                if item.startswith("COLOR"):
                    color = item.split("=")[-1]
                    if color =="default":
                        color = hex2rgb(base_color)
                    else:
                        color = hex2rgb(color)
    
    for _ in range(circle.level):
        color =   color_shade(color, shade)
    
    item = can.create_oval((xpix-rpix, ypix-rpix, xpix+rpix, ypix+rpix), fill=rgb2hex(color),outline=rgb2hex(color_shade(color,-0.2)), )
    can.tag_bind(item, "<Enter>", lambda event, arg=tag: enter_tag(event,arg))
    can.tag_bind(item, "<Leave>", lambda event, arg=tag: leave_tag())

 

    
    def enter_tag(event,tag):
        can.create_text(event.x+20, event.y-20, text=tag, tags="hover")
        
    def leave_tag():
        can.delete("hover")
    
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
    shaded = []
    for col in color:
        if adjust > 0:
            out = 1 * adjust + float(col) * (1-adjust)
        else:
            out = float(col) * (1-abs(adjust))
        shaded.append(int(out))
    return shaded


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