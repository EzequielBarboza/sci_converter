#!/usr/bin/env python

#decide which of the planes are perpendicular to the molecule plane

#class Molecule:
#refactor, this should be a class,
#the contents of a molecule should be a map of strings
def get_p_plane(mol_file):
    totalizator = [0,0,0]
    index_ = 0
    for line in mol_file.readlines() :
        if len(line.split()) >= 4 :
            x = abs(float(line.split()[1])) if is_number(line.split()[1])else ""
            y = abs(float(line.split()[2])) if is_number(line.split()[2])else ""
            z = abs(float(line.split()[3])) if is_number(line.split()[3])else ""
            if x == "" or y == "" or z == "" :#do not compute invalid lines
                continue
            index_ = 0 if x < y and x < z else 1 if y < z and y < x else 2
            totalizator[index_] += 1
    if totalizator[0] > totalizator[1] :
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
def get_biggest_coordinate(mol_file):
    biggest_ = 0
    for line in mol_file.readlines() :
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
