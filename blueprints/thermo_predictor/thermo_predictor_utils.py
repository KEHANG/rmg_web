import os
import numpy as np
from sklearn.neighbors import NearestNeighbors

from rmgpy.molecule import Molecule
from rmgpy.cnn_framework.predictor import Predictor
from rmgpy.cnn_framework.molecule_tensor import get_molecule_tensor, pad_molecule_tensor

def load_cnn_thermo_predictor(thermo_predictor_model='zb_biycyclics_t.r.0.5'):

    thermo_predictor_data = os.path.join(os.path.dirname(__file__),
                                        'data')

    datasets_file = os.path.join(thermo_predictor_data,
                                'predictor_models',
                                thermo_predictor_model,
                                'datasets.txt')

    predictor_input = os.path.join(thermo_predictor_data,
                                'predictor_models',
                                thermo_predictor_model,
                                'predictor_input.py')

    h298_predictor = Predictor(datasets_file=datasets_file)
    h298_predictor.load_input(predictor_input)
    param_path = os.path.join(thermo_predictor_data,
                            'predictor_models',
                            thermo_predictor_model,
                            'saved_model',
                            'full_train.h5')
    h298_predictor.load_parameters(param_path)

    return h298_predictor

def load_nearest_neighbours(datasets,
                            molconv_model,
                            thermo_predictor_model='zb_biycyclics_t.r.0.5'):

    thermo_predictor_data = os.path.join(os.path.dirname(__file__),
                                        'data')

    datasets = datasets

    training_smis = []
    for _, db, table, _ in datasets:
        training_example_meta_file = os.path.join(thermo_predictor_data,
                                            'predictor_models',
                                           thermo_predictor_model,
                                           '{0}.{1}_smis_train.txt'.format(db, table))
        with open(training_example_meta_file, 'r') as f_in:
            for line in f_in:
                if line.strip():
                    training_smis.append(line.strip())

    mol_tensors = []
    print("\nCrunching training fingerprints...")
    for smi in training_smis:
        mol_tensor = pad_molecule_tensor(get_molecule_tensor(Molecule(SMILES=smi)), 20)
        mol_tensors.append(mol_tensor)

    print("\nFinished.")

    training_fps = molconv_model.predict(np.array(mol_tensors))

    nbrs = NearestNeighbors(n_neighbors=20, algorithm='ball_tree').fit(training_fps)

    return nbrs, training_smis

