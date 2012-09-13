#!/usr/bin/env python

from commons import is_number

#keep information that can be retrieved from a mol file
class Molecule():

    #the molecule is a file in a format given in the specifications
    #this file gives us a set of properties, which are extracted using the below routines
    def __init__(self, mol_file):
        self.axis_enum = ['X', 'Y', 'Z']
        self.mol_file = mol_file
#calculating the perpendicular axis to the molecule
#go by every atom of the molecule and get the coordinate closest to zero
#the perpendicular axis to a molecule is found looking at every atom and getting the smallest values
#the axis with more small values is the winner: it is the perpendicular axis to the molecule
        self.p_axis = self.get_p_axis()
        self.biggest_coordinate = self.get_biggest_coordinate()
        self.symmetry = '0 1 1' if self.p_axis == 'X' else '1 0 1' if self.p_axis == 'Y' else '1 1 0'
        self.magnetic_field = 'B'+self.p_axis+'LAO'

    #the contents of a molecule should be a map of strings
    def get_p_axis(self):
        totalizator = [0, 0, 0]#each of the indexes refer to an axis of the cartesian space
        for line in self.mol_file :#run through the file searching for values near 0 'zero'
            data = line.split()
            if len(data) >= 4:#it is agreed that the lines must have this length and all the values should be numbers
                if not is_number(data[1]) : continue
                if not is_number(data[2]) : continue
                if not is_number(data[3]) : continue

                axis = [
                    ('X', 0, abs(float(data[1]))),
                    ('Y', 1, abs(float(data[2]))),
                    ('Z', 2, abs(float(data[3])))]
                temp = sorted(axis, key=lambda eixo:eixo[2] )

                totalizator[temp[0][1]] += 1

        greater = 0
        for i in range(len(totalizator)):
            if totalizator[i] > totalizator[greater]:
                greater = i
        return self.axis_enum[greater]

    #wouldn't be better to have a constructor to initialize the molecule, defining which is the
    #perpendicular axis, the biggest coordinate, and do so on?
    def get_biggest_coordinate(self):#get the biggest coordinate of any atom in a molucule in any axis
        biggest_ = 0
        for line in self.mol_file :
            if len(line.split()) >= 4 :
                x = abs(float(line.split()[1])) if is_number(line.split()[1])else ""
                y = abs(float(line.split()[2])) if is_number(line.split()[2])else ""
                z = abs(float(line.split()[3])) if is_number(line.split()[3])else ""
                if x == "" or y == "" or z == "" :#do not compute invalid lines
                    continue
                if biggest_ < x :
                    biggest_ = x
                if biggest_ < y :
                    biggest_ = y
                if biggest_ < z:
                    biggest_ = z
        return biggest_
