Установите необходимые зависимости:

sudo apt-get install -y libxtables12 libxtables-dev
Скачайте исходный код pyiptables:

git clone https://github.com/ldx/python-iptables.git
Перейдите в каталог python-iptables:

cd python-iptables
Установите pyiptables:

sudo python3 setup.py install
Обратите внимание, что используется python3, а не pip3.

После выполнения этих шагов pyiptables должен быть успешно