# aiida-raspa-EQeq

A prototypal package to test a screening study on a MOF database using a state-of-the-art calculation : Equilibration of Charges.

## Installation

### Virtual environment with Conda
```
conda create -n aiida python=3.11
```

### Other dependies 

#### Python 
```
pip install -r requirements.txt
```
#### Slurm
Installing and configuring Slurm scheduler on a local computer may be painful. We recommend to use SSH connections to a cluster node, where one can find a configured scheduler is installed (jean-zay:`slurm`, gricad:`oar`).

For quick tests, on Ubuntu (22.04 tested), one can use :
```
sudo apt-get install slurm-wlm
```

### Initialize the aiida framework
We need to install `aiida`using a conda environment following the [installation procedure](https://aiida.readthedocs.io/projects/aiida-core/en/latest/intro/install_conda.html).
Then, to run code using the pre-defined `workchain` and `calcJob` objects in the plugin `aiida-raspa`, we can follow the following steps using the [documentation](https://aiida.readthedocs.io/projects/aiida-core/en/latest/howto/run_codes.html):
- set up a computer
```bash
verdi computer setup --config config/computer_slurm.yml
```
- create a code

```bash
verdi code create core.code.installed
        --label raspa_run_slurm \
        --computer curie \
        --filepath-executable "/opt/raspa_v2.0.48/bin/simulate"
```
Indicate after `--filepath-executable` the executable path of RASPA installed in the computer.

or use a existing configuration :
```bash
verdi computer setup --config config/code_raspa_slurm.yml
```

To check how the aiida code looks like, use `verdi code show <PK>`:
```
-----------------------  -----------------------------------------
PK                       2240
UUID                     72fc9725-3c2d-4cd0-b6c3-4296d9d1e00d
Type                     core.code.installed
Computer                 localhost_slurm (localhost), pk: 2
Filepath executable      /opt/raspa_v2.0.48/bin/simulate
Label                    raspa_run_slurm
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

> Note : if one want to use the direct scheduler from Aiida, it results in the following example that all processes are ran simultaneously, independently of the number of available CPUs. To avoid this behavior, one use the SLURM scheduler


## Example

### Run on CoRE MOF 2019
- **Input structures** : `examples/subset-coremof/cif`
    As an input, we provide a folder with 4140 cif files obtained by :
    - downloading the dataset `coremof-2019` through [MOFXDB](https://github.com/snurr-group/mofdb-x-archive/tree/dc8a0295db) (12018 MOFs)
    - converting CIF format using `openbabel`
    - selecting only the cif files we already have charges calculated using [lsmo-epfl/EQeq](https://github.com/lsmo-epfl/EQeq) (4140 MOFs)
    - correcting the name of the CIF file with `python check_and_convert_filenames.py`. `aiida-raspa` do not accept nonalphanumeric (exept underscore) in the filename (e.g. j.inoche.2015.06.036_inc06102-mmc1_clean_openbabel.cif).

- **Running the calculation**
command to submit all jobs at once from the root directory:
```bash
verdi run eqeq_raspa_screening.py raspa_run_slurm \
    --inputpath examples/subset-coremof/cif_converted/ \
    --num_max 80
```
To test the submission on a few structures rather than the whole database, one can pass the maximum number of submission with `--num_max`.

## Troubleshooting

### Aiida

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

### Slurm
The default configuration of Slurm using `apt` might be limited. We noticed for example that we could not run more than one job in the same time and Slurm was chaining jobs. To fix this, we changed the configuration file for Slurm, usually in `/etc/slurm/slurm.conf`, and add the following line at the end of the file :
```
SelectType=select/cons_res
SelectTypeParameters=CR_Core

# Define a single compute node with only 40 cpus over the total 40 cpus
NodeName=localhost CPUs=40 Boards=1 SocketsPerBoard=1 CoresPerSocket=40 ThreadsPerCore=1 RealMemory=64031

PartitionName=debug Nodes=localhost Default=YES MaxTime=INFINITE State=UP
```


## Additional scripts
### Cif name checker
If you use as inputs CIF files with filenames using characters different from `_` and alphanumeric characters, the screening will fail. To fix that, one can copy and rename the problematic CIF filenames with :
```
python scripts/check_and_convert_filenames.py
```
The input set of CIF files must be present in `examples/cif/` and the output CIF files will be copied to  `examples/cif_converted/`.

### Visualize output data
It might be a bit complicated to look for the data located in the database for a non-expert of Aiida, the following script allows to quickly identify the path directory of a specific calculation :
```
python scripts/calcjob2path.py
```
You will need to enter your aiida (database) profile (see `verdi profile list`) and the PK, the index of your calculation process (e.g. found using `verdi process list`). It will return the absolute path where the remote data is stored (e.g. */data/hardiagon/.aiida/f7/9b/8e3b-dee2-4f0c-be99-45a2e47ccb21*)