from tello import Tello

file_name = sys.argv[1]

with open(file_name, 'r') as f:
    commands = f.readlines()

t1 = Tello(tello_ip='192.168.199.3')

for command in commands:
    command = command.strip()
    if '#' in command:
        index = command.index('#')
        command = command[0:index].strip()
        if not command:
            continue

    if command:
        t1.send_command(command)

print('process completed!')
