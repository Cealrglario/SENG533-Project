import os
import glob
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

RESULTS_DIR = 'results'
OUTPUT_DIR = 'graphs'

def load_and_aggregate_data():
    """Parses all CSV files in the results directory and aggregates the data."""
    print("Parsing result files...")
    data = []
    
    # Locate all Locust stat files
    stat_files = glob.glob(os.path.join(RESULTS_DIR, '*_stats.csv'))
    
    if not stat_files:
        print(f"No stat files found in '{RESULTS_DIR}'. Have you run the experiments yet?")
        return None

    for stat_file in stat_files:
        # Extract factors from filename (e.g., Apache_Dynamic_4c_200u_run1_stats.csv)
        base_name = os.path.basename(stat_file)
        parts = base_name.replace('_stats.csv', '').split('_')
        
        if len(parts) < 5:
            continue
            
        arch = parts[0]
        load = parts[1]
        cores = int(parts[2].replace('c', ''))
        users = int(parts[3].replace('u', ''))
        run = int(parts[4].replace('run', ''))
        
        # 1. Get Throughput and Response Time from Locust
        try:
            df_stats = pd.read_csv(stat_file)
            # Grab the final "Aggregated" row for the total run metrics
            agg_row = df_stats[df_stats['Name'] == 'Aggregated'].iloc[0]
            throughput = agg_row['Requests/s']
            resp_time = agg_row['Average Response Time']
        except Exception as e:
            print(f"Error reading {stat_file}: {e}")
            continue
            
        # 2. Get CPU Utilization from Docker Stats
        cpu_file = stat_file.replace('_stats.csv', '_cpu.csv')
        cpu_util = 0.0
        if os.path.exists(cpu_file):
            try:
                df_cpu = pd.read_csv(cpu_file)
                # Calculate the mean CPU percentage across the duration of this specific test run
                cpu_util = df_cpu['CPU_Percentage'].mean()
            except Exception as e:
                print(f"Warning: Could not parse CPU stats for {cpu_file}")
                
        # Append to our dataset
        data.append({
            'Architecture': arch,
            'Workload': load,
            'Cores': cores,
            'Concurrent Users': users,
            'Run': run,
            'Throughput (Req/s)': throughput,
            'Response Time (ms)': resp_time,
            'CPU Utilization (%)': cpu_util
        })
        
    df = pd.DataFrame(data)
    
    # Average the metrics across the 10 runs for each configuration to ensure statistical reliability
    print("Aggregating averages across test runs...")
    grouped_df = df.groupby(['Architecture', 'Workload', 'Cores', 'Concurrent Users']).mean().reset_index()
    return grouped_df

def generate_plots(df):
    """Generates and saves the required graphs for the performance evaluation report."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    sns.set_theme(style="whitegrid")
    
    metrics = {
        'Throughput (Req/s)': 'higher_is_better',
        'Response Time (ms)': 'lower_is_better',
        'CPU Utilization (%)': 'context_dependent'
    }

    workloads = df['Workload'].unique()
    
    print("Generating visualizations...")
    
    # Create separate charts for Static and Dynamic workloads
    for workload in workloads:
        workload_data = df[df['Workload'] == workload]
        
        for metric in metrics.keys():
            # Create a factor plot showing Metric vs. Cores, separated by Architecture, with columns for User load
            g = sns.catplot(
                data=workload_data, 
                x='Cores', 
                y=metric, 
                hue='Architecture', 
                col='Concurrent Users', 
                kind='point', # Point charts clearly show the "Scalability" trendlines
                height=5, 
                aspect=1,
                palette={'Apache': '#D22128', 'Node': '#68A063'} # Brand colors for clarity
            )
            
            g.fig.suptitle(f"{workload} Workload: {metric} vs. CPU Cores", y=1.05, fontsize=16)
            g.set_axis_labels("Number of CPU Cores", metric)
            
            # Save the figure
            filename = f"{OUTPUT_DIR}/{workload.lower()}_{metric.split(' ')[0].lower()}_scaling.png"
            plt.savefig(filename, bbox_inches='tight', dpi=300)
            plt.close()
            print(f"Saved: {filename}")

if __name__ == "__main__":
    df_aggregated = load_and_aggregate_data()
    
    if df_aggregated is not None and not df_aggregated.empty:
        # Save the aggregated statistical data to a clean CSV for your report tables
        summary_csv = f"{OUTPUT_DIR}/aggregated_results_summary.csv"
        df_aggregated.to_csv(summary_csv, index=False)
        print(f"Saved numerical summary to: {summary_csv}")
        
        generate_plots(df_aggregated)
        print("\nAll data processing and visualization complete!")
    else:
        print("No data was processed. Please check your results directory.")