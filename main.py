#!/usr/bin/env python
#-------------------------------------------------------------------------------
# Name:        main
# Purpose: use a previously written program that processes the output of gaussian
# turning it into a set of dirac input files
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

from london         import London
from j              import *
from integrate      import *
from molecule       import Molecule
from scf            import Scf
from template       import Template
from module         import Module
from job            import Job
from periodic_table import periodic_table
from gauge          import Gauge
from dirac          import Dirac

#log_file = sys.argv[1] #soon we will be receiving the .log file (output from a gaussian processing)
mol_file_name = sys.argv[1]
scf_file_name = sys.argv[2]

#Two main input files
f = open(mol_file_name, 'r')
mol_input = map(string.strip, f.readlines())
f.close()

f = open(scf_file_name, 'r')
scf_input = map(string.strip, f.readlines())
f.close()

#this guy is wrapping the call to the existing library cris_utility that have the ability to generate the xyz
#necessary for the rest of the processing
#xyz_file = cris_utility.getXyz(log_file)#pass the .log file

#now I gotta generate the .mol
#mol_input = create_mol(xyz_file)

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

london_folder   = output_path + os.sep + 'london' + os.sep
gauge_folder    = output_path + os.sep + 'gauge' + os.sep

os.mkdir(output_path)
os.mkdir(london_folder)
os.mkdir(gauge_folder)

##mol_file_copy = output_path + os.sep + os.path.basename(mol_file_name)
##shutil.copy2(mol_file_name, mol_file_copy)

print 'Working on the following files'
print 'Mol file: '+ mol_file_name
print 'SCF file: ' + scf_file_name
print 'Output folder: ' + output_path

#end of file creation/manipulation module

#write the files
try:
    #assemble input
    #the template should be static, as the periodic table
    template    = Template()
    molecule    = Molecule(mol_input)
    scf         = Scf(scf_input, molecule.atoms)

    #if we are runing an inptest, call dirac and change the molecule
    if scf.getModule(template.dirac).getProperty(template, template.inptest):
        dirac = Dirac()
        dirac.run(scf_file_name, mol_file_name)
        #get the output of running Dirac and reset the molecule
        molecule.resetMolecule(dirac.parse())
        #remove the inptest and continue with the calculations
        scf.getModule(template.dirac).removeProperty(template.inptest)

#print the description of each atom
    for atom in molecule.atoms:
        atom.print_mol_file(output_path)
        atom.print_inp_file(periodic_table, scf, template, output_path)

#assemble output of the main files
#1.london
    #1.1 the london file
    london = London(scf, molecule)
    # a master j file
    j_london = J(scf, molecule)

    #1.2. create a j's
    j_london_dia = JDia(j_london)
    j_london_para = JPara(j_london)
    j_london_total = JTotal(j_london)

    #1.3.integrate : gotta pass the j preprocessed by the J class because the integrated is based on it
    #gotta generate one file for each of the axis
    integrate_london_dia_1 = IntegrateDia(j_london_dia, 1)
    integrate_london_dia_2 = IntegrateDia(j_london_dia, 2)
    integrate_london_para_1 = IntegratePara(j_london_para, 1)
    integrate_london_para_2 = IntegratePara(j_london_para, 2)
    integrate_london_total_1 = IntegrateTotal(j_london_total, 1)
    integrate_london_total_2 = IntegrateTotal(j_london_total, 2)

#2. gauge
    #2.1 the gauge file
    gauge = Gauge(scf, molecule)
    #a master j gauge
    j_gauge = J(scf, molecule, False)
    #2.2. create a j's
    j_gauge_dia = JDia(j_gauge)
    j_gauge_para = JPara(j_gauge)
    j_gauge_total = JTotal(j_gauge)
    #2.3.integrate : gotta pass the j preprocessed by the J class because the integrated is based on it
    #gotta generate one file for each of the axis
    integrate_gauge_dia_1 = IntegrateDia(j_gauge_dia, 1)
    integrate_gauge_dia_2 = IntegrateDia(j_gauge_dia, 2)
    integrate_gauge_para_1 = IntegratePara(j_gauge_para, 1)
    integrate_gauge_para_2 = IntegratePara(j_gauge_para, 2)
    integrate_gauge_total_1 = IntegrateTotal(j_gauge_total, 1)
    integrate_gauge_total_2 = IntegrateTotal(j_gauge_total, 2)

