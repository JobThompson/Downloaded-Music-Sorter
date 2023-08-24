from get_file_metadata import get_file_metadata
from library import Library
import shutil
import traceback


class FileConsolidator:
    def __init__(self, library_path, allowed_file_types) -> None:
        self.library_path = library_path
        self.allowed_file_types = allowed_file_types | []
        self.files_to_sort = []
        self.sorted_file_identifiers = []
        self.sorted_files = []
        self.existing_libraries = Library(self.library_path)
    
    def compare_files(self):
        for i in self.existing_libraries.get_song_paths_unstripped():
            if i.split('.')[-1:][0] not in self.allowed_file_types:
                continue
            try:
                stats = get_file_metadata(i)
                try:
                    file_name = f'{stats["Filename"]}'    
                    try:
                        hasInt = int(file_name.split(' - ')[0])
                        file_name = ' - '.join(file_name.split(' - ')[1:])
                    except Exception:
                        pass
                        
                    if stats['Title'] != '':
                        file_name = stats['Title']

                    print(f"{stats['Filename']} {stats['File extension']} BY: {stats['Authors']}")
                        
                    sorted_file_identifier = f"{file_name} BY: {stats['Authors']}"
                    if(stats['Album artist'] != ''):
                        sorted_file_identifier = f"{file_name} BY: {stats['3Album artist']}"

                    if sorted_file_identifier not in self.sorted_file_identifiers:
                        self.sorted_file_identifiers.append(sorted_file_identifier)
                        self.sorted_files.append(stats["Path"])
                        
                except Exception as e:
                        print(f'Could not check if file was duplicate: {e}')
                        
            except Exception as e:
                print(f'Could not get metadata for file: {e}')

    def copy_sorted_files(self):
        print('Moving Sorted Files...')
        sorted_len = len(self.sorted_files)
        index = 0
        for i in self.sorted_files:
            index += 1
            print(f'{index} of {sorted_len}')
            try:
                file_name = i.split('\\')[-1:][0]
                try:
                    if int(file_name.split(' - ')[0]):
                        file_name = ' - '.join(file_name.split(' - ')[2:])
                except Exception:
                    if len(file_name.split(' - ')) > 1:
                        file_name = ' - '.join(file_name.split(' - ')[1:])
                shutil.copy2(i, f'{self.library_path}\\{file_name}')
            except Exception as e:
                print(f'Could not copy file: {e}')
                    