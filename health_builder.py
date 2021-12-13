import csv
import socket
from datetime import datetime
import send_email
from health_check import cpu_times, disk_utilization, ram_usage, network_utilization

MEGABYTE = 1048576  # number of bytes in one megabyte
warnings = []
time_now = datetime.now().strftime('%d-%b-%Y %H:%M:%S')


def main():
    parse_cpu()
    parse_memory()
    parse_disk()
    print(warnings)


# parse cpu
def parse_cpu():
    cpu_data = cpu_times()
    print(cpu_data)
    if cpu_data["percent"] > 10:
        warnings.append(f"[cpu][{socket.gethostname()}][{time_now}] high cpu usage: {cpu_data['percent']:.2f}")


# parse memory
def parse_memory():
    ram_data = ram_usage()
    print(ram_data)
    if ram_data["percent"] > 50:
        warnings.append(
            f"[ram][{socket.gethostname()}][{time_now}] high memory usage: {ram_data['percent']}")


# parse disk
def parse_disk():
    disk_data = disk_utilization()
    print(disk_data)
    for mount, disk in disk_data.items():
        warnings.append(
            f"[disk: {mount}][{socket.gethostname()}][{time_now}] high disk usage: {disk['percent']}")


# parse network

if __name__ == "__main__":
    main()
