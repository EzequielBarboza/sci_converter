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

from j import *

class Integrate(object):
    axis_enum = ['X', 'Y', 'Z']#enumeration of the axis
    # each index in the arrays represent an axis
    #gross translation of what is a dot, to number index in a array [x,y,z]=[0,0,0]
    #retrieve the perpendicular plane in a molecule (the plane where most atoms are closer to zero)
    XZ = [0,2]
    YZ = [1,2]
    XY = [0,1]

    def integrate(self):
        #calculate what are we supposed to integrate here
        self.p_planes = [self.YZ, self.XZ] if self.molecule.perpendicularAxis == 'Z' else [self.XZ, self.XY] if self.molecule.perpendicularAxis == 'X' else [self.YZ, self.XY]
        #make the integration
        two_d_int = self.createTwoDIntProperty()

        self.getModule(self.template.visual).removeProperty(self.template.two_d)
        self.getModule(self.template.visual).addProperty(self.template, two_d_int)

    def createTwoDIntProperty(self):
        if self.which_plane == 2 :
            indexForLine2 = self.p_planes[1][0]#this is the value of the first axis
            indexForLine3 = self.p_planes[1][1]#this is the value of the second axis
        else :
            indexForLine2 = self.p_planes[0][0]#this is the value of the first axis
            indexForLine3 = self.p_planes[0][1]#this is the value of the second axis

        #resolve the file name
        self.integrate_name = self.integrate_name + '_' + self.axis_enum[indexForLine2] + self.axis_enum[indexForLine3]

        #since I found the perpendicular axis of a molecule, I can say that I can tranform it in two directions
        #say, it is Z, there are (at least) two perpendicular self.p_planes to the molecule,
        #XZ and YZ, then, I don't move the center of the coordinates: line1
        #but move the other two, since there are 2 possibilities, we have to create 2 output files
        #self.p_planes discovered, lets assemble 2 possible outputs
        line1 = ['0.0', '0.0', '0.0']#each of this lines in the file, represent a line to be written to the output
        line2 = ['0.0', '0.0', '0.0']#coordinates in the cartesian space
        line3 = ['0.0', '0.0', '0.0']

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

#I'm a J!!!
class IntegrateDia(JDia, Integrate):
    def __init__(self, jdia, which_plane=1):
        self.integrate_name = 'integrate_dia'
        #basic validation
        self.validateJDia(jdia)
        #grab a copy of the properties
        jdia.copyPropertiesIntoAnotherJ(self)
        #initialize which_plane
        self.which_plane = which_plane
        #do the integration
        self.integrate()

class IntegratePara(JPara, Integrate):
    def __init__(self, jpara, which_plane=1):
        self.integrate_name = 'integrate_para'
        self.validateJPara(jpara)
        #grab a copy of the properties
        jpara.copyPropertiesIntoAnotherJ(self)
        #initialize which_plane
        self.which_plane = which_plane
        #do the integration
        self.integrate()

class IntegrateTotal(JTotal, Integrate):
    def __init__(self, jtotal, which_plane=1):
        self.integrate_name = 'integrate_total'
        self.validateJTotal(jtotal)
        #grab a copy of the properties
        jtotal.copyPropertiesIntoAnotherJ(self)
        #initialize which_plane
        self.which_plane = which_plane
        #do the integration
        self.integrate()
