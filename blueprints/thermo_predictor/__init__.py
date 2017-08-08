import os
import numpy as np
from keras.models import Model
from flask import Blueprint, render_template, request

from rmgpy.molecule import Molecule
from rmgpy.cnn_framework.molecule_tensor import get_molecule_tensor, pad_molecule_tensor

from blueprints.utils import connect_to_PPD, draw_molecule_from_aug_inchi
from thermo_predictor_utils import load_cnn_thermo_predictor, load_nearest_neighbours

thermo_predictor = Blueprint('thermo_predictor', __name__,
                            template_folder='templates',
                            static_folder='./static',
                            static_url_path='/blueprints/thermo_predictor/static')

# access predictor performance db
ppd_client = connect_to_PPD()
predictorPerformanceDB =  getattr(ppd_client, 'predictor_performance')
molconv_performance_table = getattr(predictorPerformanceDB, 'molconv_performance_table')

# create predictor instance
h298_predictor = load_cnn_thermo_predictor()
molconv_model = Model(input=h298_predictor.model.input,
                    output=h298_predictor.model.layers[0].output)

nbrs, training_smis = load_nearest_neighbours(h298_predictor.datasets, molconv_model)

@thermo_predictor.route('/performance')
def performance():

    latest_molconv_performance = list(molconv_performance_table.find().sort([('timestamp', -1)]).limit(1))[0]
    small_cyclic_performance = [latest_molconv_performance['small_cyclic_table']]
    large_linear_polycyclic_performance = [latest_molconv_performance['large_linear_polycyclic_table']]
    large_fused_polycyclic_performance = [latest_molconv_performance['large_fused_polycyclic_table']]

    small_O_only_polycyclic_performance = [latest_molconv_performance['small_O_only_polycyclic_table']]
    large_linear_O_only_polycyclic_performance = [latest_molconv_performance['large_linear_O_only_polycyclic_table']]
    large_fused_O_only_polycyclic_performance = [latest_molconv_performance['large_fused_O_only_polycyclic_table']]

    return render_template('predictor_performance.html',
                            small_cyclic_performance=small_cyclic_performance,
                            large_linear_polycyclic_performance=large_linear_polycyclic_performance,
                            large_fused_polycyclic_performance=large_fused_polycyclic_performance,
                            small_O_only_polycyclic_performance=small_O_only_polycyclic_performance,
                            large_linear_O_only_polycyclic_performance=large_linear_O_only_polycyclic_performance,
                            large_fused_O_only_polycyclic_performance=large_fused_O_only_polycyclic_performance)

@thermo_predictor.route('/thermo_estimation', methods=['GET', 'POST'])
def thermo_estimation():
    if request.method == 'POST':
        molecule_smiles = str(request.form['molecule_smiles'])
        try:
            mol = Molecule(SMILES=molecule_smiles)
            aug_inchi = mol.toAugmentedInChI()
            draw_molecule_from_aug_inchi(aug_inchi, thermo_predictor.static_folder + '/img')

            # sort out the nearest neighbours
            moltensor = pad_molecule_tensor(get_molecule_tensor(mol), 20)
            fp = molconv_model.predict(np.array([moltensor]))

            distances, indices = nbrs.kneighbors(fp)
            for i, mol_idx in enumerate(indices[0][:4]):
                smi = training_smis[mol_idx]
                mol_nb = Molecule(SMILES=smi)
                path = os.path.join(thermo_predictor.static_folder,
                                    'img',
                                    aug_inchi.replace('/', '_slash_')+'_nb{0}.svg'.format(i))
                mol_nb.draw(path)
        except:
            return render_template('thermo_estimation.html')
        
        thermo_result = h298_predictor.predict(mol)
        return render_template('thermo_estimation.html', 
                                thermo_result=thermo_result,
                                molecule_smiles=molecule_smiles,
                                aug_inchi=aug_inchi)
    else:

        return render_template('thermo_estimation.html')