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

from molecule import Molecule

class Dirac:
    def run(self, scf, mol):
        retcode = subprocess.call(["pam", "--global-scratch-disk", "--inp="+scf, "--mol="+mol])

    def parse(self):

        scf_mol_file_name = os.getcwd() + os.sep + 'scf_mol.out'

        beginPattern = re.compile('Centered and rotated coordinates.*')
        endPattern = re.compile('The following elements were found.*')

        f = open(scf_mol_file_name, 'r')
        scf_mol_file = map(string.strip, f.readlines())
        f.close()

        atoms = []
        while i in range(len(scf_mol_file)):
            line = scf_mol_file[i]
            if re.match(beginPattern, line):
                while not re.match(endPattern, line):
                    i += 1
                    line = scf_mol_file[i]
                    if re.match(Molecule.atom_pattern, line):
                        symbol = line.split()[0]
                        coordinates = line.split()[1:4]
                        if symbol in atoms:
                            atoms[atoms.index(symbol)].coordinates.append(coordinates)
                        elif periodic_table.get(symbol):
                            atom = periodic_table.get(symbol).copy()
                            atoms.append(atom)
                        else:
                            raise InvalidAtom(symbol)
                break
        return atoms