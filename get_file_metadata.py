from win32com.client import Dispatch
from pprint import pprint
import mutagen

shell = Dispatch("Shell.Application")

def get_file_metadata_shell(file_path):
    _dict = {}
    file_namespace = '\\'.join(file_path.split('\\')[:-1])
    if file_namespace[-1:] == '\\':
        file_namespace = file_namespace[:-1]
    ns = shell.NameSpace(file_namespace)
    
    file_name = file_path.split('\\')[-1:][0]
    file_name = '.'.join(str(file_name).split('.')[:-1])
    
    for i in ns.Items():
        if str(i) == file_name:
            for j in range(0,500):
                _dict[ns.GetDetailsOf(j,j)] = ns.GetDetailsOf(i,j)
            break
    if (len(_dict) == 0):
        raise Exception('No metadata found for file: ' + file_path)
    
    # pprint(_dict)
    return _dict

def get_file_metadata_mutagen(file_path):
    metadata = mutagen.File(file_path)
    return metadata