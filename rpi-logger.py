from pyembedded.raspberry_pi_tools.raspberrypi import PI
import time
import datetime
import os
from csv import writer

# get node name this script runs on
hostname = os.uname()[1]
pi = PI()

def get_data():
    # get parameters via pymbedded
    ram = pi.get_ram_info()
    disk = pi.get_disk_space()
    cpu = pi.get_cpu_usage()
    temperature = pi.get_cpu_temp()

    return [temperature, ram[1], disk[1], cpu, str(datetime.datetime.now())]


while True:
    metrics = get_data()
    with open('./logs/node-' + hostname + '.csv', 'a') as f_object:
        writer_object = writer(f_object)
        writer_object.writerow(metrics)
        f_object.close()
    time.sleep(1)  # sleep for 1 seconds before next call