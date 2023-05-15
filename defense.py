import subprocess
import time

def add_iptables_rule(rule):
    command = ['iptables', '-A', 'INPUT'] + rule.split()
    subprocess.run(command, check=True)

# Пример правила для блокировки трафика с определенного IP-адреса
def block_ip(ip):
    rule = f'-s {ip} -j DROP'
    add_iptables_rule(rule)


def block_protocol(protocol, duration):
    # Получаем текущую дату и время
    current_time = time.strftime('%Y-%m-%d %H:%M:%S')

    # Создаем временное имя цепочки для блокировки
    chain_name = f"BLOCK_{protocol.upper()}_{current_time}"

    try:
        # Создаем временную цепочку
        create_chain_cmd = ['iptables', '-N', chain_name]
        subprocess.run(create_chain_cmd, check=True)

        # Добавляем правило для блокировки протокола во временную цепочку
        block_protocol_cmd = ['iptables', '-A', chain_name, '-p', protocol.upper(), '-j', 'DROP']
        subprocess.run(block_protocol_cmd, check=True)

        # Добавляем правило перенаправления во временную цепочку
        redirect_cmd = ['iptables', '-I', 'INPUT', '-p', protocol.upper(), '-j', chain_name]
        subprocess.run(redirect_cmd, check=True)

        # Ожидаем указанное время
        time.sleep(duration)

    finally:
        # Удаляем правило перенаправления
        delete_redirect_cmd = ['iptables', '-D', 'INPUT', '-p', protocol.upper(), '-j', chain_name]
        subprocess.run(delete_redirect_cmd, check=True)

        # Удаляем правило блокировки
        delete_block_cmd = ['iptables', '-F', chain_name]
        subprocess.run(delete_block_cmd, check=True)

        # Удаляем временную цепочку
        delete_chain_cmd = ['iptables', '-X', chain_name]
        subprocess.run(delete_chain_cmd, check=True)

# Пример использования: блокировка протокола ICMP на 60 секунд
block_protocol('icmp', 60)