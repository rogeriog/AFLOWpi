import AFLOWpi
import logging
import os

def _post_proc(oneCalc,ID,plot_num,**kwargs):
    if "data_postfix" in list(kwargs.keys()):
        data_postfix="_"+kwargs["data_postfix"]
        del kwargs["data_postfix"]
    else:
        data_postfix=""

    if "extra_inputpp" in list(kwargs.keys()):
        extra_inputpp=kwargs["extra_inputpp"]
    else:
        extra_inputpp=""
    
    try:
        os.mkdir("PP")
    except:
        print("PP folder already created.")
    
    pp_input=f'''&inputpp
prefix = '{oneCalc["_AFLOWPI_PREFIX_"]}',
outdir = './'
filplot = './PP/{ID}{data_postfix.split('.')[0]}'
plot_num={plot_num}
{extra_inputpp}
/
&PLOT
nfile = 1
filepp(1) = './PP/{ID}{data_postfix.split('.')[0]}'
weight(1) = 1.0
fileout = './PP/{ID}{data_postfix}'
'''
    ## additional lines like iflag will be inserted through this one
    pp_input+=",\n".join(["%s=%s"%(k,v.replace("'", "")) for k,v in kwargs.items()])+"\n/\n"

    infn=os.path.join(oneCalc["_AFLOWPI_FOLDER_"],f"./PP/{ID}{data_postfix.split('.')[0]}.in")
    with open(infn,"w") as ofo:
        ofo.write(pp_input)

    execPrefix = AFLOWpi.prep._ConfigSectionMap("run","exec_prefix")
    AFLOWpi.run._oneRun("",oneCalc,f"./PP/{ID}{data_postfix.split('.')[0]}",engine='espresso',calcType='custom',execPath='./pp.x',execPrefix=execPrefix )

