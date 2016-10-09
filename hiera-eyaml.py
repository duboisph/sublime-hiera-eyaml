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


def plugin_loaded():
  global s
  s = sublime.load_settings("hiera-eyaml.sublime-settings")


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
      sublime.error_message('Hiera-eyaml: Error\n\n%s' % err)
  except OSError:
    exc = sys.exc_info()[1]
    sublime.error_message('Hiera-eyaml: Error\n\n%s' % str(exc))


def encrypt(cleartext):
  eyamlbin = s.get('hiera_eyaml_bin', 'eyaml')
  return runCmd([eyamlbin, 'encrypt', '-q', '-o', 'string', '-s', cleartext])


def decrypt(ciphertext):
  eyamlbin = s.get('hiera_eyaml_bin', 'eyaml')
  return runCmd([eyamlbin, 'decrypt', '-q', '-s', ciphertext])


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
