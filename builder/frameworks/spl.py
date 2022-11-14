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

from SCons.Script import DefaultEnvironment
from frameworks_src import framework_ststm8spl_c_splitter

env = DefaultEnvironment()

framwork_ststm8spl = framework_ststm8spl_c_splitter.FrameworkStStm8Spl(env)

env.Append(
    CFLAGS=["--opt-code-size"]
)
