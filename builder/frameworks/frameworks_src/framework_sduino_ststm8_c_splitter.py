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
Arduino

Arduino Wiring-based Framework allows writing cross-platform software to
control devices attached to a wide range of Arduino boards to create all
kinds of creative coding, interactive objects, spaces or physical experiences.

http://arduino.cc/en/Reference/HomePage
"""

import os

import SCons.Script

from . import framework


class FrameworkSduino(framework.Framework):

    def __init__(self, env: SCons.Script.DefaultEnvironment):
        super().__init__(env, 'framework-sduino-ststm8-c-splitter')

    def add_sources_to_env(self):
        self.env.Append(
            CPPDEFINES=[
                "ARDUINO_ARCH_STM8",
                ("ARDUINO", 10802),
                ("double", "float"),
                "__PROG_TYPES_COMPAT__"
            ],

            CPPPATH=[
                os.path.join(self.framework_dir, "cores", self.env.BoardConfig().get("build.core")),
                os.path.join(self.framework_dir, "STM8S_StdPeriph_Driver", "inc")
            ],

            LIBPATH=[
                os.path.join(self.framework_dir, "STM8S_StdPeriph_Driver", "lib")
            ],

            LIBS=[self.board_config.get("build.mcu")[0:8].upper()],

            LIBSOURCE_DIRS=[
                os.path.join(self.framework_dir, "libraries")
            ]
        )

        #
        # Target: Build Sduino core Library
        #

        libs = []

        if "build.variant" in self.env.BoardConfig():
            self.env.Append(
                CPPPATH=[
                    os.path.join(self.framework_dir, "variants", self.env.BoardConfig().get("build.variant"))
                ]
            )
            libs.append(self.env.BuildLibrary(
                os.path.join("$BUILD_DIR", "FrameworkArduinoVariant"),
                os.path.join(self.framework_dir, "variants", self.env.BoardConfig().get("build.variant"))
            ))

        libs.append(self.env.BuildLibrary(
            os.path.join("$BUILD_DIR", "FrameworkArduino"),
            os.path.join(self.framework_dir, "cores", self.env.BoardConfig().get("build.core"))
        ))

        self.env.Prepend(LIBS=libs)
