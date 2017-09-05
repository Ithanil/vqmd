"""
This file contains various routines for parsing of i-Pi trajectory files

Copyright (C) 2014-2015 i-PI developers < https://github.com/cosmo-epfl/i-pi-dev >
Copyright (C) 2017 Jan Kessler

This file is part of vqmd. It is subject to the license terms in the LICENSE file found in the
top-level directory of this distribution and at https://github.com/Ithanil/vqmd .
No part of vqmd, including this file, may be copied, modified, propagated, or distributed except
according to the terms contained in the LICENSE file.
"""

import numpy as np
import math
import sys
import os
import re
import copy

from vqmd.lib.units import Elements

mode_map = {
    "bin":  "binary",
}

io_map = {
    "read":       "read_%s",
}

cell_re = [re.compile('CELL[\(\[\{]abcABC[\)\]\}]: ([-+0-9\.Ee ]*)\s*'),
           re.compile('CELL[\(\[\{]GENH[\)\]\}]: ([-+0-9\.?Ee ]*)\s*'),
           re.compile('CELL[\(\[\{]H[\)\]\}]: ([-+0-9\.?Ee ]*)\s*')]

def read_xyz(filedesc, **kwargs):
    """Reads an XYZ-style file with i-PI style comments and returns data in raw format for further units transformation
    and other post processing.

    Args:
        filedesc: An open readable file object from a xyz formatted file with i-PI header comments.

    Returns:
        i-Pi comment line, cell array, data (positions, forces, etc.), atoms names and masses
    """

    try:
        natoms = int(filedesc.__next__())
    except (StopIteration, ValueError):
        raise EOFError

    # if natoms == '':              # Work with temporary files
    #     raise EOFError

    # natoms = int(natoms)

    comment = filedesc.__next__()

    # Extracting cell
    cell = [key.search(comment) for key in cell_re]
    usegenh = False
    if cell[0] is not None:    # abcABC
        a, b, c  = [float(x) for x in cell[0].group(1).split()[:3]]
        alpha, beta, gamma = [float(x) * np.pi/180.0
                              for x in cell[0].group(1).split()[3:6]]
        h = abc2h(a, b, c, alpha, beta, gamma)
    elif cell[1] is not None:  # GENH
        h = np.array(cell[1].group(1).split()[:9], float)
        h.resize((3,3))
    elif cell[2] is not None:  # H
        genh = np.array(cell[2].group(1).split()[:9], float)
        genh.resize((3,3))
        invgenh = np.linalg.inv(genh)
        # convert back & forth from abcABC representation to get an upper triangular h
        h = abc2h(*genh2abc(genh))
        usegenh = True
    else:                     # defaults to unit box
        h = np.array([[-1.0, 0.0, 0.0],[0.0, -1.0, 0.0],[0.0, 0.0, -1.0]])
    cell = h

    qatoms = np.zeros(3*natoms)
    names = np.zeros(natoms,dtype='|S4')
    masses = np.zeros(natoms)

    # Extracting a time-frame information
    atom_counter = 0
    for iat, line in enumerate(filedesc):
        body = line.split()
        names[iat], masses[iat] = body[0], Elements.mass(body[0])
        x, y, z = float(body[1]), float(body[2]), float(body[3])

        # TODO: The following in matrices would use vectorial computaiton
        if usegenh:
            # must convert from the input cell parameters to the internal convention
            u = np.array([x,y,z])
            us = np.dot(u, invgenh)
            u = np.dot(h, us)
            x, y, z = u

        qatoms[3*iat], qatoms[3*iat+1], qatoms[3*iat+2] = x, y, z
        atom_counter +=1
        if atom_counter == natoms:
            break


    if natoms != len(names):
        raise ValueError("The number of atom records does not match the header of the xyz file.")

    return comment, cell, qatoms, names, masses


def read_pdb(filedesc, **kwargs):
    """Reads a PDB-style file and creates an Atoms and Cell object.

    Args:
        filedesc: An open readable file object from a pdb formatted file.

    Returns:
        An Atoms object with the appropriate atom labels, masses and positions,
        and a Cell object with the appropriate cell dimensions and an estimate
        of a reasonable cell mass.
    """

    header = filedesc.readline()
    comment = ''
    if "TITLE" in header:
        # skip the comment field
        comment = copy.copy(header)
        header = filedesc.readline()
    if 'positions{' not in comment:
        comment = comment.strip()
        comment += ' positions{angstrom}\n'
    if 'cell{' not in comment:
        comment = comment.strip()
        comment += ' cell{angstrom}\n'
    if header == "":
        raise EOFError("End of file or empty header in PDB file")

    a = float(header[6:15])
    b = float(header[15:24])
    c = float(header[24:33])
    alpha = float(header[33:40])
    beta = float(header[40:47])
    gamma = float(header[47:54])
    alpha *= np.pi/180.0
    beta *= np.pi/180.0
    gamma *= np.pi/180.0
    h = abc2h(a, b, c, alpha, beta, gamma)
    cell = h

    natoms = 0
    body = filedesc.readline()
    qatoms = []
    names = []
    masses = []
    while (body.strip() != "" and body.strip() != "END"):
        natoms += 1
        name = body[12:16].strip()
        names.append(name)
        masses.append(Elements.mass(name))
        x = float(body[31:39])
        y = float(body[39:47])
        z = float(body[47:55])
        qatoms.append(x)
        qatoms.append(y)
        qatoms.append(z)

        body = filedesc.readline()

    return comment, cell, np.asarray(qatoms), np.asarray(names, dtype='|S4'), np.asarray(masses)


