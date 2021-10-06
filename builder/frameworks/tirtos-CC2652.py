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

    os_path = join( env.framework_dir, 'library', 'tirtos')
    dev_set_linker( env, join(os_path, 'tirtos.lds') )

    env.Append( 
        CPPDEFINES = [ "USE_TIRTOS" ], 
        CPPPATH    = [ 
            os_path,
            join(os_path, 'src'),
            join(env.SDK_PATH, 'ti', 'drivers'), 
        ], 
        LIBS       = [ 
            'drivers_cc26x2', 
            'tirtos_cc26x2', 
            'dpl_cc26x2'           
        ],   
        LINKFLAGS  = [ '--entry=ResetISR', ]             
    )    

    templates = join(env.PioPlatform().get_package_dir("framework-wizio-cc"), "templates")   
    project = join(env.subst("$PROJECT_DIR"), "src") 

    env.BuildSources( join( "$BUILD_DIR", platform, "tirtos" ), join( os_path, 'src', 'startup') )
    #env.BuildSources( join( "$BUILD_DIR", platform, "tirtos", 'knl' ), join( os_path, 'src', 'ti', 'sysbios' , 'knl', 'Task.c') )
