import socket
import argparse


def scan_port(host: str, port: int, timeout: float = 1.0) -> bool:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            result = sock.connect_ex((host, port))
            return result == 0
    except socket.error:
        return False


def parse_ports(port_string: str) -> range:
    if "-" in port_string:
        start, end = port_string.split("-", 1)
        return range(int(start), int(end) + 1)
    return range(int(port_string), int(port_string) + 1)


def main() -> None:
    parser = argparse.ArgumentParser(description="Escáner de puertos básico")
    parser.add_argument("host", help="Dirección IP o nombre de host a escanear")
    parser.add_argument("-p", "--ports", default="1-1024",
                        help="Rango de puertos a escanear. Ejemplo: 20-80 o 22")
    parser.add_argument("-t", "--timeout", type=float, default=0.5,
                        help="Tiempo de espera por puerto en segundos")

    args = parser.parse_args()
    ports = parse_ports(args.ports)

    print(f"Escaneando {args.host} en puertos {args.ports}...")
    for port in ports:
        if scan_port(args.host, port, args.timeout):
            print(f"Puerto abierto: {port}")


if __name__ == "__main__":
    main()
