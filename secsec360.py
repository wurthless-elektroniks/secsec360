'''
secsec360: Xbox 360 HDD security sector dumper

Further reading: https://eaton-works.com/2023/01/24/how-the-xbox-360-knows-if-your-hard-drive-is-genuine/
'''

import os
import sys
import struct

MS_LOGO_SHA1 = bytes([ 0x3b, 0x0f, 0xd7, 0x3f, 0x82, 0x77, 0xfe, 0x41, 0xc6, 0xf6, 0xa2, 0x5d, 0xfc, 0x17, 0x2c, 0x17, 0x7a, 0xd4, 0xf8, 0xd6])

class Xbox360SecuritySector():
    def __init__(self, bits: bytes):
        self._bits = bits

    def drive_serial(self) -> str:
        return self._bits[0x000:0x014].decode('ascii').strip()

    def drive_firmware(self) -> str:
        return self._bits[0x014:0x01C].decode('ascii').strip()

    def drive_model(self) -> str:
        return self._bits[0x01C:0x044].decode('ascii').strip()

    def logo_sha1(self) -> bytes:
        return self._bits[0x044:0x058]

    def sector_count(self) -> int:
        # little endian value on a big endian console... great job microsoft
        return struct.unpack("<I", self._bits[0x058:0x05C])[0]
    
    def signature(self) -> bytes:
        return self.bits[0x05C:0x15C]

    def bits(self):
        return self._bits

def _giga(num: int):
    return num * 1000000000


def main(args):
    if len(args) < 2:
        print(f"usage: {args[0]} path-to-physical-drive")
        print("you will need to run this program as superuser for physical drive access")
        return
    
    path = args[1]

    print(f"try opening: {path}")

    sector = None
    with open(path,"rb") as f:
        f.seek(0x2000)

        # one sector is 512 bytes; read the full sector anyway
        sector = Xbox360SecuritySector(f.read(0x200))

        if sector.logo_sha1() != MS_LOGO_SHA1:
            print("error: MS logo SHA-1 mismatch")
            return
        
    print("got security sector OK")
    print(f"\tdrive serial:   {sector.drive_serial()}")
    print(f"\tdrive firmware: {sector.drive_firmware()}")
    print(f"\tdrive model:    {sector.drive_model()}")
    print(f"\tnum sectors:    {sector.sector_count()} (approx bytes = {sector.sector_count() * 512})")
    print(f"\tlogo SHA-1:     {sector.logo_sha1().hex()}")        

    num_bytes = sector.sector_count() * 512
    if _giga(20) <= num_bytes <= _giga(22):
        dump_pfx = "20gb"
    elif _giga(60) <= num_bytes <= _giga(62):
        dump_pfx = "60gb"
    elif _giga(120) <= num_bytes <= _giga(122):
        dump_pfx = "120gb"
    elif _giga(250) <= num_bytes <= _giga(252):
        dump_pfx = "250gb"
    elif _giga(320) <= num_bytes <= _giga(322):
        dump_pfx = "320gb"
    elif _giga(500) <= num_bytes <= _giga(502):
        dump_pfx = "500gb"
    else:
        dump_pfx = "other"

    # create folder if it doesn't exist yet
    outfolder = f"dumps/{dump_pfx}/{sector.drive_model()}"
    try:
        os.mkdir(outfolder)
    except FileExistsError:
        pass


    outpath = f"{outfolder}/{sector.drive_serial()}.bin"

    print(f"attempt write sector to: {outpath}")
    with open(outpath, "wb") as f:
        f.write(sector.bits())
        print("write done")

if __name__ == "__main__":
    main(sys.argv)