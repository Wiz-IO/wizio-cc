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
    dev_compiler(env)
    dev_create_template(env) 
    print('  * OS           : TIRTOS ... NOT READY !!! ... TODO')
    exit()

    #[INI] board_build.linker = $PROJECT_DIR/custom.ld
    linker = env.BoardConfig().get("build.linker", "cc26x2r1f.lds")
    if "cc26x2r1f.lds" != linker and "$PROJECT_DIR" in linker:
        linker = linker.replace('$PROJECT_DIR', env["PROJECT_DIR"]).replace("\\", "/")
        env.Append( LDSCRIPT_PATH = linker )
        pass
    else:
        env.Append( LDSCRIPT_PATH = join(env.DEVICE, 'linker_files', 'cc26x2r1f-cpp.ld') )

    env.Append( 
        CPPPATH = [ join(env.SDK_PATH, 'ti', 'drivers'), ], 
        LIBS    = [ 'libdrivers_cc26x2', ],              
    )    

    templates = join(env.PioPlatform().get_package_dir("framework-wizio-cc"), "templates")   
    project = join(env.subst("$PROJECT_DIR"), "src") 