# 📊 Backtest chiến lược Quant

## 🎯 Tổng quan dự án

**Backtest_BrealVol** là sự kết hợp phân tích cơ bản (Fundamental Analysis - FA) và phân tích kỹ thuật (Technical Analysis - TA) để tạo ra các tín hiệu mua/bán tự động.

## 🚀 Các bước thực hiện chính

### 1. **Đọc và Xử lý Dữ liệu** (`load_and_process_data()`)
- **Đọc dữ liệu HSX**: Giá, khối lượng giao dịch, khối lượng lưu hành từ các file CSV
- **Đọc dữ liệu bổ sung**: Thông tin từ FiinTrade (PE, vốn hóa, dòng tiền nước ngoài)
- **Chuẩn hóa dữ liệu**: Xử lý tên cột, định dạng ngày tháng
- **Gộp dữ liệu**: Kết hợp tất cả nguồn dữ liệu thành một DataFrame duy nhất
- **Xử lý hệ số điều chỉnh**: Tính toán giá điều chỉnh theo adratio cho các sự kiện cổ tức, chia tách

### 2. **Đọc Dữ liệu Doanh nghiệp** (`load_earnings_data()`)
- **Đọc báo cáo tài chính**: Dữ liệu tăng trưởng lợi nhuận theo quý
- **Xử lý tăng trưởng**: Tính toán tăng trưởng YoY cho từng quý
- **Lọc doanh nghiệp tăng trưởng**: Áp dụng tiêu chí sàn lọc cơ bản

### 3. **Tính toán Chỉ số Kỹ thuật** (`calculate_technical_indicators()`)
- **Chỉ số cơ bản**: Volume SMA, GTGD trung bình, biến động giá
- **RSI**: Chỉ số sức mạnh tương đối (14 ngày)
- **MACD**: Chỉ báo hội tụ/phân kỳ trung bình động
- **Bollinger Bands**: Dải Bollinger (20 ngày, 2 độ lệch chuẩn)
- **Moving Averages**: MA5, MA9, MA20, MA200, SMA50

### 4. **Tạo Tín hiệu Mua/Bán** (`generate_signals()`)
- **Lọc cơ bản**: PE < 50, vốn hóa > 1000 tỷ, GTGD > 20 tỷ
- **Nhóm 1 - Thu hút dòng tiền**:
  - MACD > Signal (tối thiểu 0.18)
  - Khối lượng > 1.5x trung bình 15 ngày
  - Khối lượng mua > 0.85x khối lượng bán
  - Giá tăng 3-15% trong 3-15 ngày
- **Nhóm 2 - Breakout MA200**:
  - Giá tăng > 5% và vượt MA200
  - 20 phiên trước đó đều dưới MA200

### 5. **Chạy Backtest** (`run_backtest()`)
- **Quản lý danh mục**: Mua/bán theo tín hiệu, rebalancing
- **Quản lý rủi ro**: Stop loss 10%, trailing stop 10%, MA9 stop
- **Xử lý T+2/T+3**: Mô phỏng thời gian thanh toán thực tế
- **Mua lại cổ phiếu**: Logic mua lại sau 10-60 ngày bị loại

### 6. **Xuất Kết quả** (`export_results()`)
- **Excel**: Portfolio History, Trading History, Daily Signals, Removed Stocks
- **Word**: Báo cáo chi tiết với biểu đồ và thống kê
- **Biểu đồ**: Hiệu suất NAV, top cổ phiếu đóng góp lợi nhuận

## 🏗️ Cấu trúc Code

### Class chính: `BacktestOptimizer`

```python
class BacktestOptimizer:
    def __init__(self):
        # Cấu hình backtest
        self.INITIAL_CAPITAL = 1_000_000_000  # 1 tỷ VNĐ
        self.STOP_LOSS_PCT = 0.1              # 10%
        self.TRAILING_STOP_PCT = 0.1          # 10%
        self.TRANSACTION_FEE_RATE = 0.001     # 0.1%
        
        # Đường dẫn file dữ liệu
        self.file_paths = {
            'hsx_klgd': 'HSX.KLGD.Upto03.07.2025.csv',
            'hsx_price': 'HSX.AdPrice.Upto03.07.2025.csv',
            'hsx_volume': 'HSX.Volume.Upto03.07.2025.csv',
            'fiin': 'HOSE.Upto04.07.2025.csv',
            'earnings': 'FiinProX_DE_Doanh_nghiep_20250220.csv'
        }
```

### Các phương thức chính:

1. **`load_and_process_data()`**: Xử lý dữ liệu thị trường
2. **`load_earnings_data()`**: Xử lý dữ liệu doanh nghiệp
3. **`calculate_technical_indicators()`**: Tính toán chỉ số kỹ thuật
4. **`generate_signals()`**: Tạo tín hiệu mua/bán
5. **`run_backtest()`**: Chạy mô phỏng backtest
6. **`export_results()`**: Xuất kết quả ra Excel/Word

## 📁 Cấu trúc File

