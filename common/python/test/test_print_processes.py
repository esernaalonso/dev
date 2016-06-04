import psutil

def print_processes():
    # Iterate over all system processes (ps)
    for proc in psutil.process_iter():
        if "python" in proc.name():
            print proc
            print proc.name()
            print proc.cmdline()


if __name__ == '__main__':
    print_processes()
