import AFLOWpi
import urllib2
import ast
import copy 
import re
class parser():



    def __init__(self):
        self.search_base = 'http://aflowlib.duke.edu/search/API/?'
        self.search_parameters = {}
        self.auid_list         = []
        self.search_vals       = []
        self.results           = {}
#    def by_icsd(self,icsd_number,attribute=None):
        #    connection = urllib2.urlopen('http://aflowlib.org/material.php?id=%s'%icsd_number)                        


    def add_value(self,parameter):
        self.search_vals.append(parameter)


    def remove_value(self,parameter):
        pass

    def remove_condition(self,parameter):
        condition_string=''.join(condition_string.split())
        self.search_parameters.remove(condition_string)

    def add_condition(self,parameter,condition):
        self.search_parameters[parameter]=condition

    def get_file(self,filename):
        num_entries = len(self.results.keys())
        print 'Parsing AFLOWlib entries for %s\n' % filename
        found_counter=0
        for auid,entry in self.results.iteritems():
            search_str = 'http://'+entry['aurl'].replace(':','/')+'/'

            try:
                connection = urllib2.urlopen(search_str+filename)
                relax_file_str = connection.read()
                
                page_str = '!# http://aflowlib.org/material.php?id=aflow:'+auid+'\n'
                   
                self.results[auid]['url']=page_str
                self.results[auid][filename]=page_str+relax_file_str
                found_counter+=1
            except:
                self.results[auid][filename]=''
                

        print 'Found %s in %s of %s entries.\n'%(filename,found_counter,num_entries)

    
#    def _transform_condition(parameter,condition):

        

    def search(self,limit=10000):
        
        search_string=''
        for parameter,condition in self.search_parameters.iteritems():
            search_string+=parameter+'('+condition+')'+','
        for value in self.search_vals:
            search_string+=value+','

        #truncate the tail comma
        null_to_none   = re.compile('null')
        true_to_True   = re.compile('true')
        false_to_False = re.compile('false')


        return_dict={}
        counter=0
        paging=0
        print 'Parsing AFLOWlib...'
        while True:
            paging+=1

            search = self.search_base+search_string+'paging(%d)'%paging

            connection = urllib2.urlopen(search)            
            res_str = connection.read()

            #change some json stuff to python form before using ast.literal
            res_str = true_to_True.sub('True',res_str)
            res_str = false_to_False.sub('False',res_str)
            res_str = null_to_none.sub('None',res_str)

            #end of the paging
            if res_str.strip()=='[]':
                break

            #translate text to python list obj
            temp_dict=ast.literal_eval(res_str)

            if paging==1:
                num_res = int(temp_dict.keys()[0].split()[-1])
                if num_res>limit:
                    print 'Total number of results: %s. Results limited to %s'%(num_res,limit)
                else:
                    print 'Total number of results: %s'%num_res

                
                
            temp_dict=temp_dict.values()     

            #convert list object to dictionary entries
            for v in temp_dict:
                ID=v['auid'].split(':')[-1]
                v_copy = copy.deepcopy(v)
                del v_copy['auid']
                return_dict[ID]=v_copy
                counter+=1

                if counter>=limit:
                    ub=limit
                    break


            ub = (paging-1)*40+len(temp_dict)
            if counter>=limit:
                ub=limit
                break




            lb = ((paging-1)*40)+1
            print 'Retreving results %s-%s'%(lb,ub)

        print 'Done\n'

        print 'Found %s entries.\n'%len(return_dict.keys())
        

        self.results = return_dict
        return return_dict


    def display(self,parameter_list=None):
        pass