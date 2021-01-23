import struct

from signature import *

class apfs:
    global f
    global apfs_signature
    global vcsb_signature
    global root_id
    global block_size
    global MSB
    global VS
    global VCSB
    global BTOM
    global EBT
    global volume_name

    def set_msb_addr(self):
        self.MSB=0xC805000
        self.f.seek(self.MSB)
        data=self.f.read(0xB0)
        self.apfs_signature=struct.unpack_from(">I", data, 0x0 + 0x20)[0]
        apfs_check_signature(self.apfs_signature)
        self.block_size=struct.unpack_from("<I",data, 0x0 + 0x24)[0]

    def set_vs_addr(self):
        self.f.seek(self.MSB)
        data=self.f.read(0xB0)
        offset=struct.unpack_from("<I", data, 0x0 + 0xA0)[0]
        self.f.seek(self.MSB+offset*self.block_size)
        data=self.f.read(self.block_size)
        offset=struct.unpack_from("<I", data, 0x0 + 0x30)[0]
        self.VS=self.MSB+self.block_size*offset

    def set_vcsb_addr(self):
        self.f.seek(self.VS)
        data=self.f.read(self.block_size)
        """
        key_info_len=struct.unpack_from("<I", data, 0x0 + 0x2A)[0]%0x1000
        key_data_offset=data[0x38:0x38+key_info_len]
        key_data_offset_list=[]
        """
        offset = struct.unpack_from("<I", data, 0x0 + 0xFD0)[0]
        self.VCSB=self.MSB+self.block_size*offset

    def set_btom_ebt_addr(self):
        self.f.seek(self.VCSB)
        data=self.f.read(self.block_size)
        self.vcsb_signature=struct.unpack_from(">I", data, 0x0 + 0x20)[0]
        vcsb_check_signature(self.vcsb_signature)
        BTOM_offset=struct.unpack_from("<I", data, 0x0 + 0x80)[0]
        self.root_id=struct.unpack_from("<I", data, 0x0 + 0x88)[0]
        EBT_offset=struct.unpack_from("<I", data, 0x0 + 0x90)[0]
        self.f.seek(self.MSB+self.block_size*BTOM_offset)
        data=self.f.read(self.block_size)
        BTOM_offset=struct.unpack_from("<I", data, 0x0 + 0x30)[0]
        self.BTOM=self.MSB+self.block_size*BTOM_offset
        self.EBT=self.MSB+self.block_size*EBT_offset
        self.f.seek(self.VCSB+0x2C0)
        self.volume_name=str(self.f.read(self.block_size-0x2C0)).split('\\x00')[0][2:]

    def print_info(self):
        print("File name\t: "+str(self.f)[26:-2].split('\\')[-1]
              +"\nVolume name\t: "+str(self.volume_name)
              +"\nBlock size\t: "+hex(self.block_size)
              +"\nRoot ID\t\t: "+hex(self.root_id)
              +"\nMSB addr\t: "+hex(self.MSB)
              +"\nVS addr\t\t: "+hex(self.VS)
              +"\nVCSB addr\t: "+hex(self.VCSB)
              +"\nBTOM addr\t: "+hex(self.BTOM)
              +"\nEBT addr\t: "+hex(self.EBT))

    def __init__(self, f):
        self.f=f
        self.set_msb_addr()
        self.set_vs_addr()
        self.set_vcsb_addr()
        self.set_btom_ebt_addr()
        self.print_info()