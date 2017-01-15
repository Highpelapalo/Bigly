from .gwapp import run
import sys

if __name__ == '__main__':
    host = None
    if len(sys.argv) > 1:
        host = sys.argv[1]
    run(host)
