from scapy.all import ARP, Ether, srp
import argparse 

def arp_scan(ip_range):
    print(f"[+] Сканирование сети {ip_range}...\n")
    
    arp_request = ARP(pdst=ip_range)
    ether_frame = Ether(dst="ff:ff:ff:ff:ff:ff")
    
    packet = ether_frame/arp_request
    
    result = srp(packet, timeout=2, verbose=False)[0]
    
    devices = []
    
    for sent, received in result:
        devices.append({'ip': received.psrc, 'mac': received.hwsrc})
        
    return devices

def print_result(devices):
    print("IP" + " " * 18 + "MAC-адрес")
    print("-" * 40)
    for device in devices:
        print(f"{device['ip']:20} {device['mac']}")
    print(f"\n[✓] Найдено устройств: {len(devices)}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ARP Scanner — выводит IP и MAC адреса устройств в сети")
    parser.add_argument("-t", "--target", help="Целевая подсеть (например: 192.168.1.1/24)", required=True)

    args = parser.parse_args()
    scanned_devices = arp_scan(args.target)
    print_result(scanned_devices)