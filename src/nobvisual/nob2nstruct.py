"""Module to convert a Nested object to a Nob-struct object

Nob struc is a description of a Nob compatible with a Circular packing representation"""


__all__ = ["build_nstruct"]



def build_nstruct(nob):
    """Build the nested_structure of a nested object
   
    :param nob: a nested object

    returns :
    ---------
        nested dicts of type
        {
            "id": name,
            "datum": 1.,   <- tot nb of children
            "path": path,   <_full path to this item
            "color": level, <- the level for now
            "children:[]     <- if children list of nesting here
        } 
        in a list.
    """ 
    nobd = mv_to_dict(nob)
    out = [_rec_nstruct(nobd)]
   
    return out


def _rec_nstruct(in_, level=0, name=".", path="."):
    """recusive building of nstruct"""

    out = {
        "id": name,
        "datum": 1.,
        "path": path,
        "color": level,
    }

    if isinstance(in_, dict):
        out["datum"] =float(dict_childs(in_))
        out["children"] =list()
        for key in in_:
            out["children"].append(
                _rec_nstruct(
                    in_[key], 
                    level=level+1, 
                    name=key,
                    path=path+"/"+key
                ),
            )
    else:
        out["id"] = name + ":" + str(in_)
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
