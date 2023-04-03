import csv

with open('../log-files/final-test-data.csv', 'r') as final_test_data, open('../log-files/final-test-data-with-bias.csv', 'w', newline='') as final_test_data_with_bias:
    data_reader = csv.reader(final_test_data)
    complete_data_writer = csv.writer(final_test_data_with_bias)

    for data in data_reader:
        data.insert(-1, 1)
        complete_data_writer.writerow(data)