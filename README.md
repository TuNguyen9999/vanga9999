# 📊 Backtest chiến lược Quant

## 🎯 Tổng quan dự án

**Backtest_BreakVol** là sự kết hợp phân tích cơ bản (Fundamental Analysis - FA) và phân tích kỹ thuật (Technical Analysis - TA) để tạo ra các tín hiệu mua/bán tự động.

## 🚀 Các bước thực hiện chính

### 1. **Đọc và xử lý dữ liệu** (`load_and_process_data()`)
- **Đọc dữ liệu HSX**: Giá, khối lượng giao dịch, khối lượng lưu hành từ các file CSV
- **Đọc dữ liệu bổ sung**: Thông tin từ FiinTrade (PE, vốn hóa, dòng tiền nước ngoài)
- **Chuẩn hóa dữ liệu**: Xử lý tên cột, định dạng ngày tháng
- **Gộp dữ liệu**: Kết hợp tất cả nguồn dữ liệu thành một DataFrame duy nhất
- **Xử lý hệ số điều chỉnh**: Tính toán giá điều chỉnh theo adratio cho các sự kiện cổ tức, chia tách

### 2. **Đọc dữ liệu doanh nghiệp** (`load_earnings_data()`)
- **Đọc báo cáo tài chính**: Dữ liệu tăng trưởng lợi nhuận theo quý
- **Xử lý tăng trưởng**: Tính toán tăng trưởng YoY cho từng quý
- **Lọc doanh nghiệp tăng trưởng**: Áp dụng tiêu chí sàn lọc cơ bản

### 3. **Tính toán chỉ số kỹ thuật** (`calculate_technical_indicators()`)
- **Chỉ số cơ bản**: Volume SMA, GTGD trung bình, biến động giá
- **RSI**: Chỉ số sức mạnh tương đối (14 ngày)
- **MACD**: Chỉ báo hội tụ/phân kỳ trung bình động
- **Bollinger Bands**: Dải Bollinger (20 ngày, 2 độ lệch chuẩn)
- **Moving Averages**: MA5, MA9, MA20, MA200, SMA50

### 4. **Tạo tín hiệu Mua/Bán** (`generate_signals()`)
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

