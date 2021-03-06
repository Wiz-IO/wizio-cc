# WizIO 2021 Georgi Angelov
#   http://www.wizio.eu/
#   https://github.com/Wiz-IO

import os
from os.path import join, normpath, basename
from shutil import copyfile
from colorama import Fore
from SCons.Script import DefaultEnvironment, Builder, ARGUMENTS

from pylink_uploader import upload
def dev_uploader(target, source, env):
    print("UPLOADER IS NOT READY YET !!!")
    print("Use SEGGER J-Flash ... upload HEX file")
    upload(target, source, env)

def do_copy(src, dst, name):
    if False == os.path.isfile( join(dst, name) ):
        copyfile( join(src, name), join(dst, name) )

def do_mkdir(path, name):
    dir = join(path, name)
    if False == os.path.isdir( dir ):
        try:
            os.mkdir(dir)
        except OSError:
            print ("[ERROR] Creation of the directory %s failed" % dir)
            exit(1)
    return dir

def dev_create_template(env):
    src = join(env.PioPlatform().get_package_dir("framework-wizio-cc"), "templates")
    if 'APPLICATION'== env.get("PROGNAME"):
        dst = join(env.subst("$PROJECT_DIR"), "src")
        if False == os.path.isfile( join(dst, "main.cpp") ):
            do_copy(src, dst, "main.c" )
        if False == os.path.isfile( join(dst, "ccfg.c") ):
            do_copy(src, dst, "ccfg.c" )                 

def dev_nano(env): # do not use
    enable_nano = env.BoardConfig().get("build.nano", "disable") 
    nano = []
    if enable_nano == "enable":
        nano = ["-specs=nano.specs", "-u", "_printf_float", "-u", "_scanf_float" ]
    if len(nano) > 0: print('  * SPECS        :', nano[0][7:])
    else:             print('  * SPECS        : default')
    return nano

def dev_set_linker(env, file_name):
    #[INI] board_build.linker = $PROJECT_DIR/custom.ld
    linker = env.BoardConfig().get("build.linker", "default")
    if "default" != linker and "$PROJECT_DIR" in linker:
        linker = linker.replace('$PROJECT_DIR', env["PROJECT_DIR"]).replace("\\", "/")
        env.Append( LDSCRIPT_PATH = linker )    
    else:
        env.Append( LDSCRIPT_PATH = file_name )

def dev_compiler(env, application_name = 'APPLICATION'):
    env.sdk = env.BoardConfig().get("build.sdk", "SDK") # get/set default SDK
    env.SDK_PATH = join(env.framework_dir, env.sdk) 
    env.TI = join(env.framework_dir, env.sdk, 'ti')    
    env.DEVICE = join(env.framework_dir, env.sdk, 'ti', 'devices', 'cc13x2_cc26x2') 

    env.core = env.BoardConfig().get("build.core")
    env.mcu = env.BoardConfig().get("build.mcu")

    #print()
    print( Fore.BLUE + "Texas Instruments %s" % ( env.mcu.upper() ) )
    env.Replace(
        BUILD_DIR = env.subst("$BUILD_DIR").replace("\\", "/"),
        AR="arm-none-eabi-ar",
        AS="arm-none-eabi-as",
        CC="arm-none-eabi-gcc",
        GDB="arm-none-eabi-gdb",
        CXX="arm-none-eabi-g++",
        OBJCOPY="arm-none-eabi-objcopy",
        RANLIB="arm-none-eabi-ranlib",
        SIZETOOL="arm-none-eabi-size",
        ARFLAGS=["rc"],
        SIZEPROGREGEXP=r"^(?:\.text|\.data|\.boot2|\.rodata)\s+(\d+).*",
        SIZEDATAREGEXP=r"^(?:\.data|\.bss|\.ram_vector_table)\s+(\d+).*",
        SIZECHECKCMD="$SIZETOOL -A -d $SOURCES",
        SIZEPRINTCMD='$SIZETOOL --mcu=$BOARD_MCU -C -d $SOURCES',
        PROGSUFFIX=".elf",
        PROGNAME=application_name
    )
    cortex = ["-mcpu=cortex-m4", "-march=armv7e-m", "-mfpu=fpv4-sp-d16", "-mfloat-abi=hard", "-mthumb"] 
    optimization = env.BoardConfig().get("build.optimization", "-Os")

    env.Append(
        ASFLAGS=[ cortex, "-x", "assembler-with-cpp" ],
        CPPDEFINES = [
            'DeviceFamily_CC13X2_CC26X2',
            "%s" % env.mcu, 
        ],        
        CPPPATH = [
            join(env.subst('$PROJECT_DIR'), 'src'),
            join(env.subst('$PROJECT_DIR'), 'include'),
            env.SDK_PATH,
            env.DEVICE
        ],
        CCFLAGS = [
            cortex,
            optimization,
            "-fdata-sections",
            "-ffunction-sections",
            '-fno-strict-aliasing',
            "-Wall",
            "-Wextra",
            "-Wfatal-errors",
            "-Wno-sign-compare",
            "-Wno-type-limits",
            "-Wno-unused-parameter",
            "-Wno-unused-function",
            "-Wno-unused-but-set-variable",
            "-Wno-unused-variable",
            "-Wno-unused-value",
            "-Wno-unused-label",
            "-Wno-strict-aliasing",
            "-Wno-maybe-uninitialized",
            "-Wno-implicit-fallthrough",
            #"-Wno-missing-field-initializers",
            #'-Wno-comment',
        ],      
        CFLAGS = [
            cortex,
            "-Wno-discarded-qualifiers",
            "-Wno-ignored-qualifiers"
        ],
        CXXFLAGS = [
            "-fno-rtti",
            "-fno-exceptions",
            "-fno-threadsafe-statics",
            "-fno-non-call-exceptions",
            "-fno-use-cxa-atexit",
        ],
        LINKFLAGS = [
            cortex,
            optimization,
            "-nostartfiles",
            "-mno-unaligned-access",
            "-Xlinker", "--gc-sections",
            "-Wl,--gc-sections",
            dev_nano(env)
        ],
        LIBPATH = [ 
            join( env.TI, 'library'),       # LIB SDK
            join( '$PROJECT_DIR', 'lib' ),  # LIB PROJECT
        ], 
        LIBS    = [ 'm', 'gcc', 'device_drivers.a' ],
        BUILDERS = dict(
            ElfToBin = Builder(
                action = env.VerboseAction(" ".join([
                    "$OBJCOPY", "-O", "binary",
                    "$SOURCES", "$TARGET",
                ]), "Building $TARGET"),
                suffix = ".bin"
            ),
            ElfToHex = Builder(
                action = env.VerboseAction(" ".join([
                    "$OBJCOPY", "-O", "ihex",
                    "$SOURCES", "$TARGET",
                ]), "Building $TARGET"),
                suffix = ".hex"
            ),            
        ),
        UPLOADCMD = dev_uploader        
    )

    ###[INI] board_build.use_patch = enable
    use_patch = env.BoardConfig().get("build.use_patch", "disable") 
    if use_patch == "enable":
        env.BuildSources( join("$BUILD_DIR", env.platform, 'ti', 'cc13x2_cc26x2', 'rf_patches'), join(env.ti, 'cc13x2_cc26x2', 'rf_patches') ) 
    