#! /usr/bin/env python
import numpy as np
import ROOT
from rootpy.plotting.style import set_style
from hgc_tpg.utilities.tree import read_and_match
from hgc_tpg.efficiency.efficiency import turnon
from hgc_tpg.plotting.styles import style_turnon
from hgc_tpg.plotting import plot_efficiency



def main(parameters):
    set_style(style_turnon)
    l1_variables = [parameters.l1_pt]
    if parameters.identification_inputs!=None:
        l1_variables = [parameters.l1_pt]+parameters.identification_inputs
    data = read_and_match(
            parameters.input_file, parameters.input_tree,
            ref_variables=[parameters.reference_pt],
            l1_variables=l1_variables,
            selection=parameters.reference_selection,
            matching=parameters.matching
            )
    ref_pt = data[parameters.reference_pt]
    l1_pt = data[parameters.l1_pt]
    identification_inputs = data[parameters.identification_inputs]\
                .view((np.float32, len(parameters.identification_inputs)))
    efficiency = turnon(ref_pt, l1_pt,
            threshold=parameters.threshold,
            selection_function=parameters.identification_function,
            selection_inputs=identification_inputs
            )
    plot_efficiency.plot(parameters.plot_params, efficiency)

if __name__=='__main__':
    import sys
    import os
    import optparse
    import importlib
    usage = 'usage: %prog [options]'
    parser = optparse.OptionParser(usage)
    parser.add_option('--cfg', dest='parameter_file', help='Python file containing the definition of parameters ', default='pars.py')
    (opt, args) = parser.parse_args()
    current_dir = os.getcwd();
    sys.path.append(current_dir)
    # Remove the extension of the python file before module loading
    if opt.parameter_file[-3:]=='.py': opt.parameter_file = opt.parameter_file[:-3]
    parameters = importlib.import_module(opt.parameter_file).parameters
    main(parameters)

