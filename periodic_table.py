#!/usr/bin/env python
#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      ezequiel
#
# Created:     29/09/2012
# Copyright:   (c) ezequiel 2012
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from atoms import Atom

#atomic number(Z) symbol	fancy_name
H   = Atom(1,       'H',    'hydrogen'  )
He  = Atom(2,       'He',   'helium'    )
Li  = Atom(3,       'Li',   'lithium'   )
Be  = Atom(4,       'Be',   'beryllium' )
B   = Atom(5,       'B',    'boron'     )
C   = Atom(6,       'C',    'carbon'    )
N   = Atom(7,       'N',    'nitrogen'  )
O   = Atom(8,       'O',    'oxygen'    )
F   = Atom(9,       'F',    'fluorine'  )
Ne  = Atom(10,      'Ne',   'neon'      )
Na  = Atom(11,      'Na',   'sodim'     )
Mg  = Atom(12,      'Mg',   'magnesium' )
Al  = Atom(13,      'Al',   'aluminum'  )
Si  = Atom(14,      'Si',   'silicon'   )
P   = Atom(15,      'P',    'phosphorus')
S   = Atom(16,      'S',    'sulfur'    )
Cl  = Atom(17,      'Cl',   'chlorine'  )
Ar  = Atom(18,      'Ar',   'argon'     )
K   = Atom(19,      'K',    'potassium' )
Ca  = Atom(20,      'Ca',   'calcium'   )
Sc  = Atom(21,      'Sc',   'scandium'  )
Ti  = Atom(22,      'Ti',   'titanium'  )
V   = Atom(23,      'V',    'vanadium'  )
Cr  = Atom(24,      'Cr',   'chromium'  )
Mn  = Atom(25,      'Mn',   'manganese' )
Fe  = Atom(26,      'Fe',   'iron'      )
Co  = Atom(27,      'Co',   'cobalt'    )
Ni  = Atom(28,      'Ni',   'nickel'    )
Cu  = Atom(29,      'Cu',   'copper'    )
Zn  = Atom(30,      'Zn',   'zinc'      )
Ga  = Atom(31,      'Ga',   'gallium'   )
Ge  = Atom(32,      'Ge',   'germanium' )
As  = Atom(33,      'As',   'arsenic'   )
Se  = Atom(34,      'Se',   'selenium'  )
Br  = Atom(35,      'Br',   'bromine'   )
Kr  = Atom(36,      'Kr',   'krypton'   )
Ac  = Atom(89,      'Ac',   'actinium'  )


periodic_table = {  'H' : H,
                    'He': He,
                    'Li': Li,
                    'Be': Be,
                    'B' : B,
                    'C' : C,
                    'N' : N,
                    'O' : O,
                    'F' : F,
                    'Ne': Ne,
                    'Na': Na,
                    'Mg': Mg,
                    'Al': Al,
                    'Si': Si,
                    'P' : P,
                    'S' : S,
                    'Cl': Cl,
                    'Ar': Ar,
                    'K' : K,
                    'Ca': Ca,
                    'Sc': Sc,
                    'Ti': Ti,
                    'V' : V,
                    'Cr': Cr,
                    'Mn': Mn,
                    'Fe': Fe,
                    'Co': Co,
                    'Ni': Ni,
                    'Cu': Cu,
                    'Zn': Zn,
                    'Ga': Ga,
                    'Ge': Ge,
                    'As': As,
                    'Se': Se,
                    'Br': Br,
                    'Kr': Kr,
                    'Ac': Ac}