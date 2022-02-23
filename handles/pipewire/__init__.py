import os, socket


class PipeWire:
    pipewire_socket: socket.socket

    def __init__(self, socket_address=None):
        self.pipewire_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.pipewire_socket.settimeout(20)

        if socket_address is None:
            user_sockets_path = os.environ["XDG_RUNTIME_DIR"] + "/"
            user_sockets_directory = os.listdir(user_sockets_path)

            socket_paths = []

            for user_socket in user_sockets_directory:
                if os.path.isdir(user_sockets_path + user_socket):
                    continue
                elif os.path.isfile(user_sockets_path + user_socket):
                    continue
                elif os.path.islink(user_sockets_path + user_socket):
                    continue
                socket_paths.append(user_sockets_path + user_socket)

            del user_socket, user_sockets_directory

            pipewire_sockets = []

            for socket_path in socket_paths:
                if socket_path.__contains__("pipewire"):
                    pipewire_sockets.append(socket_path)

            del socket_path, socket_paths

            pipewire_sockets_living = []

            for pipewire_socket in pipewire_sockets:
                if os.path.exists(pipewire_socket + ".lock"):
                    pipewire_sockets_living.append(pipewire_socket)

            del pipewire_socket, pipewire_sockets

            del user_sockets_path

            selected = 1
            if pipewire_sockets_living.__len__() > 1:
                print("Select pipewire service socket:")
                count = 1
                for pipewire_living_socket in pipewire_sockets_living:
                    print(f"    {count}: {pipewire_living_socket}")
                    count += 1

                try:
                    selected = input("\nChoice [1]:")
                    if not selected == "":
                        try:
                            selected = int(selected)
                        except Exception as x:
                            print(x)
                            pass
                except EOFError:
                    pass

            socket_address = pipewire_sockets_living[selected - 1]

            del selected, pipewire_sockets_living

        self.pipewire_socket.connect(socket_address)
        self.pipewire_socket.settimeout(20)

    def send_control_message(self, message):
        self.pipewire_socket.send(message)

    def receive_control_message(self):
        return self.pipewire_socket.recvmsg(65565)

    def __del__(self):
        self.pipewire_socket.close()
