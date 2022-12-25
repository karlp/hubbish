#!python3
"""
Generates i2cutils commands to write usb strings to a usb2517 eeprom
"""
import struct

mfr = "ekta labs"
prod = "hubbish r3"
ser = "00002"

def chunkdump(addr, dat, stride=16):
    # stride is 16 from teh 24series eeprom, BUT
    # we must roll over if our address crosses a a 16byte boundary...
    if len(dat) > 31:
        raise RuntimeException("Max strings are 31chars")
    buf = dat.encode("utf-16le")
    outvals = []
    pos = addr
    for x in buf:
        outvals.append(x)
        pos += 1
        if pos % stride == 0:
            vals = " ".join([hex(zz) for zz in outvals])
            print(f"i2cset -c 0x50 -r {addr:#x} {vals}")
            addr += len(outvals)
            outvals = []
    vals = " ".join([hex(zz) for zz in outvals])
    print(f"i2cset -c 0x50 -r {addr:#x} {vals}")


print(f"i2cset -c 0x50 -r 0x13 {len(mfr)} {len(prod)} {len(ser)}")
chunkdump(0x16, mfr)
chunkdump(0x54, prod)
chunkdump(0x92, ser)

# redo this to take all the config into a 256byte array,a nd then just
# dump the 16byte chunks to be programmed in one hit.

def default_settings():
    blob = []
    # vid, pid, did
    blob.extend([0x24, 0x4, 0x17, 0x25, 0x0, 0])
    # config, NR dev, port disables.
    blob.extend([0x9b, 0x20, 0x0, 0x0, 0x0, 0x0])
    # max powers / Power on times
    blob.extend([0x1, 0x32, 0x1, 0x32, 0x32])
    # langs/str lends
    blob.extend([0, 0, 0, 0, 0])
    blob.extend([0]*62) # mfr str
    blob.extend([0]*62) # prod str
    blob.extend([0]*62) # serial
    blob.extend([0]*38) # reserved
    # boost, reserved... (0xf6...
    blob.extend([0, 0, 0, 0])
    # port swap, port remaps, smbus stat
    blob.extend([0, 0, 0, 0, 0, 0])
    assert(len(blob) == 256)
    return bytearray(blob)


kmem = memoryview(default_settings())
kmem[0:2] = struct.pack("<H", 0xcafe)
#kmem[6] = no changes to cfg1, defaults to per port power switching
kmem[7] = 0xa0 # enable dynamic power
kmem[8] = 0xb # dyn power, speed mode, and string support
kmem[0x13] = len(mfr)
kmem[0x14] = len(prod)
kmem[0x15] = len(ser)
z = mfr.encode("utf-16le")
print(f"z is..{z} len {len(z)}, len mfr is {len(mfr)}")
kmem[0x16:0x16+2*len(mfr)] = mfr.encode("utf-16le")
kmem[0x54:0x54+2*len(prod)] = prod.encode("utf-16le")
kmem[0x92:0x92+2*len(ser)] = ser.encode("utf-16le")
# Port maps for hubbish r3 to be "nicely" ordered.
# remember, it's physical to logical mappings.
kmem[0xfb] = 0x43
kmem[0xfc] = 0x21
kmem[0xfd] = 0x57
kmem[0xfe] = 0x06

print(kmem)

print(f"i2cconfig --sda=21 --scl=22")
for i in range(len(kmem)//16):
    vals = " ".join([hex(zz) for zz in kmem[i*16:(i+1)*16]])
    print(f"i2cset -c 0x50 -r {i*16} {vals}")
    

