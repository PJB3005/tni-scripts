#!/usr/bin/env python3

import argparse

def main() -> int:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    parser_switch = subparsers.add_parser("switch")
    parser_switch.set_defaults(func=cmd_switch)
    parser_switch.add_argument("addr")
    parser_switch.add_argument("ports")
    parser_switch.add_argument("--trunk")

    parser_router = subparsers.add_parser("router")
    parser_router.set_defaults(func=cmd_router)
    parser_router.add_argument("addr")
    parser_router.add_argument("ports")
    parser_router.add_argument("trunk")

    args = parser.parse_args()
    return args.func(args) or 0

def cmd_switch(args: argparse.Namespace):
    ports = parse_ports(args.ports)
    for port in ports:
        print(f"vlan tag port{port} with #{port} on {args.addr}; ", end="")

    if trunk := args.trunk:
        all_vlans = ' '.join(map(lambda p: f"#{p}", ports))
        print(f"vlan tag port{trunk} with {all_vlans} on {args.addr}; ", end="")

def cmd_router(args: argparse.Namespace):
    trunk = int(args.trunk)

    ports = parse_ports(args.ports)
    all_vlans = ' '.join(map(lambda p: f"#{p}", ports))
    print(f"vlan tag port{trunk} with {all_vlans} on {args.addr}; ", end="")

    for port in ports:
        print(f"vlan tag port{trunk}.{port + 1} with #{port} on {args.addr}; ", end="")

def parse_ports(arg: str) -> set[int]:
    arg = arg.strip()

    l: set[int] = set()

    for r in arg.split(","):
        bounds = r.split("-")
        match len(bounds):
            case 1:
                l.add(int(r))
            case 2:
                [start, end] = bounds
                l.update(range(int(start), int(end)))

    return l

if __name__ == "__main__":
    exit(main())