```
Backtest_BrealVol/
├── Backtest_BrealVol(0908)_Run.py    # File chính chạy backtest
├── README.md                          # Hướng dẫn sử dụng
├── Data/                              # Thư mục chứa dữ liệu
│   ├── HSX.KLGD.Upto03.07.2025.csv
│   ├── HSX.AdPrice.Upto03.07.2025.csv
│   ├── HSX.Volume.Upto03.07.2025.csv
│   ├── HOSE.Upto04.07.2025.csv
│   └── FiinProX_DE_Doanh_nghiep_20250220.csv
├── Output/                            # Kết quả xuất ra
│   ├── Quant_Portfolio.xlsx
│   ├── Quant_Report.docx
│   ├── nav_chart.png
│   └── top10_*.png
└── Requirements.txt                   # Thư viện cần thiết
```

## 🔧 Cài đặt và Chạy

### 1. Cài đặt thư viện cần thiết

```bash
pip install pandas numpy matplotlib python-docx xlsxwriter backtrader
```

### 2. Chuẩn bị dữ liệu

- Đặt các file CSV vào thư mục `Data/`
- Cập nhật đường dẫn trong `self.file_paths` nếu cần

### 3. Chạy backtest

```bash
python Backtest_BrealVol(0908)_Run.py
```

## 📊 Kết quả Output

### 1. **File Excel** (`Quant_Portfolio.xlsx`)
- **Portfolio History**: Lịch sử NAV, giao dịch, danh mục cuối ngày
- **Trading History**: Chi tiết tất cả giao dịch mua/bán
- **Daily Signals**: Tín hiệu mua/bán theo ngày
- **Removed Stocks**: Cổ phiếu bị loại khỏi danh mục
- **Danh mục cuối ngày**: Tỷ trọng và return của từng mã

### 2. **File Word** (`Quant_Report.docx`)
- Báo cáo chi tiết chiến lược đầu tư
- So sánh hiệu suất với thị trường (VN30, VNINDEX, VNALLSHARE)
- Thống kê giao dịch theo năm
- Top cổ phiếu đóng góp lợi nhuận

### 3. **Biểu đồ**
- **nav_chart.png**: Hiệu suất NAV và số mã đang nắm giữ
- **top10_*.png**: Top 10 mã đóng góp lợi nhuận theo năm

## 🎯 Chiến lược Đầu tư

### **Tiêu chí sàn lọc cơ bản:**
- Hai quý liên tiếp tăng trưởng lợi nhuận (quý hiện tại > 20% YoY)
- Tăng trưởng lợi nhuận quý hiện tại > 100% YoY
- P/E < 50
- Vốn hóa > 1.000 tỷ VNĐ
- GTGD trung bình > 10 tỷ VNĐ

### **Điều kiện mua:**
- **Nhóm 1**: Cổ phiếu thu hút dòng tiền, thoát tích lũy
- **Nhóm 2**: Breakout MA200 sau 20 phiên dưới MA200
- **Mua lại**: Cổ phiếu từng bị loại sau 10-60 ngày

### **Điều kiện bán:**
- Stop loss: 10%
- Trailing stop: 10%
- Giá < MA9
- Nhóm 2: Bán khi tăng 10% hoặc giữ tối đa 10 phiên
- Mua lại breakout: Giữ tối đa 20 phiên

## 📈 Hiệu suất Backtest

### **Thời gian backtest:** 01/01/2024 - 31/08/2025
### **Vốn ban đầu:** 1.000.000.000 VNĐ (1 tỷ)
### **Chi phí giao dịch:** 0.1% mỗi lần mua/bán
### **Số lượng cổ phiếu tối đa:** Không giới hạn (chia đều vốn)

## 🔍 Debug và Kiểm tra

### **Debug close_ad:**
```python
# Kiểm tra giá điều chỉnh cho mã SIP
optimizer.debug_close_ad('SIP')
```

### **Kiểm tra dữ liệu:**
- Xem log console để theo dõi quá trình xử lý
- Kiểm tra file CSV output để debug dữ liệu
- Sử dụng `print()` để kiểm tra các biến trung gian

## ⚠️ Lưu ý quan trọng

1. **Dữ liệu giả lập**: Hệ thống tự động giả lập dữ liệu cho các ngày còn thiếu
2. **Thời gian thanh toán**: Mô phỏng T+2 cho tiền, T+3 cho cổ phiếu
3. **Rebalancing**: Chỉ thực hiện khi chênh lệch > 1.5% NAV
4. **Quản lý rủi ro**: Áp dụng stop loss và trailing stop tự động

## 🚨 Xử lý lỗi

### **Lỗi thường gặp:**
1. **File không tìm thấy**: Kiểm tra đường dẫn trong `self.file_paths`
2. **Dữ liệu thiếu**: Kiểm tra định dạng CSV và encoding
3. **Lỗi tính toán**: Kiểm tra dữ liệu số và xử lý NaN

### **Debug mode:**
```python
# Bật debug mode để xem chi tiết
import traceback
traceback.print_exc()
```

## 📞 Hỗ trợ

- **Tác giả**: Tú Nguyễn
- **Công ty**: VCAM
- **Phiên bản**: 1.0
- **Ngày cập nhật**: 09/08/2025

---

*© 2025 VCAM | Confidential – For Internal Use Only*
