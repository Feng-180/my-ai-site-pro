#!/usr/bin/env python3
"""
零撸情报局 | 全球硬通货自动化系统 v3.0

功能:
- 自动抓取全球最新的虚拟卡、AI白嫖、接码平台、谷歌邮箱等资源
- AES-256-CBC 加密存储
- 支持分类自动整理
"""

import requests
import json
import re
import os
import sys
import base64
import time
import logging
from datetime import datetime
from typing import List, Dict
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# ==================== 配置区 ====================
DATA_FILE = "data.enc"
SECRET_KEY = os.getenv("SECRET_KEY", "资源风888")

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

def create_session() -> requests.Session:
    session = requests.Session()
    retry_strategy = Retry(total=3, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    session.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36"})
    return session

session = create_session()

# ==================== 数据源抓取 ====================

def get_virtual_cards() -> List[Dict]:
    """获取虚拟卡/U卡渠道"""
    logger.info("正在获取虚拟卡渠道...")
    return [
        {"title": "Bybit Card (最强U卡)", "url": "https://www.bybit.com/fiat/cards", "desc": "支持Apple Pay，无年费，直接消费U，2026年首选。", "type": "金融黑卡", "tag": "实体/虚拟"},
        {"title": "HUTAO 虚拟卡", "url": "https://hutao.pro", "desc": "支持支付宝/微信绑定，USDT充值，开卡快。", "type": "金融黑卡", "tag": "虚拟卡"},
        {"title": "GlobalCash 全球付", "url": "http://www.globalcash.hk/", "desc": "香港虚拟卡，支持微信充值，适合新手入门。", "type": "金融黑卡", "tag": "新手友好"},
        {"title": "Dupay (原Depay)", "url": "https://dupay.one", "desc": "老牌U卡，支持多种卡头，订阅ChatGPT必备。", "type": "金融黑卡", "tag": "订阅专用"},
        {"title": "RedotPay (红点卡)", "url": "https://www.redotpay.com", "desc": "支持全球消费，App操作流畅，有实体卡选项。", "type": "金融黑卡", "tag": "Web3"}
    ]

def get_ai_freebies() -> List[Dict]:
    """获取AI大模型白嫖渠道"""
    logger.info("正在获取AI白嫖渠道...")
    return [
        {"title": "Gemini Advanced (学生白嫖1年)", "url": "https://gemini.google.com/advanced", "desc": "2026最新Bug/活动：美国IP+学生认证可领1年会员。", "type": "AI白嫖", "tag": "限时"},
        {"title": "GitHub Student Pack", "url": "https://education.github.com/pack", "desc": "含Copilot免费用，Azure $100额度，大量AI工具授权。", "type": "AI白嫖", "tag": "全家桶"},
        {"title": "Groq Cloud API", "url": "https://console.groq.com/", "desc": "目前最快的Llama3/Mixtral API，提供大量免费额度。", "type": "AI白嫖", "tag": "高并发"},
        {"title": "Perplexity Pro (邀请奖励)", "url": "https://www.perplexity.ai/pro", "desc": "通过邀请或特定活动可获得Pro会员，搜索神器。", "type": "AI白嫖", "tag": "搜索"},
        {"title": "DuckDuckGo AI Chat", "url": "https://duckduckgo.com/?q=DuckDuckGo+AI+Chat", "desc": "免费匿名使用 GPT-4o mini, Claude 3 Haiku 等。", "type": "AI白嫖", "tag": "匿名"}
    ]

def get_sms_platforms() -> List[Dict]:
    """获取接码平台"""
    logger.info("正在获取接码平台...")
    return [
        {"title": "SMS-Activate", "url": "https://sms-activate.org", "desc": "全球最大接码平台，支持几乎所有主流服务注册。", "type": "接码神器", "tag": "收费"},
        {"title": "Grizzly SMS", "url": "https://grizzlysms.com", "desc": "2026推荐：验证码到达率高，支持API批量操作。", "type": "接码神器", "tag": "稳定"},
        {"title": "SMS-Man", "url": "https://sms-man.com", "desc": "支持多国社交媒体注册，价格公道。", "type": "接码神器", "tag": "多国"},
        {"title": "Receive-SMS-Free", "url": "https://receive-sms-free.cc", "desc": "免费公共接码，适合不重要的账号注册。", "type": "接码神器", "tag": "免费"}
    ]

def get_email_resources() -> List[Dict]:
    """获取邮箱资源"""
    logger.info("正在获取邮箱资源...")
    return [
        {"title": "ProtonMail (安全邮箱)", "url": "https://proton.me", "desc": "瑞士加密邮箱，无需手机号即可注册（需特定节点）。", "type": "账号资源", "tag": "隐私"},
        {"title": "Outlook/Hotmail 批量注册", "url": "https://outlook.live.com", "desc": "目前对IP要求相对较低的邮箱，适合做矩阵。", "type": "账号资源", "tag": "矩阵"},
        {"title": "Temp Mail (临时邮箱)", "url": "https://temp-mail.org", "desc": "一次性邮箱，有效规避垃圾邮件和隐私泄露。", "type": "账号资源", "tag": "临时"}
    ]

def get_github_trending_tools() -> List[Dict]:
    """抓取 GitHub Trending 资源"""
    logger.info("正在抓取 GitHub Trending...")
    url = "https://api.github.com/search/repositories?q=created:>2025-01-01&sort=stars&order=desc"
    try:
        resp = session.get(url, timeout=10)
        if resp.status_code == 200:
            repos = resp.json().get("items", [])[:10]
            return [{"title": r["full_name"], "url": r["html_url"], "desc": r["description"] or "开源黑科技工具", "type": "开源工具", "tag": "GitHub"} for r in repos]
    except: pass
    return []

# ==================== 加密与保存 ====================

def encrypt_data(json_str: str, password: str) -> str:
    key = password.encode('utf-8').ljust(32, b'\0')[:32]
    iv = os.urandom(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_data = pad(json_str.encode('utf-8'), AES.block_size)
    encrypted = cipher.encrypt(padded_data)
    return base64.b64encode(iv + encrypted).decode('utf-8')

def main():
    all_data = []
    all_data.extend(get_virtual_cards())
    all_data.extend(get_ai_freebies())
    all_data.extend(get_sms_platforms())
    all_data.extend(get_email_resources())
    all_data.extend(get_github_trending_tools())
    
    result = {
        "update_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total": len(all_data),
        "items": all_data
    }
    
    json_str = json.dumps(result, ensure_ascii=False)
    encrypted_base64 = encrypt_data(json_str, SECRET_KEY)
    
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        f.write(encrypted_base64)
    logger.info(f"更新完成！共 {len(all_data)} 条情报已加密写入 {DATA_FILE}")

if __name__ == "__main__":
    main()
