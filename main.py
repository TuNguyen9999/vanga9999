"""
Stock News Bot - Bot tự động thu thập và gửi tin tức chứng khoán
Tuân thủ chuẩn PTB 20.7
"""

import asyncio
import os
import re
import ssl
import signal
import sys
import threading
import time
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Dict, List, Optional, Set, Tuple

import httpx
import schedule
import smtplib
from bs4 import BeautifulSoup
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# ================== CẤU HÌNH ==================
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "7200591128:AAFtBUbfLpp-OoI9II9hQArMTZFwelTT6_Y")

# ================== CẤU HÌNH EMAIL ==================
EMAIL_SENDER = os.getenv("EMAIL_SENDER", "vcamnews@gmail.com")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "dsel ocad nqqj hdxy")
EMAIL_RECIPIENT = os.getenv("EMAIL_RECIPIENT", "tunguyen3214@gmail.com")
VIETCAPITAL_EMAILS_STR = os.getenv("VIETCAPITAL_EMAILS", "tu.nguyen@vietcapital.com.vn")
VIETCAPITAL_EMAILS = [email.strip() for email in VIETCAPITAL_EMAILS_STR.split(",") if email.strip()]
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465

# Khởi tạo Flask app để tạo web server
app = Flask(__name__)

# ================== DANH SÁCH MÃ CỔ PHIẾU ==================
TICKER_COMPANY_MAP: Dict[str, List[str]] = {
    # ============== Cổ phiếu VN30 ==============
    "ACB": ["NGÂN HÀNG TMCP Á CHÂU"],
    "BCM": ["BECAMEX", "TỔNG CÔNG TY ĐẦU TƯ VÀ PHÁT TRIỂN CÔNG NGHIỆP"],
    "BID": ["BIDV", "NGÂN HÀNG ĐẦU TƯ VÀ PHÁT TRIỂN VIỆT NAM"],
    "BVH": ["BẢO VIỆT"],
    "CTG": ["VIETINBANK", "NGÂN HÀNG CÔNG THƯƠNG VIỆT NAM"],
    "FPT": ["FPT Corp", "CÔNG TY CỔ PHẦN FPT", "CTCP FPT"],
    "GAS": ["PVGAS", "TỔNG CÔNG TY KHÍ VIỆT NAM"],
    "GVR": ["TẬP ĐOÀN CÔNG NGHIỆP CAO SU VIỆT NAM", "CAO SU VIỆT NAM"],
    "HDB": ["HDBANK", "NGÂN HÀNG PHÁT TRIỂN THÀNH PHỐ HỒ CHÍ MINH"],
    "HPG": ["TẬP ĐOÀN HÒA PHÁT", "HÒA PHÁT"],
    "MBB": ["MBBANK", "NGÂN HÀNG QUÂN ĐỘI"],
    "MSN": ["MASAN", "TẬP ĐOÀN MASAN"],
    "MWG": ["THẾ GIỚI DI ĐỘNG", "MOBILE WORLD"],
    "PLX": ["PETROLIMEX", "TẬP ĐOÀN XĂNG DẦU VIỆT NAM"],
    "POW": ["PV POWER", "TỔNG CÔNG TY ĐIỆN LỰC DẦU KHÍ VIỆT NAM"],
    "SAB": ["SABECO", "TỔNG CÔNG TY BIA - RƯỢU - NƯỚC GIẢI KHÁT SÀI GÒN"],
    "SHB": ["NGÂN HÀNG SÀI GÒN - HÀ NỘI"],
    "SSB": ["SEABANK", "NGÂN HÀNG ĐÔNG NAM Á"],
    "SSI": ["CHỨNG KHOÁN SSI", "CÔNG TY CỔ PHẦN CHỨNG KHOÁN SSI"],
    "STB": ["SACOMBANK", "NGÂN HÀNG SÀI GÒN THƯƠNG TÍN"],
    "TCB": ["TECHCOMBANK", "NGÂN HÀNG KỸ THƯƠNG VIỆT NAM"],
    "TPB": ["TPBANK", "NGÂN HÀNG TIÊN PHONG"],
    "VCB": ["VIETCOMBANK", "NGÂN HÀNG NGOẠI THƯƠNG VIỆT NAM"],
    "VHM": ["VINHOMES", "CÔNG TY CỔ PHẦN VINHOMES"],
    "VIB": ["NGÂN HÀNG QUỐC TẾ VIỆT NAM"],
    "VIC": ["VINGROUP", "TẬP ĐOÀN VINGROUP"],
    "VJC": ["VIETJET AIR", "CÔNG TY CỔ PHẦN HÀNG KHÔNG VIETJET"],
    "VNM": ["VINAMILK", "CÔNG TY CỔ PHẦN SỮA VIỆT NAM"],
    "VPB": ["VPBANK", "NGÂN HÀNG VIỆT NAM THỊNH VƯỢNG"],
    "VRE": ["VINCOM RETAIL", "CÔNG TY CỔ PHẦN VINCOM RETAIL"],
    "CEO": ["CEO GROUP", "TẬP ĐOÀN CEO"],
    "CTD": ["COTECCONS", "CÔNG TY CỔ PHẦN XÂY DỰNG COTECCONS"],
    "AGG": ["AN GIA"],
    "ANV": ["NAM VIỆT"],
    "ASM": ["SAO MAI GROUP", "TẬP ĐOÀN SAO MAI"],
    "BCG": ["BAMBOO CAPITAL", "BAMBOO"],
    "BMP": ["NHỰA BÌNH MINH"],
    "BSI": ["CHỨNG KHOÁN BIDV"],
    "BWE": ["NƯỚC BÌNH DƯƠNG", "BIWASE"],
    "CII": ["ĐẦU TƯ HẠ TẦNG KỸ THUẬT"],
    "CMG": ["CMC GROUP", "TẬP ĐOÀN CMC"],
    "CTR": ["CÔNG TRÌNH VIETTEL", "VIETTEL CONSTRUCTION", "VIETTEL"],
    "DBC": ["DABACO"],
    "DCM": ["ĐẠM CÀ MAU"],
    "DGC": ["ĐỨC GIANG"],
    "DGW": ["DIGIWORLD"],
    "DHC": ["ĐÔNG HẢI BẾN TRE"],
    "DIG": ["DIC CORP"],
    "DPM": ["ĐẠM PHÚ MỸ"],
    "DXG": ["ĐẤT XANH"],
    "DXS": ["ĐẤT XANH"],
    "EIB": ["EXIMBANK"],
    "FRT": ["FRT RETAIL"],
    "FTS": ["CHỨNG KHOÁN FPT"],
    "GEX": ["GELEX"],
    "GMD": ["GEMADEPT"],
    "HCM": ["CHỨNG KHOÁN HSC"],
    "HDC": ["PHÁT TRIỂN NHÀ BÀ RỊA VŨNG TÀU"],
    "HDG": ["HÀ ĐÔ"],
    "HHV": ["ĐÈO CẢ"],
    "HSG": ["HOA SEN"],
    "KBC": ["KINH BẮC"],
    "KDH": ["KHANG ĐIỀN"],
    "LPB": ["LỘC PHÁT"],
    "MSB": ["HÀNG HẢI"],
    "NKG": ["THÉP NAM KIM"],
    "NLG": ["NAM LONG"],
    "NT2": ["NHƠN TRẠCH"],
    "NVL": ["NOVALAND"],
    "OCB": ["PHƯƠNG ĐÔNG"],
    "PAN": ["TẬP ĐOÀN PAN"],
    "PC1": ["TẬP ĐOÀN PC1"],
    "PDR": ["PHÁT ĐẠT"],
    "PHR": ["PHƯỚC HÒA"],
    "PNJ": ["CỔ PHIẾU PNJ"],
    "PPC": ["NHIỆT ĐIỆN PHẢ LẠI"],
    "PTB": ["PHÚ TÀI"],
    "PVD": ["PV DRILLING"],
    "PVT": ["PV TRANS"],
    "REE": ["CƠ ĐIỆN LẠNH REE", "CỔ PHIẾU REE"],
    "SCR": ["ĐỊA ỐC SÀI GÒN THƯƠNG TÍN", "TTC LAND"],
    "SCS": ["DỊCH VỤ HÀNG HÓA SÀI GÒN"],
    "SJS": ["SÔNG ĐÀ SUDICO"],
    "SZC": ["SONADEZI CHÂU ĐỨC"],
    "TCH": ["HOÀNG HUY"],
    "TMS": ["TRANSIMEX"],
    "VCG": ["VINACONEX"],
    "VCI": ["CHỨNG KHOÁN BẢN VIỆT", "VIETCAPITAL"],
    "VHC": ["VĨNH HOÀN"],
    "VIX": ["CHỨNG KHOÁN VIX"],
    "VND": ["VNDIRECT"],
    "TLG": ["THIÊN LONG"],
    "VTO": ["VITACO"],
    "VIP": ["VIPCO"],
    "MSH": ["MAY SÔNG HỒNG"],
    "TNG": ["DỆT MAY"],
    "DHG": ["DƯỢC HẬU GIANG"],
    "FOX": ["VIỄN THÔNG FPT"],
    "VGS": ["VIỆT ĐỨC"],
    "TTN": ["TTN"],
    "HVN": ["VIETNAM AIRLINES"],
    "HAH": ["HẢI AN"],
    "NTL": ["TỪ LIÊM"],
    "KHG": ["KHẢI HOÀN"],
    "LGL": ["LONG GIANG"],
    "CKG": ["KIÊN GIANG"],
    "HVH": ["HVC GROUP"],
    "EVF": ["TÀI CHÍNH ĐIỆN LỰC"],
    "CSV": ["HOÁ CHẤT"],
    "IDC": ["IDICO"],
    "NTC": ["NAM TÂN UYÊN"],
    "LHG": ["LONG HẬU"],
    "DTD": ["THÀNH ĐẠT"],
    "D2D": ["CÔNG NGHIỆP SỐ 2"],
    "DPR": ["CAO SU ĐỒNG PHÚ"],
    "VGC": ["VIGLACERA"],
    "SIP": ["SÀI GÒN VRG"],
    "TRC": ["CAO SU TÂY NINH"],
    "PVS": ["KĨ THUẬT DẦU KHÍ"],
    "VTP": ["VIETTEL POST"],
    "QTP": ["NHIỆT ĐIỆN QUẢNG NINH"],
    "STK": ["SỢI THẾ KỶ"],
    "TCM": ["THÀNH CÔNG"],
    "GIL": ["GILIMEX, XUẤT NHẬP KHẨU BÌNH THẠNH"],
    "VGT": ["DỆT MAY VIỆT NAM"],
    "ADS": ["DAMSAN"],
    "PET": ["PETROSETCO"],
    "MCH": ["MASAN CONSUMER"],
    "LCG": ["LIZEN"],
    "C4G": ["CIENCO4"],
    "HBC": ["HÒA BÌNH"],
    "FCN": ["FECON"],
    "PLC": ["HÓA DẦU PETROLIMEX"],
    "HT1": ["XI MĂNG HÀ TIÊN 1"],
    "KSB": ["KHOÁNG SẢN"],
    "DPG": ["ĐẠT PHƯƠNG"],
    "DHA": ["HOÁ AN"],
    "CTI": ["CƯỜNG THUẬN IDICO"],
    "TV2": ["TƯ VẤN XÂY DỰNG ĐIỆN 2"],
    "DRC": ["CAO SU ĐÀ NẴNG"],
    "DRI": ["CAO SU ĐẮK LẮK"],
    "HAX": ["HAXACO"],
    "VEA": ["VEAM"],
    "CSM": ["CAO SU MIỀN NAM"],
    "ACV": ["CẢNG HÀNG KHÔNG"],
    "SAS": ["SASCO"],
    "NCS": ["SUẤT ĂN HÀNG KHÔNG NỘI BÀI"],
    "SGN": ["PHỤC VỤ MẶT ĐẤT SÀI GÒN"],
    "NCT": ["DỊCH VỤ HÀNG HÓA NỘI BÀI"],
    "QNS": ["ĐƯỜNG QUẢNG NGÃI"],
    "SLS": ["MÍA ĐƯỜNG SƠN LA"],
    "IJC": ["BECAMEX IJC"],
    "TDC": ["BECAMEX TDC"],
    "NAF": ["NAFOOD"],
    "MIG": ["BẢO HIỂM QUÂN ĐỘI"],
    "PVI": ["BẢO HIỂM PVI"],
    "GEG": ["ĐIỆN GIA LAI"],
    "GEE": ["GELEX"],
    "NTP": ["NHỰA THIẾU NIÊN TIỀN PHONG"],
    "DDV": ["DAP VINACHEM"],
    "ACG": ["GỖ AN CƯỜNG"],
    "VCS": ["VICOSTONE"],
    "VLB": ["VẬT LIỆU XÂY DỰNG"],
    "THG": ["TIỀN GIANG"],
    "FMC": ["SAO TA"],
    "MPC": ["MINH PHÚ"],
    "CMX": ["CAMIMEX"],
    "IMP": ["IMEXPHARM"],
    "DBD": ["DƯỢC BÌNH ĐỊNH"],
    "DVM": ["VIETMEC"],
    "PVC": ["DẦU KHÍ"],
    "PVB": ["BỌC ỐNG"],
    "BSR": ["BÌNH SƠN"],
    "OIL": ["TỔNG CÔNG TY DẦU VIỆT NAM"],
    "BFC": ["BÌNH ĐIỀN"],
    "LAS": ["LÂM THAO"],
    "BAF": ["BAF VIỆT NAM"],
    "HAG": ["HOÀNG ANH GIA LAI"],
    "VLC": ["VILICO"],
    "ITC": ["ĐẦU TƯ KINH DOANH NHÀ"],
    "VFG": ["KHỬ TRÙNG"],
    "VGI": ["VIETTEL GLOBAL"],
    "ELC": ["ELCOM"],
    "FOC": ["FPT ONLINE"],
    "KSV": ["KHOÁNG SẢN VIỆT NAM"]
}

