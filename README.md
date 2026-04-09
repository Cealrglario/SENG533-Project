# SENG 533 Project: Performance Evaluation of Apache vs. Node.js (Group 32)

This repository contains an automated performance evaluation pipeline designed to benchmark and compare the scaling efficiency of Apache and Node.js web servers under static and dynamic workloads using Locust and Docker.

---

## Important Prerequisites (Windows Users)
This project relies on strict CPU core pinning (`taskset`) to isolate the load generator from the web servers and prevent resource contention. Because `taskset` is a Linux-specific kernel utility, the automated test suite **cannot** be run natively in the Windows Command Prompt, PowerShell, or Git Bash. 

You must use WSL (Windows Subsystem for Linux) to execute this pipeline.

### 1. Install & Configure WSL
1. Open PowerShell as Administrator and run `wsl --install`. (Ubuntu is the default and recommended distribution).
2. Restart your computer if prompted.
3. If you have Docker Desktop installed, open its Settings > **Resources** > **WSL Integration**. Ensure "Enable integration with my default WSL distro" is checked, and explicitly toggle the switch for **Ubuntu** to the ON position.

---

## Environment Setup (One-Time Configuration)

Because WSL mounts your Windows file system, using a Windows-based Python virtual environment (like a standard `.venv`) will cause terminal crashes when attempting to run Linux binaries. You must create a completely isolated Linux virtual environment specifically for WSL.

**1. Open your Ubuntu Terminal**
Ensure you are using the Ubuntu terminal, not Git Bash.

**2. Navigate to the Project Directory**
Your Windows `C:\` drive is mounted under `/mnt/c/`. Navigate to the folder (update the path with your actual Windows username):

```bash
cd "/mnt/c/Users/YOUR_WINDOWS_USERNAME/path/to/SENG533-Project"
```

**3. Install Python Core Libraries**

```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
```

**4. Create & Activate the WSL Sandbox**
Create a new virtual environment named `.venv-wsl` to prevent conflicts with any existing Windows environments:

```bash
python3 -m venv .venv-wsl
source .venv-wsl/bin/activate
```
*(You should now see `(.venv-wsl)` at the start of your terminal prompt).*

**5. Install All Dependencies**
With the sandbox activated, install the load generator and data visualization libraries:

```bash
pip install locust pandas matplotlib seaborn
```

---

## Execution Instructions

**Crucial Note Before Running:** The full test suite takes approximately **4 hours** to complete. Ensure your computer is plugged in and your OS power settings are strictly set to **"Never Sleep."** If the computer sleeps, Docker will suspend and the tests will fail. 

**1. Activate the Environment**
If you opened a new terminal, you must reactivate the WSL sandbox so the script can locate Locust:

```bash
source .venv-wsl/bin/activate
```

**2. Grant Execution Permissions**

```bash
chmod +x run_experiments.sh
```

**3. Run the Automated Suite**
Execute the bash script. This will systematically tear down and rebuild the Docker containers, execute Locust load tests across 480 configurations, and log the CPU utilizations.

```bash
./run_experiments.sh
```

---

## Data Visualization

Once the bash script completes successfully, all raw data will be populated inside the `/results` folder. 

To process this data into scalability trendlines and calculate the statistical confidence intervals:

**1. Ensure the Environment is Active**

```bash
source .venv-wsl/bin/activate
```

**2. Run the Processing Script**

```bash
python3 visualize_results.py
```

**3. Review the Output**
Check the `/graphs` folder. You will find:
* `.png` graphs illustrating Throughput, Response Time, and normalized CPU Utilization across the core counts (with 95% Confidence Intervals).
* `aggregated_results_summary.csv`, containing the formal mathematical table of all calculated means and standard deviations for the final report.