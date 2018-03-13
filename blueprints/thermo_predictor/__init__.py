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
thermo_predictor_name = "full_train"
h298_predictor = load_cnn_thermo_predictor(thermo_predictor_name)
molconv_model = Model(input=h298_predictor.model.input,
                    output=h298_predictor.model.layers[0].output)

nbrs, training_smis = load_nearest_neighbours(h298_predictor.datasets, molconv_model)

@thermo_predictor.route('/performance')
@thermo_predictor.route('/cyclic_performance')
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

@thermo_predictor.route('/overall_performance/<target>/')
def overall_performance(target):
    if target not in ['Hf298', 'S298', 'Cp']:
        target = 'Hf298'
    
    cnn_target_table = getattr(predictorPerformanceDB, 'cnn_{0}_table'.format(target))
    latest_cnn_performance = list(cnn_target_table.find().sort([('timestamp', -1)]).limit(1))[0]
    
    # get meta data
    meta_dict = {"date":latest_cnn_performance['date'],
                 "rmgpy_branch":latest_cnn_performance['rmgpy_branch'],
                 "rmgdb_branch":latest_cnn_performance['rmgdb_branch'],
                 "rmgpy_sha":latest_cnn_performance['rmgpy_sha'],
                 "rmgdb_sha":latest_cnn_performance['rmgdb_sha'],
    }

    evaluation_results = latest_cnn_performance['evaluation_results']

    # tabulate performance results
    row_names=['C, H, O', 'N contained', 'S contained']
    column_names=['Linear', 'Cyclics', 'Radicals']
    performance_dict = dict.fromkeys(row_names)
    for row in performance_dict:
        performance_dict[row] = dict.fromkeys(column_names)

    # linear performance
    cho_linear_sdata134k = evaluation_results['rmg/sdata134k/sdata134k_cho_linear_table_test']
    N_linear_sdata134k = evaluation_results['rmg/sdata134k/sdata134k_N_linear_table_test']
    cho_linear_rmg = evaluation_results['rmg/rmg_internal/rmg_cho_linear_table_test']
    N_linear_rmg = evaluation_results['rmg/rmg_internal/rmg_N_linear_table_test']
    S_linear_rmg = evaluation_results['rmg/rmg_internal/rmg_S_linear_table_test']

    performance_dict['C, H, O']['Linear'] = {"sdata134k": cho_linear_sdata134k,
                                             "rmg_internal": cho_linear_rmg}

    performance_dict['N contained']['Linear'] = {"sdata134k": N_linear_sdata134k,
                                                 "rmg_internal": N_linear_rmg}

    performance_dict['S contained']['Linear'] = {"sdata134k": None,
                                                 "rmg_internal": S_linear_rmg}

    # cyclics performance
    cho_cyclics_sdata134k = evaluation_results['rmg/sdata134k/sdata134k_cho_cyclics_table_test']
    N_cyclics_sdata134k = evaluation_results['rmg/sdata134k/N_cyclics_table_test']
    cho_cyclics_rmg = evaluation_results['rmg/rmg_internal/rmg_cho_cyclic_table_test']
    N_cyclics_rmg = evaluation_results['rmg/rmg_internal/rmg_N_cyclic_table_test']
    S_cyclics_rmg = evaluation_results['rmg/rmg_internal/rmg_S_cyclic_table_test']

    performance_dict['C, H, O']['Cyclics'] = {"sdata134k": cho_cyclics_sdata134k,
                                              "rmg_internal": cho_cyclics_rmg}

    performance_dict['N contained']['Cyclics'] = {"sdata134k": N_cyclics_sdata134k,
                                                  "rmg_internal": N_cyclics_rmg}

    performance_dict['S contained']['Cyclics'] = {"sdata134k": None,
                                                  "rmg_internal": S_cyclics_rmg}

    # rads performance
    cho_rads_rmg= evaluation_results['rmg/rmg_internal/rmg_cho_rads_table_test']
    N_rads_rmg= evaluation_results['rmg/rmg_internal/rmg_N_rads_table_test']
    S_rads_rmg= evaluation_results['rmg/rmg_internal/rmg_S_rads_table_test']

    performance_dict['C, H, O']['Radicals'] = {"sdata134k": None,
                                              "rmg_internal": cho_rads_rmg}

    performance_dict['N contained']['Radicals'] = {"sdata134k": None,
                                                  "rmg_internal": N_rads_rmg}

    performance_dict['S contained']['Radicals'] = {"sdata134k": None,
                                                  "rmg_internal": S_rads_rmg}

    return render_template('overall_performance.html',
                            target=target,
                           row_names=row_names,
                           column_names=column_names,
                           performance_dict=performance_dict,
                           meta_dict=meta_dict)

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