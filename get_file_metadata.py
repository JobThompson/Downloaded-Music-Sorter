from win32com.client import Dispatch
from pprint import pprint

shell = Dispatch("Shell.Application")

def get_file_metadata(file_path):
    _dict = {}
    
    file_namespace = '\\'.join(file_path.split('\\')[:-1])
    ns = shell.NameSpace(file_namespace)
    
    file_name = file_path.split('\\')[-1:][0]
    file_name = '.'.join(str(file_name).split('.')[:-1])
    
    for i in ns.Items():
        if str(i) == file_name:
            for j in range(0,1000):
                _dict[ns.GetDetailsOf(j,j)] = ns.GetDetailsOf(i,j)
            break
    if (len(_dict) == 0):
        raise Exception('No metadata found for file: ' + file_path)
    
    # pprint(_dict)
    return _dict
