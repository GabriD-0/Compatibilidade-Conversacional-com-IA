import atexit
import logging
from typing import Optional
from sshtunnel import SSHTunnelForwarder
from paramiko import RSAKey, Ed25519Key, ECDSAKey

log = logging.getLogger(__name__)

_tunnel = None


def start_ssh_tunnel(config) -> Optional[int]:
    """
    Abre túnel SSH para o PostgreSQL remoto. Retorna a porta local efetiva
    ou None se o túnel não foi usado.
    """
    global _tunnel

    if not getattr(config, "DB_USE_SSH_TUNNEL", False):
        return None

    if not config.SSH_HOST or not config.SSH_USERNAME:
        raise RuntimeError("DB_USE_SSH_TUNNEL exige SSH_HOST e SSH_USERNAME definidos.")


    ssh_pkey = None
    if config.SSH_KEY_PATH:
        path = config.SSH_KEY_PATH

        for key_cls in (Ed25519Key, RSAKey, ECDSAKey):
            try:
                ssh_pkey = key_cls.from_private_key_file(path)
                break
            except Exception:
                continue
        if ssh_pkey is None:
            raise RuntimeError(f"Não foi possível carregar a chave SSH: {path}")

    kwargs = {
        "ssh_address_or_host": (config.SSH_HOST, config.SSH_PORT),
        "ssh_username": config.SSH_USERNAME,
        "remote_bind_address": (config.SSH_REMOTE_BIND_ADDRESS, config.SSH_REMOTE_BIND_PORT),
        "local_bind_address": ("127.0.0.1", config.SSH_LOCAL_BIND_PORT),
    }

    if ssh_pkey is not None:
        kwargs["ssh_pkey"] = ssh_pkey
    elif config.SSH_PASSWORD:
        kwargs["ssh_password"] = config.SSH_PASSWORD
    else:
        raise RuntimeError("Defina SSH_KEY_PATH ou SSH_PASSWORD para o túnel SSH.")

    tunnel = SSHTunnelForwarder(**kwargs)
    tunnel.start()
    _tunnel = tunnel
    local_port = tunnel.local_bind_port
    log.info("Túnel SSH ativo em 127.0.0.1:%s -> %s:%s", local_port, config.SSH_REMOTE_BIND_ADDRESS, config.SSH_REMOTE_BIND_PORT)
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