#!/usr/bin/env python

#import os
from molecule import Molecule
from module import Module,Property,SubModule
from diracfile import DiracFile

#considering that the only change to be done in this file is regarding the plane and the symmetry
#nothing else is been taken from the mol and the scf.inp files
def write_london(scf, molecule):
    printable = ''
    for module in scf.modules:
        if module.name != DiracFile.visual.name:
            printable += module.__str__()

    nmr = SubModule('*NMR')
    nmr.add_property('.LONDON')
    nmr.add_property('.DOEPRN')
    nmr.add_property('.INTFLG', [molecule.symmetry])

    newModule = Module('**PROPERTIES')
    newModule.add_property('.' + magnetic_field)
    newModule.submodules.update({'*NMR':nmr})

    printable += newModule.__str__()
    printable += '*END OF\n'
