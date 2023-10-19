#! /bin/sh
set -e
export EWCONFIG_ROOT=$(dirname $(readlink -f $0))

# Pull git submodules if needed
echo "Syncing git submodules..."
git submodule update --init --recursive

# Make sure scripts are all executable
chmod +x $EWCONFIG_ROOT/configs/scripts/*
chmod +x $EWCONFIG_ROOT/configs/nautilus/scripts/*

# -- Directory Setup --
set -x

# Ensure that needed directories exist
mkdir -p ~/bin          # Personal bin dir. Reduces the risk of breaking ~/.local/bin
mkdir -p ~/projects     # For my projects

# Build the directory structure if ~/.config
mkdir -p ~/.config/git
mkdir -p ~/.config/git/config-fragments
mkdir -p ~/.cargo
mkdir -p ~/.ssh

# -- Config Linking --

# Configure the shell
ln -sf $EWCONFIG_ROOT/configs/shells/zsh/.zshrc ~/.zshrc
ln -sf $EWCONFIG_ROOT/configs/shells/bash/.bashrc ~/.bashrc

# Configure Git
ln -sf $EWCONFIG_ROOT/configs/git/.gitconfig ~/.gitconfig
ln -sf $EWCONFIG_ROOT/configs/sssh/allowed_signers ~/.ssh/allowed_signers
ln -sf $EWCONFIG_ROOT/configs/git/.mailmap ~/.config/git/.mailmap

# Configure SSH
ln -sf $EWCONFIG_ROOT/configs/ssh/config ~/.ssh/config
chmod 644 "$HOME/.ssh/config"
chown "$USER:$USER" "$HOME/.ssh/config"