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

from util import seed


swift_func_template = """
public func complexCrap{0}<T>(arg: Int, stuff:T) -> Int {{
    let a = Int(4 * {1} + Int(Float(arg) / 32.0))
    let b = Int(4 * {1} + Int(Float(arg) / 32.0))
    let c = Int(4 * {1} + Int(Float(arg) / 32.0))
    return Int(4 * {1} + Int(Float(arg) / 32.0)) + a + b + c
}}"""

swift_class_template = """
public class MyClass{0} {{
    public let x: Int
    public let y: String

    public init() {{
        x = 7
        y = "hi"
    }}

    {1}
}}"""


class FileResult(object):
    def __init__(self, text, functions, classes):
        super(FileResult, self).__init__()
        self.text = text  # string
        self.text_line_count = text.count('\n')
        self.functions = functions  # list of indexes
        self.classes = classes  # {class index: function indexes}


class FileGenerator(object):
    def gen_file(self, class_count, function_count, line_goal):
        return FileResult("", [], {})


class SwiftFileGenerator(FileGenerator):

    def __init__(self):
        self.gen_state = {}

    def gen_func(self, function_count, var_name):
        out = []
        nums = []

        for _ in xrange(function_count):
            num = seed()
            text = swift_func_template.format(num, var_name)
            nums.append(num)
            out.append(text)

        return "\n".join(out), nums

    def gen_class(self, class_count, func_per_class_count):
        out = []
        class_nums = {}

        for _ in xrange(class_count):
            num = seed()
            func_out, func_nums = self.gen_func(func_per_class_count, "x")
            out.append(swift_class_template.format(num, func_out))
            class_nums[num] = func_nums

        return "\n".join(out), class_nums

    def gen_file(self, class_count, function_count, import_list=[]):
        imports = "\n".join(["import " + i for i in import_list])
        func_out, func_nums = self.gen_func(function_count, "7")
        class_out, class_nums = self.gen_class(class_count, 5)

        chunks = [imports, func_out, class_out]

        return FileResult("\n".join(chunks), func_nums, class_nums)

    def gen_main(self, importing_module_name, class_num, func_num):
        import_line = 'import {}'.format(importing_module_name)
        action_expr = 'MyClass{}().complexCrap{}(arg: 4,stuff: 2)'.format(class_num, func_num)
        print_line = 'print("\\({})")'.format(action_expr)
        return '\n'.join([import_line, print_line])
