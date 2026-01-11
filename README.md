<<<<<<< HEAD
# -hypervisor-switcher
Herramienta gráfica para Linux que permite alternar entre KVM y VirtualBox de forma segura, detectando máquinas activas y gestionando los módulos del kernel para evitar conflictos de virtualización.
=======
# Hypervisor Switcher

Herramienta gráfica para Linux que permite alternar entre KVM y VirtualBox de forma segura.

Detecta máquinas virtuales activas y gestiona los módulos del kernel para evitar conflictos de virtualización.

## Características

- Interfaz gráfica con GTK
- Detección de VMs en ejecución
- Cambio seguro entre KVM y VirtualBox
- Uso de scripts con privilegios mediante `pkexec`

## Requisitos

- Linux
- Python 3
- GTK 4
- VirtualBox y/o KVM instalados

## Uso

```bash
python3 app.py

>>>>>>> 029da5d (Initial project files)
