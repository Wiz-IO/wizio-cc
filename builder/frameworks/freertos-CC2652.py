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

    # CHANGE default linker script
    #   [INI] board_build.linker = $PROJECT_DIR/custom.ld
    linker = env.BoardConfig().get('build.linker', 'default')
    if 'default' != linker and '$PROJECT_DIR' in linker:
        linker = linker.replace('$PROJECT_DIR', env['PROJECT_DIR']).replace('\\', '/')
        env.Append( LDSCRIPT_PATH = linker )
    else:
        env.Append( LDSCRIPT_PATH = join(os_path, 'freertos.ld') )

    # COPY default FreeRTOSConfig.h to the PROJECT
    templates = join(env.PioPlatform().get_package_dir('framework-wizio-cc'), 'templates')   
    include = join(env.subst('$PROJECT_DIR'), 'include')   
    if False == os.path.isfile( join(include, 'FreeRTOSConfig.h') ): 
        do_copy(templates, include, 'FreeRTOSConfig.h' ) 

    # DPL default is LIB( libdpl_freertos.a ) or compile as:
    #   [INI] board_build.dpl = src or lib
    dpl_path = join(os_path, 'dpl')     
    dpl = env.BoardConfig().get('build.dpl', 'default')
    if dpl == 'default' and True == os.path.isfile( join(dpl_path, 'libdpl_freertos.a') ):
        env.Append( LIBPATH = [dpl_path], LIBS = [ 'dpl_freertos', ], ) 
        print('  * OS-DPL       : Library')
    elif dpl == 'src':
        env.BuildSources( join( '$BUILD_DIR', platform, 'dpl' ), join( os_path, 'dpl') ) 
        print('  * OS-DPL       : compiled as SRC')
    elif dpl == 'lib':
        env.libs.append( env.BuildLibrary( join( '$BUILD_DIR', platform, 'dpl_freertos' ), join( os_path, 'dpl') ) )
        env.Append(LIBS = env.libs)  
        print('  * OS-DPL       : compiled as LIB')   
    else:  
        print('  * OS-DPL       : ERRROR !!! [INI] board_build.dpl = src OR lib')
        exit(0)

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

    env.BuildSources( join( '$BUILD_DIR', platform, 'src' ), join( os_path, 'src') )
    env.BuildSources( join( '$BUILD_DIR', platform, 'sdk' ), join( os_path, 'sdk') )