from pywinauto.application import Application

app = Application(backend='uia').start(
    "C:\\Users\\Administrator\\AppData\\Local\Programs\\xtp_rich_client.gangtise-newquote-develop\\SmartX.gangtise-newquote-develop.exe")
app.UntitledNotepad.type_keys("sdfs")
