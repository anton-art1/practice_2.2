import psutil


def getCpuInfo():
    return psutil.cpu_percent(interval=1)


def getMemoryInfo():
    return psutil.virtual_memory().used / (1024 ** 3)


def getDiskInfo():
    diskPartitions = psutil.disk_partitions()
    disksUsage = []
    for partition in diskPartitions:
        diskUsage = psutil.disk_usage(partition.mountpoint)
        disksUsage.append((partition.device, diskUsage.percent))
    return disksUsage

def main():
    print("ЗАГРУЗКА CPU:")
    print(f"{getCpuInfo()}%", '\n')

    print("ОПЕРАТИВНАЯ ПАМЯТЬ (RAM):")
    print(getMemoryInfo(), '\n')

    print("ДИСКОВОЕ ПРОСТРАНСТВО:")
    for diskUsage in getDiskInfo():
        print(f"{diskUsage[0]} занят на {diskUsage[1]}%", '\n')


if __name__ == "__main__":
    main()