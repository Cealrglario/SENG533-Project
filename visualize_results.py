import os
import glob
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

RESULTS_DIR = 'results'
OUTPUT_DIR = 'graphs'

def load_data():
    """Parses all CSV files in the results directory and returns the raw data."""
    print("Parsing result files...")
    data = []
    
    stat_files = glob.glob(os.path.join(RESULTS_DIR, '*_stats.csv'))
    
    if not stat_files:
        print(f"No stat files found in '{RESULTS_DIR}'. Have you run the experiments yet?")
        return None, None

    for stat_file in stat_files:
        base_name = os.path.basename(stat_file)
        parts = base_name.replace('_stats.csv', '').split('_')
        
        if len(parts) < 5:
            continue
            
        arch = parts[0]
        load = parts[1]
        cores = int(parts[2].replace('c', ''))
        users = int(parts[3].replace('u', ''))
        run = int(parts[4].replace('run', ''))
        
        try:
            df_stats = pd.read_csv(stat_file)
            agg_row = df_stats[df_stats['Name'] == 'Aggregated'].iloc[0]
            throughput = agg_row['Requests/s']
            resp_time = agg_row['Average Response Time']
        except Exception as e:
            continue
            
        cpu_file = stat_file.replace('_stats.csv', '_cpu.csv')
        cpu_util = 0.0
        if os.path.exists(cpu_file):
            try:
                df_cpu = pd.read_csv(cpu_file)
                cpu_util = df_cpu['CPU_Percentage'].mean() / cores
            except Exception as e:
                pass
                
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
        
    df_raw = pd.DataFrame(data)
    
    # Calculate both Mean and Standard Deviation for the summary table
    print("Calculating statistical means and standard deviations...")
    df_summary = df_raw.groupby(['Architecture', 'Workload', 'Cores', 'Concurrent Users']).agg(
        {
            'Throughput (Req/s)': ['mean', 'std'],
            'Response Time (ms)': ['mean', 'std'],
            'CPU Utilization (%)': ['mean', 'std']
        }
    ).reset_index()
    
    # Flatten the multi-level column names (e.g., "Throughput_mean", "Throughput_std")
    df_summary.columns = ['_'.join(col).strip() if col[1] else col[0] for col in df_summary.columns.values]
    
    return df_raw, df_summary

def generate_plots(df_raw):
    """Generates graphs with 95% Confidence Intervals using the raw data."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    sns.set_theme(style="whitegrid")
    
    metrics = {
        'Throughput (Req/s)': 'higher_is_better',
        'Response Time (ms)': 'lower_is_better',
        'CPU Utilization (%)': 'context_dependent'
    }

    workloads = df_raw['Workload'].unique()
    
    print("Generating visualizations with 95% Confidence Intervals...")
    
    for workload in workloads:
        workload_data = df_raw[df_raw['Workload'] == workload]
        
        for metric in metrics.keys():
            # Pass the RAW data to Seaborn. 
            # errorbar=('ci', 95) tells it to calculate the 95% confidence interval across the 10 runs.
            # capsize=0.1 adds the horizontal ticks at the top and bottom of the error bars.
            g = sns.catplot(
                data=workload_data, 
                x='Cores', 
                y=metric, 
                hue='Architecture', 
                col='Concurrent Users', 
                kind='point', 
                errorbar=('ci', 95), 
                capsize=0.1,         
                height=5, 
                aspect=1,
                palette={'Apache': '#D22128', 'Node': '#68A063'}
            )
            
            g.fig.suptitle(f"{workload} Workload: {metric} vs. CPU Cores (95% CI)", y=1.05, fontsize=16)
            g.set_axis_labels("Number of CPU Cores", metric)
            
            filename = f"{OUTPUT_DIR}/{workload.lower()}_{metric.split(' ')[0].lower()}_scaling.png"
            plt.savefig(filename, bbox_inches='tight', dpi=300)
            plt.close()
            print(f"Saved: {filename}")

if __name__ == "__main__":
    df_raw, df_summary = load_data()
    
    if df_raw is not None and not df_raw.empty and df_summary is not None and not df_summary.empty:
        summary_csv = f"{OUTPUT_DIR}/aggregated_results_summary.csv"
        df_summary.to_csv(summary_csv, index=False)
        print(f"Saved statistical summary (Means & Standard Deviations) to: {summary_csv}")
        
        generate_plots(df_raw)
        print("\nAll data processing and visualization complete!")
    else:
        print("No data was processed. Please check your results directory.")