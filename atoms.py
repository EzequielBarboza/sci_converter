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
    t_g = 'gerade'
    t_u = 'ungerade'
    pauling = [(1, t_g, 2),
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
    layers_capacity = { 1:2,
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
        (self.cs, self.os) = self.get_shells()
        self.basis = ''
        self.coef  = (self.symbol + '_') if len(self.symbol) < 2 else self.symbol
        self.coef += 'COEF'

    def print_inp_file(self, periodic_table, scf_file, template, output_path):
        atom_file = scf_file.copy()
        wave_function = atom_file.contains(template.wave_function.name)

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
        closed_shell.add_value(template, ' '.join(map(str, self.cs)))
        scf_submodule.addProperty(template, closed_shell)

        if self.os[0] > 0:
            open_shell = template.openshell.copy()
            open_shell.add_value(template, str(self.os[0]))
            open_shell.add_value(template, str(self.os[1]) + '/' + ','.join(map(str, self.os[2])))
            scf_submodule.addProperty(template, open_shell)

        general = template.general.copy()

        #add the newly crated components to the atomfile
        atom_file.addModule(general)
        #get the string representation of the atom
        printable = atom_file.__str__()
        #print to the output
        output_file = open(output_path + os.sep + self.symbol.lower() + '.inp', 'w')
        output_file.write(printable)
        output_file.close()

    def get_shells(self):
        remainder = self.z
        index = 0
        closed = [0, 0]
        open_shell = [0, 0, [0, 0]]
        while remainder > 0:
            layer, _type, capacity = Atom.pauling[index]
            #initializes the number of eletrons entering this orbital
            entering = remainder
            #extracts all that does not fit, due to capacity
            remainder -= capacity

            #adjusts the remainder if all entered
            if remainder > 0:
                entering -= remainder

            if remainder >= 0:
                if _type == Atom.t_g:
                    closed[0] += entering
                else:
                    closed[1] += entering
            else:
                if _type == Atom.t_g:
                    open_shell = [1, entering, [capacity, 0]]
                else:
                    open_shell = [1, entering, [0, capacity]]
            index += 1
        return (closed, open_shell)

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





##O   = Atom(8, 'O', new CS(4,        0), new OS(-1,      4))
##F   = Atom(9, 'F', new CS(4,        0), new OS(-1,      5))


##10	                  Ne	        4	        6
##11	                  Na	        4	        6	       1
##12	                  Mg	        6	        6
##13	                  Al	        6	        6		             1
##14	                  Si	        6	        6		             2
##15	                  P	6	6		3
##16	Si	6	6		4
##17	Cl	6	6		5
##18	Ar	6	12
##19	K	6	12	1
##20	Ca	8	12
##21	Sc	8	12	1
##22	Ti	8	12	2
##23	V	8	12	3
##24	Cr	8	12	4
##25	Mn	8	12	5
##26	Fe	8	12	6
##27	Co	8	12	7
##28	Ni	8	12	8
##29	Cu	8	12	9
##30	Zn	18	12
##31	Ga	18	12		1
##32	Ge	18	12		2
##33	As	18	12		3
##34	Se	18	12		4
##35	Br	18	12		5
##36	Kr	18	18

##    atoms = {   'Ac':   Ac,
##                'C' :   C,
##                'H' :   H,
##                'N' :   N}

###control the opened layers
##            if not opened_layers.has_key(layer):
##                opened_layers.update({layer : entering})
##            else:
##                value = opened_layers.get(layer)
##                opened_layers.update({layer : value + entering })
##
##            elif remainder < 0:
##                if _type == t_g:
##                    open_shell[]
##            if :
##
##            index += 1

##
##class AtomEnum():
##    #atomic number(Z) symbol	closed shell		open shell
##    #		                    gerade	ungerade	gerade	ungerade
##    H   = Atom(1,       'H', new CS(0,	   0), new OS(1,      0))
##    He  = Atom(2, 'He',new CS(2,       -1), new OS(-1,     -1))
##    Li  = Atom(3, 'Li',new CS(3,       -1), new OS(1,      -1))
##    Be  = Atom(4, 'Be',new CS(4,       -1), new OS(-1,     -1))
##    B   = Atom(5, 'B', new CS(4,        0), new OS(-1,      1))
##    C   = Atom(6, 'C', new CS(4,	    0), new OS(-1,      2))
##    N   = Atom(7, 'N', new CS(4,        0), new OS(-1,      3))
##    O   = Atom(8, 'O', new CS(4,        0), new OS(-1,      4))
##    F   = Atom(9, 'F', new CS(4,        0), new OS(-1,      5))

##class CS():
##    def __init__(self, gerade, ungerade):
##        self.gerade = gerade
##        self.ungerade = ungerade
##
##class OS():
##    def __init__(self, gerade, ungerade):
##        self.gerade = gerade
##        self.ungerade = ungerade
