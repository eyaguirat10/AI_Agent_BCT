import subprocess

with open("requirements.txt") as f:
    packages = [line.strip().split("==")[0] for line in f if line.strip() and not line.startswith("#")]

for package in packages:
    subprocess.run(["pip", "uninstall", "-y", package])
