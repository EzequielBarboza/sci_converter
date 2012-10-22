#!/usr/bin/env python
#-------------------------------------------------------------------------------
# Name:         template
# Purpose:      The template is the set of possible relationships between the various
# modules, submodules and properties that the system handles
# It does depict a formal structure, as a language, that must be obeyied
#
# Author:      ezequiel.barboza
#
# Created:     01/08/2012
# Copyright:   (c) ezequiel.barboza 2012
# Licence:     GPL
#-------------------------------------------------------------------------------

import re

from module import Property,Module,SubModule

class Template:


    property_pattern = re.compile(' *\..+')
    submodule_pattern = re.compile(' *\*.+')
    module_pattern = re.compile(' *\*\*.+')

    def __init__(self):
######hamiltonian
        self.levy_leblond    = Property('.LEVY-LEBLOND')
        self.urkbal          = Property('.URKBAL')
        self.lvcorr          = Property('.LVCORR')

        self.hamiltonian = Module('**HAMILTONIAN')
        self.hamiltonian.properties.update({'.LEVY-LEBLOND': self.levy_leblond})
        self.hamiltonian.properties.update({'.URKBAL': self.urkbal})
        self.hamiltonian.properties.update({'.LVCORR': self.lvcorr})
    ########dirac
        self.wave_function_prop  = Property('.WAVE FUNCTION')
        self.properties_prop     = Property('.PROPERTIES')
        self.inptest             = Property('.INPTEST')

        self.dirac = Module('**DIRAC')
        self.dirac.properties.update({'.WAVE FUNCTION'   :self.wave_function_prop})
        self.dirac.properties.update({'.PROPERTIES'      :self.properties_prop})
        self.dirac.properties.update({'.INPTEST'         :self.inptest})
    ##########wave function
        self.scf_prop    = Property('.SCF')
        self.evccnv      = Property('.EVCCNV')
        self.atomst      = Property('.ATOMST')
        self.closed      = Property('.CLOSED')
        self.openshell   = Property('.OPEN SHELL')

        self.scf = SubModule('*SCF')
        self.scf.properties.update({'.EVCCNV':self.evccnv})
        self.scf.properties.update({'.ATOMST':self.atomst})
        self.scf.properties.update({'.CLOSED':self.closed})
        self.scf.properties.update({'.OPEN SHELL':self.openshell})

        self.wave_function = Module('**WAVE FUNCTION')
        self.wave_function.properties.update({'.SCF':self.scf_prop})
        self.wave_function.submodules.update({'*SCF':self.scf})
    ############integrals submodule
        self.uncontract  = Property('.UNCONTRACT')
        self.readin      = SubModule('*READIN')
        self.readin.properties.update({'.UNCONTRACT':self.uncontract})

        self.screen = Property('.SCREEN')
        self.twoint      = SubModule('*TWOINT')
        self.twoint.properties.update({'.SCREEN':self.screen})

        self.integrals   = Module('**INTEGRALS')
        self.integrals.submodules.update({'*READIN':self.readin})
        self.integrals.submodules.update({'*TWOINT':self.twoint})
    ############# properties
        ##properties for the **PROPERTIES
        self.bzlao = Property('.BZLAO')
        self.bxlao = Property('.BXLAO')
        self.bylao = Property('.BYLAO')

        ## *NMR submodule for the **PROPERTIES
        self.london = Property('.LONDON')
        self.doeprn = Property('.DOEPRN')
        self.intflg = Property('.INTFLG')
        self.gaugeo = Property('.GAUGEO')
        self.nmr = SubModule('*NMR')
        self.nmr.properties.update({'.LONDON':self.london})
        self.nmr.properties.update({'.DOEPRN':self.doeprn})
        self.nmr.properties.update({'.INTFLG':self.intflg})
        self.nmr.properties.update({'.GAUGEO':self.gaugeo})
        ## *LINEAR RESPONSE for the **PROPERTIES
        self.a_operator = Property('.A OPERATOR')
        self.b_operator = Property('.B OPERATOR')
        self.analize = Property('.ANALIZE')
        self.linear_response = SubModule('*LINEAR RESPONSE')
        self.linear_response.properties.update({'.A OPERATOR'   :self.a_operator})
        self.linear_response.properties.update({'.B OPERATOR'   :self.b_operator})
        self.linear_response.properties.update({'.ANALIZE'      :self.analize})

        self.prop_module  = Module('**PROPERTIES')
        self.prop_module.properties.update({'.BZLAO':self.bzlao})
        self.prop_module.properties.update({'.BXLAO':self.bxlao})
        self.prop_module.properties.update({'.BYLAO':self.bylao})
        self.prop_module.submodules.update({'*NMR':self.nmr})
        self.prop_module.submodules.update({'*LINEAR RESPONSE':self.linear_response})
    ############# visual
        self.jdia        = Property('.JDIA')
        self.j           = Property('.J')
        self.noreortho   = Property('.NOREORTHO')
        self.nodirect    = Property('.NODIRECT')
        self.two_d       = Property('.2D')
        self.two_d_int   = Property('.2D_INT')
        self.visual = Module('**VISUAL')
        self.visual.properties.update({'.JDIA'       :self.jdia})
        self.visual.properties.update({'.J'          :self.j})
        self.visual.properties.update({'.NOREORTHO'  :self.noreortho})
        self.visual.properties.update({'.NODIRECT'   :self.nodirect})
        self.visual.properties.update({'.LONDON'     :self.london})
        self.visual.properties.update({'.2D'         :self.two_d})
        self.visual.properties.update({'.2D_INT'     :self.two_d_int})
