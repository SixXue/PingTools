import tkinter as tk
import subprocess
import datetime
import threading
import time
#import psutil
import os
class PingUtility:
    def __init__(self, ip_address, interval, packet_size, count, timeout=2):
        self.ip_address = ip_address
        self.interval = interval
        self.packet_size = packet_size
        self.count = count + 2
        self.timeout = timeout
        self.process = None
        self.running = False
        self.counter = 0
        self.continuous_ping = False
        self.save_to_file = False

    def start_ping(self):
        if self.running:
            print("已经在进行 ping 了")
            return
        self.running = True
        self.thread = threading.Thread(target=self.ping_thread)
        self.thread.start()

    def ping_thread(self):
        while self.running:
            print(continuous_ping_var.get())
            continuous_ping = continuous_ping_var.get()
            if continuous_ping == True:
                command = ['ping', '-t', '-l', str(self.packet_size), '-w', str(self.timeout), self.ip_address]
                print('执行一直ping操作')
            else:
                command = ['ping', '-n', str(self.count), '-l', str(self.packet_size), '-w', str(self.timeout), self.ip_address]
                print('未执行一直ping操作')
            self.process = subprocess.Popen(command, stdout=subprocess.PIPE, universal_newlines=True,creationflags=subprocess.CREATE_NO_WINDOW)
            self.read_output()

            if not self.continuous_ping:
                break

            time.sleep(self.interval)

    def read_output(self):
        line_count = 0
        file_output = ""

        for line in self.process.stdout:
            timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            output = f"{timestamp} - {line.strip()}\n"
            update_debug_text(output)

            if self.save_to_file:
                file_output += output

            continuous_ping = continuous_ping_var.get()
            print(continuous_ping)
            if continuous_ping == True:
                line_count -= 1
            else:
                line_count += 1

            if line_count >= self.count:
                break

            self.counter += 1
            if self.counter >= self.count and not self.continuous_ping:
                self.stop_ping()
                break

            if not self.running:
                break

        self.process.stdout.close()

        if self.save_to_file:
            save_output_to_file(file_output)

        self.running = False

    def stop_ping(self):
        if self.running:
            self.process.kill()
            self.running = False
            print("Ping 已停止")

        else:
            print("没有进行 ping")

    #def terminate_child_processes(self):
    #    current_process = psutil.Process()
    #    children = current_process.children(recursive=True)
#
    #    for child in children:
    #        child.terminate()
#
    #    psutil.wait_procs(children, timeout=5)
#
    #    # 终止当前进程
    #    current_process.terminate()
    #    current_process.wait(5)


def start_ping_handler():
    global ping_utility

    if ping_utility is None:
        ping_utility = PingUtility(ip_entry.get(), int(frequency_entry.get()), int(package_entry.get()), int(count_entry.get()))
        ping_utility.continuous_ping = continuous_ping_var.get()
        ping_utility.save_to_file = save_to_file_var.get()
        ping_utility.start_ping()

def stop_ping_handler():
    global ping_utility

    if ping_utility is not None:
        ping_utility.stop_ping()
        ping_utility = None

def update_debug_text(text):
    debug_text.insert(tk.END, text)
    debug_text.see(tk.END)

def save_output_to_file(file_output):
    with open(f"ping{ip_entry.get()}.txt", "w",encoding="UTF-8") as file:
        file.write(file_output)

window = tk.Tk()
window.title("Ping Tools")
window.geometry("600x425")
window.resizable(False, False)

ip_label = tk.Label(window, text="IP地址:", pady=5, padx=20)
ip_label.grid(row=0, column=0, sticky="N")
ip_entry = tk.Entry(window)
ip_entry.insert(0, "10.49.233.254")
ip_entry.grid(row=0, column=1, sticky="W")

frequency_label = tk.Label(window, text="Ping间隔（毫秒）：")
frequency_label.grid(row=1, column=0, sticky="N")
frequency_entry = tk.Entry(window)
frequency_entry.insert(0, 1000)
frequency_entry.grid(row=1, column=1, sticky="W")

package_label = tk.Label(window, text="Ping字节大小:")
package_label.grid(row=2, column=0, sticky="N")
package_entry = tk.Entry(window)
package_entry.insert(0, 500)
package_entry.grid(row=2, column=1, sticky="W")

count_label = tk.Label(window, text="Ping次数：", pady=5, padx=20)
count_label.grid(row=3, column=0, sticky="N")
count_entry = tk.Entry(window)
count_entry.insert(0, 5)
count_entry.grid(row=3, column=1, sticky="W")

continuous_ping_var = tk.BooleanVar()
continuous_ping_var.set(True)
continuous_ping_cb = tk.Checkbutton(window, text="一直 ping", variable=continuous_ping_var)
continuous_ping_cb.grid(row=4, column=0, sticky="W")

save_to_file_var = tk.BooleanVar()
save_to_file_var.set(1)
save_to_file_cb = tk.Checkbutton(window, text="保存输出到文件", variable=save_to_file_var)
save_to_file_cb.grid(row=4, column=1, sticky="W")

ping_utility = None

start_button = tk.Button(window, text="开始", command=start_ping_handler)
start_button.grid(row=0, column=2)

stop_button = tk.Button(window, text="停止", command=stop_ping_handler)
stop_button.grid(row=1, column=2)

debug_label = tk.Label(window, text="信息")
debug_label.grid(row=5, column=0, columnspan=2)

debug_text = tk.Text(window, borderwidth=3, height=18)
debug_text.grid(row=6, column=0, rowspan=4, padx=7, pady=5, columnspan=3)

scrollbar = tk.Scrollbar(window)
scrollbar.grid(row=6, column=3, rowspan=4, sticky='ns', pady=5)

debug_text.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=debug_text.yview)

def close_window():
    # 终止所有进程
    os._exit(0)
window.protocol("WM_DELETE_WINDOW", close_window)

window.mainloop()

