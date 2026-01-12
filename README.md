# Hypervisor Switcher

IMPORTANTE en si tiene un problama cojonudo en si la accion de cambiar del hypervisor te da un error ( que tu no ves)  que lo registra /var/log/syslog y registra cada accion en si y se va acmulando todo hasta petar el sistema hasta que busque una solucion mi recomendacion es que cada cierto tiempo es ejecutar este comando en si es esta : "sudo truncate -s 0 /var/log/syslog" esto es lo que hacia es vaciarlo en si nada mas 

---
Herramienta gráfica para Linux que permite alternar entre **KVM** y **VirtualBox** de forma segura, detectando máquinas activas y gestionando los módulos del kernel para evitar conflictos de virtualización.

El objetivo es resolver un problema común en entornos de laboratorio:  
KVM y VirtualBox no pueden usar VT-x / AMD-V al mismo tiempo. Cambiar manualmente entre ellos suele implicar descargar módulos, parar servicios y reiniciar. Esta aplicación centraliza todo ese proceso en una interfaz simple.

---

## Características

- Interfaz gráfica basada en GTK 4  
- Detección de máquinas virtuales activas  
- Prevención de cambios con VMs en ejecución  
- Activación automática de:
  - VirtualBox (descargando KVM)
  - KVM (descargando VirtualBox)
- Uso de `pkexec` para ejecutar acciones privilegiadas de forma segura  
- Código modular y escalable (pensado para añadir más hipervisores en el futuro)

---

## Requisitos

- Linux
- Python 3
- GTK 4 (`python3-gi`)
- KVM y/o VirtualBox instalados
- `pkexec` disponible en el sistema
- Permisos de administrador para cambiar módulos del kernel

---

## Estructura del proyecto
├── app.py
├── controller.py
├── system/
│ ├── status.sh
│ ├── use_kvm.sh
│ └── use_virtualbox.sh
└── ui/

- `app.py`  
  Interfaz gráfica y lógica de interacción con el usuario.

- `controller.py`  
  Lógica del sistema: detección de procesos, estado actual y ejecución con privilegios.

- `system/*.sh`  
  Scripts que cargan/descargan módulos y servicios según el hipervisor seleccionado.

---

## Uso

Ejecuta la aplicación:
bash
python3 app.py
