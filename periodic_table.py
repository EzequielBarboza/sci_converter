#!/usr/bin/env python
#-------------------------------------------------------------------------------
# Name:        periodic_table
# Purpose:      Keep a static representation of atoms and the periodic table for
#               several calculations
#
# Author:      ezequiel
#
# Created:     29/09/2012
# Copyright:   (c) ezequiel 2012
# Licence:     GPL
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
Rb  = Atom(37,      'Rb',   'rubidium'  )
Sr  = Atom(38,      'Sr',   'strontium' )
Y   = Atom(39,      'Y',    'yttrium'   )
Zr  = Atom(40,      'Zr',   'zirconium' )
Nb  = Atom(41,      'Nb',   'niobium'   )
Mo  = Atom(42,      'Mo',   'molybdenum')
Tc  = Atom(43,      'Tc',   'technetium')
Ru  = Atom(44,      'Ru',   'ruthenium' )
Rh  = Atom(45,      'Rh',   'rhodium'   )
Pd  = Atom(46,      'Pd',   'palladium' )
Ag  = Atom(47,      'Ag',   'silver'    )
Cd  = Atom(48,      'Cd',   'cadmium'   )
In  = Atom(49,      'In',   'indium'    )
Sn  = Atom(50,      'Sn',   'tin'       )
Sb  = Atom(51,      'Sb',   'antimony'  )
Te  = Atom(52,      'Te',   'tellurium' )
I   = Atom(53,      'I',    'iodine'    )
Xe  = Atom(54,      'Xe',   'xenon'     )
Cs  = Atom(55,      'Cs',   'caesium'   )
Ba  = Atom(56,      'Ba',   'barium'    )
La  = Atom(57,      'La',   'lanthanum' )
Ce  = Atom(58,      'Ce',   'cerium'        )
Pr  = Atom(59,      'Pr',   'praseodymium'  )
Nd  = Atom(60,      'Nd',   'neodymium'     )
Pm  = Atom(61,      'Pm',   'promethium'    )
Sm  = Atom(62,      'Sm',   'samarium'      )
Eu  = Atom(63,      'Eu',   'europium'      )
Gd  = Atom(64,      'Gd',   'gadolinium'    )
Tb  = Atom(65,      'Tb',   'terbium'       )
Dy  = Atom(66,      'Dy',   'dysprosium'    )
Ho  = Atom(67,      'Ho',   'holmium'       )
Er  = Atom(68,      'Er',   'erbium'        )
Tm  = Atom(69,      'Tm',   'thulium'       )
Yb  = Atom(70,      'Yb',   'ytterbium'     )
Lu  = Atom(71,      'Lu',   'lutetium'      )
Hf  = Atom(72,      'Hf',   'hafnium'       )
Ta  = Atom(73,      'Ta',   'tantalum'      )
W   = Atom(74,      'W',    'tungsten'      )
Re  = Atom(75,      'Re',   'rhenium'       )
Os  = Atom(76,      'Os',   'osmium'        )
Ir  = Atom(77,      'Ir',   'iridium'       )
Pt  = Atom(78,      'Pt',   'platinum'      )
Au  = Atom(79,      'Au',   'gold'          )
Hg  = Atom(80,      'Hg',   'mercury'       )
Tl  = Atom(81,      'Tl',   'thallium'      )
Pb  = Atom(82,      'Pb',   'lead'          )
Bi  = Atom(83,      'Bi',   'bismuth'       )
Po  = Atom(84,      'Po',   'polonium'      )
At  = Atom(85,      'At',   'astatine'      )
Rn  = Atom(86,      'Rn',   'radon'         )
Fr  = Atom(87,      'Fr',   'francium'      )
Ra  = Atom(88,      'Ra',   'radium'        )
Ac  = Atom(89,      'Ac',   'actinium'      )
Th  = Atom(90,      'Th',   'thorium'       )
Pa  = Atom(91,      'Pa',   'protactinium'  )
U   = Atom(92,      'U',    'uranium'       )
Np  = Atom(93,      'Np',   'neptunium'     )
Pu  = Atom(94,      'Pu',   'plutonium'     )
Am  = Atom(95,      'Am',   'americium'     )
Cm  = Atom(96,      'Cm',   'curium'        )
Bk  = Atom(97,      'Bk',   'berkelium'     )
Cf  = Atom(98,      'Cf',   'californium'   )
Es  = Atom(99,      'Es',   'einsteinium'   )
Fm  = Atom(100,      'Fm',   'fermium'      )
Md  = Atom(101,      'Md',   'mendelevium'  )
No  = Atom(102,      'No',   'nobelium'     )
Lr  = Atom(103,      'Lr',   'lawrencium'   )
Rf  = Atom(104,      'Rf',   'rutherfordium')
Db  = Atom(105,      'Db',   'dubnium'      )
Sg  = Atom(106,      'Sg',   'seaborgium'   )
Bh  = Atom(107,      'Bh',   'bohrium'      )
Hs  = Atom(108,      'Hs',   'hassium'      )
Mt  = Atom(109,      'Mt',   'meitnerium'   )
Ds  = Atom(110,      'Ds',   'darmstadtium' )
Rg  = Atom(111,      'Rg',   'roentgenium'  )
Cn  = Atom(112,      'Cn',   'copernicium'  )
Uut = Atom(113,      'Uut',  'ununtrium'    )
Fl  = Atom(114,      'Fl',   'flerovium'    )
Uup = Atom(115,      'Uup',  'ununpentium'  )
Lv  = Atom(116,      'Lv',   'livermorium'  )
Uus = Atom(117,      'Uus',  'ununseptium'  )
Uuo = Atom(118,      'Uuo',  'ununoctium'   )

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
                    'Rb': Rb,
                    'Sr': Sr,
                    'Y' : Y,
                    'Zr': Zr,
                    'Nb': Nb,
                    'Mo': Mo,
                    'Tc': Tc,
                    'Ru': Ru,
                    'Rh': Rh,
                    'Pd': Pd,
                    'Ag': Ag,
                    'Cd': Cd,
                    'In': In,
                    'Sn': Sn,
                    'Sb': Sb,
                    'Te': Te,
                    'I' : I,
                    'Xe': Xe,
                    'Cs': Cs,
                    'Ba': Ba,
                    'La': La,
                    'Ce': Ce,
                    'Pr': Pr,
                    'Nd': Nd,
                    'Pm': Pm,
                    'Sm': Sm,
                    'Eu': Eu,
                    'Gd': Gd,
                    'Tb': Tb,
                    'Dy': Dy,
                    'Ho': Ho,
                    'Er': Er,
                    'Tm': Tm,
                    'Yb': Yb,
                    'Lu': Lu,
                    'Hf': Hf,
                    'Ta': Ta,
                    'W' : W,
                    'Re': Re,
                    'Os': Os,
                    'Ir': Ir,
                    'Pt': Pt,
                    'Au': Au,
                    'Hg': Hg,
                    'Tl': Tl,
                    'Pb': Pb,
                    'Bi': Bi,
                    'Po': Po,
                    'At': At,
                    'Rn': Rn,
                    'Fr': Fr,
                    'Ra': Ra,
                    'Ac': Ac,
                    'Th': Th,
                    'Pa': Pa,
                    'U' : U,
                    'Np': Np,
                    'Pu': Pu,
                    'Am': Am,
                    'Cm': Cm,
                    'Bk': Bk,
                    'Cf': Cf,
                    'Es': Es,
                    'Fm': Fm,
                    'Md': Md,
                    'No': No,
                    'Lr': Lr,
                    'Rf': Rf,
                    'Db': Db,
                    'Sg': Sg,
                    'Bh': Bh,
                    'Hs': Hs,
                    'Mt': Mt,
                    'Ds': Ds,
                    'Rg': Rg,
                    'Cn': Cn,
                    'Uut':Uut,
                    'Fl': Fl,
                    'Uup':Uup,
                    'Lv': Lv,
                    'Uus':Uus,
                    'Uuo':Uuo}