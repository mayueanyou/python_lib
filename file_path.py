import os,sys

#file_path = FilePath(os.path.abspath(__file__))
class FilePath:
    def __init__(self,file_path) -> None:
        self.file_path = file_path
        self.folder_path = self.upper(1)
    
    def upper(self,level):
        path = self.file_path
        for _ in range(level): path = os.path.abspath(os.path.dirname(path) + os.path.sep + ".")
        return path
    
if __name__ == '__main__':
    fp = FilePath(os.path.abspath(__file__))
    print(__file__)
    print(fp.base_path)
    print(fp.upper(1))
    print(fp.upper(2))
    print(fp.upper(3))