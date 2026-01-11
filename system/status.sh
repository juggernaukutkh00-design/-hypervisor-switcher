#!/usr/bin/env bash
set -e

# 1) VirtualBox activo si hay procesos vivos
if pgrep -f 'VirtualBoxVM|VBoxHeadless|VBoxSVC' >/dev/null; then
  echo "virtualbox"
  exit 0
fi

# 2) KVM activo si los módulos están cargados
if lsmod | grep -q 'kvm'; then
  echo "kvm"
  exit 0
fi

# 3) Ninguno
echo "none"
