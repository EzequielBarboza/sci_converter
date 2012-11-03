#!/usr/bin/env python
#-------------------------------------------------------------------------------
# Name:        atoms
# Purpose: Enummerates the atoms and its eletronic distribution
#
# Author:      ezequiel
#
# Created:     29/09/2012
# Copyright:   (c) ezequiel 2012
# Licence:     GPL
#-------------------------------------------------------------------------------

import string
import os

class Atom():
    t_g = 'gerade'#define the gerade type
    t_u = 'ungerade'#define the ungerade type
    pauling = [(1, t_g, 2),#the distribution of eletrons in each sublayer, associated with the type of the eletrons(regarding the sublayer they occupy)
               (2, t_g, 2),
               (2, t_u, 6),
               (3, t_g, 2),
               (3, t_u, 6),
               (4, t_g, 2),
               (3, t_g, 10),
               (4, t_u, 6),
               (5, t_g, 2),
               (4, t_g, 10),
               (5, t_u, 6),
               (6, t_g, 2),
               (4, t_u, 14),
               (5, t_g, 10),
               (6, t_u, 6),
               (7, t_g, 2),
               (5, t_u, 14),
               (6, t_g, 10),
               (7, t_u, 6)]
    layers_capacity = { 1:2,#the capacity for each layer,
                        2:8,
                        3:18,
                        4:32,
                        5:32,
                        6:18,
                        7:8}

    def __init__(self, z, symbol, fancy_name):
        self.z = z
        self.symbol = symbol
        self.fancy_name = fancy_name
        self.coordinates = []
        (self.cs, self.os) = self.get_shells()
        self.basis = ''
        self.coef  = (self.symbol + '_') if len(self.symbol) < 2 else self.symbol
        self.coef += 'COEF'
        #if there are closed shell, add one to the type of orbitals
        self.types_of_layers = 1 if (self.cs[0] > 0 or self.cs[1] > 0) else 0
        #if there are open shell, add one to the type of orbitals
        if self.os[0] > 0:
            self.types_of_layers += 1

    def copy(self):
        return Atom(self.z, self.symbol, self.fancy_name)

    #prints out the inp representation of this atom
    def print_inp_file(self, periodic_table, scf_file, template, output_path):
        inp_file = scf_file.copy()
        wave_function = inp_file.getModule(template.wave_function)

        if  wave_function:
            scf_submodule = wave_function.submodules.get(template.scf.name)
            if scf_submodule:
                atomst = scf_submodule.properties.get(template.atomst.name)
                if atomst:
                    scf_submodule.properties.pop(atomst.name)
                else: return ''
            else: return ''
        else: return ''

        #copy the new components from the template. They are going to be improved
        closed_shell = template.closed.copy()
        closed_shell.add_value(template, ' '.join(map(str, self.cs[0:2])))
        scf_submodule.addProperty(template, closed_shell)

        if self.os[0] > 0:
            open_shell = template.openshell.copy()
            open_shell.add_value(template, str(self.os[0]))
            open_shell.add_value(template, str(self.os[1]) + '/' + ','.join(map(str, self.os[2])))
            scf_submodule.addProperty(template, open_shell)

        general = template.general.copy()

        #add the newly crated components to the atomfile
        inp_file.addModule(general)
        #get the string representation of the atom#in this case, is a representation of the modules that this atom contains# do not mistake with the atom itself
        printable = inp_file.__str__()
        #print to the output
        output_file = open(output_path + os.sep + self.symbol.lower() + '.inp', 'w')
        output_file.write(printable)
        output_file.close()

    def get_shells(self):
        remainder = self.z
        index = 0
        #[gerade, ungerade, acumulator for the number of orbitals closed, whole capacity allocated(same as summation of 0 and 1 indexes]
        closed = [0, 0, 0, 0]
        #[#of openshells, #of eletrons on the openshells,[capacity of the gerade, capacity of the ungerade], acumulator for the capacity]
        open_shell = [0, 0, [0, 0], 0]
        while remainder > 0:
            layer, _type, capacity = Atom.pauling[index]
            #initializes the number of eletrons entering this orbital
            entering = remainder
            #extracts all that does not fit, due to capacity
            remainder -= capacity

            #adjusts the remainder if all entered
            ## REMEMBER!!! it is just an adjustment, doesn't have nothing to do with the next if/else
            if remainder > 0:
                entering -= remainder
            #if there is already something to be calculated, something is closed
            if remainder >= 0:
                #increments the number of orbitals closed for this atoms(orbitals totally filled)
                closed[2] += 1
                #increments the capacity (it is a property of each orbital)
                closed[3] += capacity
                if _type == Atom.t_g:
                    closed[0] += entering
                else:
                    closed[1] += entering
            else:
                if _type == Atom.t_g:
                    open_shell = [1, entering, [capacity, 0], (open_shell[3]+capacity)]
                else:
                    open_shell = [1, entering, [0, capacity], (open_shell[3]+capacity)]
            index += 1
        return (closed, open_shell)

    # prints out the mol representation of this atom
    def print_mol_file(self, output_path):
        printable = 'DIRAC\n'
        printable += self.fancy_name + ' atom\n'
        printable += '\n'
        #the spaces are important
        printable += 'C   1              A\n'
        printable += '      ' + str(self.z) + '.' + '   1\n'
        #the number of spaces are important
        printable += self.symbol + '        0.000000000      0.000000000      0.000000000\n'
        printable += self.basis + '\n'
        printable += 'FINISH\n'
        #print to the output
        output_file = open(output_path + os.sep + self.symbol.lower() + '.mol', 'w')
        output_file.write(printable)
        output_file.close()

    def __eq__(self, other):
        if isinstance(other, Atom):
            return other.symbol == self.symbol
        elif isinstance(other, str):
            return other == self.symbol
        return False

    def __str__(self):
        printable = self.coef + ' ' + str(self.types_of_layers) + '\n'
        # first the closed, if they exist
        number_of_closed_orbitals = 0
        if self.cs[3] > 0:#just if there is any closed orbitals
            #print the layers
            number_of_closed_orbitals = self.cs[3] / 2 #dont know why the hell it is calculated this bloody way
            if number_of_closed_orbitals > 1:#if there is more than 1 closed orbital, then gotta print from 1..n
                printable += '1..' + str(number_of_closed_orbitals)
            else:
                printable += '1'
            printable += '\n'
            printable += str(float(self.cs[0] + self.cs[1]) / self.cs[3]) #ocupation = lotacao / capacidade#in the end will always be ONE
        # then the opened
        if self.os[3] > 0:
            #depends on whether I want to consider the closed (they might not exist)
            number_of_open_orbitals = self.os[3] / 2
            if number_of_closed_orbitals > 0 :
                printable += '\n'
                printable += str(number_of_closed_orbitals + 1) + '..' + str(number_of_closed_orbitals + number_of_open_orbitals)
            elif number_of_open_orbitals > 1:
                printable += '1..' + str(number_of_open_orbitals)
            else:
                printable += '1'
            printable += '\n'
            printable += str(float(self.os[1]) / self.os[3]) #ocupation = lotacao / capacidade#in the end will always be ONE
        return printable
