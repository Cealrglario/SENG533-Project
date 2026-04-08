## How to Run Experiments/Visualize Data
1. Give yourself permission to run the scripts with ```chmod +x run_experiments.sh```
2. Run the bash script to automate all experimnets with ```./run_experiments.sh```
   - NOTE: This will take a LONG TIME, as there are 480 experiments, with each experiment running for 30 seconds
3. Ensure Python dependencies are installed for visualizations. Run ```pip install pandas matplotlib seaborn```
4. Run Python script to visualize data with ```python visualize_results.py```
5. You will find generated csv's in the ```results``` folder and the PNG's of the generated graphs/visualizations in the ```graphs``` folder