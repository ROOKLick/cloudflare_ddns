# 动态 DNS 更新器 / Dynamic DNS Updater

## 项目简介 / Project Introduction

动态 DNS 更新器是一款基于 Python 的工具，可自动更新 Cloudflare DNS 记录。通过简单的 GUI 界面，用户可以设置 API Token、域名和检测间隔，实时监控本地网络设备的 IP 地址变化，并将其同步到 Cloudflare 的 DNS 记录。

Dynamic DNS Updater is a Python-based tool for automatically updating Cloudflare DNS records. With a simple GUI interface, users can configure API Token, domain name, and check intervals to monitor local network device IP changes in real-time and sync them to Cloudflare DNS records.

---

## 功能特点 / Features

- **动态 IP 更新 / Dynamic IP Update**:
  实时监控网络设备的 IP 地址变化，自动更新到 Cloudflare。
  Real-time monitoring of network device IP changes and automatic updates to Cloudflare.

- **手动更新 / Manual Update**:
  支持用户手动输入 IP 地址并更新到 DNS 记录。
  Supports manual input of IP addresses to update DNS records.

- **易于使用的图形界面 / User-friendly GUI**:
  提供简单直观的界面，轻松配置和操作。
  Provides a simple and intuitive interface for easy configuration and operation.

- **支持多种网络设备 / Supports Multiple Network Devices**:
  允许用户选择和管理多个网络接口。
  Allows users to select and manage multiple network interfaces.

---

## 安装与运行 / Installation and Usage

### 1. 安装依赖 / Install Dependencies

确保已安装 Python 3.9 或更高版本，并运行以下命令安装必要依赖：
Ensure Python 3.9 or higher is installed, and run the following command to install required dependencies:
```bash
pip install psutil requests
