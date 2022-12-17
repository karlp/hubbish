#!python3
"""
Generates i2cutils commands to write usb strings to a usb2517 eeprom
"""

mfr = "ekta labs"
prod = "hubbish r3"
ser = "00001"

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

kmem = bytearray([])
# Port maps for hubbish r3 to be "nicely" ordered.
kmem[0xfb] = 0x43
kmem[0xfc] = 0x21
kmem[0xfd] = 0x67
kmem[0xfe] = 0x05
