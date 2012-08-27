#!/usr/bin/env python

#import os
from mol import get_p_plane

#considering that the only change to be done in this file is regarding the plane and the symmetry
#nothing else is been taken from the mol and the scf.inp files
def write_london(london_file, scf_file, mol_file):
    for line in scf_file.readlines():
        trimmed = line.strip()
        if trimmed != '*END OF':
            london_file.write(trimmed)
            london_file.write('\n')
        else :
            london_file.write('**PROPERTIES')
            london_file.write('\n')
            plane = get_p_plane(mol_file)
            london_file.write(plane)
            london_file.write('\n')
            london_file.write('*NMR')
            london_file.write('\n')
            london_file.write('.LONDON')
            london_file.write('\n')
            london_file.write('.DOEPRN')
            london_file.write('\n')
            london_file.write('.INTFLG')
            london_file.write('\n')
            symmetry = '0 1 1' if plane == 'BXLAO' else '1 0 1' if plane == 'BYLAO' else '1 1 0'
            london_file.write(symmetry)
            london_file.write('\n')
            london_file.write('*END OF')