#open output files
    scf_file = open(output_path + os.sep + scf_file_name.rsplit(os.sep)[-1], 'w')#pay attention: the scf_file_output has the same name parsed when creting the job file
    mol_file = open(output_path + os.sep + mol_file_name.rsplit(os.sep)[-1], 'w')#pay attention: the scf_file_output has the same name parsed when creting the job file

    london_file            = open(london_folder + 'london.inp', 'w')
    london_job_file        = open(london_folder + 'job.sub', 'w')
    j_london_dia_file      = open(london_folder + 'j_dia.inp', 'w')
    j_london_para_file     = open(london_folder + 'j_para.inp', 'w')
    j_london_total_file    = open(london_folder + 'j_total.inp', 'w')
    int_london_dia_file1   = open(london_folder + integrate_london_dia_1.integrate_name + '.inp', 'w')
    int_london_dia_file2   = open(london_folder + integrate_london_dia_2.integrate_name + '.inp', 'w')
    int_london_para_file1  = open(london_folder + integrate_london_para_1.integrate_name + '.inp', 'w')
    int_london_para_file2  = open(london_folder + integrate_london_para_2.integrate_name + '.inp', 'w')
    int_london_total_file1 = open(london_folder + integrate_london_total_1.integrate_name + '.inp', 'w')
    int_london_total_file2 = open(london_folder + integrate_london_total_2.integrate_name + '.inp', 'w')

    gauge_file            = open(gauge_folder + 'gauge.inp', 'w')
    gauge_job_file        = open(gauge_folder + 'job.sub', 'w')
    j_gauge_dia_file      = open(gauge_folder + 'j_dia.inp', 'w')
    j_gauge_para_file     = open(gauge_folder + 'j_para.inp', 'w')
    j_gauge_total_file    = open(gauge_folder + 'j_total.inp', 'w')
    int_gauge_dia_file1   = open(gauge_folder + integrate_gauge_dia_1.integrate_name + '.inp', 'w')
    int_gauge_dia_file2   = open(gauge_folder + integrate_gauge_dia_2.integrate_name + '.inp', 'w')
    int_gauge_para_file1  = open(gauge_folder + integrate_gauge_para_1.integrate_name + '.inp', 'w')
    int_gauge_para_file2  = open(gauge_folder + integrate_gauge_para_2.integrate_name + '.inp', 'w')
    int_gauge_total_file1 = open(gauge_folder + integrate_gauge_total_1.integrate_name + '.inp', 'w')
    int_gauge_total_file2 = open(gauge_folder + integrate_gauge_total_2.integrate_name + '.inp', 'w')

    london_files = [london_file, j_london_dia_file, j_london_para_file, j_london_total_file, int_london_dia_file1, int_london_para_file1, int_london_total_file1, int_london_dia_file2, int_london_para_file2 , int_london_total_file2, london_job_file]

    gauge_files = [gauge_file, j_gauge_dia_file, j_gauge_para_file, j_gauge_total_file, int_gauge_dia_file1, int_gauge_para_file1, int_gauge_total_file1, int_gauge_dia_file2, int_gauge_para_file2 , int_gauge_total_file2, gauge_job_file]

    other_files = [scf_file, mol_file]

    all_files = [london_files, gauge_files, other_files]
#5.job : this guy gotta be here because the job uses all the file names used for generate all the files
    london_job  = Job(scf_file_name, mol_file_name, london_files, molecule, j_london)
    gauge_job = Job(scf_file_name, mol_file_name, gauge_files, molecule, j_gauge)

    london_objects = [  london,
                        j_london_dia, j_london_para, j_london_total,
                        integrate_london_dia_1, integrate_london_para_1, integrate_london_total_1, integrate_london_dia_2, integrate_london_para_2, integrate_london_total_2, london_job]
    gauge_objects = [   gauge,
                        j_gauge_dia, j_gauge_para, j_gauge_total,
                        integrate_gauge_dia_1, integrate_gauge_para_1, integrate_gauge_total_1, integrate_gauge_dia_2, integrate_gauge_para_2, integrate_gauge_total_2, gauge_job]
    other_objects = [   scf, molecule ]

    for i in range(len(london_files)):
        london_files[i].write(str(london_objects[i]))
        london_files[i].close()

    for i in range(len(gauge_files)):
        gauge_files[i].write(str(gauge_objects[i]))
        gauge_files[i].close()

    for i in range(len(other_files)):
        other_files[i].write(str(other_objects[i]))
        other_files[i].close()

except:
    raise
sys.exit()
