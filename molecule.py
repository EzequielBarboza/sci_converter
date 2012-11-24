#!/usr/bin/env python
#-------------------------------------------------------------------------------
# Name:        molecule
# Purpose:
# The execution of the cris_utility can generate files in the following format:
# 1. Gaussian: Files with a header given
# 2. Chemcraft: the same content from the above, without the header
# 3. Dalton: The same content of the first, but with the atoms grouped by type
#
# from a file in the format of a Dirac mol (which could be generated from the above
# extraction process, a set of information could be extracted:
# 1. The perpendicular axis to the molecule;
# 2. The biggest coordinate of the molecule;
# 3. The diferent atoms that compose the molecule,
#       and mapping to a eletronic distribution given by the Atom enum
#
#
# Author:      ezequiel.barboza
#
# Created:     01/08/2012
# Copyright:   (c) ezequiel.barboza 2012
# Licence:     GPL
#-------------------------------------------------------------------------------
import re

from commons        import  *
from atoms          import  Atom
from periodic_table import  periodic_table
import string

#keep information that can be retrieved from a mol file
#a mol file is a collection of Atoms
class Molecule():
    basis_pattern = re.compile('.+ BASIS .+')
    atom_declaration_pattern = re.compile(' +[1-9]\. +[1-9]{2,2}')
    atom_pattern = re.compile('[A-Z]{1,1}[a-z]* +[-]{0,1}[0-9]+\.[0-9]+ +[-]{0,1}[0-9]+\.[0-9]+ +[-]{0,1}[0-9]+\.[0-9]+')
    #the molecule is a file in a format given in the specifications
    #this file gives us a set of properties, which are extracted using the below routines
    def __init__(self, mol_file):
        (self.atoms, self.header) = self.parse(mol_file)
        (self.perpendicularAxis, self.biggestCoordinate) = self.initializeProperties()
        self.magneticField = 'B' + self.perpendicularAxis + 'LAO'

    def resetMolecule(self, atoms):
        self.atoms = atoms
        (self.perpendicularAxis, self.biggestCoordinate) = self.initializeProperties()
        self.magneticField = 'B' + self.perpendicularAxis + 'LAO'

#parsing: We are assuming that:
    def parse(self, mol_file):
        atoms = []
        #mol_file[0] = DIRAC|INTGRL
        #mol_file[1] = file name
        #mol_file[3] = C=Cartesian, n= number of different atoms in molecule, {0} with symmetry? A in angstrons
        molecule_header = [mol_file[0], mol_file[1], mol_file[2], mol_file[3]]
        for i in range(5, len(mol_file)):
            line = mol_file[i]
            if re.match(Molecule.basis_pattern, line):
                atoms[-1].basis = line.strip()
            elif re.match(Molecule.atom_pattern, line):
                symbol = line.split()[0]
                coordinates = line.split()[1:4]
                if symbol in atoms:
                    atoms[atoms.index(symbol)].coordinates.append(coordinates)
                elif periodic_table.get(symbol):
                    atom = periodic_table.get(symbol).copy()
                    atom.coordinates.append(coordinates)
                    atoms.append(atom)
                else:
                    raise InvalidAtom(symbol)
        return (atoms, molecule_header)

#go by every atom of the molecule and get the coordinate closest to zero
#the perpendicular axis to a molecule is found looking at every atom and getting the smallest values
#the axis with more small values is the winner: it is the perpendicular axis to the molecule
    def initializeProperties(self):
        totalizatorPerpendicular = [0, 0, 0]#each of the indexes refer to an axis of the cartesian space
        biggestCoordinate = float("-inf")
        for atom in self.atoms:
            for coordinate in atom.coordinates:
                axis = [
                    ('X', 0, abs(float(coordinate[0]))),
                    ('Y', 1, abs(float(coordinate[1]))),
                    ('Z', 2, abs(float(coordinate[2])))]
                temp = sorted(axis, key=lambda eixo:eixo[2] )
                totalizatorPerpendicular[temp[0][1]] += 1
                biggestCoordinate = temp[2][2] if temp[2][2] > biggestCoordinate else biggestCoordinate
        greater = 0
        for i in range(len(totalizatorPerpendicular)):
            if totalizatorPerpendicular[i] > totalizatorPerpendicular[greater]:
                greater = i
        return (axis_enum[greater], biggestCoordinate)

    def __str__(self):
        printable = ''
        for line in self.header:
            printable += line + NEW_LINE
        for atom in self.atoms:
            printable += six_spaces + str(atom.z) + '.' + three_spaces + str(len(atom.coordinates)) + NEW_LINE
            for coordinate in atom.coordinates:
                printable += atom.symbol + eight_spaces + six_spaces.join(map(str, coordinate)) + NEW_LINE
            printable += atom.basis + NEW_LINE
        printable += FINISH + NEW_LINE
        return printable

#gotta parse the molecule file and create its units. latter the mol file will be reconstructed and can be recreated too, adding or changing the atoms.
##    def set_atoms(self, atoms)

