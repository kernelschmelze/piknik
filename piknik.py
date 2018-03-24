import sublime
import sublime_plugin
import subprocess
import os

def execute(cmd, content):
    try:
        if os.name == "nt":
            si = subprocess.STARTUPINFO()
            si.dwFlags |= subprocess.SW_HIDE | subprocess.STARTF_USESHOWWINDOW
            process = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, startupinfo=si, shell=False, creationflags=subprocess.SW_HIDE)
        else:
            process = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        result, error = process.communicate(input=content.encode())
        if error:
            print(error.decode())
            return None
        return result.decode()
    except IOError as e:
        print('Error: %s' % e)
    except OSError as e:
        print('Error: %s' % e)

class CopyToPiknik(sublime_plugin.TextCommand):
    def run(self, edit):
        content = u''
        v = self.view
        for region in v.sel():
            if not region.empty():
                if content: 
                    content += "\n"
                content += v.substr(region)
        if not content:
            content += v.substr(sublime.Region(0, v.size()))
        cmd = ['piknik', '-copy']
        execute(cmd, content)

class PasteFromPiknik(sublime_plugin.TextCommand):
    def run(self, edit):
        cmd = ['piknik', '-paste']
        content = execute(cmd, "")
        if content:
            v = self.view
            v.insert(edit, v.sel()[0].begin(), content)

class PasteFromPiknikToClipboard(sublime_plugin.TextCommand):
    def run(self, edit):
        cmd = ['piknik', '-paste']
        content = execute(cmd, "")
        if content:
            sublime.set_clipboard(content)
