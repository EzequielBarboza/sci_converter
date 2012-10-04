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

from london         import write_london
from j              import J
from integrate      import Integrate
from molecule       import Molecule
from scf            import Scf
from template       import Template
from module         import Module
from job            import Job
from periodic_table import periodic_table

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

mol_file_copy = output_path + os.sep + os.path.basename(mol_file_name)
shutil.copy2(mol_file_name, mol_file_copy)

scf_file_copy = output_path + os.sep + os.path.basename(scf_file_name)
shutil.copy2(scf_file_name, scf_file_copy)

print 'Working on the following files'
print 'Mol file: '+ mol_file_name
print 'SCF file: ' + scf_file_name
print 'Output folder: ' + output_path


#end of file creation/manipulation module

#write_integrate_dia_file(integrated_dia_file, scf_file, mol_file)
#THE HANDLING OF THESE FILES WHERE DELEGATED TO THE SPECIFIC CODE
#integrated_dia_file, integrate_para_file, integrate_total_file,
try:
    #assemble input
    template = Template()
    scf_file = Scf(template, scf_file)

#print the description of each atom
    molecule = Molecule(mol_file)
    for atom in molecule.atoms:
        atom.print_mol_file(output_path)
        atom.print_inp_file(periodic_table, scf_file, template, output_path)

#assemble output of the main files
    #1.london
    london_text = write_london(template, scf_file, molecule)
    #2.j the processed j file will be passed to the integrate
    j = J(template, scf_file, molecule)
    jdia_text = j.write_j_dia(template)
    jpara_text = j.write_j_para(template)
    jtotal_text = j.write_j_total(template)
    #3.integrate
    integrate = Integrate(template, j.scf, molecule)
    (int_dia_text_1, int_dia_text_2) = integrate.write_integrate_dia()
    (int_para_text_1, int_para_text_2) = integrate.write_integrate_para()
    (int_total_text_1, int_total_text_2) = integrate.write_integrate_total()

#open output the files
    j_dia_file      = open(output_path + os.sep + 'j_dia.inp', 'w')
    j_para_file     = open(output_path + os.sep + 'j_para.inp', 'w')
    j_total_file    = open(output_path + os.sep + 'j_total.inp', 'w')
    int_dia_file1   = open(output_path + os.sep + 'integrate_dia_' + integrate.axis_enum[integrate.p_planes[0][0]] + integrate.axis_enum[integrate.p_planes[0][1]] + '.inp', 'w')
    int_dia_file2   = open(output_path + os.sep + 'integrate_dia_' + integrate.axis_enum[integrate.p_planes[1][0]] + integrate.axis_enum[integrate.p_planes[1][1]] + '.inp', 'w')
    int_para_file1  = open(output_path + os.sep + 'integrate_para_' + integrate.axis_enum[integrate.p_planes[0][0]] + integrate.axis_enum[integrate.p_planes[0][1]] + '.inp', 'w')
    int_para_file2  = open(output_path + os.sep + 'integrate_para_' + integrate.axis_enum[integrate.p_planes[1][0]] + integrate.axis_enum[integrate.p_planes[1][1]] + '.inp', 'w')
    int_total_file1 = open(output_path + os.sep + 'integrate_total_' + integrate.axis_enum[integrate.p_planes[0][0]] + integrate.axis_enum[integrate.p_planes[0][1]] + '.inp', 'w')
    int_total_file2 = open(output_path + os.sep + 'integrate_total_' + integrate.axis_enum[integrate.p_planes[1][0]] + integrate.axis_enum[integrate.p_planes[1][1]] + '.inp', 'w')
    london_file     = open(output_path + os.sep + 'london.inp', 'w')
    job_file        = open(output_path + os.sep + 'job.sub', 'w')
    output_files = [london_file, j_dia_file, j_para_file, j_total_file, int_dia_file1, int_para_file1, int_total_file1, int_dia_file2, int_para_file2 , int_total_file2, job_file]

    #4.job
    job         = Job(scf_file_name, mol_file_name, output_files, molecule, j.lvcorr)
    job_text    = job.write_job()

    j_dia_file.write(jdia_text)
    j_para_file.write(jpara_text)
    j_total_file.write(jtotal_text)
    int_dia_file1.write(int_dia_text_1)
    int_dia_file2.write(int_dia_text_2)
    int_para_file1.write(int_para_text_1)
    int_para_file2.write(int_para_text_2)
    int_total_file1.write(int_total_text_1)
    int_total_file2.write(int_total_text_2)
    london_file.write(london_text)
    job_file.write(job_text)

    for file_ in output_files :
        file_.close()
except:
    raise
sys.exit()
