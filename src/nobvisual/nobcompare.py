"""Compare two nested objects, and store the result in a circlufy nested structure"""

import yaml
import nobvisual as nobv
import circlify as circ

__all__ = ["nob_compare", "nob_compare_tkinter", "visual_comparefile"]

LEFT_COLOR   = "#ffd700"
RIGHT_COLOR  = "#005b96"
DIFFER_COLOR = "#d62d20"

def visual_comparefile(path_left, path_right):
    """Show visually the differences between two serialization file.
    
    The circular packing is computed using the circlify package.
    The graphical output is done using tkinter.
    
    """
    noba=nobv.file_2_nob(path_left)
    nobb=nobv.file_2_nob(path_right)

    title="Showing file differences"
    title+="\nLeft: " + path_left
    title+="\nRight: " + path_right
    nob_compare_tkinter(noba, nobb, title=title)

def nob_compare_tkinter(noba, nobb, title=None):
    """Compare two nested objects.
    
    :params noba: left node
    :params nobb: right node
    
    :returns nothing:

    Open a tkinter object to show the comparison  
    
    """
    cmp_ = nobv.nobcompare.nob_compare(noba, nobb)
    circles = circ.circlify(cmp_, show_enclosure=True)

    nobv.tkinter_circlify.tkcirclify(
        circles,
        color="#eeeeee",
        shade=0.1,
        legend=[
            ("Only in left", LEFT_COLOR),
            ("Only in right", RIGHT_COLOR),
            ("Differ", DIFFER_COLOR),
        ],
        title=title
    )


def nob_compare(noba, nobb):
    """Compare two nested objects.
    
    :params noba: left node
    :params nobb: right node
    
    :returns cirlify_nob:  
    
    """

    out = [_rec_compare(
        nobv.nob2nstruct.mv_to_dict(noba),
        nobv.nob2nstruct.mv_to_dict(nobb),
    )]
    
    return out


def val_as_str(data, max_=30):
    """return a short_string for any value"""
    if isinstance(data, dict):
        out = ""
    else:
        val_ = str(data)
        if len(val_)>max_:
            val_ = val_[:10]+"..."+val_[-max_+10:]
        out =  ":" + val_
    return out

def path_as_str(path):
    """represent path as string"""

    indent = ""
    out = ""
    for item in path:
        out += indent + "- " +item + "\n"
        indent += "  "
    return out

def _rec_compare(left, right, path=None, ptype = "both"):
    """Recursive build"""

    if path is None:
        path = list()
    #print(path)
    out = {
        "id": path_as_str(path),
        "datum": 1.,
    }
    
    type_ = ptype
    void = dict()
    size= 1
    out["children"] = list()
        
    if isinstance(left, dict) and isinstance(right, dict):
        
        for key in left:
            if key in right:
                out["children"].append(
                    _rec_compare(
                        left[key],
                        right[key],
                        path=path+[key],
                        ptype=type_
                    ),
                )
            else:
                out["children"].append(
                    _rec_compare(
                        left[key],
                        void,
                        path=path+[key],
                        ptype="only_left"
                    ),
                )
            size += out["children"][-1]["datum"]

        for key in right:
            if key not in left:
                out["children"].append(
                    _rec_compare(
                        void,
                        right[key],
                        path=path+[key],
                        ptype="only_right"
                    ),
                )
                size += out["children"][-1]["datum"]
        
    else:

        if left != right and left != void and right != void:
            type_ = "differ"
            val_left = val_as_str(left)
            val_right = val_as_str(right)
            out["id"] = path_as_str(path)
            out["id"] += "<- " + val_left
            out["id"] += "\n-> " + val_right
        elif left != void:
            val_left = val_as_str(left)
            out["id"] += val_left
        elif right != void:
            val_right = val_as_str(right)
            out["id"] += val_right
            
            
                           
    out["datum"] = size

    if type_ ==  "differ":
        out["id"] += "|COLOR=" + DIFFER_COLOR  
    if type_ ==  "only_left":
        out["id"] += "|COLOR=" + LEFT_COLOR 
    if type_ ==  "only_right":
        out["id"] += "|COLOR=" + RIGHT_COLOR 

    return out

#test_nc()