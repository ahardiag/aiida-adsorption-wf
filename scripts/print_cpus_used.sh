#!/bin/bash

user=$(id -nu)              # User
executable="simulate"       # Executable to follow
threshold=10                # Threshold CPU usage to consider a CPU as "used"
interval=5                  # Interval in seconds between checks
log_file="./cpu_usage.log"  # Log file to store the CPU usage over time

echo "Timestamp,CPUs Used" > "$log_file"
while true; do
    # Get the current date and time
    timestamp=$(date +"%Y-%m-%d %H:%M:%S")

    # Count how many processes are using more than the threshold CPU percentage
    cpus_used=$(ps -eo pid,comm,pcpu | awk -v exe="$executable" -v threshold="$threshold" '$2==exe && $3>=threshold { count++ } END { print count+0 }')


    echo "$timestamp,$cpus_used" #>> "$log_file"
    echo "$timestamp,$cpus_used" >> "$log_file"
    sleep "$interval"
done
