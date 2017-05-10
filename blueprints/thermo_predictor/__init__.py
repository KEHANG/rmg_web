from flask import Blueprint, render_template, request

from rmgpy.molecule import Molecule

from thermo_predictor_utils import h298_predictor
from blueprints.utils import connect_to_PPD, draw_molecule_from_aug_inchi

thermo_predictor = Blueprint('thermo_predictor', __name__,
                        	template_folder='templates',
                            static_folder='./static')

# access predictor performance db
ppd_client = connect_to_PPD()
predictorPerformanceDB =  getattr(ppd_client, 'predictor_performance')
molconv_performance_table = getattr(predictorPerformanceDB, 'molconv_performance_table')


@thermo_predictor.route('/performance', methods=['GET', 'POST'])
def performance():
    if request.method == 'POST':
        molecule_smiles = str(request.form['molecule_smiles'])
        try:
            mol = Molecule(SMILES=molecule_smiles)
            aug_inchi = mol.toAugmentedInChI()
            draw_molecule_from_aug_inchi(aug_inchi, thermo_predictor.static_folder + '/img')
        except:
            return render_template('thermo_estimation.html')
        
        thermo_result = h298_predictor.predict(mol)
        return render_template('thermo_estimation.html', 
                                thermo_result=thermo_result,
                                molecule_smiles=molecule_smiles,
                                aug_inchi=aug_inchi)
    else:

        return render_template('thermo_estimation.html')