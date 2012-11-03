#-------------------------------------------------------------------------------
# Name:        dirac
# Purpose:
#
# Author:      ezequiel
#
# Created:     28/10/2012
# Copyright:   (c) ezequiel 2012
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import subprocess
import re
import os
import string

from molecule import Molecule
from periodic_table import periodic_table

class Dirac:
    def __init__(self, scf_file_name, mol_file_name, molecule_original):
        self.scf_file_name = scf_file_name
        self.mol_file_name = mol_file_name
        self.molecule_original = molecule_original

    def run(self):
        retcode = subprocess.call(["pam", "--global-scratch-disk", "--inp="+self.scf_file_name, "--mol="+self.mol_file_name])

    def parse(self):

        scf_mol_file_name = os.getcwd() + os.sep + 'scf_mol.out'

        beginPattern = re.compile('Centered and rotated coordinates.*')
        endPattern = re.compile('The following elements were found.*')

        f = open(scf_mol_file_name, 'r')
        scf_mol_file = map(string.strip, f.readlines())
        f.close()

        atoms = []
        i = 0
        while i < len(scf_mol_file):
            line = scf_mol_file[i]
            if re.match(beginPattern, line):
                while not re.match(endPattern, line) and i < len(scf_mol_file):
                    i += 1
                    line = scf_mol_file[i]
                    if re.match(Molecule.atom_pattern, line):
                        symbol = line.split()[0]
                        coordinates = line.split()[1:4]
                        if symbol in atoms:
                            atoms[atoms.index(symbol)].coordinates.append(coordinates)
                        elif periodic_table.get(symbol):
                            atom = periodic_table.get(symbol).copy()
                            #copy the basis from the original file
                            original_atoms = self.molecule_original.atoms
                            atom.basis = original_atoms[original_atoms.index(symbol)].basis
                            #added the coordinates
                            atom.coordinates.append(coordinates)
                            atoms.append(atom)
                        else:
                            raise InvalidAtom(symbol)
                break
            i += 1
        return atoms