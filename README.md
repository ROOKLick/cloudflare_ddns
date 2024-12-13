动态 DNS 更新器 / Dynamic DNS Updater

项目简介 / Project Introduction

动态 DNS 更新器是一款基于 Python 的工具，可自动更新 Cloudflare DNS 记录。通过简单的 GUI 界面，用户可以设置 API Token、域名和检测间隔，实时监控本地网络设备的 IP 地址变化，并将其同步到 Cloudflare 的 DNS 记录。

Dynamic DNS Updater is a Python-based tool for automatically updating Cloudflare DNS records. With a simple GUI interface, users can configure API Token, domain name, and check intervals to monitor local network device IP changes in real-time and sync them to Cloudflare DNS records.

功能特点 / Features

动态 IP 更新 / Dynamic IP Update:
实时监控网络设备的 IP 地址变化，自动更新到 Cloudflare。
Real-time monitoring of network device IP changes and automatic updates to Cloudflare.

手动更新 / Manual Update:
支持用户手动输入 IP 地址并更新到 DNS 记录。
Supports manual input of IP addresses to update DNS records.

易于使用的图形界面 / User-friendly GUI:
提供简单直观的界面，轻松配置和操作。
Provides a simple and intuitive interface for easy configuration and operation.

支持多种网络设备 / Supports Multiple Network Devices:
允许用户选择和管理多个网络接口。
Allows users to select and manage multiple network interfaces.

安装与运行 / Installation and Usage

1. 安装依赖 / Install Dependencies

确保已安装 Python 3.9 或更高版本，并运行以下命令安装必要依赖：
Ensure Python 3.9 or higher is installed, and run the following command to install required dependencies:

pip install psutil requests

2. 运行程序 / Run the Program

运行以下命令启动程序：
Run the following command to start the program:

python your_program.py

3. 打包为可执行文件 / Build Executable

如果需要打包为 .exe 文件，可以使用 PyInstaller：
If you need to build an .exe file, you can use PyInstaller:

pip install pyinstaller
pyinstaller --onefile --noconsole your_program.py

配置说明 / Configuration

必填项 / Required Fields:

API Token:
从 Cloudflare Dashboard 获取 API Token。
Obtain your API Token from the Cloudflare Dashboard.

域名 / Domain Name:
填写需要更新的域名，例如 example.com 或 sub.example.com。
Specify the domain name to update, such as example.com or sub.example.com.

检测间隔 / Check Interval:
设置检测 IP 变化的时间间隔（单位：秒）。
Configure the interval to check for IP changes (in seconds).

开发 / Development

欢迎贡献代码！请按照以下步骤设置开发环境：
Contributions are welcome! Follow these steps to set up the development environment:

克隆仓库 / Clone the repository:

git clone https://github.com/YourGitHubUsername/YourRepositoryName.git
cd YourRepositoryName

安装依赖 / Install dependencies:

pip install -r requirements.txt

运行测试 / Run tests:

python -m unittest discover tests

许可协议 / License

本项目使用 GPL v3 协议。
This project is licensed under the GPL v3 license.

查看完整协议内容 / See the full license text: LICENSE

联系方式 / Contact

如有任何问题，请通过以下方式联系我们：
For any questions, please contact us:

电子邮件 / Email: gudulengshen@126.com

GitHub: ROOKLick

