"""
Build a nested object from a serialization file
===============================================

"""

import os
import yaml
import json
import f90nml

__all__ = ["file_2_nob"]

def file_2_nob(path):
    """ Load a nob from a serialization file
    :params path: path to a file
    """

    ext = os.path.splitext(path)[-1]
    if ext in [".yaml", ".yml"]:
        with open(path, "r") as fin:
            nob = yaml.load(fin, Loader=yaml.SafeLoader)
    elif ext in [".json"]:
        with open(path, "r") as fin:
            nob = json.load(fin)
    elif ext in [".nml"]:
        nmlp = f90nml.Parser()
        nmlp.read(path)
        nob = nmlp.tokens
        raise NotImplementedError("Namelist not fully implemented")
    else:
        raise RuntimeError("Format not supported")
    
    return nob