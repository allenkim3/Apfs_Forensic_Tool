import sqlite3

from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import *

class MyApp(QWidget):
    global conn
    global c
    global QTree
    global QTable
    global QTab
    global tab1
    global tab2
    global label
    global scrollArea
    global font
    global apfs
    global f

    def __init__(self, apfs_tmp, f):
        super().__init__()
        self.conn=sqlite3.connect("apfs.db", isolation_level=None)
        self.c=self.conn.cursor()
        self.apfs=apfs_tmp
        self.f=f
        self.initUI()

    def initUI(self):
        self.fname=str(self.f).replace("/", "\\").split('\\')[-1][:-2]
        self.treeUI()

        self.QTable = QTableWidget(0, 4)
        self.QTable.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.QTable.setHorizontalHeaderLabels(["Name", "Size", "Type", "Date Modified"])
        self.QTable.setAutoScroll(True)
        self.QTable.verticalHeader().setVisible(False)
        self.QTable.setColumnWidth(0, 250)
        self.QTable.setColumnWidth(1, 100)
        self.QTable.setColumnWidth(2, 100)
        self.QTable.setColumnWidth(3, 200)

        self.tab1=QWidget()
        self.tab2=QWidget()
        self.QTab=QTabWidget()
        self.QTab.addTab(self.tab1, 'Hex')
        self.QTab.addTab(self.tab2, 'PreView')
        self.label=QLabel()
        self.font=QFont("DejaVu Sans Mono", 8, QFont.Normal, True)
        self.scrollArea=QScrollArea()

        self.QTree.itemClicked.connect(self.tableUI)
        self.QTable.itemClicked.connect(self.tabUI)

        window = QGridLayout()
        window.addWidget(self.QTree, 0, 0, 3, 1)
        window.addWidget(self.QTable, 0, 1, 1, 1)
        window.addWidget(self.QTab, 2, 1, 1, 1)
        self.setLayout(window)
        self.setGeometry(300, 300, 1000, 700)
        self.setWindowTitle('APFS - '+self.fname)
        self.show()

    def treeUI(self):
        self.QTree = QTreeWidget()
        self.QTree.setMaximumWidth(300)

        parent = QTreeWidgetItem(self.QTree)
        parent.setText(0, self.apfs.volume_name)
        self.findParent(parent, '0x1')

    def findParent(self, parent, parent_id):
        self.c.execute("select * from file where ParentFolderID='"+parent_id+"' \
                        and GroupPermission/4096=4")
        result=self.c.fetchall()
        for i in range(len(result)):
            child = QTreeWidgetItem(parent)
            child.setText(0, result[i][12])             #12번 인덱스가 파일 이름
            self.findParent(child, result[i][1])        #1번 인덱스가 parent id

    def tableUI(self):
        selectedFile=self.QTree.currentItem().text(0)
        self.c.execute("select FileID from file where Name='"+selectedFile+"'")
        parent_id=self.c.fetchone()[0]
        self.c.execute("select Name, FileSize, GroupPermission, LastWrittenDate \
                        from file where ParentFolderID='"+parent_id+"'")
        result=self.c.fetchall()
        count=len(result)
        self.QTable.setRowCount(count)

        for i in range(count):
            Name, FileSize, GroupPermission, LastWrittenDate=result[i]
            self.QTable.setItem(i, 0, QTableWidgetItem(Name))
            self.QTable.setItem(i, 1, QTableWidgetItem(FileSize))
            if int(GroupPermission) // 0x1000 == 8:
                self.QTable.setItem(i, 2, QTableWidgetItem("File"))
            else:
                self.QTable.setItem(i, 2, QTableWidgetItem("Folder"))
            self.QTable.setItem(i, 3, QTableWidgetItem(LastWrittenDate))

    def tabUI(self):
        row=self.QTable.currentIndex().row()
        selectedFileName=self.QTable.item(row, 0).text()
        self.c.execute("select FileSize, BlockCount, GroupPermission from file \
                        where Name='"+selectedFileName+"'")
        fileSize, blockCount, groupPermission=self.c.fetchone()

        if int(groupPermission)//0x1000==4:
            msg="This is forder."
        else:
            self.f.seek(self.apfs.MSB+self.apfs.block_size*int(blockCount))
            msg=[]
            offset=0
            for i in range(int(fileSize)//0x10):
                data=self.f.read(0x10).hex()
                lst=[]
                [lst.append(data[i:i+2]) for i in range(0, len(data), 2)]
                output="%08X:  " % (offset)
                for i in range(0x10):
                    if(i==8):
                        output +=" "
                    output+=lst[i]+" "
                output+="  |"

                for i in range(0x10):
                    if(int(lst[i], 16)>=0x20 and int(lst[i], 16)<=0x7E):
                        output+=chr(int(lst[i], 16))
                    else:
                        output+="."
                output+="\n"
                msg.append(output)
                offset+=0x10
            msg="".join(msg)
        self.label.setText(msg)
        self.label.setFont(self.font)
        self.scrollArea.setWidget(self.label)
        self.tab1.layout=QVBoxLayout(self)
        self.tab1.layout.addWidget(self.scrollArea)
        self.tab1.setLayout(self.tab1.layout)