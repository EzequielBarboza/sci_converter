sci_converter
=============

sci_converter

system that allows several convertions between file formats used by scientific programs, like gaussian and dirac

One mol.mol file must be generated from a gaussian output:
	1. gaussian generates a .log file
	2. cris_utility toolset generates a xyz file
	3. this system generates a set of dirac input files
	
Project goals:
	1. Turn the cris_utility into a library
	2. Reuse the cris_utility functionality
	3. From a .log file (gaussian output) add the possibility of generating the set of files that will be the dirac input