def read_binary(filedesc, **kwarg):
    try: 
        cell = np.fromfile(filedesc, dtype=float, count=9)
        cell.shape = (3,3)
        nat = np.fromfile(filedesc, dtype=int, count=1)[0]
        qatoms = np.fromfile(filedesc, dtype=float, count=3*nat)
        nat = np.fromfile(filedesc, dtype=int, count=1)[0]
        names = np.fromfile(filedesc, dtype='|S1', count=nat)
        names = "".join(names)
        names = names.split('|')
        masses = np.zeros(len(names))
    except (StopIteration,ValueError):
        raise EOFError
    return ("", cell, qatoms, names, masses)


def read_to_dict(comment, cell, qatoms, names, masses, output='objects'):
    """Convert the data in the file to a dictionary

    Args:
        comment:
        cell:
        qatoms:
        names:
        masses:
        output:
    """

    return {
        "data": qatoms,
        "masses": masses,
        "names": names,
        "natoms": len(names),
        "cell": cell,
    }


def _get_io_function(mode, io):
    """Returns io function with specified mode.

    This will be determined on the fly based on file name extension and
    available ipi/utils/io/backends/io_*.py backends.

    Args:
        mode: Which format has the file? e.g. "pdb", "xml" or "xyz"
        io: One of "print_path", "print", "read" or "iter"
    """

    mode = mode[mode.find(".")+1:]
    if mode in mode_map:
        mode = mode_map[mode]

    try:
        func = getattr(sys.modules[__name__], io_map[io] % mode)
    except KeyError:
        print("Error: io %s is not supported with mode %s." % (io, mode))
        sys.exit()

    return func


def read_file(mode, filedesc, output="objects", **kwargs):
    """Reads one frame from an open `mode`-style file.

    Args:
        filedesc: An open readable file object from a `mode` formatted file.
        All other args are passed directly to the responsible io function.

    Returns:
        A dictionary as returned by `read_to_dict`.
    """

    reader = _get_io_function(mode, "read")

    return read_to_dict(*reader(filedesc=filedesc, **kwargs), output=output)


def read_file_name(filename):
    """Read one frame from file, guessing its format from the extension.

    Args:
        filename: Name of input file.

    Returns:
        A dictionary with 'atoms', 'cell' and 'comment'.
    """

    return read_file(os.path.splitext(filename)[1], open(filename))


def iter_file(mode, filedesc, output="objects", **kwargs):
    """Takes an open `mode`-style file and yields one Atoms object after another.

    Args:
        filedesc: An open readable file object from a `mode` formatted file.

    Returns:
        Generator of frames dictionaries, as returned by `read_to_dict`.
    """

    reader = _get_io_function(mode, "read")

    try:
        while True:
            yield read_to_dict(*reader(filedesc=filedesc, **kwargs), output=output)
    except EOFError:
        pass


def iter_file_name(filename):
    """Open a trajectory file, guessing its format from the extension.

    Args:
        filename: Filename of a trajectory file.

    Returns:
        Generator of frames (dictionary with 'atoms', 'cell' and 'comment') from the trajectory in `filename`.
    """

    return iter_file(os.path.splitext(filename)[1], open(filename))


def genh2abc(h):
   """ Returns a description of the cell in terms of the length of the
      lattice vectors and the angles between them in radians.

   Takes the representation of the system box in terms of a full matrix
   of row vectors, and returns the representation in terms of the
   lattice vector lengths and the angles between them in radians.

   Args:
      h: Cell matrix in upper triangular column vector form.

   Returns:
      A list containing the lattice vector lengths and the angles between them.
   """

   a = math.sqrt(np.dot(h[0],h[0]))
   b = math.sqrt(np.dot(h[1],h[1]))
   c = math.sqrt(np.dot(h[2],h[2]))
   gamma = math.acos(np.dot(h[0],h[1])/(a*b))
   beta  =  math.acos(np.dot(h[0],h[2])/(a*c))
   alpha = math.acos(np.dot(h[2],h[1])/(b*c))

   return a, b, c, alpha, beta, gamma


def abc2h(a, b, c, alpha, beta, gamma):
   """Returns a lattice vector matrix given a description in terms of the
   lattice vector lengths and the angles in between.

   Args:
      a: First cell vector length.
      b: Second cell vector length.
      c: Third cell vector length.
      alpha: Angle between sides b and c in radians.
      beta: Angle between sides a and c in radians.
      gamma: Angle between sides b and a in radians.

   Returns:
      An array giving the lattice vector matrix in upper triangular form.
   """

   h = np.zeros((3,3) ,float)
   h[0,0] = a
   h[0,1] = b*math.cos(gamma)
   h[0,2] = c*math.cos(beta)
   h[1,1] = b*math.sin(gamma)
   h[1,2] = (b*c*math.cos(alpha) - h[0,1]*h[0,2])/h[1,1]
   h[2,2] = math.sqrt(c**2 - h[0,2]**2 - h[1,2]**2)
   return h
