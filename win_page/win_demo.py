from pywinauto.application import Application

app = Application(backend='uia').start(
    r"D:\tmwork\SDK_package\artifacts (1)\sdk\DemoApp\WinX64Release\MFCDemo.exe")
# app.UntitledNotepad.type_keys("sdfs")


js_path = r"D:\tmwork\SDK_package\artifacts (1)\sdk\DemoApp\WinX64Release\sdkSZSE.js"
log_path = r"D:\tmwork\SDK_package\artifacts (1)\sdk\DemoApp\WinX64Release\log"

