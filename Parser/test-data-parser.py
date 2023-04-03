import csv
from datetime import datetime

with open('../log-files/final-metric-logs.csv', 'r') as metrics_logger_file, open('../log-files/experiment-results.csv', 'r') as experiment_results_file:
    metrics_logger_reader = csv.DictReader(metrics_logger_file)
    experiment_results_reader = csv.DictReader(experiment_results_file)

    processed_data = []
    experiment_results_extracted = []

    for data_row in experiment_results_reader:
        date = data_row['date'].replace('/', '-')
        start_time = datetime.strptime(date + ' ' + data_row['start_time'], '%Y-%m-%d %H:%M:%S')
        end_time = datetime.strptime(date + ' ' + data_row['end_time'], '%Y-%m-%d %H:%M:%S')
        power = float(data_row['power'])

        experiment_results_extracted.append([start_time, end_time, power])

    i = 0

    num_of_containers = 0
    container_cpu_sum = 0
    container_mem_sum = 0
    master_cpu_sum = 0
    master_mem_sum = 0
    count = 0

    start_time = experiment_results_extracted[i][0]
    end_time = experiment_results_extracted[i][1]
    power = experiment_results_extracted[i][2]

    for metrics_row in metrics_logger_reader:
        metrics_time = datetime.strptime(metrics_row['timestamp'][:19], '%Y-%m-%d %H:%M:%S')

        if start_time <= metrics_time:
            if end_time >= metrics_time:
                num_of_containers = int(metrics_row['count_container'])
                container_cpu_sum += int(metrics_row['container_cpu_usage'])
                container_mem_sum += int(metrics_row['container_mem_usage'])
                master_cpu_sum += int(metrics_row['master_node_cpu'])
                master_mem_sum += int(metrics_row['master_node_mem'])
                count += 1
            else:
                if count != 0:
                    container_cpu_avg = float(container_cpu_sum) / count
                    container_mem_avg = float(container_mem_sum) / count
                    master_cpu_avg = float(master_cpu_sum) / count
                    master_mem_avg = float(master_mem_sum) / count

                    processed_data.append([master_cpu_avg, master_mem_avg, num_of_containers, container_cpu_avg, container_mem_avg, power])

                i += 1
                if i == len(experiment_results_extracted):
                    break
                else:
                    start_time = experiment_results_extracted[i][0]
                    end_time = experiment_results_extracted[i][1]
                    power = experiment_results_extracted[i][2]

    with open('../log-files/processed_data.csv', 'a', newline='') as f_object:
        writer = csv.writer(f_object)
        for data in processed_data:
            writer.writerow(data)
