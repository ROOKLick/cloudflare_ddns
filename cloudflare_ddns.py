import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import psutil
import socket
import requests
import json
import threading
import time

# 全局变量
selected_interface = None
stop_flag = threading.Event()
log_text = None

# 日志记录
def log_message(message):
    if log_text:
        log_text.configure(state="normal")
        log_text.insert(tk.END, f"{message}\n")
        log_text.configure(state="disabled")
        log_text.see(tk.END)
    print(message)

# 获取网络接口信息
def get_network_interfaces():
    interfaces = psutil.net_if_addrs()
    network_info = []
    for iface, addrs in interfaces.items():
        for addr in addrs:
            if addr.family == socket.AF_INET:  # 仅获取 IPv4 地址
                network_info.append({"name": iface, "ip": addr.address})
    return network_info

# 自动获取 Zone ID
def get_zone_id(api_token, domain_name):
    """
    根据域名获取 Zone ID
    """
    try:
        url = "https://api.cloudflare.com/client/v4/zones"
        headers = {"Authorization": f"Bearer {api_token}", "Content-Type": "application/json"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        if data["success"]:
            for zone in data["result"]:
                if zone["name"] == domain_name.split(".", 1)[-1]:  # 匹配根域名
                    log_message(f"自动获取到 Zone ID: {zone['id']} 对应域名: {zone['name']}")
                    entry_zone_id.delete(0, tk.END)
                    entry_zone_id.insert(0, zone["id"])
                    return zone["id"]
            log_message(f"未找到匹配的 Zone ID，请检查域名: {domain_name}")
            return None
        else:
            log_message(f"获取 Zone ID 失败: {data}")
            return None
    except requests.RequestException as e:
        log_message(f"获取 Zone ID 失败: {e}")
        return None

# 获取 DNS 记录 ID
def get_dns_record_id(api_token, zone_id, domain_name):
    """
    获取 DNS 记录 ID
    """
    try:
        url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records?name={domain_name}"
        headers = {"Authorization": f"Bearer {api_token}", "Content-Type": "application/json"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        if data["success"] and data["result"]:
            return data["result"][0]["id"]
        else:
            log_message(f"未找到指定的 DNS 记录: {data}")
            return None
    except requests.RequestException as e:
        log_message(f"获取 DNS 记录 ID 失败: {e}")
        return None

# 更新 Cloudflare DNS 记录
def update_dns_record(api_token, zone_id, record_id, domain_name, ip_address):
    try:
        url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/{record_id}"
        headers = {"Authorization": f"Bearer {api_token}", "Content-Type": "application/json"}
        payload = {
            "type": "A",
            "name": domain_name,
            "content": ip_address,
            "ttl": 1,
            "proxied": False
        }
        response = requests.put(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        data = response.json()
        if data["success"]:
            log_message(f"成功更新 DNS 记录为 IP: {ip_address}")
            return True
        else:
            log_message(f"更新 DNS 记录失败: {data}")
            return False
    except requests.RequestException as e:
        log_message(f"更新 DNS 记录失败: {e}")
        return False

# 自动更新任务
def auto_update_dns(api_token, zone_id, domain_name, interval):
    """
    自动检测 IP 并更新 DNS
    """
    global selected_interface
    last_ip = None
    record_id = get_dns_record_id(api_token, zone_id, domain_name)
    if not record_id:
        log_message("无法获取 DNS 记录 ID，任务退出！")
        return

    while not stop_flag.is_set():
        interfaces = get_network_interfaces()
        for iface in interfaces:
            if iface["name"] == selected_interface:
                current_ip = iface["ip"]
                if current_ip and current_ip != last_ip:
                    log_message(f"检测到新 IP: {current_ip}")
                    if update_dns_record(api_token, zone_id, record_id, domain_name, current_ip):
                        last_ip = current_ip
                break
        time.sleep(interval)

# 手动设置 IP
def manual_update_dns():
    api_token = entry_api_token.get()
    zone_id = entry_zone_id.get()
    domain_name = entry_domain_name.get()
    manual_ip = entry_manual_ip.get()

    if not all([api_token, zone_id, domain_name, manual_ip]):
        messagebox.showwarning("警告", "请填写完整信息和手动 IP 地址！")
        return

    record_id = get_dns_record_id(api_token, zone_id, domain_name)
    if not record_id:
        messagebox.showerror("错误", "无法获取 DNS 记录 ID，请检查配置！")
        return

    if update_dns_record(api_token, zone_id, record_id, domain_name, manual_ip):
        log_message(f"手动更新成功，IP 地址为: {manual_ip}")

# 刷新界面上的网络接口列表
def refresh_interfaces():
    interfaces = get_network_interfaces()
    network_listbox.delete(0, tk.END)
    for iface in interfaces:
        network_listbox.insert(tk.END, f"{iface['name']} - {iface['ip']}")
    if not interfaces:
        messagebox.showinfo("信息", "未检测到任何网络设备！")

def on_select_interface():
    global selected_interface
    selected = network_listbox.curselection()
    if selected:
        index = selected[0]
        iface_name = interfaces[index]["name"]
        selected_interface = iface_name
        messagebox.showinfo("选择的网络设备", f"已选择设备: {iface_name}")
    else:
        messagebox.showwarning("警告", "请先选择一个网络设备！")

def start_monitoring():
    api_token = entry_api_token.get()
    domain_name = entry_domain_name.get()
    interval = int(entry_interval.get())

    if not all([api_token, domain_name, selected_interface]):
        messagebox.showwarning("警告", "请填写完整信息并选择网络设备！")
        return

    zone_id = get_zone_id(api_token, domain_name)  # 自动获取 Zone ID
    if not zone_id:
        messagebox.showerror("错误", "无法自动获取 Zone ID，请检查 API Token 和域名！")
        return

    stop_flag.clear()
    threading.Thread(target=auto_update_dns, args=(api_token, zone_id, domain_name, interval), daemon=True).start()
    log_message("动态更新任务已启动！")

def stop_monitoring():
    stop_flag.set()
    log_message("动态更新任务已停止！")

# 创建主窗口
root = tk.Tk()
root.title("Cloudflare 动态 DNS 更新器")
root.geometry("600x700")

# 配置区域
frame_config = tk.Frame(root, padx=10, pady=10)
frame_config.pack(fill=tk.X)

tk.Label(frame_config, text="API Token:").grid(row=0, column=0, sticky=tk.W)
entry_api_token = tk.Entry(frame_config, width=50)
entry_api_token.grid(row=0, column=1, padx=5)

tk.Label(frame_config, text="域名:").grid(row=1, column=0, sticky=tk.W)
entry_domain_name = tk.Entry(frame_config, width=50)
entry_domain_name.grid(row=1, column=1, padx=5)

tk.Label(frame_config, text="Zone ID:").grid(row=2, column=0, sticky=tk.W)
entry_zone_id = tk.Entry(frame_config, width=50)
entry_zone_id.grid(row=2, column=1, padx=5)

tk.Label(frame_config, text="检测间隔 (秒):").grid(row=3, column=0, sticky=tk.W)
entry_interval = tk.Entry(frame_config, width=10)
entry_interval.grid(row=3, column=1, sticky=tk.W, padx=5)
entry_interval.insert(0, "300")

# 手动设置 IP 区域
frame_manual = tk.Frame(root, padx=10, pady=10)
frame_manual.pack(fill=tk.X)

tk.Label(frame_manual, text="手动设置 IP:").grid(row=0, column=0, sticky=tk.W)
entry_manual_ip = tk.Entry(frame_manual, width=30)
entry_manual_ip.grid(row=0, column=1, padx=5)
btn_manual_update = ttk.Button(frame_manual, text="手动更新", command=manual_update_dns)
btn_manual_update.grid(row=0, column=2, padx=5)

# 网络设备区域
frame_devices = tk.Frame(root, padx=10, pady=10)
frame_devices.pack(fill=tk.BOTH, expand=True)

scrollbar = tk.Scrollbar(frame_devices, orient=tk.VERTICAL)
network_listbox = tk.Listbox(frame_devices, height=10, yscrollcommand=scrollbar.set)
scrollbar.config(command=network_listbox.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
network_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

btn_refresh = ttk.Button(frame_devices, text="刷新列表", command=refresh_interfaces)
btn_refresh.pack(pady=5)

btn_select = ttk.Button(frame_devices, text="选择设备", command=on_select_interface)
btn_select.pack(pady=5)

# 操作按钮
frame_buttons = tk.Frame(root, padx=10, pady=10)
frame_buttons.pack(fill=tk.X)

btn_start = ttk.Button(frame_buttons, text="开始监听", command=start_monitoring)
btn_start.grid(row=0, column=0, padx=5)

btn_stop = ttk.Button(frame_buttons, text="停止监听", command=stop_monitoring)
btn_stop.grid(row=0, column=1, padx=5)

btn_exit = ttk.Button(frame_buttons, text="退出", command=root.destroy)
btn_exit.grid(row=0, column=2, padx=5)

# 日志区域
frame_log = tk.Frame(root, padx=10, pady=10)
frame_log.pack(fill=tk.BOTH, expand=True)

log_text = scrolledtext.ScrolledText(frame_log, state="disabled", wrap=tk.WORD)
log_text.pack(fill=tk.BOTH, expand=True)

# 初始化网络设备列表
interfaces = get_network_interfaces()
refresh_interfaces()

# 运行主循环
root.mainloop()
