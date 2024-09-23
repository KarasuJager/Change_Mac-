import os
import random
import re
import subprocess

def get_interfaces():
    """Obtiene una lista de interfaces de red disponibles."""
    result = subprocess.run(["ifconfig"], capture_output=True, text=True)
    interfaces = re.findall(r'^(\w+): flags', result.stdout, re.MULTILINE)
    return interfaces

def get_random_mac():
    """Genera una dirección MAC aleatoria."""
    mac = [0x00, 0x16, 0x3E,  # Prefijo válido para máquinas virtuales
           random.randint(0x00, 0x7F),
           random.randint(0x00, 0xFF),
           random.randint(0x00, 0xFF)]
    return ':'.join(map(lambda x: "%02x" % x, mac))

def change_mac(interface, new_mac):
    """Cambia la dirección MAC de una interfaz de red."""
    print(f"[+] Cambiando MAC de {interface} a {new_mac}...")
    os.system(f"sudo ifconfig {interface} down")
    os.system(f"sudo ifconfig {interface} hw ether {new_mac}")
    os.system(f"sudo ifconfig {interface} up")

def get_current_mac(interface):
    """Obtiene la dirección MAC actual de la interfaz de red."""
    result = subprocess.run(["ifconfig", interface], capture_output=True, text=True)
    match = re.search(r"ether (\w\w:\w\w:\w\w:\w\w:\w\w:\w\w)", result.stdout)
    if match:
        return match.group(1)
    else:
        return None

def choose_interface(interfaces):
    """Permite al usuario seleccionar una interfaz de red."""
    print("Interfaces de red disponibles:")
    for idx, iface in enumerate(interfaces):
        print(f"{idx + 1}. {iface}")
    
    choice = input("Selecciona el número de la interfaz que deseas usar: ")
    return interfaces[int(choice) - 1]

if __name__ == "__main__":
    interfaces = get_interfaces()
    
    if not interfaces:
        print("[-] No se encontraron interfaces de red.")
        exit()

    # Seleccionar la interfaz
    interface = choose_interface(interfaces)

    current_mac = get_current_mac(interface)
    print(f"[+] Dirección MAC actual de {interface}: {current_mac}")
    
    new_mac = get_random_mac()
    print(f"[+] Generando nueva dirección MAC: {new_mac}")
    
    change_mac(interface, new_mac)
    
    updated_mac = get_current_mac(interface)
    if updated_mac == new_mac:
        print(f"[+] Dirección MAC de {interface} cambiada exitosamente a {updated_mac}")
    else:
        print(f"[-] No se pudo cambiar la dirección MAC de {interface}.")
