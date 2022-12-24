# encoding: utf-8
# __author:  angel
# date:  2022/12/24


import subprocess
import os

err = EnvironmentError("adb not found in $ANDROID_HOME path: %s." % os.environ["ANDROID_HOME"])
# 判断是否设置ANDROID_HOME
command = os.path.join(os.environ["ANDROID_HOME"], "platform-tools", "adb") if "ANDROID_HOME" in os.environ else err


class Shell:
    @staticmethod
    def start(cmd):
        output, errors = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        output_utf8 = output.decode("utf-8")
        return output_utf8


class ADB(object):
    def __init__(self, device_id=""):
        self.device_id = "-s %s" % device_id if device_id else device_id

    def adb(self, args):
        cmd = "%s %s %s" % (command, self.device_id, str(args))
        return Shell.start(cmd)

    def adb_shell(self, args):
        cmd = "%s %s shell %s" % (command, self.device_id, str(args))
        return Shell.start(cmd)

    def get_device_state(self):
        return self.adb("get-state").stdout.read().strip()

    def get_device_id(self):
        return self.adb("get-serialno").stdout.read().strip()

    def get_android_version(self):
        return self.adb_shell("getprop ro.build.version.release").strip()

    def get_sdk_version(self):
        return self.adb_shell("getprop ro.build.version.sdk").strip()

