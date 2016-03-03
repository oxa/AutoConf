import jinja2
from openpyxl import Workbook,load_workbook

wb = Workbook()
wb = load_workbook('input/L2.xlsx')
ws=wb['Phiscal layout']
interfaces=[]

for row in ws.rows:
    if (row[2].value==u"trunk"):
        interfaces.append({
        "ifname" : "fastethernet",
        "vlanid":row[2].value,
        "ifnumber":row[1].value,
        "description" :row[3].value
            })
    elif(isinstance(row[2].value,float)):
        interfaces.append({
        "ifname" : "fastethernet",
        "vlanid":int(row[2].value),
        "ifnumber":row[1].value,
        "description" :row[3].value
    })


templateLoader = jinja2.FileSystemLoader( searchpath="templates" )
templateEnv = jinja2.Environment( loader=templateLoader )
TEMPLATE_FILE = "switch-interfaces"
template = templateEnv.get_template( TEMPLATE_FILE )
templateVars={"interfaces":interfaces}

outputText = template.render( templateVars )
with open("conf/device.cfg", "wb") as fh:
    fh.write(outputText)