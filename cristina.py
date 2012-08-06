#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
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
from london import write_london

#log_file = sys.argv[1] #soon we will be receiving the .log file (output from a gaussian processing)
mol_file_name = sys.argv[1]
scf_file_name = sys.argv[2]

#
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
integrated_dia_file     = open(''.join([output_path, os.sep, "integrate_dia.inp"]), 'w')
integrate_para_file     = open(''.join([output_path, os.sep, "integrate_para.inp"]), 'w')
integrate_total_file    = open(''.join([output_path, os.sep, "integrate_total.inp"]), 'w')
j_dia_london_file       = open(''.join([output_path, os.sep, "j_dia_london.inp"]), 'w')
j_para_london_file      = open(''.join([output_path, os.sep, "j_para_london.inp"]), 'w')
j_total_london_file     = open(''.join([output_path, os.sep, "j_total_london.inp"]), 'w')
london_file             = open(''.join([output_path, os.sep, "london.inp"]), 'w')

#end of file manipulation module

#write_integrated_dia_file(integrated_dia_file, scf_file, mol_file)
output_files = [integrated_dia_file, integrate_para_file, integrate_total_file, j_dia_london_file, j_para_london_file, j_total_london_file, london_file]
try:
    write_london(london_file, scf_file, mol_file)
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