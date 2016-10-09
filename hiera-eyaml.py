import os
import re
import sublime
import sublime_plugin
import subprocess
import sys

# Some test strings
# hello world
# hello world && touch ~/foo
# $ac\/ii'sd'\:^
# foo  bar

# TODO: Need to make this autodetect and/or a setting
eyamlbin = '/Users/duboisph/.rbenv/shims/eyaml'


def runCmd(args):
  try:
    proc = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = proc.communicate()
    if proc.returncode == 0:
      return out.decode('utf-8').strip(os.linesep)
    else:
      err = err.decode('utf-8').strip()
      # Remove ANSI control characters (see: http://www.commandlinefu.com/commands/view/3584/remove-color-codes-special-characters-with-sed)
      err = re.sub(r'\x1B\[([0-9]{1,2}(;[0-9]{1,2})?)?[m|K]', '', err)
      sublime.status_message(' > Hiera-eyaml - Fail: ' + err)
  except OSError:
    exc = sys.exc_info()[1]
    sublime.status_message(' > Hiera-eyaml - Fail: ' + str(exc))


def encrypt(cleartext):
  return runCmd([eyamlbin, 'encrypt', '-q', '-o', 'string', '-s', cleartext])


def decrypt(ciphertext):
  return runCmd([eyamlbin, 'decrypt', '-q', '-s', ciphertext])


class EyamlEncryptCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    for region in self.view.sel():
      if not region.empty():
        cleartext = self.view.substr(region)
        ciphertext = encrypt(cleartext)
        self.view.replace(edit, region, ciphertext)
        sublime.status_message(' > Hiera-eyaml - Encrypted...')
      else:
        sublime.status_message(' > Hiera-eyaml - No text selected...')


class EyamlDecryptCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    for region in self.view.sel():
      if not region.empty():
        ciphertext = self.view.substr(region)
        cleartext = decrypt(ciphertext)
        self.view.replace(edit, region, cleartext)
        sublime.status_message(' > Hiera-eyaml - Decrypted...')
      else:
        sublime.status_message(' > Hiera-eyaml - No text selected...')
