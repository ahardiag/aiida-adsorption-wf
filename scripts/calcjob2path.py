import aiida
from aiida.orm import load_node, CalcJobNode
from aiida.common.exceptions import NotExistent,ProfileConfigurationError

# Input the name of the AiiDA profile and the PK of the calculation job
profile_name = input("Enter the name of the AiiDA profile: ")
calcjob_pk = input("Enter the PK of the calculation job: ")

try:
    # Load the specified AiiDA profile
    aiida.load_profile(profile_name)
except ProfileConfigurationError:
    print(f"Error: The specified AiiDA profile '{profile_name}' does not exist.")
    exit(1)

try:
    # Convert PK to integer and load the node
    calcjob_pk = int(calcjob_pk)
    raspa_node = load_node(calcjob_pk)
    
    # Check if the node is a CalcJobNode
    if not isinstance(raspa_node, CalcJobNode):
        print(f"Error: The node with PK {calcjob_pk} is not a CalcJob.")
        exit(1)

    # Access the remote folder output node (RemoteData type)
    remote_folder_node = raspa_node.outputs.remote_folder

    # Get the remote folder path
    remote_folder_path = remote_folder_node.get_remote_path()
    print(f"Remote folder path: {remote_folder_path}")

except ValueError:
    print("Error: The PK must be an integer.")
except NotExistent:
    print(f"Error: No node found with PK {calcjob_pk} or it does not have a remote folder.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