# ================== BIẾN GLOBAL ==================
app_instance: Optional[Application] = None

def cleanup_old_instances() -> None:
    """
    Dọn dẹp các instance cũ và đảm bảo chỉ có một instance chạy.
    """
    global app_instance
    if app_instance:
        try:
            app_instance.stop()
            app_instance.shutdown()
        except Exception as e:
            print(f"⚠️ Lỗi khi dọn dẹp instance cũ: {e}")
        finally:
            app_instance = None

def check_telegram_connection() -> bool:
    """
    Kiểm tra kết nối đến Telegram API.
    """
    try:
        import requests
        response = requests.get(f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getMe", timeout=10)
        if response.status_code == 200:
            print("✅ Kết nối Telegram API thành công")
            return True
        else:
            print(f"❌ Lỗi kết nối Telegram API: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Không thể kết nối Telegram API: {e}")
        return False

def restart_polling() -> None:
    """
    Khởi động lại polling nếu gặp lỗi.
    """
    global app_instance
    if app_instance:
        try:
            print("🔄 Đang khởi động lại polling...")
            app_instance.run_polling(
                allowed_updates=Update.ALL_TYPES,
                drop_pending_updates=True,
                close_loop=False,
                stop_signals=None
            )
        except Exception as e:
            print(f"❌ Lỗi khi khởi động lại polling: {e}")
            # Thử lại sau 5 giây
            time.sleep(5)
            restart_polling()

def signal_handler(signum, frame):
    """
    Xử lý signal để tắt bot một cách an toàn.
    """
    print(f"\n🛑 Nhận signal {signum}, đang tắt bot...")
    cleanup_old_instances()
    sys.exit(0)

# ================== URL CẦN CRAWL ==================
urls_to_crawl: List[str] = [
    "https://cafef.vn/thi-truong-chung-khoan.chn",  # Thị trường chứng khoán
    "https://cafef.vn/doanh-nghiep.chn",  # Doanh nghiệp
    "https://cafef.vn/tai-chinh-ngan-hang.chn",  # Tài chính - Ngân hàng
    "https://cafef.vn/bat-dong-san.chn",  # Bất động sản
    "https://vietnambiz.vn/doanh-nghiep.htm",
    "https://vietnambiz.vn/chung-khoan.htm",
    "https://vietnambiz.vn/tai-chinh.htm",
    "https://www.tinnhanhchungkhoan.vn/doanh-nghiep/", # Thêm trang mới
    "https://www.tinnhanhchungkhoan.vn/chung-khoan/",   # Thêm trang mới
    "https://www.tinnhanhchungkhoan.vn/bat-dong-san/",      # Thêm trang mới
    "https://www.tinnhanhchungkhoan.vn/tai-chinh/"      # Thêm trang mới
]


def check_stock_and_company_in_soup(
    soup: BeautifulSoup, 
    ticker_company_map: Dict[str, List[str]], 
    site_name: str
) -> Optional[str]:
    """
    Kiểm tra đồng thời mã cổ phiếu và tên công ty trong nội dung bài viết.
    
    Args:
        soup: BeautifulSoup object của trang web
        ticker_company_map: Dictionary mapping mã cổ phiếu với tên công ty
        site_name: Tên trang web (cafef, vietnambiz, tinnhanhchungkhoan)
        
    Returns:
        Mã cổ phiếu nếu tìm thấy cả hai, None nếu không tìm thấy
    """
    # Cải tiến: Sử dụng selectors riêng cho từng trang
    content_selectors = {
        "cafef": [
            ".detail-content", ".detail-content-body", ".news-content",
            "article", ".content-detail", "#mainContent"
        ],
        "vietnambiz": [
            ".article-content", "article.content", ".content-detail",
            "#mainContent", ".journal-content-article",
            "body"  # Phương án cuối cùng: quét toàn bộ trang
        ],
        "tinnhanhchungkhoan": [
            "article.story .body",
            "article.story", 
            ".article-body", 
            ".article__body", 
            "article .article-body", 
            "#mainContent .article-body"
        ]
    }

    selectors_to_use = content_selectors.get(site_name)
    # Nếu site_name không hợp lệ, trả về None để tránh lỗi
    if not selectors_to_use:
        return None

    for selector in selectors_to_use:
        content_element = soup.select_one(selector)
        if content_element:
            content_upper = content_element.get_text().upper()

            for ticker, company_names in ticker_company_map.items():
                ticker_upper = ticker.upper()

                # 1. Kiểm tra sự xuất hiện của mã cổ phiếu (ticker)
                ticker_found = False
                ticker_patterns = [
                    f"\\(Mã:\\s*{ticker_upper}\\)",  # Dạng (Mã: HUT)
                    f"\\({ticker_upper}\\)",  # Dạng (HUT)
                    f"\\[{ticker_upper}\\]",  # Dạng [HUT]
                    f"\\s{ticker_upper}\\s",  # Dạng " HUT " (có khoảng trắng bao quanh)
                    f":\\s*{ticker_upper}\\b",
                    f":{ticker_upper}\\b",
                    f"MÃ:\\s*{ticker_upper}\\b",
                    f"MÃ\\s+{ticker_upper}\\b",
                ]
                for pattern in ticker_patterns:
                    if re.search(pattern, content_upper):
                        ticker_found = True
                        break

                # 2. Nếu tìm thấy ticker, kiểm tra tiếp tên công ty
                if ticker_found:
                    for company_name in company_names:
                        # Tìm kiếm tên công ty một cách đơn giản, không cần regex phức tạp
                        if company_name.upper() in content_upper:
                            return ticker  # Trả về ticker nếu tìm thấy cả hai
    return None

def find_all_tickers_in_soup(
    soup: BeautifulSoup, 
    ticker_company_map: Dict[str, List[str]], 
    site_name: str
) -> List[str]:
    """
    Tìm tất cả mã cổ phiếu xuất hiện trong nội dung bài viết.
    
    Args:
        soup: BeautifulSoup object của trang web
        ticker_company_map: Dictionary mapping mã cổ phiếu với tên công ty
        site_name: Tên trang web (cafef, vietnambiz, tinnhanhchungkhoan)
        
    Returns:
        Danh sách mã cổ phiếu tìm thấy
    """
    content_selectors = {
        "cafef": [
            ".detail-content", ".detail-content-body", ".news-content",
            "article", ".content-detail", "#mainContent"
        ],
        "vietnambiz": [
            "div.post-body-content", ".article-content", "article.content", ".content-detail",
            "#mainContent", ".journal-content-article"
            
        ],
        "tinnhanhchungkhoan": [
            "article.story .body",
            "article.story", 
            ".article-body", 
            ".article__body", 
            "article .article-body", 
            "#mainContent .article-body"
        ]
    }
    selectors_to_use = content_selectors.get(site_name)
    if not selectors_to_use:
        return []
    tickers_found = set()
    for selector in selectors_to_use:
        content_element = soup.select_one(selector)
        if content_element:
            content_upper = content_element.get_text().upper()
            for ticker, company_names in ticker_company_map.items():
                ticker_upper = ticker.upper()
                ticker_patterns = [
                    f"\\(Mã:\\s*{ticker_upper}\\)",
                    f"\\({ticker_upper}\\)",
                    f"\\[{ticker_upper}\\]",
                    f"\\s{ticker_upper}\\s",
                    f":\\s*{ticker_upper}\\b",
                    f":{ticker_upper}\\b",
                    f"MÃ:\\s*{ticker_upper}\\b",
                    f"MÃ\\s+{ticker_upper}\\b",
                ]
                ticker_found = False
                for pattern in ticker_patterns:
                    if re.search(pattern, content_upper):
                        ticker_found = True
                        break
                if ticker_found:
                    for company_name in company_names:
                        if company_name.upper() in content_upper:
                            tickers_found.add(ticker)
                            break
    return list(tickers_found)

def parse_date_from_soup(soup: BeautifulSoup) -> Optional[datetime]:
    """
    Lấy ngày đăng bài từ đối tượng BeautifulSoup.
    
    Args:
        soup: BeautifulSoup object của trang web
        
    Returns:
        Datetime object nếu tìm thấy, None nếu không tìm thấy
    """

    # Chiến lược 1 (Mới): Lấy từ meta tags (đáng tin cậy nhất)
    meta_selectors = [
        "meta[property='article:published_time']",
        "meta[name='pubdate']"
    ]
    for selector in meta_selectors:
        meta_tag = soup.select_one(selector)
        if meta_tag and meta_tag.get('content'):
            date_iso_str = meta_tag.get('content')
            try:
                # fromisoformat handles formats like '2025-06-20T23:20:00'
                return datetime.fromisoformat(date_iso_str)
            except ValueError:
                # Fallback for just date part or other variations
                try:
                    return datetime.strptime(date_iso_str.split('T')[0], "%Y-%m-%d")
                except ValueError:
                    continue # Try next selector

    # Chiến lược 2: Thử các selector CSS cụ thể trong body
    date_selectors = [
        "span.pdate", "span.date", ".post-time", ".time", ".datepost",
        "span[class*='time']", "span[class*='date']", ".article-time",
        ".news-time",
        "span.datetime" # Thêm selector cho Vietnambiz
    ]
    
    date_text = None
    for selector in date_selectors:
        date_element = soup.select_one(selector)
        if date_element:
            date_text = date_element.get_text()
            break
    
    # Chiến lược 3: Nếu không thành công, tìm kiếm văn bản theo mẫu (cho vietnambiz)
    if not date_text:
        # Mẫu này đặc trưng cho định dạng "HH:MM | DD/MM/YYYY" của Vietnambiz
        found_text_node = soup.find(text=re.compile(r'\d{1,2}:\d{2}\s*\|\s*\d{1,2}/\d{1,2}/\d{4}'))
        if found_text_node:
            date_text = found_text_node.strip()

    if date_text:
        # Cải tiến: Gộp các pattern và tìm kiếm một lần.
        # Pattern này sẽ tìm dd-mm-yyyy, dd/mm/yyyy, d-m-yyyy, d/m/yyyy.
        match = re.search(r'(\d{1,2}/\d{1,2}/\d{4})|(\d{1,2}-\d{1,2}-\d{4})', date_text)
        if match:
            # Lấy group không rỗng đầu tiên
            date_str = next(g for g in match.groups() if g is not None)
            # Cải tiến: Thử các định dạng một cách an toàn và đa nền tảng
            # %d, %m, %Y xử lý được cả số có 1 và 2 chữ số.
            for fmt in ("%d/%m/%Y", "%d-%m-%Y"):
                try:
                    return datetime.strptime(date_str, fmt)
                except ValueError:
                    pass # Thử định dạng tiếp theo
    return None

def get_page_urls(url: str, page: int = 1) -> str:
    """
    Lấy URL cho trang phân trang một cách chính xác và an toàn.
    
    Args:
        url: URL gốc của trang
        page: Số trang cần lấy (mặc định là 1)
        
    Returns:
        URL đã được format cho trang cụ thể
    """
    if page == 1:
        return url
    if "vietnambiz.vn" in url:
        # Ví dụ: https://vietnambiz.vn/doanh-nghiep.htm -> https://vietnambiz.vn/doanh-nghiep/trang-2.htm
        return url.replace(".htm", f"/trang-{page}.htm")
    if "tinnhanhchungkhoan.vn" in url:
        # Ví dụ: https://www.tinnhanhchungkhoan.vn/doanh-nghiep/ -> https://www.tinnhanhchungkhoan.vn/doanh-nghiep/trang-2.html
        return f"{url}trang-{page}.html"
    # Thay thế phần đuôi .chn bằng /trang-{page}.chn cho Cafef
    return url.replace(".chn", f"/trang-{page}.chn")

async def fetch_news(target_date_str: Optional[str] = None) -> List[Dict[str, str]]:
    """
    Tìm nạp tin tức từ các trang web tài chính cho một ngày cụ thể.
    
    Args:
        target_date_str: Chuỗi ngày theo định dạng dd-mm-yyyy hoặc dd/mm/yyyy
        
    Returns:
        Danh sách các bài viết với thông tin mã cổ phiếu, tiêu đề, link và ngày đăng
    """
    if target_date_str:
        try:
            if '-' in target_date_str:
                target_date = datetime.strptime(target_date_str, "%d-%m-%Y").date()
            else:
                target_date = datetime.strptime(target_date_str, "%d/%m/%Y").date()
        except ValueError:
            target_date = datetime.now().date()
    else:
        target_date = datetime.now().date()

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
    }
    data = []
    processed_urls = set()

    article_selectors_cafef = ", ".join([
        ".knswli-title a", ".newscontent h3 a", ".top_noibat h3 a",
        ".list_news_home h3 a", ".tlitem h3 a", ".box-title a",
        "article h3 a", ".visit-popup", ".title a",
        ".story__heading a", ".news-item a", ".list-news a"
    ])
    # Cải tiến: Mở rộng bộ selectors cho Vietnambiz dựa trên phản hồi của người dùng
    article_selectors_vietnambiz = ", ".join([
        "h3.title-news a",      # Selector được gợi ý
        "a.title",              # Selector được gợi ý
        "h3.title-list-news a"  # Selector cũ, giữ lại để phòng trường hợp
    ])
    # Bộ selectors cho Tin nhanh chứng khoán
    article_selectors_tinnhanhchungkhoan = ", ".join([
        "h2.story__heading a",
        "h3.story__heading a",
        ".story--multi__heading a",
        ".story--stream__heading a"
    ])


    async with httpx.AsyncClient(headers=headers, timeout=20.0, follow_redirects=True) as client:
        for base_url in urls_to_crawl:
            
            site_name = "cafef" # Mặc định
            # Chọn bộ selector và URL gốc phù hợp với trang web
            if "vietnambiz.vn" in base_url:
                article_selector_str = article_selectors_vietnambiz
                site_base_url = "https://vietnambiz.vn"
                site_name = "vietnambiz"
            elif "tinnhanhchungkhoan.vn" in base_url:
                article_selector_str = article_selectors_tinnhanhchungkhoan
                site_base_url = "https://www.tinnhanhchungkhoan.vn"
                site_name = "tinnhanhchungkhoan"
            else: # Mặc định là cafef.vn
                article_selector_str = article_selectors_cafef
                site_base_url = "https://cafef.vn"

            for page in range(1, 4):
                list_url = get_page_urls(base_url, page)
                print(f"Đang truy cập: {list_url}") # Thêm dòng này để gỡ lỗi
                try:
                    list_res = await client.get(list_url)
                    # Nếu gặp trang không có (404), bỏ qua và tiếp tục
                    if list_res.status_code == 404:
                        continue
                    list_res.raise_for_status()
                except httpx.RequestError as e:
                    print(f"Lỗi khi tải trang danh sách {e.request.url}: {e}")
                    continue

                list_soup = BeautifulSoup(list_res.text, 'html.parser')

                for article_link in list_soup.select(article_selector_str):
                    try:
                        title = article_link.get_text(strip=True)
                        article_url = article_link.get('href', '')

                        if not title or not article_url:
                            continue

                        # LỌC TIÊU ĐỀ: Bỏ qua nếu tiêu đề ngắn hơn 15 ký tự
                        if len(title.strip()) < 15:
                            continue

                        # LỌC TIÊU ĐỀ: Bỏ qua các bài viết "Cổ phiếu cần quan tâm"
                        if "cổ phiếu cần quan tâm" in title.lower():
                            continue

                        # LỌC TIÊU ĐỀ: Bỏ qua các bài viết "Giao dịch chứng khoán"
                        if "giao dịch chứng khoán" in title.lower():
                            continue

                        # LỌC TIÊU ĐỀ: Bỏ qua các bài viết "sự kiện"
                        if "sự kiện" in title.lower():
                            continue

                        # LỌC TIÊU ĐỀ: Bỏ qua các bài viết "Nhận định thị trường"
                        if "nhận định thị trường" in title.lower():
                            continue

                        # SỬA LỖI: Xử lý linh hoạt các miền của vietnambiz
                        if not article_url.startswith('http'):
                            if "vietnambiz.vn" in article_url:
                                article_url = "https:" + article_url if article_url.startswith('//') else "https://" + article_url.lstrip('/')
                            else:
                                article_url = site_base_url + article_url
                        
                        if article_url in processed_urls:
                            continue
                        processed_urls.add(article_url)

                        try:
                            article_res = await client.get(article_url)
                            article_res.raise_for_status()
                        except httpx.RequestError as e:
                            print(f"Lỗi khi tải bài viết {e.request.url}: {e}")
                            continue

                        article_soup = BeautifulSoup(article_res.text, 'html.parser')
                        date_posted = parse_date_from_soup(article_soup)

                        if not date_posted or date_posted.date() != target_date:
                            continue

                        # Lấy tất cả mã cổ phiếu xuất hiện trong bài viết
                        tickers = find_all_tickers_in_soup(article_soup, TICKER_COMPANY_MAP, site_name)
                        if len(tickers) == 0:
                            continue
                        if len(tickers) > 1:
                            continue  # Bỏ qua bài viết có hơn 2 mã cổ phiếu
                        ticker = tickers[0]  # Lấy mã đầu tiên để hiển thị
                        data.append({
                            "Mã cổ phiếu": ticker,
                            "Tiêu đề": title,
                            "Đường link": article_url,
                            "Ngày đăng": date_posted.strftime("%d/%m/%Y")
                        })
                    except Exception as e:
                        print(f"Lỗi khi xử lý bài viết {article_url}: {e}")
                        continue
    return data

