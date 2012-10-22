#!/usr/bin/env python
#-------------------------------------------------------------------------------
# Name:        integrate
#
# Purpose:      turn one scf input file into a set of integrate files
#
# Author:      ezequiel.barboza
#
# Created:     18/10/2012
# Copyright:   (c) ezequiel.barboza 2012
# Licence:     GPL
#-------------------------------------------------------------------------------

import os

from j import J

class Integrate(J):
    axis_enum = ['X', 'Y', 'Z']#enumeration of the axis
    # each index in the arrays represent an axis
    #gross translation of what is a dot, to number index in a array [x,y,z]=[0,0,0]
    #retrieve the perpendicular plane in a molecule (the plane where most atoms are closer to zero)
    XZ = [0,2]
    YZ = [1,2]
    XY = [0,1]

    #since I found the perpendicular axis of a molecule, I can say that I can tranform it in two directions
    #say, it is Z, there are (at least) two perpendicular self.p_planes to the molecule,
    #XZ and YZ, then, I don't move the center of the coordinates: line1
    #but move the other two, since there are 2 possibilities, we have to create 2 output files
    #self.p_planes discovered, lets assemble 2 possible outputs
    line1 = ['0.0', '0.0', '0.0']#each of this lines in the file, represent a line to be written to the output
    line2 = ['0.0', '0.0', '0.0']#coordinates in the cartesian space
    line3 = ['0.0', '0.0', '0.0']

    def __init__(self, j, molecule, which_plane=1):
##        j = J()
        teste = j.__class__()
        super(self, j)
        self.validateJ(j)
        self.modules = j.copy().modules
        template = self.template#it is just easier to refer like this
        self.p_planes = [YZ, XZ] if molecule.p_axis == 'Z' else [XZ, XY] if molecule.p_axis == 'X' else [YZ, XY]

        two_d_int = self.createTwoDIntProperty(which_plane)

        self.getModule(template.visual).removeProperty(template.two_d)
        self.getModule(template.visual).addProperty(template, two_d_int)

    def createTwoDIntProperty(self, which_plane):
        if which_plane == 2 :
            indexForLine2 = self.p_planes[1][0]#this is the value of the first axis
            indexForLine3 = self.p_planes[1][1]#this is the value of the second axis
        else :
            indexForLine2 = self.p_planes[0][0]#this is the value of the first axis
            indexForLine3 = self.p_planes[0][1]#this is the value of the second axis

        line2[indexForLine2] = '10.0'
        line3[indexForLine3] = '10.0'

        values = []
        values.append(' '.join(line1))
        values.append(' '.join(line2))
        values.append('10')
        values.append(' '.join(line3))
        values.append('10')
        values.append('10')

        two_d_int = self.template.two_d_int.shallow_copy()
        two_d_int.add_values(self.template, values)

        return two_d_int
