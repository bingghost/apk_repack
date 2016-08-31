
# apk repack
>* 重打包APK用于调试的python脚本


### 步骤

	1. apktool解包
	2. 设置允许调试 AndroidManifest.xml OnCreate()
	3. 重新编译打包
	4. 签名
	5. am debug
#
#
#

OnCreate不加入下列代码也可以调试

	invoke-static {}, Landroid/os/Debug;->waitForDebugger()V


### 使用方法
	python E:\Code\python\apk_repack\apk_repack.py SimpleTetris.apk


### 使用手册
	http://www.cnblogs.com/bingghost/p/5825402.html


