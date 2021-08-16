import pylink
from os.path import join

def upload(target, source, env):
   hex  = join(env.get("BUILD_DIR"), env.get("PROGNAME")) + '.hex'
   serial_no = '000000000'
   jlink = pylink.JLink()
   jlink.open()
   jlink.connect("CC2652R1F", verbose=True)
   jlink.flash_file(hex, 0x0)
   jlink.reset()