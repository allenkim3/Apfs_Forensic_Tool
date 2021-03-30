import os
import sys

from apfs import *
from gui import *
from nodes import *
from files import *
from dbmanager import *

#C:\\Users\\twoonewoo\\Documents\\Virtual Machines\\macOS Mojave 10.14.4 APFS by Techsviewer\\macOS Mojave 10.14.4 APFS by Techsviewer-0-flat.vmdk

input_file=input("Input the disk file : ")
f=open(input_file,'rb')
apfs=apfs(f)
if os.path.isfile("apfs.db"):
    os.remove("apfs.db")
for i in apfs.volume_info:
    nodes=node(apfs, i)
    files=file(apfs, i, nodes.node_id_offset)
    dbmanagers=dbmanager(files.file_info, i)
if __name__ == '__main__':
    app=QApplication(sys.argv)
    ex = MyApp(apfs, f)
    sys.exit(app.exec_())

f.close()