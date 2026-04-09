## How to Run Experiments/Visualize Data

### Prerequisites (Windows Users)
This project relies on strict CPU core pinning (`taskset`) to isolate the load generator from the web servers. Because this is a Linux-specific kernel command, the automated test suite **cannot** be run natively in the Windows Command Prompt, PowerShell, or Git Bash. You must use WSL.

1. **Install WSL (Windows Subsystem for Linux):** Open PowerShell as Administrator and run `wsl --install`. Restart your computer if prompted (Ubuntu is the default and recommended distribution).
2. **Install Docker Desktop:** Download and install Docker Desktop for Windows. In Docker Desktop's settings, ensure that **"Use the WSL 2 based engine"** is checked and enabled.
3. **Install Python in WSL:** Even if you have Python installed on Windows, you need it inside your Linux environment. Open your WSL/Ubuntu terminal and run:
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip

### Main steps

1. Open a bash terminal in the root of this project directory
2. Give yourself permission to run the scripts with ```chmod +x run_experiments.sh```
3. Run the bash script to automate all experimnets with ```./run_experiments.sh```
   - NOTE: This will take a LONG TIME, as there are 480 experiments, with each experiment running for 30 seconds
4. Ensure Python dependencies are installed for visualizations. Run ```pip install pandas matplotlib seaborn```
5. Run Python script to visualize data with ```python visualize_results.py```
6. You will find generated csv's in the ```results``` folder and the PNG's of the generated graphs/visualizations in the ```graphs``` folder