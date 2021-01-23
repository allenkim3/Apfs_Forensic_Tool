from keydata import *

class node:
    global node_id_offset   #list

    def set_node_id_offset(self, apfs, kd):
        node_id_offset=[]
        for i in kd.key_data:
            apfs.f.seek(apfs.BTOM+0x38+kd.size+i[0])
            node_id=int.from_bytes(apfs.f.read(8)[::-1], byteorder='big')
            apfs_id=int.from_bytes(apfs.f.read(8)[::-1], byteorder='big')   #이거 근데 쓰는거임?
            apfs.f.seek(apfs.BTOM+apfs.block_size-0x28-i[1])
            apfs.f.read(4)
            block_size=int.from_bytes(apfs.f.read(4)[::-1], byteorder='big')    #굳이 또?
            offset=int.from_bytes(apfs.f.read(8)[::-1], byteorder='big')
            node_id_offset.append([node_id, offset])
        self.node_id_offset=node_id_offset

    def __init__(self, apfs):
        kd=keydata(apfs, apfs.BTOM)
        self.set_node_id_offset(apfs, kd)