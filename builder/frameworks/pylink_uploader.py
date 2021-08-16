import pylink, sys
from os.path import join

def upload(target, source, env):
   hex  = join(env.get("BUILD_DIR"), env.get("PROGNAME")) + '.hex'
   serial_no = '000000000' # TODO
   jlink = pylink.JLink()
   jlink.open()  # serial_no
   jlink.power_on()
   #jlink.set_tif(7) # cJTAG not work
   jlink.connect("CC2652R1F", verbose=True)
   sys.stdout.write('\tARM Id: 0x%x\n' % jlink.core_id())
   sys.stdout.write('\tCPU Id: 0x%x\n' % jlink.core_cpu())
   sys.stdout.write('\tCore Name: %s\n' % jlink.core_name())
   sys.stdout.write('\tDevice Family: %d\n' % jlink.device_family())   
   jlink.erase()
   jlink.flash_file(hex, 0x0)
   jlink.reset()