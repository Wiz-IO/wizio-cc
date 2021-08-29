# WizIO 2021 Georgi Angelov
#   http://www.wizio.eu/
#   https://github.com/Wiz-IO/wizio-cc

import os, platform, copy
from os.path import join
from platform import system, machine
from platformio.managers.platform import PlatformBase

class WizioccPlatform(PlatformBase):
    def is_embedded(self): # Mac workaround
        return True

    def get_boards(self, id_=None):
        result = PlatformBase.get_boards(self, id_)
        if not result:
            return result
        if id_:
            return self._add_dynamic_options(result)
        else:
            for key, value in result.items():
                result[key] = self._add_dynamic_options(result[key])
        return result

     
    def _add_dynamic_options(self, board):

        # upload protocols
        if not board.get("upload.protocols", []):
            board.manifest["upload"]["protocols"] = ["todo"]
        if not board.get("upload.protocol", ""):
            board.manifest["upload"]["protocol"] = "todo"

        # debug tools
        debug = board.manifest.get("debug", {})
        #print('DEBUG', debug)
        non_debug_protocols   = [ "todo" ]
        supported_debug_tools = [ "openocd" ]

        upload_protocol  = board.manifest.get("upload", {}).get("protocol")
        #print('PROTO', upload_protocol)

        upload_protocols = board.manifest.get("upload", {}).get("protocols", [])
        #print('PROTOCOLS', upload_protocols)

        if debug:
            upload_protocols.extend(supported_debug_tools)
        if upload_protocol and upload_protocol not in upload_protocols:
            upload_protocols.append(upload_protocol)

        board.manifest["upload"]["protocols"] = upload_protocols
        if "tools" not in debug:
            debug["tools"] = {}

        for link in upload_protocols:
            if link in non_debug_protocols or link in debug["tools"]: continue
            #print('LINK', link, 'TARGET', debug.get("openocd_target"))
            server_args = [
                "-s", "$PACKAGE_DIR/scripts",
                "-f", "interface/%s.cfg" % 'jlink', # link,
                "-f", "target/%s" % 'ti_cc26x2.cfg' # debug.get("openocd_target")
            ]
            print('SERVER ARG', server_args)
            
            if link == "openocd":
                init_cmds = [] # use pio default settings

            if link == 'openocd': # JLINK
                debug["tools"][link] = {
                    "server": {
                        "package"    : "tool-openocd",
                        "executable" : "bin/openocd", # EXE
                        "arguments"  : server_args,
                    },
                    "init_cmds"      : init_cmds,
                    "onboard"        : link in debug.get("onboard_tools", []),
                    "default"        : link == debug.get("default_tool"),
                }                

        board.manifest["debug"] = debug
        return board

    def configure_debug_options(self, initial_debug_options, ide_data):
        """
        Deprecated. Remove method when PlatformIO Core 5.2 is released
        """
        debug_options = copy.deepcopy(initial_debug_options)
        if "cmsis-dap" in debug_options["tool"]:
            debug_options["server"]["arguments"].extend( [
                    "-c", "adapter speed %s" % (initial_debug_options.get("speed") or "20000"),
                    "-c", "transport select swd"
                ]
            )
        return debug_options                
