#!/usr/bin/env python
#
# Copyright (c) 2001, 2002 Steven Knight
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY
# KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
# WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

__revision__ = "__FILE__ __REVISION__ __DATE__ __DEVELOPER__"

import sys
import TestSCons

python = sys.executable

test = TestSCons.TestSCons()

test.subdir('subdir')

test.write('build.py', r"""
import sys
contents = open(sys.argv[2], 'rb').read() + open(sys.argv[3], 'rb').read()
file = open(sys.argv[1], 'wb')
file.write(contents)
file.close()
""")

test.write('SConstruct', """
Foo = Builder(action = r"%s build.py $TARGET $SOURCES subdir/foo.dep")
Bar = Builder(action = r"%s build.py $TARGET $SOURCES subdir/bar.dep")
env = Environment(BUILDERS = { 'Foo' : Foo, 'Bar' : Bar })
env.Depends(target = ['f1.out', 'f2.out'], dependency = 'subdir/foo.dep')
env.Depends(target = 'f3.out', dependency = 'subdir/bar.dep')
env.Foo(target = 'f1.out', source = 'f1.in')
env.Foo(target = 'f2.out', source = 'f2.in')
env.Bar(target = 'f3.out', source = 'f3.in')
SConscript('subdir/SConscript', "env")
""" % (python, python))

test.write(['subdir', 'SConscript'], """
Import("env")
env.Depends(target = 'f4.out', dependency = 'bar.dep')
env.Bar(target = 'f4.out', source = 'f4.in')
""")

test.write('f1.in', "f1.in\n")

test.write('f2.in', "f2.in\n")

test.write('f3.in', "f3.in\n")

test.write(['subdir', 'f4.in'], "subdir/f4.in\n")

test.write(['subdir', 'foo.dep'], "subdir/foo.dep 1\n")

test.write(['subdir', 'bar.dep'], "subdir/bar.dep 1\n")

test.run(arguments = '.')

test.fail_test(test.read('f1.out') != "f1.in\nsubdir/foo.dep 1\n")
test.fail_test(test.read('f2.out') != "f2.in\nsubdir/foo.dep 1\n")
test.fail_test(test.read('f3.out') != "f3.in\nsubdir/bar.dep 1\n")
test.fail_test(test.read(['subdir', 'f4.out']) !=
               "subdir/f4.in\nsubdir/bar.dep 1\n")

test.write(['subdir', 'foo.dep'], "subdir/foo.dep 2\n")

test.write(['subdir', 'bar.dep'], "subdir/bar.dep 2\n")

test.run(arguments = '.')

test.fail_test(test.read('f1.out') != "f1.in\nsubdir/foo.dep 2\n")
test.fail_test(test.read('f2.out') != "f2.in\nsubdir/foo.dep 2\n")
test.fail_test(test.read('f3.out') != "f3.in\nsubdir/bar.dep 2\n")
test.fail_test(test.read(['subdir', 'f4.out']) !=
               "subdir/f4.in\nsubdir/bar.dep 2\n")

test.write(['subdir', 'bar.dep'], "subdir/bar.dep 3\n")

test.run(arguments = '.')

test.fail_test(test.read('f1.out') != "f1.in\nsubdir/foo.dep 2\n")
test.fail_test(test.read('f2.out') != "f2.in\nsubdir/foo.dep 2\n")
test.fail_test(test.read('f3.out') != "f3.in\nsubdir/bar.dep 3\n")
test.fail_test(test.read(['subdir', 'f4.out']) !=
               "subdir/f4.in\nsubdir/bar.dep 3\n")

test.pass_test()
