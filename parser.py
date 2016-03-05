import jinja2
from openpyxl import Workbook,load_workbook

def cast(val, to_type, default=None):
    try:
        return to_type(val)
    except (ValueError,TypeError):
        default=val
        return default

l2wb = Workbook()
l3wb = Workbook()
#Load the excel configuration file
l2wb = load_workbook('input/L2 (1).xlsx')
l3wb = load_workbook('input/L3.xlsx')
valid_interface = ["gigabitethernet","fastethernet","vlan","port-channel","tengigabitethernet","tunnel","loopback","serial"]
devices_list= list(set(l2wb.get_sheet_names())|set(l3wb.get_sheet_names()))
#Set columns information parameters
#Colomun id interface name
c_ifname=1
#Colomun id interface number id
c_ifnumber=2
#Colomun id interface description
c_desc=4
#Colomun id vlan id
c_vlanid=3

for device in devices_list:
    try:
        l2interfaces=[]
        l2ws=l2wb.get_sheet_by_name(device)
        for row in l2ws.rows:
            if (row[c_vlanid].value==u"trunk"):
                 l2interfaces.append({
                "ifname" : row[c_ifname].value,
                 "vlanid":row[c_vlanid].value,
                 "ifnumber":row[c_ifnumber].value,
                 "description" :row[c_desc].value
                     })
            elif(isinstance(row[c_vlanid].value,float)):
                l2interfaces.append({
                "ifname" : row[c_ifname].value,
                "vlanid":int(row[c_vlanid].value),
                "ifnumber":row[c_ifnumber].value,
                "description" :row[c_desc].value
                })
    except (KeyError):
            pass
    try:
        l3interfaces=[]
        l3ws=l3wb.get_sheet_by_name(device)
        for row in l3ws.rows:
            if row[0].value in valid_interface :
                l3interfaces.append({
                "ifname" : row[0].value,
                "vlanid":cast(row[2].value,int),
                "ifnumber":cast(row[1].value,int),
                "description" :row[7].value,
                "ipaddr" : row[5].value,
                "netmask" : row[6].value,
                "subint" : cast(row[2].value,int),
                "autoconf": row[3].value
                    })
            else:
                print "Unknown interface type : ",row[0].value
    except (KeyError):
        pass






    templateLoader = jinja2.FileSystemLoader( searchpath="templates" )
    templateEnv = jinja2.Environment( loader=templateLoader )
    TEMPLATE_FILE = "config"
    template = templateEnv.get_template( TEMPLATE_FILE )
    templateVars={"l2interfaces":l2interfaces,"l3interfaces":l3interfaces}
    #templateVars={"l3interfaces":l3interfaces}

    outputText = template.render( templateVars,trim_blocks=True,lstrip_blocks=True )
    with open("conf/"+device+".cfg", "wb") as fh:
        fh.write(outputText)