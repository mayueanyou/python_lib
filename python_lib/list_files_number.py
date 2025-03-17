from pathlib import Path

class Folder:
    def __init__(self,path) -> None:
        self.path = Path(path)
        self.folder_list = []
        self.file_list = []
        for item in path.iterdir():
            if item.is_dir(): self.folder_list.append(item)
            else: self.file_list.append(item)
    
    def __str__(self):
        for folder in self.folder_list: print(folder)
        for file in self.file_list: print(file)
        return ''

class FolderMonitor:
    def __init__(self,path) -> None:
        self.path = Path(path)
        self.monitor()
        print(self.total_files())
    
    def monitor(self,level=-1):
        folder_list = []
        folder = Folder(self.path)
        print(folder)
    
    def total_files(self):
        return len([x for x in self.path.rglob('*') if x.is_file()])


fm = FolderMonitor('.')




