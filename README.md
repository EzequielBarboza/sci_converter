sci_converter
=============

sci_converter

System that allows several convertions between file formats used by scientific programs, like gaussian and dirac

One mol.mol file must be generated from a gaussian output:
	1. gaussian generates a .log file
	2. cris_utility toolset generates a xyz file
	3. this system generates a set of dirac input files
	
Project goals:
	1. Turn the cris_utility into a library
	2. Reuse the cris_utility functionality
	3. From a .log file (gaussian output) add the possibility of generating the set of files that will be the dirac input
	
Para automatizar a preparação de inputs para o dirac, evitando erros. 
Preparar uma série de cálculos similares

//from a given molecule.mol and an scf.inp files:
DIRAC
Cl-cisfluorenaceno

C   3   0         A
      6.    20
6        0.000000000     -0.537410378      0.000000000
6        1.194777000      0.182558622      0.000000000
6        1.193446000      1.594228622      0.000000000
6        0.000000000      2.309403622      0.000000000
6       -1.193446000      1.594228622      0.000000000
6       -1.194777000      0.182558622      0.000000000
6       -2.615319000      2.114452622      0.000000000
6       -3.436959000      0.843308622      0.000000000
6       -2.588310000     -0.279855378      0.000000000
6        2.615319000      2.114452622      0.000000000
6        3.436959000      0.843308622      0.000000000
6        2.588310000     -0.279855378      0.000000000
6       -3.129721000     -1.565215378      0.000000000
6       -4.514235000     -1.724265378      0.000000000
6       -5.337133000     -0.598692378      0.000000000
6       -4.816695000      0.695278622      0.000000000
6        4.816695000      0.695278622      0.000000000
6        5.337133000     -0.598692378      0.000000000
6        4.514235000     -1.724265378      0.000000000
6        3.129721000     -1.565215378      0.000000000
LARGE BASIS cc-pVDZ
      1.    12
1        2.491910000     -2.442009378      0.000000000
1        4.956258000     -2.712286378      0.000000000
1        5.482349000      1.549957622      0.000000000
1        2.825239000      2.733595622     -0.879807000
1       -2.825239000      2.733595622     -0.879807000
1       -5.482349000      1.549957622      0.000000000
1       -4.956258000     -2.712286378      0.000000000
1       -2.491910000     -2.442009378      0.000000000
1        0.000000000      3.395309622      0.000000000
1        0.000000000     -1.622078378      0.000000000
1       -2.825239000      2.733595622      0.879807000
1        2.825239000      2.733595622      0.879807000
LARGE BASIS cc-pVDZ
     17.    2
17       7.084884000     -0.816284378      0.000000000
17      -7.084884000     -0.816284378      0.000000000
LARGE BASIS cc-pVDZ
FINISH
//explanation:
//firts column: name or atomic number, the other 3 columns: x,y,z coordinates

//scf.inp:
**DIRAC
.WAVE FUNCTION
.PROPERTIES
#.INPTEST
**HAMILTONIAN
.LEVY-LEBLOND
#.URKBAL
**INTEGRALS
*READIN
.UNCONTRACT
*TWOINT
.SCREEN
 1.0D-17
**WAVE FUNCTION
.SCF
*SCF
.EVCCNV
 1.0D-6
.ATOMST
 C_COEF 2
 1..2
 1.0
 3..5
 0.33
 H_COEF 1
 1
 0.5
 N_COEF 2
 1..2
 1.0
 3..5
 0.50
 O_COEF 2
 1..2
 1.0
 3..5
 0.67
*END OF
//

ALL THE OUTPUTS:
J files:
They are 3:
j_dia: 
j_para:
j_total: