"""
Application made by David Abreu
github: github.com/davidabreu7/system-health-check

System health monitor script in python:
 - checks system metrics,
 - send alert emails
 - store data in csv to make reports based on metrics collectd (TODO)
"""
import math
import os.path
import socket
import sys
import logbook
from datetime import datetime
from send_email import send_email
from system_check import cpu_times, disk_utilization, ram_usage

time_now = datetime.now().strftime('%d-%b-%Y %H:%M:%S')
warnings = []


def main():
    init_logging()
    parse_cpu()
    print(parse_memory())
    print(parse_disk())
    if len(warnings) > 0:
        email_body = "".join(warn + "\n" for warn in warnings)
        send_email(f"Subject: ALERTA {socket.gethostname()} - servidores DIPROD\n\n{email_body}")


def convert_size(size_bytes):
    """
    byte converter function
    :param size_bytes:
    :return: return the biggest possible size
    """
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i])


def parse_cpu():
    """
    gets info from cpu_times() and check alert trigger
    If alert is triggered logs event and sends email
    :return:
    """
    cpu_data = cpu_times()
    alert_trigger = 10
    log_cpu = logbook.Logger("CPU")
    if cpu_data["percent"] > alert_trigger:
        log_cpu.warning(f"high cpu usage: {cpu_data['percent']:.2f}")
        warnings.append(f"ALERTA: {socket.gethostname()}\n\n alto uso de CPU: {cpu_data['percent']:.2f}")


def parse_memory():
    """
    gets info from ram_usage() and checks alert trigger
    If alert is triggered logs event and sends email
    :return: ram_usage() converted with convert_size()
    """
    ram_data = ram_usage()
    alert_trigger = 10
    ram_parsed = {key: convert_size(value) for key, value in ram_data.items() if key != "percent"}
    log_ram = logbook.Logger("RAM")

    if ram_data["percent"] > alert_trigger:
        log_ram.warning(f"high memory usage: {ram_data['percent']}")
        warnings.append(f"ALERTA: {socket.gethostname()}\n\n alto uso de MEMORIA: {ram_data['percent']:.2f}")
    return ram_parsed


def parse_disk():
    """
    gets info from disk_utilizaiton() and checks alert trigger
    If alert is triggered logs event and sends email
    :return: disk_utilization() converted with convert_size()
    """
    disk_data = disk_utilization()
    alert_trigger = 10
    log_disk = logbook.Logger("DISK")
    for mount_dir, mount_space in disk_data.items():
        if disk_data[mount_dir]["percent"] > alert_trigger:
            log_disk.warning(f"high disk usage: {mount_space['percent']}")
            warnings.append(
                f"ALERTA: {socket.gethostname()}\n\n alto uso de DISCO: {disk_data[mount_dir]['percent']:.2f}")
    return {mount: {category: convert_size(space) for category, space in disk_space.items() if category != "percent"}
            for mount, disk_space in disk_data.items()}


def init_logging():
    if not os.path.exists("../log"):
        os.mkdir("../log")
    level = logbook.WARNING
    log_path = os.path.join("../log", socket.gethostname()) + ".log"

    if log_path:
        logbook.FileHandler(log_path, level=level).push_application()
    else:
        logbook.StreamHandler(sys.stdout, level=level).push_application()


if __name__ == "__main__":
    main()
