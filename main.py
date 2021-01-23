import sys

from apfs import *
from gui import *
from nodes import *
from files import *
from dbmanager import *

input_file=input("Input the disk file : ")
f=open(input_file,'rb')
apfs=apfs(f)
node=node(apfs)
file=file(apfs, node.node_id_offset)
dbmanager=dbmanager(file.file_info, apfs.volume_name)
if __name__ == '__main__':
    app=QApplication(sys.argv)
    ex = MyApp(apfs, f)
    sys.exit(app.exec_())
    
f.close()