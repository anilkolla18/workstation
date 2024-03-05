#!/usr/bin/env python3
import os
from datetime import datetime

# Define the function for displaying usage information
def usage():
    print(f"Usage: {os.path.basename(__file__)} DPHOST DOMAIN")
    print("required:")
    print("DPHOST, DOMAIN")
    exit()

# Check if the correct number of arguments are provided
if len(sys.argv) != 3:
    usage()

DPHOST = sys.argv[1]
DOMAIN = sys.argv[2]
TMPFILE = "/tmp/tempfile.dp"
OUTFILE = "/tmp/outfile.dp"
TS = datetime.now().strftime("%Y%m%d%H%MXS")

print(f"dphost: {DPHOST}")
print(f"domain: {DOMAIN}")

for host in DPHOST:
    print(f"===========Running on {host}===========")
    with open(TMPFILE, 'w') as f:
        f.write(f"{DP_USER_ID}\n{DP_PASSWORD}\n{DOMAIN}\nshow version\nexit\n")

    # Execute SSH command
    os.system(f"ssh -T {host} < {TMPFILE} 1 > {OUTFILE}.{TS}")

    # Process the output file
    with open(f"{OUTFILE}.{TS}") as f:
        lines = f.readlines()
        for line in lines:
            if "Version" in line and "build" not in line:
                print(line.strip())

    # Clean up temporary files
    os.remove(TMPFILE)
    os.remove(f"{OUTFILE}.{TS}")
    print()

