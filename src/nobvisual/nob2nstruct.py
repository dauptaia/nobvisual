"""
Convert a Nested object to a circlify object
============================================

Nob-struc is a description of a Nob compatible with a Circular packing representation, using the circlify package API.
"""

import circlify as circ
from nobvisual import tkcirclify, file_2_nob

__all__ = ["visual_treefile", "build_nstruct", "mv_to_dict"]


COLOR_BOOL = "#00ffff"
COLOR_INT = "#00ccff"
COLOR_FLOAT ="#0066aa"
COLOR_STRING ="#00aa00"
COLOR_NONE ="#dddddd"
COLOR_UKN ="#ffcc00"


def visual_treefile(path):
    """Show the circular nested packing of a serialization file.
    
    The circular packing is computed using the circlify package.
    The graphical output is done using tkinter.
    Area of circles is proportional to lthe log10 of file sizes.
    
    """
    nob = file_2_nob(path)

    nstruct= build_nstruct(nob)
    circles = circ.circlify(nstruct, show_enclosure=True)
    tkcirclify(
        circles,
        color="#eeeeee",
        legend=[
            ("int", COLOR_INT),
            ("float", COLOR_FLOAT),
            ("string", COLOR_STRING),
            ("boolean", COLOR_BOOL),
            ("None", COLOR_NONE),
            ("other", COLOR_UKN)
        ],
        title=f"Showing {str(path)}"
    )

def build_nstruct(nob):
    """Build the nested_structure of a nested object.
   
    :param nob: a nested object
        for exampke the content of a YAML or JSON file.

    :returns:
    
    nested dicts of type

    ::

        {
            "id": name,
            "datum": 1.,      # <- tot nb of children
            "children: [ ],   # <- if children list of nesting here
        } 
    
    in a list. This is compatible with the circlify package.

    """ 
    nobd = mv_to_dict(nob)
    out = [_rec_nstruct(nobd)]
   
    return out


def val_as_str(data, max_=30):
    """return a short_string for any value"""
    if isinstance(data, dict):
        out = ""
    else:
        val_ = str(data)
        if len(val_)>max_:
            val_ = val_[:10]+" (...) "+val_[-max_+10:]
        out = val_
    return out

def path_as_str(path):
    """represent path as string"""

    indent = ""
    out = ""
    for item in path:
        out += indent + "- " +item + "\n"
        indent += "  "
    return out

def _rec_nstruct(in_, path=None):
    """recusive building of nstruct"""

    if path is None:
        path = list()
    name = path_as_str(path)
    

    out = {
        "id": name,
        "datum": 1.,
    }

    if isinstance(in_, dict):
        out["datum"] =float(dict_childs(in_))
        out["children"] =list()
        for key in in_:
            out["children"].append(
                _rec_nstruct(
                    in_[key], 
                    path=path + [key]
                ),
            )
    else:
        out["id"] += ":" + val_as_str(in_)
        if isinstance(in_, int):
            out["id"] += "|COLOR=" + COLOR_INT
        elif isinstance(in_, float):
            out["id"] += "|COLOR=" + COLOR_FLOAT
        elif isinstance(in_, str):
            out["id"] += "|COLOR=" + COLOR_STRING
        elif isinstance(in_, bool):
            out["id"] += "|COLOR=" + COLOR_BOOL
        elif in_ is None:
            out["id"] += "|COLOR=" + COLOR_NONE
        else:
            out["id"] += "|COLOR=" + COLOR_UKN
            
    return out


def dict_depth(data, level=1):
    """ compute dictionnary depth
    Warning - recursive

    Parameters:
    -----------
    data : the init-dictionnary /or one of its subitems
    level : integer, the level to return

    Returns:
    --------
    level : integer, the max level of the current item
    """
    if not isinstance(data, dict) or not data:
        return level
    return max(dict_depth(data[key], level + 1) for key in data)


def dict_childs(data, childs=1):
    """ compute dictionnary population
    Warning - recursive

    Parameters:
    -----------
    data : the init-dictionnary /or one of its subitems
    childs : integer, the level to return

    Returns:
    --------
    childs : integer, the total number of childs
    """
    if not isinstance(data, dict) or not data:
        return childs

    childs = 0
    for key in data:
        childs += dict_childs(data[key])
    return childs


def rec_childs(data, dict_={}, parent="/", childs=1):
    """ compute dictionnary childs
    ie a dict associating each node with the population underneath
    Warning - recursive

    Parameters:
    -----------
    data : the init-dictionnary /or one of its subitems
    childs : integer, the level to return

    Returns:
    --------
    childs : integer, population of the dict/subitem
    dict_childs_nb : the dictionnary recording all childs
    """


    if not isinstance(data, dict) or not data:
        return childs, dict_

    childs = 0
    for key in data:
        path = parent + key + "/"
        dict_[path], _ = rec_childs(data[key], dict_, parent=path)
        childs += dict_[path]


    return childs, dict_



def mv_to_dict(data):
    """ Convert a multiple value data into a dict

    Parameters:
    -----------
    data : a multiple valued data , usually list or dict
    
    Returns:
    --------
    dictdata :  same data as a disctionnary
    """
    if isinstance(data, list):
        #print(data)
        n_data = dict()
        for i, item in enumerate(data):
            n_data[str(i)]=item
        data = n_data
    if isinstance(data, dict):
        for key in data:
            #print(key, data[key])
            data[key] = mv_to_dict(data[key])
    return data



         
