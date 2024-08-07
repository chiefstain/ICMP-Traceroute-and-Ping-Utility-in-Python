from icmp_helper_library import IcmpHelperLibrary


def main():
    icmp_helper = IcmpHelperLibrary()

    # Testing ping
    print("Testing ping:")
    icmp_helper._sendIcmpEchoRequest("8.8.8.8")  # Google's public DNS

    # Testing traceroute
    print("Testing traceroute:")
    icmp_helper.traceRoute("8.8.8.8")  # Google's public DNS


if __name__ == "__main__":
    main()