def format_news_for_email(news_data: List[Dict[str, str]], display_date_str: str) -> str:
    """
    Định dạng danh sách tin tức thành một chuỗi HTML đẹp mắt cho email.
    
    Args:
        news_data: Danh sách các bài viết
        display_date_str: Chuỗi ngày để hiển thị
        
    Returns:
        Chuỗi HTML đã được format
    """
    html = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; }}
            .container {{ padding: 20px; border: 1px solid #ddd; border-radius: 5px; max-width: 700px; margin: auto; }}
            .header {{ font-size: 22px; font-weight: bold; color: #333; border-bottom: 2px solid #eee; padding-bottom: 10px; margin-bottom: 20px;}}
            .news-item {{ border-bottom: 1px solid #eee; padding: 15px 0; }}
            .news-item:last-child {{ border-bottom: none; }}
            .ticker {{ font-weight: bold; color: #0056b3; font-size: 1.1em; }}
            .title {{ font-weight: bold; color: #333; }}
            a {{ color: #007bff; text-decoration: none; font-weight: bold;}}
            a:hover {{ text-decoration: underline; }}
        </style>
    </head>
    <body>
        <div class="container">
            <p class="header">📰 Tin tức chứng khoán ngày {display_date_str}</p>
    """
    for item in news_data:
        html += f"""
            <div class="news-item">
                <span class="ticker">📈 Mã CP: {item['Mã cổ phiếu']}</span><br>
                <span class="title">📄 {item['Tiêu đề']}</span><br>
                <a href="{item['Đường link']}">🔗 Đọc thêm</a>
            </div>
        """
    html += """
        </div>
    </body>
    </html>
    """
    return html

def send_email(
    subject: str, 
    html_content: str, 
    sender: str, 
    recipients: List[str], 
    password: str
) -> Tuple[bool, str]:
    """
    Gửi email với nội dung HTML bằng Gmail (sử dụng SSL) cho nhiều người nhận.
    
    Args:
        subject: Tiêu đề email
        html_content: Nội dung HTML của email
        sender: Email người gửi
        recipients: Danh sách email người nhận
        password: Mật khẩu ứng dụng Gmail
        
    Returns:
        Tuple (success, message) - success là True nếu gửi thành công
    """
    if sender == "your_email@gmail.com" or password == "your_app_password":
        msg = "Thông tin email chưa được cấu hình trong file main.py. Bỏ qua việc gửi mail."
        print(f"CẢNH BÁO: {msg}")
        return False, msg

    # Chuyển đổi recipients thành list nếu là string
    if isinstance(recipients, str):
        recipients = [recipients]

    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = sender
    message["To"] = ", ".join(recipients)

    message.attach(MIMEText(html_content, "html"))
    context = ssl.create_default_context()
    try:
        # Sử dụng SMTP_SSL cho Gmail trên cổng 465
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=context) as server:
            server.login(sender, password)
            server.sendmail(sender, recipients, message.as_string())
        print(f"Email đã được gửi thành công tới {', '.join(recipients)}")
        return True, f"Email đã được gửi thành công tới {', '.join(recipients)}"
    except Exception as e:
        error_msg = f"Lỗi khi gửi email: {e}"
        print(error_msg)
        return False, error_msg


async def news_command_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Xử lý lệnh /news, tìm nạp, hiển thị và gửi tin tức qua email.
    
    Args:
        update: Telegram Update object
        context: Telegram Context object
    """
    
    target_date_str = None
    # Kiểm tra xem người dùng có cung cấp ngày không
    if context.args:
        target_date_str = context.args[0]
        try:
            # Chỉ kiểm tra định dạng, không chuyển đổi ở đây
            if '-' in target_date_str:
                datetime.strptime(target_date_str, "%d-%m-%Y")
            elif '/' in target_date_str:
                datetime.strptime(target_date_str, "%d/%m/%Y")
            else:
                await update.message.reply_text("❌ Định dạng ngày không hợp lệ. Vui lòng sử dụng `dd-mm-yyyy` hoặc `dd/mm/yyyy`.")
                return
        except ValueError:
            await update.message.reply_text("❌ Ngày không hợp lệ. Vui lòng sử dụng định dạng `dd-mm-yyyy` hoặc `dd/mm/yyyy`.\nVí dụ: `/news 21-04-2025`")
            return

    # Xác định chuỗi ngày để hiển thị
    if target_date_str:
        display_date_str = target_date_str.replace('-', '/')
    else:
        display_date_str = datetime.now().strftime('%d/%m/%Y')

    await update.message.reply_text(f"🔍 Đang tìm nạp tin tức cho ngày {display_date_str}, vui lòng chờ...")

    try:
        # Truyền chuỗi ngày mục tiêu vào hàm fetch_news
        news_data = await fetch_news(target_date_str)

        if not news_data:
            await update.message.reply_text(f"😕 Không tìm thấy tin tức nào cho ngày {display_date_str}.")
            return

        # Định dạng và gửi phản hồi
        header = f"<b>📰 Tin tức chứng khoán ngày {display_date_str}</b>\n"
        header += "--------------------------------------\n"
        await update.message.reply_text(header, parse_mode='HTML')

        # Gửi từng tin một
        for item in news_data:
            response = ""
            response += f"📈 <b>Mã CP:</b> {item['Mã cổ phiếu']}\n"
            response += f"📄 <b>Tiêu đề:</b> {item['Tiêu đề']}\n"
            response += f"🔗 <a href=\"{item['Đường link']}\">Đọc thêm</a>\n"
            await update.message.reply_text(response, parse_mode='HTML', disable_web_page_preview=True)

        # Sau khi gửi tin lên Telegram, tiến hành gửi email
        await update.message.reply_text("📧 Đang chuẩn bị gửi email...")
        subject = f"Tin tức chứng khoán ngày {display_date_str}"
        html_content = format_news_for_email(news_data, display_date_str)

        # Chạy hàm gửi mail đồng bộ trong một thread riêng để không block bot
        recipients = [EMAIL_RECIPIENT] + VIETCAPITAL_EMAILS
        success, message = await asyncio.to_thread(
            send_email,
            subject,
            html_content,
            EMAIL_SENDER,
            recipients,
            EMAIL_PASSWORD
        )

        if success:
            await update.message.reply_text(f"✅ {message}")
        else:
            await update.message.reply_text(f"❌ {message}")

    except Exception as e:
        print(f"Lỗi khi xử lý lệnh /news: {e}")
        await update.message.reply_text("❌ Rất tiếc, đã có lỗi xảy ra trong quá trình tìm nạp tin tức.")

async def help_message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Gửi tin nhắn hướng dẫn khi người dùng nhắn tin thông thường.
    
    Args:
        update: Telegram Update object
        context: Telegram Context object
    """
    await update.message.reply_text("👋 Chào bạn! Vui lòng sử dụng lệnh /news [dd-mm-yyyy] để nhận tin tức. Nếu không nhập ngày, bot sẽ lấy tin tức hôm nay.")

async def auto_send_news() -> None:
    """
    Hàm tự động gửi tin tức mà không cần context từ user.
    """
    try:
        print("🤖 Tự động gửi tin tức...")
        
        # Lấy ngày hiện tại
        current_date = datetime.now()
        target_date_str = current_date.strftime("%d-%m-%Y")
        display_date_str = current_date.strftime('%d/%m/%Y')
        
        # Tìm nạp tin tức
        news_data = await fetch_news(target_date_str)
        
        if not news_data:
            print(f"😕 Không tìm thấy tin tức nào cho ngày {display_date_str}.")
            return
        
        # Gửi email tự động
        subject = f"Tin tức chứng khoán ngày {display_date_str}"
        html_content = format_news_for_email(news_data, display_date_str)
        
        recipients = [EMAIL_RECIPIENT] + VIETCAPITAL_EMAILS
        success, message = await asyncio.to_thread(
            send_email,
            subject,
            html_content,
            EMAIL_SENDER,
            recipients,
            EMAIL_PASSWORD
        )
        
        if success:
            print(f"✅ Tự động gửi email thành công: {message}")
        else:
            print(f"❌ Lỗi khi tự động gửi email: {message}")
            
    except Exception as e:
        print(f"❌ Lỗi khi tự động gửi tin tức: {e}")
        import traceback
        traceback.print_exc()

def ping_server() -> None:
    """
    Hàm ping để giữ server hoạt động.
    """
    try:
        import requests
        # Ping chính server của mình để giữ nó hoạt động
        response = requests.get("https://stock-news-bot.onrender.com/ping", timeout=10)
        print(f"🔄 Ping server: {response.status_code}")
    except Exception as e:
        print(f"❌ Lỗi khi ping server: {e}")

def run_scheduler() -> None:
    """
    Chạy scheduler trong thread riêng.
    """
    def schedule_job():
        try:
            print(f"🕐 Thực hiện scheduled job lúc {datetime.now().strftime('%H:%M:%S')}")
            # Tạo event loop mới cho thread này
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(auto_send_news())
            loop.close()
            print(f"✅ Hoàn thành scheduled job lúc {datetime.now().strftime('%H:%M:%S')}")
        except Exception as e:
            print(f"❌ Lỗi trong scheduled job: {e}")
            import traceback
            traceback.print_exc()
    
    # Lập lịch gửi tin tức vào lúc 12:00 và 20:00 hàng ngày
    schedule.every().day.at("16:56").do(schedule_job)
    schedule.every().day.at("20:00").do(schedule_job)
    
    # Lập lịch ping server mỗi 15 phút để giữ nó hoạt động
    schedule.every(15).minutes.do(ping_server)
    
    print("⏰ Đã lập lịch tự động gửi tin tức vào lúc 12:00 và 20:00 hàng ngày")
    print("🔄 Đã lập lịch ping server mỗi 15 phút để giữ hoạt động")
    
    while True:
        try:
            schedule.run_pending()
            time.sleep(60)  # Kiểm tra mỗi phút
        except Exception as e:
            print(f"❌ Lỗi trong scheduler: {e}")
            import traceback
            traceback.print_exc()
            time.sleep(60)  # Tiếp tục chạy

def start_scheduler() -> None:
    """
    Khởi động scheduler trong thread riêng.
    """
    scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
    scheduler_thread.start()
    print("🚀 Scheduler đã được khởi động")

# ================== FLASK ROUTES ==================
@app.route('/')
def home() -> str:
    """Trang chủ của bot."""
    return "🤖 Stock News Bot đang hoạt động!"

@app.route('/ping')
def ping() -> str:
    """Endpoint ping để kiểm tra trạng thái bot."""
    return "🔄 Pong! Bot vẫn hoạt động bình thường."

@app.route('/health')
def health() -> Dict[str, str]:
    """Endpoint health check."""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

def main() -> None:
    """
    Hàm chính khởi động bot.
    """
    global app_instance
    
    print(f"🚀 Khởi động Stock News Bot lúc {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Dọn dẹp các instance cũ trước khi khởi động
    cleanup_old_instances()
    
    # Đăng ký signal handler để tắt bot an toàn
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Kiểm tra token
    if not TELEGRAM_BOT_TOKEN or TELEGRAM_BOT_TOKEN == "your_bot_token":
        print("❌ Lỗi: TELEGRAM_BOT_TOKEN chưa được cấu hình!")
        return
    
    # Kiểm tra kết nối Telegram API
    if not check_telegram_connection():
        print("❌ Không thể kết nối Telegram API. Vui lòng kiểm tra token và kết nối internet.")
        return
    
    try:
        # Khởi tạo Application với cấu hình đầy đủ
        app_instance = (
            Application.builder()
            .token(TELEGRAM_BOT_TOKEN)
            .get_updates_read_timeout(30)
            .get_updates_write_timeout(30)
            .get_updates_connect_timeout(30)
            .get_updates_pool_timeout(30)
            .build()
        )
        
        # Thêm trình xử lý cho lệnh /news
        app_instance.add_handler(CommandHandler("news", news_command_handler))
        
        # Thêm trình xử lý cho các tin nhắn văn bản khác để hướng dẫn người dùng
        app_instance.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, help_message_handler))

        # Khởi động scheduler
        start_scheduler()

        print("🤖 Bot đang chạy... Gửi lệnh /news [dd-mm-yyyy] để bắt đầu.")
        print("⏰ Bot sẽ tự động gửi tin tức vào lúc 12:00 và 20:00 hàng ngày")
        print("🔄 Bot sẽ ping server mỗi 15 phút để giữ hoạt động")
        print(f"📅 Thời gian hiện tại: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Chạy Flask app trong thread riêng
        def run_flask() -> None:
            """Chạy Flask app."""
            try:
                port = int(os.environ.get('PORT', 8000))
                app.run(host='0.0.0.0', port=port, debug=False)
            except Exception as e:
                print(f"❌ Lỗi Flask app: {e}")
        
        flask_thread = threading.Thread(target=run_flask, daemon=True)
        flask_thread.start()
        
        # Chạy Telegram bot với error handling và cấu hình polling an toàn
        print("🚀 Khởi động Telegram bot...")
        try:
            app_instance.run_polling(
                allowed_updates=Update.ALL_TYPES,
                drop_pending_updates=True,
                close_loop=False,
                stop_signals=None
            )
        except KeyboardInterrupt:
            print("\n🛑 Bot được tắt bởi người dùng")
            cleanup_old_instances()
        except Exception as e:
            print(f"❌ Lỗi trong polling: {e}")
            import traceback
            traceback.print_exc()
            print("🔄 Đang thử khởi động lại sau 5 giây...")
            time.sleep(5)
            restart_polling()
        
    except Exception as e:
        print(f"❌ Lỗi khởi động bot: {e}")
        import traceback
        traceback.print_exc()
        return

if __name__ == '__main__':
    main()
