#!/usr/bin/env python

from commons import is_number

#decide which of the planes are perpendicular to the molecule plane

#class Molecule:
#refactor, this should be a class,
#the contents of a molecule should be a map of strings
def get_p_axis(mol_file):
    totalizator = [0,0,0]#each of the indexes refer to an axis of the cartesian space
    index_ = 0
    for line in mol_file :#run through the file searching for values near 0 'zero'
        if len(line.split()) >= 4 :
            x = abs(float(line.split()[1])) if is_number(line.split()[1])else ""
            y = abs(float(line.split()[2])) if is_number(line.split()[2])else ""
            z = abs(float(line.split()[3])) if is_number(line.split()[3])else ""
            if x == "" or y == "" or z == "" :#do not compute invalid lines
                continue
            index_ = 0 if x < y and x < z else 1 if y < z and y < x else 2#the smaller one is the winner
            totalizator[index_] += 1#and is incremented
    if totalizator[0] > totalizator[1] :#return the string representing the axis that is perpendicular to the plane of the molucule
        if totalizator[0] > totalizator[2] :
            return 'BXLAO'
        else :
            return 'BZLAO'
    elif totalizator[1] > totalizator[2]:
        return 'BYLAO'
    else :
        return 'BZLAO'

#wouldn't be better to have a constructor to initialize the molecule, defining which is the
#perpendicular axis, the biggest coordinate, and do so on?
def get_biggest_coordinate(mol_file):#get the biggest coordinate of any atom in a molucule in any axis
    biggest_ = 0
    for line in mol_file :
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
