import AFLOWpi
import logging
import os

def _post_proc(oneCalc,ID,plot_num,**kwargs):
    if "data_postfix" in list(kwargs.keys()):
        data_postfix="_"+kwargs["data_postfix"]
        del kwargs["data_postfix"]
    else:
        data_postfix=""

#    if "additional_inputpp" in list(kwargs.keys()):
#        dict_add_inputpp=kwargs["additional_inputpp"]
#        if dict_add_inputpp['type'] == 'HOMO':
#            kband = AFLOWpi.prep._num_bands(oneCalc,mult=False)
#            kpoint = dict_add_inputpp.get('kpoint',1)
#            add_inputpp=f'''
#            kpoint = {kpoint},
#            kband = {kband},
#            '''
#        if dict_add_inputpp['type'] == 'LUMO':
#            kband = AFLOWpi.prep._num_bands(oneCalc,mult=False)+1
#            kpoint = dict_add_inputpp.get('kpoint',1)
#            add_inputpp=f'''
#            kpoint = {kpoint},
#            kband = {kband},
#            '''
#        del kwargs["additional_inputpp"]
#    else:
#        add_inputpp=""

    pp_input='''&inputpp
prefix = '%s',
outdir = './'
filplot = 'pp_temp'
plot_num=%s
%s
/
&PLOT
nfile = 1
filepp(1) = 'pp_temp'
weight(1) = 1.0
fileout = '%s%s'
''' %(oneCalc["_AFLOWPI_PREFIX_"],plot_num,add_inputpp,ID,data_postfix)

    pp_input+=",\n".join(["%s=%s"%(k,v) for k,v in kwargs.items()])+"\n/\n"

    infn=os.path.join(oneCalc["_AFLOWPI_FOLDER_"],"%s_pp_%s.in"%(ID,data_postfix))
    with open(infn,"w") as ofo:
        ofo.write(pp_input)

    execPrefix = AFLOWpi.prep._ConfigSectionMap("run","exec_prefix")
    AFLOWpi.run._oneRun("",oneCalc,"%s_pp_%s"%(ID,data_postfix),engine='espresso',calcType='custom',execPath='./pp.x',execPrefix=execPrefix ) 
