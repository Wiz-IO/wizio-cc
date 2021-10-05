# WizIO 2021 Georgi Angelov
#   http://www.wizio.eu/
#   https://github.com/Wiz-IO/wizio-cc

from os.path import join
from SCons.Script import DefaultEnvironment, Builder
from dev_common import *

def dev_init(env, platform):
    env.platform = platform
    env.framework_dir = env.PioPlatform().get_package_dir('framework-wizio-cc')
    env.libs = []
    dev_compiler(env)
    dev_create_template(env) 
    print('  * OS           : FreeRTOS')

    os_path = join( env.framework_dir, 'library', 'freertos')  

    #[INI] board_build.linker = $PROJECT_DIR/custom.ld
    linker = env.BoardConfig().get('build.linker', 'default')
    if 'default' != linker and '$PROJECT_DIR' in linker:
        linker = linker.replace('$PROJECT_DIR', env['PROJECT_DIR']).replace('\\', '/')
        env.Append( LDSCRIPT_PATH = linker )
    else:
        env.Append( LDSCRIPT_PATH = join(os_path, 'freertos.ld') )

    # COPY FreeRTOSConfig.h
    templates = join(env.PioPlatform().get_package_dir('framework-wizio-cc'), 'templates')   
    include = join(env.subst('$PROJECT_DIR'), 'include')   
    if False == os.path.isfile( join(include, 'FreeRTOSConfig.h') ): 
        do_copy(templates, include, 'FreeRTOSConfig.h' ) 

    env.Append( 
        CPPDEFINES = [ 'USE_FREERTOS' ],        
        CPPPATH    = [ 
            join( os_path, 'include'),
            join( os_path, 'sdk'),
            join( os_path, 'dpl'),             
            join(env.SDK_PATH, 'ti', 'drivers'), 
        ], 
        LIBS       = [ 'drivers_cc26x2', ],
        LINKFLAGS  = [ '--entry=resetISR', ]            
    )         

    env.BuildSources( join( '$BUILD_DIR', platform, 'freertos', 'src' ), join( os_path, 'src') )
    env.BuildSources( join( '$BUILD_DIR', platform, 'freertos', 'dpl' ), join( os_path, 'dpl') ) 
    env.BuildSources( join( '$BUILD_DIR', platform, 'freertos', 'sdk' ), join( os_path, 'sdk') )

     



