import atexit
import logging
from typing import Optional
import paramiko
from sshtunnel import SSHTunnelForwarder
from paramiko import RSAKey, Ed25519Key, ECDSAKey

log = logging.getLogger(__name__)

_tunnel = None

paramiko.DSSKey = None

# Abre túnel SSH para o PostgreSQL remoto. Retorna a porta local efetiva ou None se o túnel não foi usado.
def start_ssh_tunnel(config) -> Optional[int]:
    global _tunnel

    if not config.get("DB_USE_SSH_TUNNEL", False):
        return None

    if not config.get("SSH_HOST") or not config.get("SSH_USERNAME"):
        raise RuntimeError("DB_USE_SSH_TUNNEL exige SSH_HOST e SSH_USERNAME definidos.")

    ssh_pass_key = None
    if config.get("SSH_KEY_PATH"):
        path = config.get("SSH_KEY_PATH")

        for key_cls in (Ed25519Key, RSAKey, ECDSAKey):
            try:
                ssh_pass_key = key_cls.from_private_key_file(path)
                break
            except Exception:
                continue
        if ssh_pass_key is None:
            raise RuntimeError(f"Não foi possível carregar a chave SSH: {path}")

    ssh_host = config.get("SSH_HOST", "").strip('"')
    ssh_port = int(config.get("SSH_PORT", 22))
    
    remote_bind_address = config.get("SSH_REMOTE_BIND_ADDRESS", "127.0.0.1").strip('"').strip()
    remote_bind_port = int(config.get("SSH_REMOTE_BIND_PORT", 5432))
    
    local_bind_port = int(config.get("SSH_LOCAL_BIND_PORT", 0))

    kwargs = {
        "ssh_address_or_host": (ssh_host, ssh_port),
        "ssh_username": config.get("SSH_USERNAME"),
        "remote_bind_address": (remote_bind_address, remote_bind_port),
        "local_bind_address": ("127.0.0.1", local_bind_port),
    }

    if ssh_pass_key is not None:
        kwargs["ssh_pkey"] = ssh_pass_key
    elif config.get("SSH_PASSWORD"):
        kwargs["ssh_password"] = config.get("SSH_PASSWORD")
    else:
        raise RuntimeError("Defina SSH_KEY_PATH ou SSH_PASSWORD para o túnel SSH.")

    tunnel = SSHTunnelForwarder(**kwargs)
    tunnel.start()
    _tunnel = tunnel
    local_port = tunnel.local_bind_port
    log.info("Túnel SSH ativo em %s:%s", remote_bind_address, local_port)
    atexit.register(stop_ssh_tunnel)
    return local_port


def stop_ssh_tunnel() -> None:
    global _tunnel
    if _tunnel is not None:
        try:
            _tunnel.stop()
        except Exception as e:
            log.warning("Erro ao encerrar túnel SSH: %s", e)
        _tunnel = None