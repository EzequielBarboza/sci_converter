#!/usr/bin/env python

#import os
from mol import get_p_axis

#considering that the only change to be done in this file is regarding the plane and the symmetry
#nothing else is been taken from the mol and the scf.inp files
def write_london(london_file, scf_file, mol_file):
    for line in scf_file:
        if line != '*END OF':
            london_file.write(line + '\n')
        else :
            london_file.write('**PROPERTIES' + '\n')
            plane = get_p_axis(mol_file)
            london_file.write(plane + '\n')
            london_file.write('*NMR\n')
            london_file.write('.LONDON\n')
            london_file.write('.DOEPRN\n')
            london_file.write('.INTFLG\n')
            symmetry = '0 1 1' if plane == 'BXLAO' else '1 0 1' if plane == 'BYLAO' else '1 1 0'
            london_file.write(symmetry + '\n')
            london_file.write('*END OF\n')
