# *ew*pratten's *config* files

This repository stores *most* of my common config files. It is designed to be deployable to pretty much any UNIX-like system. Assuming ideal conditions, any machine is one `./install` away from behaving like my personal workstation.

## Setup

The scripts in this repository have the following dependencies:

- Git
- ZSH (optional, recommended)
- Neovim (optional, recommended)

Install and link everything with:

```sh
mkdir -p ~/.config && cd ~/.config
git clone https://github.com/ewpratten/ewconfig
cd ewconfig

# Linux
sh ./install-linux.sh

# Windows, with GIT BASH
sh ./install-windows.sh
```
