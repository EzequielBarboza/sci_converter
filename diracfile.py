#!/usr/bin/env python

#-------------------------------------------------------------------------------
# Name:        module
# Purpose:
#
# Author:      ezequiel
#
# Created:     01/09/2012
# Copyright:   (c) ezequiel 2012
# Licence: GPL
#-------------------------------------------------------------------------------
import re

#from module import Property
from main import teste

class DiracFile:
## the patterns for the strings
    comment_pattern = re.compile(' *#.*')
    property_pattern = re.compile(' *\..+')
    submodule_pattern = re.compile(' *\*.+')
    module_pattern = re.compile(' *\*\*.+')
    value_pattern = re.compile('^[^\*\.]')

######hamiltonian


    levy_leblond    = Property('.LEVY-LEBLOND')
    urkbal          = Property('.URKBAL')
    lvcorr          = Property('.LVCORR')

    hamiltonian = Module('**HAMILTONIAN')
    hamiltonian.properties.update({'.LEVY-LEBLOND': levy_leblond})
    hamiltonian.properties.update({'.URKBAL': urkbal})
    hamiltonian.properties.update({'.LVCORR': lvcorr})
########dirac
    wave_function_prop  = Property('.WAVE FUNCTION')
    properties_prop     = Property('.PROPERTIES')
    inptest             = Property('.INPTEST')

    dirac = Module('**DIRAC')
    dirac.properties.update({'.WAVE FUNCTION'   :wave_function_prop})
    dirac.properties.update({'.PROPERTIES'      :properties_prop})
    dirac.properties.update({'.INPTEST'         :inptest})
##########wave function
    scf_prop    = Property('.SCF')
    evccnv      = Property('.EVCCNV')
    atomst      = Property('.ATOMST')

    scf = SubModule('*SCF')
    scf.properties.update({'.EVCCNV':evccnv})
    scf.properties.update({'.ATOMST':atomst})

    wave_function = Module('**WAVE FUNCTION')
    wave_function.properties.update({'.SCF':scf_prop})
    wave_function.submodules.update({'*SCF':scf})
############integrals submodule
    uncontract  = Property('.UNCONTRACT')
    readin      = SubModule('*READIN')
    readin.properties.update({'.UNCONTRACT':uncontract})

    screen = Property('.SCREEN')
    twoint      = SubModule('*TWOINT')
    twoint.properties.update({'.SCREEN':screen})

    integrals   = Module('**INTEGRALS')
    integrals.submodules.update({'*READIN':readin})
    integrals.submodules.update({'*TWOINT':twoint})
############# properties
    bzlao = Property('.BZLAO')
    bxlao = Property('.BXLAO')
    bylao = Property('.BYLAO')

    london = Property('.LONDON')
    doeprn = Property('.DOEPRN')
    intflg = Property('.INTFLG')

    nmr = SubModule('*NMR')
    nmr.properties.update({'.LONDON':london})
    nmr.properties.update({'.DOEPRN':doeprn})
    nmr.properties.update({'.INTFLG':intflg})

    prop_module  = Module('**PROPERTIES')
    prop_module.properties.update({'.BZLAO':bzlao})
    prop_module.properties.update({'.BXLAO':bxlao})
    prop_module.properties.update({'.BYLAO':bylao})
    prop_module.submodules.update({'*NMR':nmr})
############# visual
    jdia        = Property('.JDIA')
    j           = Property('.J')
    noreortho   = Property('.NOREORTHO')
    nodirect    = Property('.NODIRECT')
    two_d       = Property('.2D')
    visual = Module('**VISUAL')
    visual.properties.update({'.JDIA'       :jdia})
    visual.properties.update({'.J'          :j})
    visual.properties.update({'.NOREORTHO'  :noreortho})
    visual.properties.update({'.NODIRECT'   :nodirect})
    visual.properties.update({'.LONDON'     :london})
    visual.properties.update({'.2D'         :two_d})

    #valid module names
    modules = {   '**HAMILTONIAN'       : hamiltonian,
                    '**DIRAC'           : dirac,
                    '**WAVE FUNCTION'   : wave_function,
                    '**INTEGRALS'       : integrals,
                    '**PROPERTIES'      : prop_module,
                    '**VISUAL'          : visual}
    #valid submodules names
    submodules = {  '*READIN'   :readin,
                    '*TWOINT'   :twoint,
                    '*SCF'      :scf,
                    '*NMR'      :nmr}
    #valid properties names
    properties = {  '.LEVY-LEBLOND' :levy_leblond,
                    '.URKBAL'       :urkbal,
                    '.LVCORR'       :lvcorr,
                    '.WAVE FUNCTION':wave_function_prop,
                    '.PROPERTIES'   :properties_prop,
                    '.INPTEST'      :inptest,
                    '.EVCCNV'       :evccnv,
                    '.ATOMST'       :atomst,
                    '.SCF'          :scf_prop,
                    '.UNCONTRACT'   :uncontract,
                    '.SCREEN'       :screen,
                    '.BZLAO'        :bzlao,
                    '.BXLAO'        :bxlao,
                    '.BYLAO'        :bylao,
                    '.LONDON'       :london,
                    '.DOEPRN'       :doeprn,
                    '.INTFLG'       :intflg,
                    '.JDIA'         :jdia,
                    '.J'            :j,
                    '.NOREORTHO'    :noreortho,
                    '.NODIRECT'     :nodirect,
                    '.2D'           :two_d
                    }
    @staticmethod
    def is_comment(line):
        m = re.match(DiracFile.comment_pattern, line)
        n = line.strip() == ''
        return m or n

    @staticmethod
    def is_property(line):
        m = re.match(DiracFile.property_pattern, line)
        return m

    @staticmethod
    def is_submodule(line):
        m = re.match(DiracFile.submodule_pattern, line)
        return m

    @staticmethod
    def is_value(line):
        m = re.match(DiracFile.value_pattern, line)
        return m

    @staticmethod
    def is_module(name):
        return DiracFile.modules.get(name) != None

