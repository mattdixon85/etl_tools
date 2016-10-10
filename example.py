
from centricities import Centricity, Stream

def main():
    config = dict(
        srcs = ['type 1','type 2','type 3','type 4','type 5','type 6','type 7']
        ,tsrcs = ['type 1','type 2','type 3','type 4','type 5','type 6','type 7','people']
        ,wsrcs = ['type 1','type 2','type 3','type 4','type 5','type 6','type 7']
        ,emit = ['type 1','type 2','type 3','type 4','type 5','type 6','type 7']
        ,immu = ['people']
        )
    stream = Stream(Centricity, config)
    stream.run(sys.stdin)
    
if __name__ == '__main__':
    main()
    