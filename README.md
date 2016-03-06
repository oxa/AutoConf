AutoConf
========

AutoConf is a Simple Cisco devices configuration generator based on jinja2 templates.

For now only .xlsx templates input are supported. In the following released json will be supported as a valid input source.
Output fle format is a Cisco .cfg file

AutoConf support :
* Cisco IOS, IOS-XE and NX-OS
* IP addressing
* VLAN / Trunking configuration
* Port-Channels

## Installing

No python package available for now. Just clone the project and install required packages.

### Prerequisites

AutoConf is written in **Python 2.7** and needs the following packages :

* jinja2
* openpyxl

## Documentation

### QuickStart

AutoConf does not support in the current release command line parameters.
Input files needs to be stored in **_/input_**.

1. Edit the **_L2.xlsx_** and/or _**L3.xlsx**_ templates based on your needed configuration
2. (OPTIONAL) Edit the **_templates/config_** file to enable/disable configurations types
3. Run **_parser.py_** and retrieve your devices configurations files in **_conf_** folder.

### Input files

#### File format
Right now only .xlsx file format is supported. In the following released json will be a suitable input format.

You have to edit the two .xlsx templates in **_input_** folder with your own data

If you rename the file you have to specify it also in **_parser.py_** :
```python
# 1. Specify the excel configuration file
l2wb = load_workbook('input/L2.xlsx')
l3wb = load_workbook('input/L3.xlsx')
```
You can modify column order.

If you rename a column you have to specify it also in **_parser.py_** :

```python
# 2. Specify column names if renamed
#General
ifname = "interface type"
ifnumber = "interface"
vlanid = "vlan"
description = "description/name"
#L2
allowedvlans="allowed vlans"
po="channel-group"
po_mode="mode"
#L3
ipaddr = "ip address"
subint = "sub int"
autoconf = "auto-conf information"
netmask = "netmask"
```

You have to create one sheet per device. Identical devices must have the same name in .xlsx templates.

#### File syntax

Please refer to the following table for column index description :

Global index

| xlsx index | AutoConf | Description |
| --- | --- | --- |
| interface type | ifname | Cisco well known interfaces type |
| interface | ifnumber | Interface number in Cisco format |
| vlan | vlanid | Vlan ID |
| description/name | description | Interface Description or Name |

L2 only index

| xlsx index | AutoConf | Description |
| --- | --- | --- |
| interface type | ifname | Serve also as a Key word for vlan declaration |
| allowed vlans | allowedvlans | List of allowed vlans |
| channel-group | po | Channel-Group ID |
| mode | po_mode | Port-Channel mode |


L3 only index

| xlsx index | AutoConf | Description |
| --- | --- | --- |
| ip address | ipaddr | Interface IP address |
| sub int | subint | Sub-Interface ID |
| netmask | netmask | Network Mask of IP address |
| auto-conf information | autoconf | Information for auto-configuration templates |

### config template

**_templates/config_** is the main template for configuration output file format.

Default .cfg configuration output include all possible configurations type from the input file;

```jinja
!L2 configuration
{% include 'l2/l2-cfg' %}

!L3 configuration
{% include 'l3/l3-cfg' %}
```

You can include your own templates to this config file.
Delete an include statement to remove it from the global render.

## API

soon


Have Fun =)
_0xa_
