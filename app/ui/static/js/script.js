/* app/ui/static/js/script.js */

document.addEventListener('DOMContentLoaded', function() {
    
    // 1. Tự động ẩn Flash Messages sau 4 giây
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            // Sử dụng Bootstrap Alert instance để đóng
            let bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 4000); // 4000ms = 4 giây
    });

    // 2. Highlight các hàng có chi phí cao trong bảng (nếu có)
    // Giả sử cột chi phí là cột thứ 6 (index 5) hoặc tìm class cụ thể
    const costCells = document.querySelectorAll('td');
    costCells.forEach(cell => {
        // Nếu nội dung là số tiền và lớn hơn 10 triệu (ví dụ logic JS đơn giản)
        let text = cell.innerText.replace(/,/g, ''); // Bỏ dấu phẩy
        if (!isNaN(text) && parseFloat(text) > 10000000) {
            cell.classList.add('text-danger', 'fw-bold'); // Tô đỏ và in đậm
        }
    });

});
