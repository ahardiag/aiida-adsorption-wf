"""Charge Equilibration through RaspaBaseWorkChain"""
import os
import sys

import click
from aiida import orm
from aiida_raspa.workchains import RaspaBaseWorkChain
from aiida.engine import submit,run
from aiida.common import NotExistent
from aiida.orm import CifData, Code, Dict, SinglefileData

def run_raspa(cifpath,raspa_code,is_submit=True):

    framework = orm.CifData(file=cifpath)
    cifname = cifpath.split('/')[-1].split('.cif')[0]  # Extracting CIF name
    cifname = cifname.replace("-","_")

    parameters = orm.Dict(
        dict={
            "GeneralSettings": {
                "SimulationType": "MonteCarlo",
                "Forcefield": "ExampleMOFsForceField",
                "NumberOfCycles": 0,
                "RestartFile": "no",
                "ChargeFromChargeEquilibration": "yes",
                "ChargeEquilibrationPeriodic": "yes",
                "ChargeEquilibrationEwald": "yes",
                "SymmetrizeFrameworkCharges": "no"
            },
            "System": {
                cifname: {
                    "type": "Framework",
                },
            },
            "Component": {
                "CO2": {
                    "MoleculeDefinition": "ExampleDefinitions",
                    "TranslationProbability": 0.5,
                    "ReinsertionProbability": 0.5,
                    "SwapProbability": 1.0,
                    "CreateNumberOfMolecules": 0,
                }
            },
        }
    )

    # Constructing builder
    builder = RaspaBaseWorkChain.get_builder()

    # Specifying the code
    builder.raspa.code = raspa_code

    # Specifying the framework
    builder.raspa.framework = {cifname: framework}

    # Specifying the input parameters
    builder.raspa.parameters = parameters

    # Specifying the scheduler options
    builder.raspa.metadata.options = {
        "resources": {
            "num_machines": 1,
            "num_mpiprocs_per_machine": 1,
        },
        "max_wallclock_seconds": 1 * 30 * 60,  # 30 min
        "withmpi": False,
    }
    builder.raspa.metadata.dry_run = False
    builder.raspa.metadata.store_provenance = True

    #if is_submit:
    submit(RaspaBaseWorkChain, **builder)
    #else:
    #    print("Generating test input ...")
    #    builder.raspa.metadata.dry_run = True
    #    builder.raspa.metadata.store_provenance = False
    #    run(builder)
    #    print("Submission test successful")
    #    print("In order to actually submit, add '--submit'")
    #print("-----")


@click.command("cli")
@click.argument("codelabel")
@click.option("--inputpath",required=True,type=str, help="Path directory to CIF database.")
@click.option("--submit", is_flag=True, help="Submit simulations to the daemon.")
@click.option("--num_max", default= 10, help="Maximal number of simulations")
@click.option("--verbose", is_flag=True, help="verbosity")
def cli(codelabel,inputpath,submit,num_max,verbose):
    """Click interface"""
    try:
        code = Code.get_from_string(codelabel)
    except NotExistent:
        print(f"The code '{codelabel}' does not exist")
        sys.exit(1)
    
    try:
        # Check if the input directory exists
        if not os.path.isdir(inputpath):
            raise FileNotFoundError(f"The directory '{inputpath}' does not exist.")
    except FileNotFoundError as e:
        print(e)
        sys.exit(1)

    # List all CIF files in the directory
    inputpath = os.path.abspath(inputpath)
    cif_files = [os.path.join(inputpath, f) for f in os.listdir(inputpath) if f.endswith('.cif')]

    # Counter for submitted jobs
    submitted_jobs = 0

    print("Submitting jobs ...")

    # Iterate over the CIF files
    for i,cif_file in enumerate(cif_files[:num_max]):
        # Verbosity
        if verbose : print(f"Running EQeq on {cif_file}")

        # Submit the workchain to AiiDA
        run_raspa(cif_file,code,is_submit=submit)

        # Increment the counter for submitted jobs
        submitted_jobs += 1
        print(f"Completed: {100 * (i + 1) / num_max:.2f}%", end='\r')

    print(f"Submitted {submitted_jobs} jobs on the queue.")

if __name__ == "__main__":
    cli()  # pylint: disable=no-value-for-parameter

# EOF

