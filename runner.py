import sys
from import_sql import Import
print(sys.argv[1])

if __name__ == '__main__':
    # Call the class and run your code here
    #
    # You can assume that sys.argv[1] is the name
    # of the file to import and that it exists.
    #
    
    imp = Import()
    with open(sys.argv[1], 'r') as f:
        contents = f.read()
    imp.import_file(sys.argv[1])
