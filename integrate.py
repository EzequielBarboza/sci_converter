#!/usr/bin/env python

import os

from molecule import Molecule
from module import Property

class Integrate():
    def __init__(self, template, scf, molecule):
        self.template = template
        self.scf = scf.copy()
        self.visual = self.scf.remove(template.visual.name)
        self.hamiltonian = self.scf.contains(template.hamiltonian.name)
#remove the .2D - it will be exchanged by the .2D_INT
        self.visual.properties.pop(template.two_d.name, None)

        self.printable = ''
        for module in self.scf.modules:
            self.printable += module.__str__()

        self.axis_enum = ['X', 'Y', 'Z']#enumeration of the axis
        # each index in the arrays represent an axis
        #gross translation of what is a dot, to number index in a array [x,y,z]=[0,0,0]
        #retrieve the perpendicular plane in a molecule (the plane where most atoms are closer to zero)
        XZ = [0,2]
        YZ = [1,2]
        XY = [0,1]

        self.p_planes = [YZ, XZ] if molecule.p_axis == 'Z' else [XZ, XY] if molecule.p_axis == 'X' else [YZ, XY]

        #now, calculating
        #since I found the perpendicular axis of a molecule, I can say that I can tranform it in two directions
        #say, it is Z, there are (at least) two perpendicular self.p_planes to the molecule,
        #XZ and YZ, then, I don't move the center of the coordinates: line1
        #but move the other two, since there are 2 possibilities, we have to create 2 output files
        #self.p_planes discovered, lets assemble 2 possible outputs
        line1 = ['0.0', '0.0', '0.0']#each of this lines in the file, represent a line to be written to the output
        line2 = ['0.0', '0.0', '0.0']#coordinates in the cartesian space
        line3 = ['0.0', '0.0', '0.0']
        indexForLine2 = self.p_planes[0][0]#this is the value of the first axis
        indexForLine3 = self.p_planes[0][1]#this is the value of the second axis
        line2[indexForLine2] = '10.0'
        line3[indexForLine3] = '10.0'

        self.option1 = []
        self.option1.append(' '.join(line1))
        self.option1.append(' '.join(line2))
        self.option1.append('10')
        self.option1.append(' '.join(line3))
        self.option1.append('10')
        self.option1.append('10')

        #reset everything
        line2 = ['0.0', '0.0', '0.0']
        line3 = ['0.0', '0.0', '0.0']
        indexForLine2 = self.p_planes[1][0]#this is the value of the first axis
        indexForLine3 = self.p_planes[1][1]#this is the value of the second axis
        line2[indexForLine2] = '10.0'
        line3[indexForLine3] = '10.0'

        self.option2 = []
        self.option2.append(' '.join(line1))
        self.option2.append(' '.join(line2))
        self.option2.append('10')
        self.option2.append(' '.join(line3))
        self.option2.append('10')
        self.option2.append('10')

#prepare the assembly of each of the inputs
        self.option1_two_d_int = Property(template.two_d_int.name)
        self.option2_two_d_int = Property(template.two_d_int.name)

        self.option1_two_d_int.add_values(self.template, self.option1)
        self.option2_two_d_int.add_values(self.template, self.option2)

    def write_integrate_dia(self) :
        #if we have lvcorr
        backup_para = self.visual.properties.pop(self.template.j.name, None)#remove the para information

        #change the name of the jdia property to j
        if self.hamiltonian.properties.get(self.template.lvcorr.name):
            backup_dia = visual.properties.pop(self.template.jdia.name, None)
            if backup_dia :
                newDia = Property(self.template.j.name)
                newDia.add_values(self.template, backup_dia.values)
                self.visual.properties.update({newDia.name:newDia})

        printable1 = self.printable
        printable1 += self.visual.__str__()
        printable1 += self.option1_two_d_int.__str__()
        printable1 += '*END OF\n'

        printable2 = self.printable
        printable2 += self.visual.__str__()
        printable2 += self.option2_two_d_int.__str__()
        printable2 += '*END OF\n'

        self.visual.properties.update({self.template.j.name:backup_para})#puts the para back where it belongs

        if self.hamiltonian.properties.get(self.template.lvcorr.name):
            self.visual.properties.update({backup_dia.name:backup_dia})

        return (printable1, printable2)

    def write_integrate_para(self):
##        self.visual = self.scf.contains(self.template.visual.name)
        #remove temporary the dia property
        backup_dia = self.visual.properties.pop(self.template.jdia.name, None)
        #print the module
        printable1 = self.printable# se essa merda nao copiar a merda da string essa merda de linguagem que va a merda
        printable1 += self.visual.__str__()
        printable1 += self.option1_two_d_int.__str__()
        printable1 += '*END OF\n'

        printable2 = self.printable
        printable2 += self.visual.__str__()
        printable2 += self.option2_two_d_int.__str__()
        printable2 += '*END OF\n'
        #restore the backup of the dia information
        self.visual.properties.update({self.template.jdia.name:backup_dia})

        return (printable1, printable2)

    def write_integrate_total(self):
        if self.hamiltonian.properties.get(self.template.lvcorr.name):
            backup_jdia = self.visual.properties.pop(self.template.jdia.name, None)

            if not backup_jdia:return ('','')

            backup_jdia.name = 'J'

            printable1 = self.printable
            printable1 += self.visual.name + '\n'
            printable1 += backup_jdia.__str__()

            printable2 = self.printable
            printable2 += self.visual.name + '\n'
            printable2 += backup_jdia.__str__()

            for prop in self.visual.properties.itervalues():
                printable1 += prop.__str__()
                printable2 += prop.__str__()
            for sub in self.visual.submodules.itervalues():
                printable1 += sub.__str__()
                printable2 += sub.__str__()

            printable1 += self.option1_two_d_int.__str__()
            printable1 += '*END OF\n'
            printable2 += self.option2_two_d_int.__str__()
            printable2 += '*END OF\n'

            backup_jdia.name = template.jdia.name
            self.visual.properties.update({backup_jdia.name:backup_jdia})
            return (printable1, printable2)

        else:
            return ('','')#for now, we wait for the inclusion of on script to generate the correct jtotal for levy-leblond
