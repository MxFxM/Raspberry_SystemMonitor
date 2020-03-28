import psutil
from influxdb import InfluxDBClient
import time

# wait before reading cpu load
time.sleep(10)

# cpu
cpu_load = psutil.cpu_percent()

# memory
# divide by 1024 two times to get from bytes to Mb
mem_free = round(psutil.virtual_memory().available / 1024.0 / 1024.0, 1)
mem_total = round(psutil.virtual_memory().total / 1024.0 / 1024.0, 1)

# disk
# divide by 1024 three times to get from bytes to Gb
dsk_free = round(psutil.disk_usage('/').free / 1024.0 / 1024.0 / 1024.0, 1)
dsk_total = round(psutil.disk_usage('/').free / 1024.0 / 1024.0 / 1024.0, 1)

# print to screen
print("CPU load: " + str(cpu_load) + "%")
print("Memory: " + str(mem_free) + "Mb / " + str(mem_total) + "Mb")
print("Disk: " + str(dsk_free) + "Gb / " + str(dsk_total) + "Gb")

json_body = [{"measurement": "system",
              "fields": {
                  "cpu_load": cpu_load,
                  "mem_total": mem_total,
                  "mem_free": mem_free,
                  "mem_used": (mem_total - mem_free),
                  "dsk_total": dsk_total,
                  "dsk_free": dsk_free,
                  "dsk_used": (dsk_total - dsk_free)
                  }
              }]

client = InfluxDBClient('localhost', 8086, 'root', 'root', 'SYSTEMMONITOR')
client.write_points(json_body)
print("uploaded")
