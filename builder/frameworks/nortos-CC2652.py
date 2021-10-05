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
    print('  * OS           : NORTOS ... NOT READY !!! ... TODO')
    exit()

    os_path = join( env.framework_dir, 'library', 'nortos')

    #[INI] board_build.linker = $PROJECT_DIR/custom.ld
    linker = env.BoardConfig().get('build.linker', 'default')
    if 'default' != linker and '$PROJECT_DIR' in linker:
        linker = linker.replace('$PROJECT_DIR', env['PROJECT_DIR']).replace('\\', '/')
        env.Append( LDSCRIPT_PATH = linker )
    else:
        env.Append( LDSCRIPT_PATH = join(os_path, 'cc13x2x7_cc26x2x7_nortos.lds') )

    env.Append( 
        CPPDEFINES = [ "USE_NORTOS" ],        
        CPPPATH    = [ 
            os_path,            
            join(env.TI, 'drivers'), 
        ],  
        LIBS      = [ 
            'drivers_cc26x2', 
            'nortos_cc26x2', 
        ],     
        LINKFLAGS = [ '--entry=resetISR', ]         
    )           

    env.BuildSources( join( "$BUILD_DIR", platform, "nortos" ), os_path )
