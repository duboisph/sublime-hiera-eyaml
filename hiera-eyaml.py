import os
import re
import sublime
import sublime_plugin
import subprocess
import sys


def plugin_loaded():
    global s
    s = sublime.load_settings("hiera-eyaml.sublime-settings")


def runCmd(args, stdin_string):
    try:
        proc = subprocess.Popen(args,
                                stdout=subprocess.PIPE,
                                stdin=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        out, err = proc.communicate(input=stdin_string.encode('utf-8'))
        if proc.returncode == 0:
            return out.decode('utf-8').strip(os.linesep)
        else:
            err = err.decode('utf-8').strip()
            # Remove ANSI control characters.
            err = re.sub(r'\x1B\[([0-9]{1,2}(;[0-9]{1,2})?)?[m|K]', '', err)
            sublime.error_message('Hiera-eyaml: Error\n\n%s' % err)
    except OSError:
        exc = sys.exc_info()[1]
        sublime.error_message('Hiera-eyaml: Error\n\n%s' % str(exc))


def encrypt(cleartext):
    eyamlbin = s.get('hiera_eyaml_bin', 'eyaml')
    return runCmd([eyamlbin, 'encrypt', '-q', '-o', 'string', '--stdin'], cleartext)


def decrypt(ciphertext):
    eyamlbin = s.get('hiera_eyaml_bin', 'eyaml')
    return runCmd([eyamlbin, 'decrypt', '-q', '--stdin'], ciphertext)


class EyamlEncryptCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        for region in self.view.sel():
            if not region.empty():
                cleartext = self.view.substr(region)
                ciphertext = encrypt(cleartext)
                self.view.replace(edit, region, ciphertext)
                sublime.status_message(' > Hiera-eyaml: Encrypted...')
            else:
                sublime.status_message(' > Hiera-eyaml: No text selected...')


class EyamlDecryptCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        for region in self.view.sel():
            if not region.empty():
                ciphertext = self.view.substr(region)
                cleartext = decrypt(ciphertext)
                self.view.replace(edit, region, cleartext)
                sublime.status_message(' > Hiera-eyaml: Decrypted...')
            else:
                sublime.status_message(' > Hiera-eyaml: No text selected...')
