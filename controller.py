import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
SYSTEM_DIR = BASE_DIR / "system"

class SwitchError(RuntimeError):
    pass

# Procesosos que se encargar de que detecte las maquinas virtules y que cancele/error para poder cerrarlas guardarlas
import subprocess

def _process_running(patterns: list[str]) -> bool:
    for p in patterns:
        result = subprocess.run(
            ["pgrep", "-f", p],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        if result.returncode == 0:
            return True
    return False


def has_running_vms(hypervisor: str) -> bool:
    if hypervisor == "virtualbox":
        return _process_running([
            "VirtualBoxVM",
            "VBoxHeadless"
        ])

    if hypervisor == "kvm":
        return _process_running([
            "qemu-system"
        ])

    return False

# Procesos que se encarga de ver que que esta y que se encargar de enceder los sistemas de vistualizaion depdende de lo qu qqueramos

def _run(cmd: list[str], *, check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, text=True, capture_output=True, check=check)

def get_status() -> str:
    script = SYSTEM_DIR / "status.sh"
    res = _run([str(script)], check=False)
    out = (res.stdout or "").strip()
    return out if out in {"kvm", "virtualbox", "none"} else "none"

def _run_as_root(script_path: Path) -> None:
    res = subprocess.run(
        ["pkexec", str(script_path)],
        text=True,
        capture_output=True
    )
    if res.returncode != 0:
        stderr = (res.stderr or "").strip()
        stdout = (res.stdout or "").strip()
        raise SwitchError(stderr or stdout or "Operacion cancelada o fallida (pkexec).")

def activate_virtualbox() -> None:
    _run_as_root(SYSTEM_DIR / "use_virtualbox.sh")

def activate_kvm() -> None:
    _run_as_root(SYSTEM_DIR / "use_kvm.sh")
