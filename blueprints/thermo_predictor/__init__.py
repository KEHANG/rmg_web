from flask import Blueprint, render_template

from blueprints.utils import connect_to_PPD

thermo_predictor = Blueprint('thermo_predictor', __name__,
                        	template_folder='templates')

# access predictor performance db
ppd_client = connect_to_PPD()
predictorPerformanceDB =  getattr(ppd_client, 'predictor_performance')
molconv_performance_table = getattr(predictorPerformanceDB, 'molconv_performance_table')


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