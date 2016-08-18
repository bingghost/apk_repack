#!/usr/bin/env python
# encoding: utf-8
'''
    Created on 2016-8-18

    @author: bingghost
'''


class Config(object):
    android_tools_path = "D:\\Tools\\Android\\"
    apktool_path = android_tools_path + r"apktool.bat"
    zipalign_path = "E:\\Android\\sdk\\build-tools\\23.0.3\\zipalign.exe"
    signapk_path = android_tools_path + r"android-tools\\signapk\\signapk.bat"

    apk_path = ""
    current_program_path = ""

    unpack_path = ""
    unsigned_path = ""

    pass