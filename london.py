#!/usr/bin/env python

#import os
from molecule import Molecule
from module import Module,Property,SubModule

#considering that the only change to be done in this file is regarding the plane and the symmetry
#nothing else is been taken from the mol and the scf.inp files
def write_london(template, scf, molecule):
    printable = ''
    for module in scf.modules:
        if module.name != template.visual.name:
            printable += module.__str__()

    nmr = SubModule('*NMR')
    nmr.add_property(template, '.LONDON')
    nmr.add_property(template, '.DOEPRN')
    nmr.add_property(template, '.INTFLG', [molecule.symmetry])

    newModule = Module('**PROPERTIES')
    newModule.add_property(template, '.' + molecule.magnetic_field)
    newModule.submodules.update({'*NMR':nmr})

    printable += newModule.__str__()
    printable += '*END OF\n'
    return printable
