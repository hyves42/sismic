import argparse
import sys

from ..io import import_from_yaml
from . import execute_bdd


parser = argparse.ArgumentParser(prog='sismic-bdd',
                                 description='Command-line utility to execute Gherkin feature files using Behave.\n'
                                             'Extra parameters will be passed to Behave.')

parser.add_argument('statechart', metavar='statechart', type=str,
                    help='A YAML file describing a statechart')
parser.add_argument('--features', metavar='features', nargs='+', type=str, required=True,
                    help='A list of files containing features')
parser.add_argument('--steps', metavar='steps', nargs='+', type=str,
                    help='A list of files containing steps implementation')
parser.add_argument('--properties', metavar='properties', nargs='+', type=str,
                    help='A list of filepaths pointing to YAML property statecharts. They will be checked at runtime following a fail fast approach.')
parser.add_argument('--show-steps', action='store_true', default=False,
                    help='Display a list of available steps (equivalent to Behave\'s --steps parameter')
parser.add_argument('--debug-on-error', action='store_true', default=False,
                    help='Drop in a debugger in case of step failure (ipdb if available)')

args, parameters = parser.parse_known_args()
if args.show_steps:
    parameters.append('--steps')

with open(args.statechart) as f:
    statechart = import_from_yaml(f)

property_statecharts = []
for property_statechart in args.properties or []:
    with open(property_statechart) as f:
        property_statecharts.append(import_from_yaml(f))

sys.exit(
    execute_bdd(
        statechart,
        args.features,
        step_filepaths=args.steps,
        property_statecharts=property_statecharts,
        debug_on_error=args.debug_on_error,
        behave_parameters=parameters
    )
)