import os
import sublime
import sublime_plugin
import subprocess

# Some test strings
# hello world
# hello world && touch ~/foo
# $ac\/ii'sd'\:^
# foo  bar

# TODO: Need to make this autodetect and/or a setting
eyamlbin = '/Users/duboisph/.rbenv/shims/eyaml'

def RunCMD(args):
  proc = subprocess.Popen(args, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  out, err = proc.communicate()
  retcode = proc.returncode
  # TODO: Add some error handling
  return out.decode().rstrip(os.linesep)

def Encrypt(cleartext):
  return RunCMD([eyamlbin, 'encrypt', '-q', '-o', 'string', '-s', cleartext])

def Decrypt(ciphertext):
  return RunCMD([eyamlbin, 'decrypt', '-q', '-s', ciphertext])

class EyamlEncryptCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    for region in self.view.sel():
      if not region.empty():
        cleartext = self.view.substr(region)
        ciphertext = Encrypt(cleartext)
        self.view.replace(edit, region, ciphertext)

class EyamlDecryptCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    for region in self.view.sel():
      if not region.empty():
        ciphertext = self.view.substr(region)
        cleartext = Decrypt(ciphertext)
        self.view.replace(edit, region, cleartext)
