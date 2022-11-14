# Copyright 2018-present PlatformIO <contact@platformio.org>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
SPL

Library that enables developers to easily exploit all the functions of the STM8
microcontrollers to address a wide range of applications.

https://www.st.com/en/embedded-software/stsw-stm8069.html
"""

import sys
import os

import SCons.Script
from platformio.proc import exec_command

from . import framework
from . import c_splitter


class FrameworkStStm8Spl(framework.Framework):

    def __init__(self, env: SCons.Script.DefaultEnvironment):
        super().__init__(env, 'framework-ststm8spl-c-splitter')
        self.env.AddBuildMiddleware(
            c_splitter.split_c_files,
            "*.c"
        )  # Needs to be added before any sources
        self._check_project_src_dir()
        self._inject_dummy_reference_to_main()
        self._add_sources_to_env()

    def _get_core_files(self):
        command = [
            self.env.subst("$CC"), "-m%s" % self.board_config.get("build.cpu"),
                                   "-D%s" % self.board_config.get("build.mcu")[0:8].upper(),
            "-I.",
            "-Wp-MM", "-E", "stm8s.h"
        ]

        result = exec_command(
            command,
            cwd=os.path.join(self.framework_dir, "Libraries", "STM8S_StdPeriph_Driver", "inc"),
            env=self.env['ENV']
        )

        if result['returncode'] != 0:
            sys.stderr.write(
                "Error: Could not parse library files for the target.\n")
            sys.stderr.write(result['err'])
            self.env.Exit(1)

        src_files = []
        includes = result['out']
        for inc in includes.split(" "):
            if "_" not in inc or ".h" not in inc or "conf" in inc:
                continue
            src_files.append(os.path.basename(inc).replace(".h", ".c").strip())

        return src_files

    def _add_sources_to_env(self):
        self.env.Append(
            CPPDEFINES=[
                "USE_STDPERIPH_DRIVER",
                "USE_STDINT"
            ],

            CPPPATH=[
                os.path.join(self.framework_dir, "Libraries", "STM8S_StdPeriph_Driver", "inc")
            ]
        )

        #
        # Target: Build SPL Library
        #

        self.env.Append(LIBS=self.env.BuildLibrary(
            os.path.join("$BUILD_DIR", "FrameworkSpl"),
            os.path.join(self.framework_dir, "Libraries", "STM8S_StdPeriph_Driver"),
            src_filter=["-<*>"] + [" +<src/%s>" % f for f in self._get_core_files()]
        ))

    # Fixes possible issue with "ASlink-Warning-No definition of area SSEG" error.
    # This message means that main.c is not pulled in by the linker because there was no
    # reference to main() anywhere. Details: https://tenbaht.github.io/sduino/usage/faq/
    def _inject_dummy_reference_to_main(self):
        build_dir = self.env.subst("$BUILD_DIR")
        dummy_file = os.path.join(build_dir, "_pio_main_ref.c")
        if not os.path.isfile(dummy_file):
            if not os.path.isdir(build_dir):
                os.makedirs(build_dir)
            with open(dummy_file, "w") as fp:
                fp.write("void main(void);void (*dummy_variable) () = main;")

        self.env.Append(PIOBUILDFILES=dummy_file)

    def _check_project_src_dir(self):
        # By default PlatformIO generates "main.cpp".
        # But Sdcc doesn't support C++ sources. Exit if a file with a C++ extension is detected.
        for root, _, files in os.walk(self.env.subst("$PROJECT_SRC_DIR")):
            for f in files:
                if f.endswith((".cpp", ".cxx", ".cc")):
                    sys.stderr.write(
                        "Error: Detected C++ file `%s` which is not compatible with the sdcc compiler as only C/ASM sources are allowed.\n"
                        % os.path.join(root, f)
                    )
                    self.env.Exit(1)
