import os,sys,argparse

class ArgparseWrapper:
    def __init__(self) -> None:
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument('-f','--function', type=str)
    
    def run(self):
        args = self.parser.parse_args()
        getattr(sys.modules[__name__], args.function)(args)

def test_1(args):
    print('test1')

def test_2(args):
    print('test2')

if __name__ == "__main__":
    IArgparseI = ArgparseWrapper()
    IArgparseI.run()