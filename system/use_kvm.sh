#!/usr/bin/env bash
set -e

# Descargar driver principal de VirtualBox si está cargado
modprobe -r vboxdrv 2>/dev/null || true

# Cargar KVM (Intel o AMD)
modprobe kvm
modprobe kvm_intel 2>/dev/null || modprobe kvm_amd 2>/dev/null

# Levantar libvirt si existe
systemctl enable libvirtd virtlogd 2>/dev/null || true
systemctl start libvirtd virtlogd 2>/dev/null || true

echo "kvm"
