#!/usr/bin/env python
#-------------------------------------------------------------------------------
# Name:        module1
# Purpose: use a previously written program that processes the output of gaussian
# turning it into a
#
# Author:      ezequiel.barboza
#
# Created:     01/08/2012
# Copyright:   (c) ezequiel.barboza 2012
# Licence:     GPL
#-------------------------------------------------------------------------------

import sys
import string
import os
import shutil

from london     import write_london
from j          import write_j_dia, write_j_para, write_j_total
from integrate import Integrate#write_integrate_dia, write_integrate_para, write_integrate_total

#log_file = sys.argv[1] #soon we will be receiving the .log file (output from a gaussian processing)
mol_file_name = sys.argv[1]
scf_file_name = sys.argv[2]

f = open(mol_file_name, 'r')
mol_file = map(string.strip, f.readlines())
f.close()

f = open(scf_file_name, 'r')
scf_file = map(string.strip, f.readlines())
f.close()

#this guy is wrapping the call to the existing library cris_utility that have the ability to generate the xyz
#necessary for the rest of the processing
#xyz_file = cris_utility.getXyz(log_file)#pass the .log file

#now I gotta generate the .mol
#mol_file = create_mol(xyz_file)

#file manipulation module

#look for folders containing the defined pattern for the name of output folders: execution_n,
#increment the folder name until one that does not exists is found
execution_folder = "execution_"
execution_seq = 1
output_path = ""
complete_path = ""

while len(output_path) == 0 :
    complete_path = "".join([os.getcwd(), os.sep, execution_folder, str(execution_seq)])
    if not os.path.exists(complete_path) :
        output_path = complete_path
    execution_seq += 1

os.mkdir(output_path)

mol_file_copy = output_path + os.pathsep + os.path.basename(mol_file_name)
shutil.copy2(mol_file_name, mol_file_copy)

scf_file_copy = output_path + os.pathsep + os.path.basename(scf_file_name)
shutil.copy2(scf_file_name, scf_file_copy)

print 'Working on the following files'
print 'Mol file: '+ mol_file_name
print 'SCF file: ' + scf_file_name
print 'Output folder: ' + output_path

#by 05/08, we are dealing directly with the mol.mol file
#integrated_dia_file     = open(''.join([output_path, os.sep, "integrate_dia.inp"]), 'w')
#integrate_para_file     = open(''.join([output_path, os.sep, "integrate_para.inp"]), 'w')
#integrate_total_file    = open(''.join([output_path, os.sep, "integrate_total.inp"]), 'w')
j_dia_file              = open(''.join([output_path, os.sep, "j_dia.inp"]), 'w')
j_para_file             = open(''.join([output_path, os.sep, "j_para.inp"]), 'w')
j_total_file            = open(''.join([output_path, os.sep, "j_total.inp"]), 'w')
london_file             = open(''.join([output_path, os.sep, "london.inp"]), 'w')
#end of file creation/manipulation module

#write_integrate_dia_file(integrated_dia_file, scf_file, mol_file)
#THE HANDLING OF THESE FILES WHERE DELEGATED TO THE SPECIFIC CODE
#integrated_dia_file, integrate_para_file, integrate_total_file,
output_files = [j_dia_file, j_para_file, j_total_file, london_file]
try:
    write_london(london_file, scf_file, mol_file)

    write_j_dia(j_dia_file, mol_file)
    write_j_para(j_para_file, mol_file)
    write_j_total(j_total_file, mol_file)

    integrate = Integrate(output_path, mol_file)
    integrate.write_integrate_dia()
    integrate.write_integrate_para()
    integrate.write_integrate_total()

except:
    raise
##    print 'Erro...'
##    # in the end, close everything
##    for file_ in output_files :
##        file_.close()
##
##    mol_file.close()
##    scf_file.close()

##    sys.exit()
# in the end, close everything
for file_ in output_files :
    file_.close()
sys.exit()