# HP iLO Metrics Exporter

Blackbox likes exporter used to exports HP Server Integrated Lights Out (iLO) states to Prometheus.

This is a fork from [infinityworks](https://github.com/infinityworks/hpilo-exporter) with some updates/extensions from 
* [dafes](https://github.com/dafes/hpilo-exporter)
* [IDNT](https://github.com/IDNT/hpilo-exporter)


### Gauges

Here are the status code of gauge
```
0 - OK
1 - Degraded
2 - Dead (Other)
```

### Enviroment Variables

The following Enviroment Variables are supported at the moment:

```
ILO_HOST
ILO_PORT
ILO_USER
ILO_PASSWORD
```

### Output example

Example of status of your iLO
```
health_at_a_glance:
  battery: {status: OK}
  bios_hardware: {status: OK}
  fans: {redundancy: Redundant, status: OK}
  memory: {status: OK}
  network: {status: Link Down},
  power_supplies: {redundancy: Redundant, status: OK}
  processor: {status: OK}
  storage: {status: Degraded}
  temperature: {status: OK}
  vrm: {status: Ok}
  drive: {status: Ok}
```

The returned output would be:
```
hpilo_battery{product_name="ProLiant DL360 Gen9",server_name="name.fqdn.domain"} 0.0
hpilo_storage{product_name="ProLiant DL360 Gen9",server_name="name.fqdn.domain"} 1.0
hpilo_fans{product_name="ProLiant DL360 Gen9",server_name="name.fqdn.domain"} 0.0
hpilo_bios_hardware{product_name="ProLiant DL360 Gen9",server_name="name.fqdn.domain"} 0.0
hpilo_memory{product_name="ProLiant DL360 Gen9",server_name="name.fqdn.domain"} 0.0
hpilo_power_supplies{product_name="ProLiant DL360 Gen9",server_name="name.fqdn.domain"} 0.0
hpilo_processor{product_name="ProLiant DL360 Gen9",server_name="name.fqdn.domain"} 0.0
hpilo_network{product_name="ProLiant DL360 Gen9",server_name="name.fqdn.domain"} 2.0
hpilo_temperature{product_name="ProLiant DL360 Gen9",server_name="name.fqdn.domain"} 0.0
hpilo_vrm{product_name="ProLiant DL380 Gen6",server_name="name.fqdn.domain"} 0.0
hpilo_drive{product_name="ProLiant DL380 Gen6",server_name="name.fqdn.domain"} 0.0
hpilo_firmware_version{product_name="ProLiant DL360 Gen9",server_name="name.fqdn.domain"} 2.5
```

#### Temperature

Also the Temperature Sensors are added to the Output

*EXAMPLE*
```
# HELP hpilo_temperature_status HP iLO temperature status
# TYPE hpilo_temperature_status gauge
hpilo_temperature_status{product_name="ProLiant DL360p Gen8",sensor="01-Inlet Ambient",server_name="host is unnamed"} 26.0
hpilo_temperature_status{product_name="ProLiant DL360p Gen8",sensor="02-CPU 1",server_name="host is unnamed"} 40.0
hpilo_temperature_status{product_name="ProLiant DL360p Gen8",sensor="03-CPU 2",server_name="host is unnamed"} 40.0
hpilo_temperature_status{product_name="ProLiant DL360p Gen8",sensor="04-P1 DIMM 1-6",server_name="host is unnamed"} 36.0
hpilo_temperature_status{product_name="ProLiant DL360p Gen8",sensor="05-P1 DIMM 7-12",server_name="host is unnamed"} 37.0
hpilo_temperature_status{product_name="ProLiant DL360p Gen8",sensor="06-P2 DIMM 1-6",server_name="host is unnamed"} 38.0
hpilo_temperature_status{product_name="ProLiant DL360p Gen8",sensor="07-P2 DIMM 7-12",server_name="host is unnamed"} 38.0
hpilo_temperature_status{product_name="ProLiant DL360p Gen8",sensor="08-P1 Mem Zone",server_name="host is unnamed"} 34.0
hpilo_temperature_status{product_name="ProLiant DL360p Gen8",sensor="09-P1 Mem Zone",server_name="host is unnamed"} 38.0
hpilo_temperature_status{product_name="ProLiant DL360p Gen8",sensor="10-P2 Mem Zone",server_name="host is unnamed"} 37.0
hpilo_temperature_status{product_name="ProLiant DL360p Gen8",sensor="11-P2 Mem Zone",server_name="host is unnamed"} 34.0
hpilo_temperature_status{product_name="ProLiant DL360p Gen8",sensor="12-HD Max",server_name="host is unnamed"} 35.0
hpilo_temperature_status{product_name="ProLiant DL360p Gen8",sensor="13-Chipset 1",server_name="host is unnamed"} 48.0
hpilo_temperature_status{product_name="ProLiant DL360p Gen8",sensor="14-Chipset1 Zone",server_name="host is unnamed"} 38.0
hpilo_temperature_status{product_name="ProLiant DL360p Gen8",sensor="15-P/S 1 Inlet",server_name="host is unnamed"} 34.0
hpilo_temperature_status{product_name="ProLiant DL360p Gen8",sensor="16-P/S 1 Zone",server_name="host is unnamed"} 36.0
hpilo_temperature_status{product_name="ProLiant DL360p Gen8",sensor="17-P/S 2 Inlet",server_name="host is unnamed"} 36.0
hpilo_temperature_status{product_name="ProLiant DL360p Gen8",sensor="18-P/S 2 Zone",server_name="host is unnamed"} 35.0
hpilo_temperature_status{product_name="ProLiant DL360p Gen8",sensor="21-VR P1",server_name="host is unnamed"} 36.0
hpilo_temperature_status{product_name="ProLiant DL360p Gen8",sensor="22-VR P2",server_name="host is unnamed"} 38.0
hpilo_temperature_status{product_name="ProLiant DL360p Gen8",sensor="23-VR P1 Mem",server_name="host is unnamed"} 30.0
hpilo_temperature_status{product_name="ProLiant DL360p Gen8",sensor="24-VR P1 Mem",server_name="host is unnamed"} 30.0
hpilo_temperature_status{product_name="ProLiant DL360p Gen8",sensor="25-VR P2 Mem",server_name="host is unnamed"} 32.0
hpilo_temperature_status{product_name="ProLiant DL360p Gen8",sensor="26-VR P2 Mem",server_name="host is unnamed"} 31.0
hpilo_temperature_status{product_name="ProLiant DL360p Gen8",sensor="27-VR P1Mem Zone",server_name="host is unnamed"} 29.0
hpilo_temperature_status{product_name="ProLiant DL360p Gen8",sensor="28-VR P1Mem Zone",server_name="host is unnamed"} 29.0
hpilo_temperature_status{product_name="ProLiant DL360p Gen8",sensor="29-VR P2Mem Zone",server_name="host is unnamed"} 31.0
hpilo_temperature_status{product_name="ProLiant DL360p Gen8",sensor="30-VR P2Mem Zone",server_name="host is unnamed"} 31.0
hpilo_temperature_status{product_name="ProLiant DL360p Gen8",sensor="31-HD Controller",server_name="host is unnamed"} 64.0
hpilo_temperature_status{product_name="ProLiant DL360p Gen8",sensor="32-HD Cntlr Zone",server_name="host is unnamed"} 43.0
hpilo_temperature_status{product_name="ProLiant DL360p Gen8",sensor="33-PCI 1 Zone",server_name="host is unnamed"} 38.0
hpilo_temperature_status{product_name="ProLiant DL360p Gen8",sensor="34-PCI 1 Zone",server_name="host is unnamed"} 38.0
hpilo_temperature_status{product_name="ProLiant DL360p Gen8",sensor="36-PCI 2 Zone",server_name="host is unnamed"} 40.0
hpilo_temperature_status{product_name="ProLiant DL360p Gen8",sensor="37-System Board",server_name="host is unnamed"} 40.0
hpilo_temperature_status{product_name="ProLiant DL360p Gen8",sensor="38-System Board",server_name="host is unnamed"} 38.0
hpilo_temperature_status{product_name="ProLiant DL360p Gen8",sensor="39-Sys Exhaust",server_name="host is unnamed"} 37.0
hpilo_temperature_status{product_name="ProLiant DL360p Gen8",sensor="40-Sys Exhaust",server_name="host is unnamed"} 38.0
hpilo_temperature_status{product_name="ProLiant DL360p Gen8",sensor="41-Sys Exhaust",server_name="host is unnamed"} 37.0
hpilo_temperature_status{product_name="ProLiant DL360p Gen8",sensor="42-SuperCAP Max",server_name="host is unnamed"} 29.0
```

### Installing

You can install exporter on the server directly or on separate machine.
To run, you must have `Python3` and `pip3` installed.

To install the requirements with `pip3`:
```
pip3 install -r requirements.txt
```

Then just:
```
python3 ./src/hpilo_exporter/main.py [--address=0.0.0.0 --port=9416 --endpoint="/metrics"]
```



### Docker

Prebuild images are available from the docker repository:
```
dafes/hpilo-exporter:latest
```


To build the image yourself
```
docker build --rm -t hpilo-exporter .
```

To run the container
```
docker run -p 9416:9416 hpilo-exporter:latest
```

You can then call the web server on the defined endpoint, `/metrics` by default.
```
curl 'http://127.0.0.1:9416/metrics?ilo_host=127.0.0.1&ilo_port=443&ilo_user=admin&ilo_password=admin'
```

Passing argument to the docker run command
```
docker run -p 9416:9416 hpilo-exporter:latest --port 9416
```

### Docker compose

Here is an example of Docker Compose deployment:

```yml
version: '3.7'
services:
  hpilo_exporter:
    image: dafes/hpilo-exporter:{{ hpilo_exporter_version }}
    container_name: hpilo_exporter
    ports:
      - 9416:9416
    restart: always
    environment:
      - ILO_USER=FOO
      - ILO_PASSWORD=FOTOPSECRET
```

### Prometheus config

Assuming:
- the exporter is available on `http://localhost:9416`
- you use same the port,username and password for all your iLO

```yml
  - job_name: 'hpilo'
    scrape_interval: 1m
    scrape_timeout: 30s
    params:
      ilo_port: ['443']
      ilo_user: ['FOO']
      ilo_password: ['FOTOPSECRET']
    static_configs:
      - targets: ['192.168.220.188']
        labels:
            service: "ILO"
            host: "ilo_prox1"

    relabel_configs:
      - source_labels: [__address__]
        target_label: __param_ilo_host
      - source_labels: [__param_ilo_host]
        target_label: ilo_host
      - target_label: __address__
        replacement: localhost:9416  # hpilo exporter.
```

