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
from abc import ABC
import os

import SCons.Script


class Framework(ABC):
    env: SCons.Script.DefaultEnvironment
    framework_dir: str

    def __init__(self, env: SCons.Script.DefaultEnvironment, framework_package_name: str):
        self.env = env
        self.platform = env.PioPlatform()
        self.board_config = env.BoardConfig()
        self.framework_dir = self.platform.get_package_dir(framework_package_name)
        assert os.path.isdir(self.framework_dir)

