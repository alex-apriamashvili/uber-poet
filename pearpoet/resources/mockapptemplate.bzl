#  Copyright (c) 2017-2018 Uber Technologies, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

apple_bundle(
    name = "App",
    binary = ":AppBinary",
    extension = "app",
    info_plist = "Info.plist",
)

apple_binary(
    name = "AppBinary",
    srcs = [
        "main.swift",
    ],
    is_universal = True,
    system_frameworks = [
        "Foundation",
        "UIKit",
    ],
    configs = {{
        "Debug": {{
            "SWIFT_WHOLE_MODULE_OPTIMIZATION": "{2}",
        }},
    }},
    deps = [
        {1}
    ],
)
