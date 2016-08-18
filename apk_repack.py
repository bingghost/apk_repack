#!/usr/bin/env python
# encoding: utf-8
"""
@author:     bingghost
@copyright:  2016 bingghost. All rights reserved.
@contact:
@date:       2016-8-18
@description: 自动从打包安装调试apk程序
"""

import os
import sys
import subprocess
from config import config

the_config = config.Config

def init():
    if len(sys.argv) != 2:
        return False, "argument error!"

    the_config.current_program_path = os.getcwd()

    apk_path = sys.argv[1]
    file_name = os.path.basename(apk_path)

    the_config.apk_path = apk_path
    the_config.unpack_path = the_config.current_program_path + "\\" + apk_path[:-4]
    the_config.unsigned_path = the_config.unpack_path + '\\dist\\'+file_name

    return True, "Success!"
    pass


class APKdebugger(object):
    def unpackaging(self,apktool_path,apk_path):
        print 'Start Unpackaging...'
        subprocess.call([apktool_path,'d','-d',apk_path],shell=True)

    def packaging(self,apktool_path,file_path):
        print 'Start Packaging...'
        subprocess.call([apktool_path,'b','-d',file_path],shell=True)

    def signer(self, jarsigner_path, unsigned_path):
        print 'Start Signing...'
        signer_comm=[jarsigner_path,unsigned_path,"signed.apk"]
        subprocess.call(signer_comm,shell=True)

    def zipalign(self,zipalign_path, outapk_path,signed_apk_path):
        print 'Start zipalign...'
        subprocess.call([zipalign_path,'-v','4',signed_apk_path,outapk_path],shell=True)

    def intall_apk(self,apk_path):
        print 'intall apk...'
        subprocess.call(["adb install",apk_path],shell=True)
        pass

def main():
    # 初始化
    ret, info = init()
    if (ret == False):
        print(info)
        return
        pass

    apk_debugger = APKdebugger()
    apk_debugger.unpackaging(the_config.apktool_path,the_config.apk_path)
    apk_debugger.packaging(the_config.apktool_path,the_config.unpack_path)
    apk_debugger.signer(the_config.signapk_path,the_config.unsigned_path)
    signed_apk_path = the_config.current_program_path + '\\signed.apk'
    debug_apk_path = the_config.current_program_path + '\\debug.apk'
    apk_debugger.zipalign(the_config.zipalign_path,debug_apk_path,signed_apk_path)
    pass


if __name__ == '__main__':
    main()
