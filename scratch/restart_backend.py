import subprocess
import re
import os

out = subprocess.check_output("netstat -ano", shell=True).decode()
pids = set()
for line in out.splitlines():
    if ":8000" in line and "LISTENING" in line:
        parts = line.strip().split()
        pid = parts[-1]
        pids.add(pid)

print("Found listening PIDs on port 8000:", pids)
for pid in pids:
    print(f"Killing PID {pid}")
    os.system(f"taskkill /F /PID {pid}")

print("Done.")
