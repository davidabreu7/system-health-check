"""
Script made by David Abreu
github: github.com/davidabreu7/system-health-check

System health monitor script in python that checks system metrics, store data in csv
and make reports based on metrics  collectd
"""
import psutil


def main():
    """
    function calls and printing values
    """
    print(cpu_times())
    print(ram_usage())
    print(disk_utilization())
    print(network_utilization())


def cpu_times() -> dict:
    """
    get CPU counters from psutil.cpu_times() -> user, system, idle
    :return: dictionary of float values for the system cpu usage
    """
    cpu_get_time = psutil.cpu_times()
    cpu_checks = ["user", "system", "idle", ]
    cpu_avg_time = [x / psutil.cpu_count() * 100 for x in psutil.getloadavg()]
    cpu_load = {field: getattr(cpu_get_time, field) for field in cpu_checks}
    cpu_load["percent"] = cpu_avg_time[1]
    return cpu_load


def ram_usage() -> dict:
    """
    get ram usage values from psutil.virtual memory -> total, available, used, percent
    :return: dictionary with values for the system ram usage
    """
    ram_system = psutil.virtual_memory()
    ram_checks = ["total", "available", "used", "percent"]
    ram_system = {check: getattr(ram_system, check) for check in ram_checks}
    return ram_system


def disk_utilization() -> dict:
    """
    get disk utilization from psutil.disk_partitions and disk_usage for each partition
    :return: dictionary of each partition and its respective disk usage values
    """
    disk_part = psutil.disk_partitions()
    disk_checks = ["total", "used", "free", "percent"]
    disk_util = {mount.mountpoint: {check: getattr(psutil.disk_usage(mount.mountpoint), check)
                                    for check in disk_checks}
                 for mount in disk_part}

    return disk_util


def network_utilization() -> dict:
    """
    get network io counters from system nic
    :return: dictionary with network io counters
    """
    net_util = psutil.net_io_counters()
    net_checks = ["bytes_sent", "bytes_recv", "errin", "errout", "dropin", "dropout"]
    net_system = {check: getattr(net_util, check) for check in net_checks}
    return net_system


if __name__ == "__main__":
    main()