############ general
        self.acmout     = Property('.ACMOUT')
        self.general    = Module('**GENERAL')
        self.general.properties.update({'.ACMOUT'   :self.acmout})

        #valid module names
        self.modules = {   '**HAMILTONIAN'       : self.hamiltonian,
                        '**DIRAC'           : self.dirac,
                        '**WAVE FUNCTION'   : self.wave_function,
                        '**INTEGRALS'       : self.integrals,
                        '**PROPERTIES'      : self.prop_module,
                        '**VISUAL'          : self.visual,
                        '**GENERAL'         : self.general}
        #valid submodules names
        self.submodules = { '*READIN'           :self.readin,
                            '*TWOINT'           :self.twoint,
                            '*SCF'              :self.scf,
                            '*NMR'              :self.nmr,
                            '*LINEAR RESPONSE'  :self.linear_response}
        #valid properties names
        self.properties = {  '.LEVY-LEBLOND' :self.levy_leblond,
                        '.URKBAL'       :self.urkbal,
                        '.LVCORR'       :self.lvcorr,
                        '.WAVE FUNCTION':self.wave_function_prop,
                        '.PROPERTIES'   :self.properties_prop,
                        '.INPTEST'      :self.inptest,
                        '.EVCCNV'       :self.evccnv,
                        '.ATOMST'       :self.atomst,
                        '.CLOSED'       :self.closed,
                        '.OPEN SHELL'   :self.openshell,
                        '.SCF'          :self.scf_prop,
                        '.UNCONTRACT'   :self.uncontract,
                        '.SCREEN'       :self.screen,
                        '.BZLAO'        :self.bzlao,
                        '.BXLAO'        :self.bxlao,
                        '.BYLAO'        :self.bylao,
                        '.LONDON'       :self.london,
                        '.DOEPRN'       :self.doeprn,
                        '.INTFLG'       :self.intflg,
                        '.GAUGEO'       :self.gaugeo,
                        '.A OPERATOR'   :self.a_operator,
                        '.B OPERATOR'   :self.b_operator,
                        '.ANALIZE'      :self.analize,
                        '.JDIA'         :self.jdia,
                        '.J'            :self.j,
                        '.NOREORTHO'    :self.noreortho,
                        '.NODIRECT'     :self.nodirect,
                        '.2D'           :self.two_d,
                        '.2D_INT'       :self.two_d_int,
                        '.ACMOUT'       :self.acmout
                        }

##    def is_module(self, name):
##        return self.modules.get(name)

    def is_property(self, line):
        return self.properties.get(line)

##    def is_submodule(self, line):
##        return self.submodules.get(line)

    def is_value(self, line):
        return re.match(self.value_pattern, line)
