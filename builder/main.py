# WizIO 2021 Georgi Angelov
#   http://www.wizio.eu/
#   https://github.com/Wiz-IO

from __future__ import print_function
from SCons.Script import (AlwaysBuild, Builder, COMMAND_LINE_TARGETS, Default, DefaultEnvironment)
from colorama import Fore
from os.path import join

env = DefaultEnvironment()
print( '<<<<<<<<<<<< ' + env.BoardConfig().get("name").upper() + " 2021 Georgi Angelov >>>>>>>>>>>>" )

elf = env.BuildProgram()
hex = env.ElfToHex( join("$BUILD_DIR", "${PROGNAME}"), elf )
bin = env.ElfToBin( join("$BUILD_DIR", "${PROGNAME}"), elf )
prg_bin = env.Alias( "build_bin", bin, [ env.VerboseAction("", "BIN DONE") ] )
prg_hex = env.Alias( "build_hex", hex, [ env.VerboseAction("", "HEX DONE") ] )
AlwaysBuild( prg_bin, prg_hex )

upload = env.Alias("upload", prg_hex, [ 
    env.VerboseAction("$UPLOADCMD", "Uploading HEX FILE"),
    env.VerboseAction("", "DONE"),
])
AlwaysBuild( upload )    

debug_tool = env.GetProjectOption("debug_tool")
if None == debug_tool:
    Default( prg_hex, prg_bin )
else:   
    if 'jlink' in debug_tool:
        Default( upload )
    else:
        Default( prg_hex, prg_bin )