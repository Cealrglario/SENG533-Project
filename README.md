## How to Run Experiments/Visualize Data
1. Open a bash terminal in the root of this project directory
2. Give yourself permission to run the scripts with ```chmod +x run_experiments.sh```
3. Run the bash script to automate all experimnets with ```./run_experiments.sh```
   - NOTE: This will take a LONG TIME, as there are 480 experiments, with each experiment running for 30 seconds
4. Ensure Python dependencies are installed for visualizations. Run ```pip install pandas matplotlib seaborn```
5. Run Python script to visualize data with ```python visualize_results.py```
6. You will find generated csv's in the ```results``` folder and the PNG's of the generated graphs/visualizations in the ```graphs``` folder