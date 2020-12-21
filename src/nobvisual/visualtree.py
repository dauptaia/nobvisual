"""Module to draw the circular packing of a folder tree"""

import os
from glob import glob

from nobvisual import tkcirclify
import circlify as circ

def visual_tree(wdir=None):
    """Show the circular paking of a directory tree"""

    if wdir is None:
        wdir = os.getcwd()

    nstruct = scan_wdir(wdir)
    circles = circ.circlify(nstruct, show_enclosure=True)
   
    tkcirclify(circles, color="#bbbbbb")

    

def scan_wdir(wdir):
    """ build the strucutre of a folder tree"""
    
    
    def _rec_subitems(path):

        name = os.path.split(path)[-1]
        out = {
            "id": name,
            "datum": 1.,
        }
        if os.path.isfile(path):
            try:
                with open(path, "r", encoding="utf8") as fin:
                    size = len(fin.readlines())
                out["id"] += "|COLOR=#9999ff"
            except UnicodeDecodeError:
                size=1000
                out["id"] += "|COLOR=#99FF99"
            out["datum"] = size
            
        else:
            size = 0
            out["children"] = list()
            paths = glob(os.path.join(path, "**"))
            for nexpath in paths:
                record = _rec_subitems(nexpath)
                size += record["datum"]
                out["children"].append(record)
            out["datum"] = size
            out["id"] += "|COLOR=default"
        return out
    
    out = [_rec_subitems(wdir)]
    
    return out
