#! /usr/bin/env python3
import argparse
import sys
import subprocess
from typing import Optional


def has_ykman() -> bool:
    try:
        subprocess.run(["ykman", "--version"], check=True, stdout=subprocess.DEVNULL)
        return True
    except subprocess.CalledProcessError:
        return False


def has_yk_plugged_in() -> bool:
    devices = subprocess.run(["ykman", "list"], check=True, stdout=subprocess.PIPE)
    devices = devices.stdout.decode("utf-8").split("\n")
    return len(devices) > 1


def is_interface_up(interface: str) -> bool:
    try:
        subprocess.run(
            ["ip", "link", "show", interface], check=True, stdout=subprocess.DEVNULL
        )
        return True
    except subprocess.CalledProcessError:
        return False


def get_oath_code(service: str) -> Optional[int]:
    response = subprocess.run(
        ["ykman", "oath", "accounts", "code", "Guru"],
        check=True,
        stdout=subprocess.PIPE,
    )
    output = response.stdout.decode("utf-8")
    if not output:
        return None
    return int(output.split("\n")[0].split(" ")[-1])


def get_password(label: str, ns: str, key: str) -> str:
    # Try to find it
    try:
        result = subprocess.run(
            ["secret-tool", "lookup", ns, key], check=True, stdout=subprocess.PIPE
        )
        return result.stdout.decode("utf-8")
    except subprocess.CalledProcessError:
        # If we are here, it doesn't exist
        print(f"Enter your {label}")
        subprocess.run(["secret-tool", "store", "--label", label, ns, key], check=True)
        return get_password(label, ns, key)


def handle_connect(args: argparse.Namespace) -> int:
    # If we are connected to AS54041, we need to briefly kill the connection
    if is_interface_up("vpn"):
        print("Bringing down AS54041 VPN")
        subprocess.run(["sudo", "wg-quick", "down", "vpn"], check=True)

    # Get the base password
    base_password = get_password("Guru VPN Password", "guru-vpn", "base-password")

    # Fetch the credentials from the Yubikey
    oath_code = get_oath_code("Guru")
    print(f"Using OATH code: {oath_code}")

    # Construct the one-time password
    password = f"{base_password}{oath_code}"

    # Connect via nmcli
    print("Bringing up Guru VPN")
    subprocess.run(
        [
            "nmcli",
            "connection",
            "modify",
            "Guru VPN",
            "vpn.secrets",
            f"password={password}",
        ],
        check=True,
    )
    subprocess.run(["nmcli", "connection", "up", "Guru VPN"], check=True)

    # Bring AS54041 back up
    print("Bringing up AS54041 VPN")
    subprocess.run(["sudo", "wg-quick", "up", "vpn"], check=True)


def main() -> int:
    # Handle program arguments
    ap = argparse.ArgumentParser(
        prog="guru-vpn", description="Utility for connecting to the Guru VPN"
    )
    ap.add_argument("operation", choices=["connect"], help="Operation to perform")
    args = ap.parse_args()

    # Ensure we can actually get credentials from the Yubikey
    if not has_ykman():
        print("Could not execute `ykman`. Is it installed?", file=sys.stderr)
    if not has_yk_plugged_in():
        print("Could not find YubiKey. Is it plugged in?", file=sys.stderr)

    # Handle subcommands
    cmd_fns = {"connect": handle_connect}
    return cmd_fns[args.operation](args)


if __name__ == "__main__":
    sys.exit(main())
