import os,sys,argparse

def hello_1(args):
    print('1')

def hello_2(args):
    print('2')

def tuple_test(args):
    print(type(args.tuple))
    print(args.tuple)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f','--function', type=str)
    parser.add_argument('-t','--tuple', type=eval)
    args = parser.parse_args()
    getattr(sys.modules[__name__], args.function)(args)