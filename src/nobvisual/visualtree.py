"""
Draw the circular packing of a folder tree.
===========================================

"""

import os
from glob import glob
import math
from nobvisual import tkcirclify
import circlify as circ

COLOR_BINARY = "#00ccff"
COLOR_ASCII ="#ffcc00"

__all__ = ["visual_tree"]


def visual_tree(tgt=None):
    """Show the circular nested packing of a directory tree.
    
    The circular packing is computed using the circlify package.
    The graphical output is done using tkinter.
    Area of circles is proportional to lthe log10 of file sizes.
    ASCII-UTF8 files are blue, others (usually Binary)  are in green. 


    :params wdir: path to a working directory. If None, set to current working directory.

    No returns.
    -----------

    Open a tkinter window with the circular packing.
    """
    if tgt is None:
        tgt = os.getcwd()

    nstruct = scan_wdir(tgt)
    circles = circ.circlify(nstruct, show_enclosure=True)
    tkcirclify(
        circles,
        color="#eeeeee",
        legend=[
            ("binary", COLOR_BINARY),
            ("ascii", COLOR_ASCII),
        ],
        title=f"Showing {str(tgt)}"
    )

def scan_wdir(wdir):
    """ Build the structure of a folder tree.
    
    :params wdir: path to a directory
    """
    def _rec_subitems(path):
        name = os.path.split(path)[-1]
        out = {
            "id": name,
            "datum": 1.,
        }
        if os.path.isfile(path):

            ext = os.path.splitext(path)[-1]

            out["id"] += "|ANCHOR="+ext

            try:
                size = math.log10(os.path.getsize(path))
            except ValueError:
                print("path", path)
                size = 1
            try:
                with open(path, "r", encoding="utf8") as fin:
                    fin.readlines()
                out["id"] += "|COLOR=" + COLOR_ASCII
            except UnicodeDecodeError:
                out["id"] += "|COLOR=" + COLOR_BINARY
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


    