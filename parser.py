import jinja2
from openpyxl import Workbook,load_workbook

wb = Workbook()
wb = load_workbook('input/L2 (1).xlsx')
#Set columns information parameters
#Colomun id interface name
c_ifname=1
#Colomun id interface number id
c_ifnumber=2
#Colomun id interface description
c_desc=4
#Colomun id vlan id
c_vlanid=3

for ws in wb :
    interfaces=[]
    for row in ws.rows:
        if (row[c_vlanid].value==u"trunk"):
            interfaces.append({
            "ifname" : row[c_ifname].value,
            "vlanid":row[c_vlanid].value,
            "ifnumber":row[c_ifnumber].value,
            "description" :row[c_desc].value
                })
        elif(isinstance(row[c_vlanid].value,float)):
            interfaces.append({
            "ifname" : row[c_ifname].value,
            "vlanid":int(row[c_vlanid].value),
            "ifnumber":row[c_ifnumber].value,
            "description" :row[c_desc].value
        })


    templateLoader = jinja2.FileSystemLoader( searchpath="templates" )
    templateEnv = jinja2.Environment( loader=templateLoader )
    TEMPLATE_FILE = "switch-interfaces"
    template = templateEnv.get_template( TEMPLATE_FILE )
    templateVars={"interfaces":interfaces}

    outputText = template.render( templateVars )
    with open("conf/"+ws.title+".cfg", "wb") as fh:
        fh.write(outputText)