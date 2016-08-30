#!/usr/bin/python
# -*- coding: utf-8 -*-

from xml.dom   import minidom
from xml.etree import ElementTree
import xml.dom.minidom
import os
import string
import copy


class AndroidManifestParser:
    def __init__(self, manifest):
        self.file_path = manifest
        self._is_loaded = False
        self.xml_result = {}

        # manifest
        self._package_name     = ""

        # uses-sdk
        self._minSdkVersion    = ""
        self._targetSdkVersion = ""

        # uses-permission
        self._list_permission  = []

        # application
        self._is_allowBackup = False
        self._is_debuggable  = False

        # activity
        self._main_activity    = ""
        self._list_activity    = []
        self._exported_activity = []

        # service
        self._list_service = []
        self._exported_service = []

        # receiver
        self._list_receiver = []
        self._exported_receiver = []

        # provider
        self._list_provider = []
        self._exported_provider = []


    def insert_Dict(self, dict, key, value):
        dict[key] = value


    def is_xml_file(self, file_path):
        try:
            xml.dom.minidom.parse(file_path)
        except:
            return False

        return True


    def check_loaded(self):
        if self._is_loaded:
            return True
        else:
            if self.read_XML(self.file_path):
                return True

        return False


    # 获取package name    格式:{'package_name':'value'}
    def read_Manifest(self, Root):
        self._package_name = Root.getAttribute('package')
        self.insert_Dict(self.xml_result, 'package_name', self._package_name)


    # 获取miniSDK
    # 格式:{'miniSDK':'value'}
    # 格式:{'targetSDK':'value'}
    def read_UsesSDK(self, ManifestRoot):
        self._minSdkVersion    = "NULL"
        self._targetSdkVersion = "NULL"

        for uses_sdk in ManifestRoot.getElementsByTagName('uses-sdk'):
            self._minSdkVersion    = uses_sdk.getAttribute('android:minSdkVersion')
            self._targetSdkVersion = uses_sdk.getAttribute('android:targetSdkVersion')
            # 若有多个[uses-sdk],目前只解析第一个
            break

        self.insert_Dict(self.xml_result, 'miniSDK', self._minSdkVersion)
        self.insert_Dict(self.xml_result, 'targetSDK', self._targetSdkVersion)


    # 获取permission
    # 格式:{'permission':['value1', 'value2' ...]}
    def read_UsesPermissions(self, ManifestRoot):
        for userPS_idx in ManifestRoot.getElementsByTagName('uses-permission'):
            self._list_permission.append(userPS_idx.getAttribute('android:name'))

        self.insert_Dict(self.xml_result, 'permission', self._list_permission)


    # 获取application 检测 allowBackup, debuggable
    def read_Application(self, ManifestRoot):
        for Application in ManifestRoot.getElementsByTagName('application'):
            self._is_allowBackup = False
            self._is_debuggable  = False
            allowBackup = Application.getAttribute('android:allowBackup')
            debuggable  = Application.getAttribute('android:debuggable')

            #if len(allowBackup) == 0 or allowBackup.lower() == u"true":
            if allowBackup.lower() == u"true":
                self._is_allowBackup = True
            if debuggable.lower() == u"true":
            #if len(debuggable) == 0 or debuggable.lower() == u"true":
                self._is_debuggable  = True

            self.read_Activity(Application)
            self.read_Service(Application)
            self.read_Receiver(Application)
            self.read_Provider(Application)

            # 若有多个[application],目前只解析第一个
            break

    # 获取activity
    # 格式:{'activity'::['value1', 'value2' ...]}
    def read_Activity(self, Application):

        for activity in Application.getElementsByTagName('activity'):
            act_name = activity.getAttribute('android:name')
            exported = activity.getAttribute('android:exported')
            filters  = activity.getElementsByTagName('intent-filter')
            self._list_activity.append(act_name)

            if len(filters) > 0:
                is_have_MAIN     = False
                is_hava_LAUNCHER = False

                # 判断是否为Main Activity
                for filter in filters:
                    for act_act in filter.getElementsByTagName('action'):
                        #print act_act.getAttribute('android:name').lower()
                        if act_act.getAttribute('android:name').lower() == u'android.intent.action.main':
                            is_have_MAIN = True

                    for act_cat in filter.getElementsByTagName('category'):
                        #print act_cat.getAttribute('android:name').lower()
                        if act_cat.getAttribute('android:name').lower() == u'android.intent.category.launcher':
                            is_hava_LAUNCHER = True

                    if is_have_MAIN and is_hava_LAUNCHER:
                        self._main_activity = act_name
                        break

                # 当存在intent-filter项,exported默认值为 True
                if len(exported) == 0 or exported.lower() == u"true":
                    self._exported_activity.append(act_name)
            else:
                # 不存在intent-filter项,exported默认值为 False
                if exported.lower() == u"true":
                    self._exported_activity.append(act_name)

        if len(self._list_activity) > 0:
            self.insert_Dict(self.xml_result, 'activity', self._list_activity)


    # 获取service
    # 格式:{'service':{'service1':['action', ...], 'service2':['action', ...],...}}
    def read_Service(self, Application):
        for service in Application.getElementsByTagName('service'):
            service_name = service.getAttribute('android:name')
            exported     = service.getAttribute('android:exported')
            filters      = service.getElementsByTagName('intent-filter')
            self._list_service.append(service_name)

            if len(filters) > 0:
                # 当存在intent-filter项,exported默认值为 True
                if len(exported) == 0 or exported.lower() == u"true":
                    self._exported_service.append(service_name)
            else:
                # 不存在intent-filter项,exported默认值为 False
                if exported.lower() == u"true":
                    self._exported_service.append(service_name)

        if len(self._list_service) > 0:
            self.insert_Dict(self.xml_result, 'service', self._list_service)

    # 获取receiver
    # 格式:{'receiver':{'receiver1':['action', ...], 'receiver2':['action', ...], ...}}
    def read_Receiver(self, Application):
        for receiver in Application.getElementsByTagName('receiver'):
            receiver_name = receiver.getAttribute('android:name')
            exported      = receiver.getAttribute('android:exported')
            filters       = receiver.getElementsByTagName('intent-filter')
            self._list_receiver.append(receiver_name)

            if len(filters) > 0:
                # 当存在intent-filter项,exported默认值为 True
                if len(exported) == 0 or exported.lower() == u"true":
                    self._exported_receiver.append(receiver_name)
            else:
                # 不存在intent-filter项,exported默认值为 False
                if exported.lower() == u"true":
                    self._exported_receiver.append(receiver_name)

        if len(self._list_receiver) > 0:
            self.insert_Dict(self.xml_result, 'receiver', self._list_receiver)


    def read_Provider(self, Application):
        #获取_exported_provider
        for provider in Application.getElementsByTagName('provider'):
            provider_name = provider.getAttribute('android:name')
            exported      = provider.getAttribute('android:exported')
            filters       = provider.getElementsByTagName('intent-filter')
            self._list_provider.append(provider_name)

            if len(filters) > 0:
                #for filter in filters:
                #    for provider_act_idx in filter.getElementsByTagName('action'):
                #        self._list_service_action.append(provider_act_idx.getAttribute('android:name'))
                #    self.insert_Dict(self._receiver_tmp, receiver_name, self._list__receiver_action)
                #self.insert_Dict(self.xml_result, 'receiver', self._receiver_tmp)

                # 当存在intent-filter项,exported默认值为 True
                if len(exported) == 0 or exported.lower() == u"true":
                    self._exported_provider.append(provider_name)
            else:
                # 不存在intent-filter项,exported默认值为 False
                if exported.lower() == u"true":
                    self._exported_provider.append(provider_name)

        if len(self._list_provider) > 0:
            self.insert_Dict(self.xml_result, 'receiver', self._list_provider)

    def read_XML(self, file_path):
        try:
            self._is_loaded = False
            dom             = xml.dom.minidom.parse(file_path)
            Root            = dom.documentElement
            Manifest        = dom.firstChild

            self.read_Manifest(Root)
            self.read_UsesSDK(Manifest)
            self.read_UsesPermissions(Manifest)
            self.read_Application(Manifest)
            self._is_loaded = True
            self.file_path  = file_path
            return True

        except:
            return False


    def get_xml_result(self):
        if self.check_loaded():
            return self.xml_result
        return []


    def get_package_name(self):
        if self.check_loaded():
            return True, self._package_name
        return False, "error"


    def get_is_allowBackup(self):
        if self.check_loaded():
            return True, self._is_allowBackup
        return False, "error"


    def get_is_debuggable(self):
        if self.check_loaded():
            return True, self._is_debuggable
        return False, "error"


    def get_main_activity(self):
        if self.check_loaded():
            return True, self._main_activity
        return False, "error"


    def get_activitys(self):
        if self.check_loaded():
            return True, self._list_activity
        return False, "error"


    def get_activity_exported(self):
        if self.check_loaded():
            return True, self._exported_activity
        return False, "error"


    def get_service_exported(self):
        if self.check_loaded():
            return True, self._exported_service
        return False, "error"


    def get_receiver_exported(self):
        if self.check_loaded():
            return True, self._exported_receiver
        return False, "error"

    def get_provider_exported(self):
        if self.check_loaded():
            return True, self._exported_provider
        return False, "error"



if __name__ == '__main__':
    parser = AndroidManifestParser(r"D:\AndroidAPK\SimpleTetris\AndroidManifest.xml")
    xml_result = parser.get_xml_result()
    print xml_result['package_name']
    print parser._main_activity
    print xml_result['activity']