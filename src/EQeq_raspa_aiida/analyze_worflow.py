import shutil,os
from datetime import datetime
from tqdm import tqdm
from aiida import load_profile
from aiida.orm import QueryBuilder
from aiida.plugins import CalculationFactory
from EQeq_raspa_aiida.calcjob2path import calcjob2path

##################### PARAMETERS ##################################

profile_name = "hardiagon" # Profile name of the Aiida database
start_time = datetime(2024, 5, 16, 16 , 0, 0) # Start datetime
end_time = datetime(2024, 5, 17, 9, 0, 0)     # Start datetime
output_directory="cifs_output"

##################### PARAMETERS ##################################

# Create output directory
output_directory=(f"{os.getcwd()}/{output_directory}")
os.makedirs(output_directory,exist_ok=True)

# Load the AiiDA profile
load_profile()

# RaspaCalculation class via the CalculationFactory
RaspaCalculation = CalculationFactory('raspa')

# Create a QueryBuilder instance
qb = QueryBuilder()

# Append the RaspaCalculation and set filters for the creation time range
qb.append(RaspaCalculation, filters={
    'ctime': {
        '>=': start_time,
        '<=': end_time
    },
    'attributes.process_state': 'finished'
})

# Count the number of nodes within the specified time range
count = qb.count()
print(f"Number of RaspaCalculation nodes created between {start_time} and {end_time}: {count}")

# Print all calcjob PKs in a file
output_file = f"{os.getcwd()}/list_pk.csv"
with open(output_file,'w') as f:
    for entry in qb.iterall():
        print(entry[0].pk,file=f)
print(f"File with list of PKs (calculation IDs): {output_file}")

# Copy the CIF files with the EQeq charges
count=0
for entry in tqdm(qb.iterall(), 
              desc=f"Copying CIF files", 
              unit="iteration", 
              total=qb.count(), 
              bar_format="{l_bar}{bar} {n_fmt}/{total_fmt} ({percentage:3.0f}%)"):
    node = entry[0]
    pk = node.pk
    path = calcjob2path(profile_name,pk)
    cif_name = list(node.inputs.framework.keys())[0]   # get Cif name from the input node connected to Calcjob node
    if os.path.isfile(f"{path}/Movies/System_0/Framework_0_final_1_1_1_P1.cif"):
        shutil.copy(f"{path}/Movies/System_0/Framework_0_final_1_1_1_P1.cif",f"{output_directory}/{cif_name}.cif")
        count+=1

print(f"Output directory with {count} CIF files: {output_directory}")