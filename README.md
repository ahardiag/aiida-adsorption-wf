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
Indicate after `--filepath-executable` the executable path of RASPA installed in the computer.

### Other dependies 
```
pip install -r requirements.txt
```

## Example

### Run on CoRE MOF 2019
- **Input structures** : `examples/subset-coremof/cif`
    As an input, we provide a folder with 4140 cif files obtained by :
    - downloading the dataset `coremof-2019` through [MOFXDB](https://github.com/snurr-group/mofdb-x-archive/tree/dc8a0295db) (12018 MOFs)
    - converting CIF format using `openbabel`
    - selecting only the cif files we already have charges calculated using [lsmo-epfl/EQeq](https://github.com/lsmo-epfl/EQeq) (4140 MOFs)
    - correcting the name of the CIF file with `python check_and_convert_filenames.py`. `aiida-raspa` do not accept nonalphanumeric (exept underscore) in the filename (e.g. j.inoche.2015.06.036_inc06102-mmc1_clean_openbabel.cif).

- **running the calculation**
We used the following code (`verdi code show 1`):
```
-----------------------  -----------------------------------------
PK                       1
UUID                     e4afcb8d-4528-4561-a23e-c68226f2b8e5
Type                     core.code.installed
Computer                 curie (localhost), pk: 1
Filepath executable      /opt/raspa_v2.0.48/bin/simulate
Label                    raspa_run
Description              Run a simulation with RASPA
Default calc job plugin  raspa
Use double quotes        False
With mpi
Prepend text             export RASPA_DIR=/opt/raspa_v2.0.48
                         export DYLD_LIBRARY_PATH=${RASPA_DIR}/lib
                         export LD_LIBRARY_PATH=${RASPA_DIR}/lib
Append text
-----------------------  -----------------------------------------
```

command to submit all jobs at once from the root directory:
```bash
verdi run eqeq_raspa_screening.py raspa_run \
    --inputpath examples/subset-coremof/cif_converted/ \
    --num_max 80 \
    --verbose 
```
To test the submission on a few structures rather than the whole database, one can pass the maximum number of submission with `--num_max`.

## Aiida troubleshooting

Sometimes, we need to restart the local database :
```
pg_ctl -D /home/hardiagon/mylocal_db start
```
where `-D` flag denotes the path to database postgresql settings (by default `$HOME/mylocal_db`) if the database server has been initialized using `initdb -D mylocal_db` (see also [aiida doc](https://aiida.readthedocs.io/projects/aiida-core/en/latest/intro/install_conda.html#installation-into-conda-environment)).

To restart the `rabbitmq` server :
```
rabbitmq-server -detached
```
To restart the daemon : 
```
verdi daemon start
```
Then one can check everything is working with `verdi status`.