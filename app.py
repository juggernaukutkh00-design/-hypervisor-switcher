import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, GLib

import controller

# Aqui esta los nombre de los controladres esto lo hago para poder en si para centralizar y ademas de eso escalable
HYPERVISOR_VBOX = "virtualbox"
HYPERVISOR_KVM = "kvm"

class HypervisorSwitcher(Gtk.Application):
    def __init__(self):
        super().__init__(application_id="local.hypervisor.switcher")

    def do_activate(self):
        self.win = Gtk.ApplicationWindow(application=self)
        self.win.set_title("Hypervisor Switcher")
        self.win.set_default_size(420, 220)

        root = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        root.set_margin_top(18)
        root.set_margin_bottom(18)
        root.set_margin_start(18)
        root.set_margin_end(18)

        self.status_label = Gtk.Label(xalign=0)
        self.info_label = Gtk.Label(xalign=0)
        self.info_label.set_wrap(True)

        btn_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)

        self.btn_vbox = Gtk.Button(label="Activar VirtualBox")
        self.btn_kvm = Gtk.Button(label="Activar KVM")
        self.btn_refresh = Gtk.Button(label="Comprobar estado")

        self.btn_vbox.connect("clicked", self.on_vbox)
        self.btn_kvm.connect("clicked", self.on_kvm)
        self.btn_refresh.connect("clicked", self.on_refresh)

        btn_box.append(self.btn_vbox)
        btn_box.append(self.btn_kvm)
        btn_box.append(self.btn_refresh)

        root.append(self.status_label)
        root.append(self.info_label)
        root.append(btn_box)

        self.win.set_child(root)
        self.refresh_status()
        self.win.present()

    def refresh_status(self):
        status = controller.get_status()
        self.status_label.set_text(f"Estado actual: {status}")
        self.info_label.set_text(
            "Nota: KVM y VirtualBox no pueden usar VT-x/AMD-V a la vez. "
            "Si cambias, puede ser recomendable reiniciar."
        )

    def _set_busy(self, busy: bool):
        self.btn_vbox.set_sensitive(not busy)
        self.btn_kvm.set_sensitive(not busy)
        self.win.set_cursor_from_name("wait" if busy else None)

    def _show_error(self, message: str):
        dialog = Gtk.AlertDialog(
            message="No se pudo completar el cambio",
            detail=message
        )
        dialog.show(self.win)

    def _warn_running_vms(self, name: str):
        dialog = Gtk.AlertDialog(
            message="Maquinas virtuales en ejecucion",
            detail=(
                f"Se han detectado maquinas activas en {name}.\n\n"
                "Apagalas para poder cambiar de hipervisor."
            )
        )
        dialog.show(self.win)

    def _confirm(self, title: str, message: str) -> bool:
        dialog = Gtk.AlertDialog(
            message=title,
            detail=message,
            buttons=["Cancelar", "Continuar"]
        )
        response = dialog.choose(self.win)
        return response == 1

    def on_vbox(self, _btn):
        # Si KVM tiene VMs activas, avisar
        if controller.has_running_vms(HYPERVISOR_KVM):
            self._warn_running_vms("KVM")
            return

        if not self._confirm(
            "Confirmar cambio de hipervisor",
            (
                "Vas a activar VirtualBox.\n\n"
                "Este cambio puede detener máquinas virtuales activas.\n"
                "Recuerda apagarlas y guardar tu información.\n\n"
                "También se liberará VT-x / AMD-V.\n\n"
                "¿Quieres continuar?"
            )
        ):
            return

        self._set_busy(True)
        GLib.idle_add(self._switch, HYPERVISOR_VBOX)

    def on_kvm(self, _btn):
        # Si VirtualBox tiene VMs activas, avisar
        if controller.has_running_vms(HYPERVISOR_VBOX):
            self._warn_running_vms("VirtualBox")
            return

        if not self._confirm(
            "Confirmar cambio de hipervisor",
            (
                "Vas a activar KVM.\n\n"
                "Este cambio puede detener máquinas virtuales activas.\n"
                "Recuerda apagarlas y guardar tu información.\n\n"
                "También se liberará VT-x / AMD-V.\n\n"
                "¿Quieres continuar?"
            )
        ):
            return

        self._set_busy(True)
        GLib.idle_add(self._switch, HYPERVISOR_KVM)

    def _switch(self, target: str):
        try:
            if target == HYPERVISOR_VBOX:
                controller.activate_virtualbox()
            elif target == HYPERVISOR_KVM:
                controller.activate_kvm()
        except Exception as e:
            self._show_error(str(e))
        finally:
            self._set_busy(False)
            self.refresh_status()
        return False
#En si este es parte del boton del refresh     
    def on_refresh(self, _btn):
        self.refresh_status()


app = HypervisorSwitcher()
app.run()
