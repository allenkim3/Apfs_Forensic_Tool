import os
import sqlite3

class dbmanager:

    def file_info_insert(self, file_info, c):
        for info in file_info:
            c.executemany("INSERT INTO file VALUES(?, ?, ?, ?, ?, ?, ?\
                            , ?, ?, ?, ?, ?, ?, ?\
                            , ?, ?, ?, ?, ?, ?, ?);", (info,))

    def __init__(self, file_info, volume_name):
        if os.path.isfile("apfs.db"):
            os.remove("apfs.db")
        conn=sqlite3.connect("apfs.db", isolation_level=None)
        c=conn.cursor()
        c.execute("CREATE TABLE file \
                    (ParentFolderID text, \
                    FileID text PRIMARY KEY, \
                    CreatedDate text, \
                    LastWrittenDate text, \
                    iNodeChangeDate text, \
                    LastAccessDate text, \
                    HardlinktoFile text, \
                    OwnPermission text, \
                    GroupPermission text, \
                    NameLength1 text, \
                    NameLength text, \
                    NameLength2 text, \
                    Name text, \
                    FileSize text, \
                    CalculatedinBlockSize text, \
                    Length text, \
                    HardLinkCount text, \
                    FileOffset text, \
                    BlockCount text, \
                    NodeID text, \
                    CreatedDate2 text)")

        c.execute("INSERT INTO file (FileID, Name) VALUES('0x1', '"+volume_name+"');")

        self.file_info_insert(file_info, c)