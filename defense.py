import subprocess

def add_iptables_rule(rule):
    command = ['iptables', '-A', 'INPUT'] + rule.split()
    subprocess.run(command, check=True)

# Пример правила для блокировки трафика с определенного IP-адреса
def block_ip(ip):
    rule = f'-s {ip} -j DROP'
    add_iptables_rule(rule)
    a = subprocess.check_output(['iptables-save'])
    return a

