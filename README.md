# aiida-raspa-EQeq

A prototypal package to test a screening study on a MOF database using a state-of-the-art calculation : Equilibration of Charges.

## Installation

### Virtual environment with Conda
```
conda create -n aiida python=3.11
```
### Initialize the aiida framework
We need to install `aiida`using a conda environment following the [installation procedure](https://aiida.readthedocs.io/projects/aiida-core/en/latest/intro/install_conda.html).
Then, to run code using the pre-defined `workchain` and `calcJob` objects in the plugin `aiida-raspa`, we can follow the following steps using the [documentation](https://aiida.readthedocs.io/projects/aiida-core/en/latest/howto/run_codes.html):
- set up a computer
```bash
verdi computer setup --config computer.yml
```
- create a code

```bash
verdi code create core.code.installed
        --label raspa_run \
        --computer curie \
        --filepath-executable "/opt/raspa_v2.0.48/bin/simulate"
```
Iddicate after `--filepath-executable` the executable path of RASA installed in the computer.

### Other dependies 
```
pip install -r requirements.txt
```



