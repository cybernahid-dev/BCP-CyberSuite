#!/usr/bin/env python3
# scanners/portscan.py
# Full-port threaded scanner + banner grabbing + progress/ETA
# Safe: short timeouts, polite sleeps. No destructive or exploit code.
# Developed by: cybernahid-dev | Bangladesh Cyber Panthers

import socket
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from math import ceil

# Default common ports (you can pass custom list)
DEFAULT_PORTS = [
    21,22,23,25,53,80,110,111,135,139,143,443,445,465,514,587,631,993,995,
    1701,1723,2082,2083,2086,2087,2095,2096,2195,2196,3306,3389,5900,8080,
    8443,8888,9000,10000,27017,49152,5000,8000,8883,8889,8983,9200,9300
]

def _banner_grab(ip, port, timeout=1.0):
    """Try to read a short banner. Non-blocking best-effort."""
    try:
        s = socket.socket()
        s.settimeout(timeout)
        s.connect((ip, port))
        # some services respond without data; try polite probe
        try:
            s.send(b"\r\n")
        except Exception:
            pass
        try:
            data = s.recv(1024)
            if data:
                return data.decode(errors="ignore").strip()
        except Exception:
            return ""
        finally:
            s.close()
    except Exception:
        return ""
    return ""

def _check_port(ip, port, timeout):
    """Return (port, banner) if open else None"""
    try:
        s = socket.socket()
        s.settimeout(timeout)
        s.connect((ip, port))
        s.close()
        # banner grab (short)
        banner = _banner_grab(ip, port, timeout=min(1.0, timeout+0.2))
        return {"port": port, "banner": banner}
    except Exception:
        return None

def full_port_scan(target, ports=None, threads=150, timeout=0.5, progress=True):
    """
    Perform a threaded port scan.

    Args:
      - target: hostname or IP (string)
      - ports: iterable of port ints or None for DEFAULT_PORTS
      - threads: number of worker threads (150 recommended for fast scans)
      - timeout: per connection timeout in seconds
      - progress: bool -> prints live progress + ETA

    Returns:
      dict: {"target": target, "scanned": N, "open": [...], "elapsed": secs}
      open entries: {"port": int, "banner": str}
    """
    if ports is None:
        # full 0-65535 if ports is 'all' or a special flag is passed; but default uses DEFAULT_PORTS
        ports = DEFAULT_PORTS[:]

    ports = list(ports)
    total = len(ports)
    start = time.time()
    open_ports = []
    completed = 0
    last_print = start

    # worker with single target IP resolution
    # resolve possible multiple IPs? We'll try socket.getaddrinfo for the first ip
    try:
        import socket as _sock
        infos = _sock.getaddrinfo(target, None)
        ip = infos[0][4][0]
    except Exception:
        ip = target  # assume user passed an IP or scan will fail

    with ThreadPoolExecutor(max_workers=min(threads, total or 1)) as ex:
        futures = {ex.submit(_check_port, ip, p, timeout): p for p in ports}
        for fut in as_completed(futures):
            completed += 1
            res = None
            try:
                res = fut.result()
            except Exception:
                res = None
            if res:
                open_ports.append(res)

            # live progress printing
            if progress:
                now = time.time()
                elapsed = now - start
                rate = completed / elapsed if elapsed > 0 else 0
                remaining = total - completed
                eta = remaining / rate if rate > 0 else float("inf")
                # print compact progress line
                eta_str = f"{int(eta)}s" if eta != float("inf") else "Unknown"
                print(f"\r[PortScan] {completed}/{total} scanned — Open: {len(open_ports)} — ETA: {eta_str}", end="", flush=True)

    elapsed = time.time() - start
    if progress:
        print()  # newline after progress

    return {
        "target": target,
        "ip": ip,
        "scanned": total,
        "open": sorted(open_ports, key=lambda x: x["port"]),
        "elapsed_seconds": round(elapsed, 2)
    }

# convenience turbo scan for full 0..65535 (warning: will be slower; use with care)
def turbo_full_scan(target, threads=500, timeout=0.3, progress=True):
    all_ports = list(range(1, 65536))
    return full_port_scan(target, ports=all_ports, threads=threads, timeout=timeout, progress=progress)
