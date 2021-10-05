# WizIO 2021 Georgi Angelov
#   http://www.wizio.eu/
#   https://github.com/Wiz-IO/wizio-cc

from os.path import join
from SCons.Script import DefaultEnvironment, Builder
from dev_common import *

def dev_init(env, platform):
    env.platform = platform
    env.framework_dir = env.PioPlatform().get_package_dir("framework-wizio-cc")
    env.libs = []
    dev_compiler(env, 'ARDUINO')
    PLATFORM_DIR = join( env.framework_dir, platform )
    env.Append(
        CPPDEFINES = [ "ARDUINO=200", ], 
        CPPPATH = [ 
            join(PLATFORM_DIR, platform),
            join(PLATFORM_DIR, "cores", env.core),
            join(PLATFORM_DIR, "variants", env.BoardConfig().get("build.variant")),  
        ],
        LIBSOURCE_DIRS = [ join(PLATFORM_DIR, "libraries", env.core) ],
        LIBPATH        = [ join(PLATFORM_DIR, "libraries", env.core) ],  
        LINKFLAGS      = [ '--entry=ResetISR', ],
        LDSCRIPT_PATH  = join(PLATFORM_DIR, "cores", env.core, 'arduino.ld')      
    )    

    OBJ_DIR = join( "$BUILD_DIR", platform, "arduino" )
 
    ###[ini] board_build.freertos = enable
    env.freertos = ( "enable" == env.BoardConfig().get("build.freertos", "disable") )
    if True == env.freertos:
        env.BuildSources( join( OBJ_DIR, "freertos" ),            join( env.framework_dir, 'library', 'freertos', 'src') )
        env.BuildSources( join( OBJ_DIR, "freertos", "arduino" ), join( env.framework_dir, 'library', 'freertos', 'arduino') )       
        env.Append(
            CPPDEFINES = [ "USE_FREERTOS" ],
            CPPPATH = [
                join( env.framework_dir, 'library', 'freertos', 'include'),
                join( env.framework_dir, 'library', 'freertos', 'arduino'),
            ]
        )

    env.BuildSources( join( OBJ_DIR, "arduino" ), join( PLATFORM_DIR, platform )  )
    env.BuildSources( join( OBJ_DIR, "core" ),    join( PLATFORM_DIR, "cores", env.core ) )
    env.BuildSources( join( OBJ_DIR, "variant" ), join( PLATFORM_DIR, "variants", env.BoardConfig().get("build.variant") )  )   