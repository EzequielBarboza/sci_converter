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

from london     import write_london
from j          import write_j_dia, write_j_para, write_j_total
from integrated import write_integrated_dia, write_integrated_para, write_integrated_total

#log_file = sys.argv[1] #soon we will be receiving the .log file (output from a gaussian processing)
mol_file_name = sys.argv[1]
scf_file_name = sys.argv[2]

#open the files
mol_file = open(mol_file_name, 'r')
#input1 = map(string.strip, f.readlines())
#f.close()

scf_file = open(scf_file_name, 'r')
#input2 = map(string.strip, f.readlines())
#f.close()

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

#by 05/08, we are dealing directly with the mol.mol file
#integrated_dia_file     = open(''.join([output_path, os.sep, "integrate_dia.inp"]), 'w')
#integrate_para_file     = open(''.join([output_path, os.sep, "integrate_para.inp"]), 'w')
#integrate_total_file    = open(''.join([output_path, os.sep, "integrate_total.inp"]), 'w')
j_dia_file              = open(''.join([output_path, os.sep, "j_dia.inp"]), 'w')
j_para_file             = open(''.join([output_path, os.sep, "j_para.inp"]), 'w')
j_total_file            = open(''.join([output_path, os.sep, "j_total.inp"]), 'w')
london_file             = open(''.join([output_path, os.sep, "london.inp"]), 'w')
#end of file creation/manipulation module

#write_integrated_dia_file(integrated_dia_file, scf_file, mol_file)
#THE HANDLING OF THESE FILES WHERE DELEGATED TO THE SPECIFIC CODE
#integrated_dia_file, integrate_para_file, integrate_total_file,
output_files = [j_dia_file, j_para_file, j_total_file, london_file]
try:
    write_london(london_file, scf_file, mol_file)

    write_j_dia(j_dia_file, scf_file, mol_file)
    write_j_para(j_para_file, scf_file, mol_file)
    write_j_total(j_total_file, scf_file, mol_file)

    write_integrated_dia(output_path, scf_file, mol_file)
    write_integrated_para(output_path, scf_file, mol_file)
    write_integrated_total(output_path, scf_file, mol_file)

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

mol_file.close()
scf_file.close()

sys.exit()