# load model into memory
import os
import re
import sys
from rmgpy.chemkin import loadChemkinFile, getSpeciesIdentifier
from rmgpy.molecule.molecule import Molecule
from rmgpy.molecule.draw import MoleculeDrawer

mech = sys.argv[1]#'pdd_scratch_add20'
path = os.path.abspath('./')
chemkinPath= path + '/data/' + mech + '/chem.inp'
dictionaryPath = path + '/data/' + mech + '/species_dictionary.txt'
species_list, reactions_list = loadChemkinFile(chemkinPath, dictionaryPath)

#generate species images
mech_path = path + '/data/' + mech
speciesPath = mech_path + '/species/'
if not os.path.isdir(speciesPath):
    os.makedirs(speciesPath)

species = species_list[:]
re_index_search = re.compile(r'\((\d+)\)$').search
for spec in species:
    match = re_index_search(spec.label)
    if match:
        spec.index = int(match.group(0)[1:-1])
        spec.label = spec.label[0:match.start()]
    # Draw molecules if necessary
    fstr = os.path.join(mech_path, 'species', '{0}.png'.format(spec))
    if not os.path.exists(fstr):
        try:
            MoleculeDrawer().draw(spec.molecule[0], 'png', fstr)
        except IndexError:
            raise OutputError("{0} species could not be drawn!".format(getSpeciesIdentifier(spec)))

species_target = sys.argv[2]#'C=CC[CH]CCCCCCC'
# search the target species in model
mol_tgt = Molecule().fromSMILES(species_target)

for spc in species_list:
    if spc.isIsomorphic(mol_tgt):
        print '{} is found in model with spc name {}'.format(mol_tgt, getSpeciesIdentifier(spc))
        break