import csv

with open('../log-files/processed_data.csv', 'r') as processed_data_file, open('../log-files/complete_processed_data.csv', 'w', newline='') as complete_processed_data_file:
    data_reader = csv.reader(processed_data_file)
    complete_data_writer = csv.writer(complete_processed_data_file)

    number_of_worker_nodes = 0
    for data in data_reader:
        data.insert(2, number_of_worker_nodes)
        complete_data_writer.writerow(data)
