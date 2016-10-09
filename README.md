# Hiera-eyaml for Sublime Text

Package to use [hiera-eyaml](https://github.com/TomPoulton/hiera-eyaml) encryption/decryption in Sublime Text.

## Installing

<!--**Package Control:** The easiest way to install Hiera-eyaml is through [Package Control](https://packagecontrol.io). Search for "[Hiera-eyaml](https://packagecontrol.io/packages/Hiera-eyaml)".-->

**Manual:** Clone this repository in your Sublime Text Packages directory (`Preferences -> Browse Packages...`). Example on macOS:

```shell
cd ~/Library/Application\ Support/Sublime\ Text\ 3/Packages
git clone https://github.com/duboisph/sublime-hiera-eyaml.git hiera-eyaml
```

***Note***: You need the [hiera-eyaml gem](https://github.com/TomPoulton/hiera-eyaml) installed and pre-configured (generated keys, KMS, ...) for this package to work.

## Usage

You can encrypt or decrypt selected text via the Menu or using the <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>E</kbd> and <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>D</kbd> keyboard shortcuts.

If Sublime Text can't find the `eyaml` binary in it's PATH on macOS, you can set the correct path via the Settings. For example:

```json
{
  "hiera_eyaml_bin": "/Users/duboisph/.rbenv/shims/eyaml"
}
```

Another option is to install the "[Fix Mac Path](https://github.com/int3h/SublimeFixMacPath)" package.

## Acknowledgements

- [Hiera eyaml backend](https://github.com/TomPoulton/hiera-eyaml)
- [Hiera-eyaml Atom plugin](https://github.com/jpohjolainen/atom-hiera-eyaml)
