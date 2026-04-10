#!/bin/bash

# Define Apache p-core mappings for the Intel Core Ultra 9 275HX
declare -A APACHE_CORES
APACHE_CORES[1]="0"
APACHE_CORES[2]="0,1"
APACHE_CORES[3]="0,1,10"
APACHE_CORES[4]="0,1,10,11"

# Define Node p-core mappings for the Intel Core Ultra 9 275HX
declare -A NODE_CORES
NODE_CORES[1]="12"
NODE_CORES[2]="12,13"
NODE_CORES[3]="12,13,22"
NODE_CORES[4]="12,13,22,23"

# Define experimental factors
CORES=(1 2 3 4)
ARCHITECTURES=("Apache" "Node")
WORKLOADS=("Static" "Dynamic")
USERS=(50 100 200)
TOTAL_RUNS=10

DURATION="60s"
SPAWN_RATE=50

mkdir -p results

echo "Starting SENG 533 Group 32 automated test suite..."

# Automation loops
for core in "${CORES[@]}"; do

    # Export isolated CPU sets
    export APACHE_CPU_SET="${APACHE_CORES[$core]}"
    export NODE_CPU_SET="${NODE_CORES[$core]}"

    echo "=================================================="
    echo "Configuring Docker: Apache on [ $APACHE_CPU_SET ] | Node on [ $NODE_CPU_SET ]"

    docker compose down
    docker compose up -d

    sleep 5

    for arch in "${ARCHITECTURES[@]}"; do
        for load in "${WORKLOADS[@]}"; do

            LOCUST_CLASS="${arch}${load}User"

            # Warm-up phase to prevent first runs from being wildly inaccurate
            echo "Warming up $arch server for $load workload (10s)..."
            taskset -c 2-9 python3 -m locust -f locustfile.py "$LOCUST_CLASS" \
                --headless \
                -u 20 \
                -r 20 \
                --run-time "10s" \
                --only-summary > /dev/null 2>&1
            sleep 2
            # --------------------------

            for user_count in "${USERS[@]}"; do
                for (( run=1; run<=TOTAL_RUNS; run++ )); do
                    
                    FILE_PREFIX="results/${arch}_${load}_${core}c_${user_count}u_run${run}"
                    
                    echo "Running: $LOCUST_CLASS | Cores: $core | Users: $user_count | Run: $run of $TOTAL_RUNS"
                    
                    # Determine which container we are testing
                    if [ "$arch" == "Apache" ]; then
                        TARGET_CONTAINER="apache_container"
                    else
                        TARGET_CONTAINER="node_container"
                    fi

                    # Start logging CPU utilization
                    echo "CPU_Percentage" > "${FILE_PREFIX}_cpu.csv"
                    (while true; do
                        docker stats $TARGET_CONTAINER --no-stream --format "{{.CPUPerc}}" | sed 's/%//' >> "${FILE_PREFIX}_cpu.csv"
                        sleep 1
                    done) &
                    CPU_LOGGER_PID=$!

                    # Force Locust to run ONLY on any one of the logical cores 2 through 9
                    # This prevents it from touching the P-cores assigned to Docker and prevents resource contention
                    taskset -c 2-9 python3 -m locust -f locustfile.py "$LOCUST_CLASS" \
                        --headless \
                        -u "$user_count" \
                        -r "$SPAWN_RATE" \
                        --run-time "$DURATION" \
                        --csv "$FILE_PREFIX" \
                        --only-summary

                    # Stop the CPU logger when Locust finishes
                    kill $CPU_LOGGER_PID

                done
            done
        done
    done
done

echo "=================================================="
echo "All 480 experiments completed successfully. Check the /results folder."