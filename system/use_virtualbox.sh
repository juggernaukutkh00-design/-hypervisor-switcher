#!/usr/bin/env bash
set -e

# Parar/Deshabilitar libvirt si existe (no falla si no está instalado/cargado)
systemctl stop libvirtd virtlogd 2>/dev/null || true
systemctl disable libvirtd virtlogd 2>/dev/null || true

# Liberar VT-x/AMD-V: descargar KVM del kernel
modprobe -r kvm_intel kvm_amd kvm 2>/dev/null || true

# Cargar driver principal de VirtualBox
modprobe vboxdrv

echo "virtualbox"

