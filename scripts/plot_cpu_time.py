import sys
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter

# Check if the CSV filename is provided as a command-line argument
if len(sys.argv) < 2:
    print("Usage: python plot_cpu_time.py <path_to_csv_file>")
    sys.exit(1)

# Read the data into a pandas DataFrame
df = pd.read_csv(sys.argv[1],sep=",")

# Convert the Timestamp column to datetime
df['Timestamp'] = pd.to_datetime(df['Timestamp'])
df['Minutes'] = (df['Timestamp'] - df['Timestamp'].iloc[0]).dt.total_seconds() / 60


# Set the Timestamp column as the index
df.set_index('Timestamp', inplace=True)

# Plot CPUs Used over time
plt.figure(figsize=(10, 6))
plt.plot(df['Minutes'], df['CPUs Used'], marker='o', linestyle='-', color='b')

plt.xlabel('Minutes since start',fontsize=15)
plt.ylabel('CPUs Used',fontsize=15)
plt.title('CPUs Used Over Time')

# Rotate date labels for better readability
#plt.xticks(rotation=45)
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)


# Show the plot
plt.tight_layout()
plt.show()