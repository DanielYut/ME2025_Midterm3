// ======================
// Modal 開啟 / 關閉
// ======================
function open_input_table() {
    document.getElementById("addModal").style.display = "block";
}
function close_input_table() {
    document.getElementById("addModal").style.display = "none";
}

// ======================
// Delete Data (DELETE /product)
// ======================
function delete_data(value) {
    fetch(`/product?order_id=${value}`, {
        method: "DELETE",
    })
    .then(response => {
        if (!response.ok) {
            throw new Error("伺服器回傳錯誤");
        }
        return response.json();
    })
    .then(result => {
        console.log(result);
        close_input_table();
        location.assign('/');
    })
    .catch(error => {
        console.error("發生錯誤：", error);
    });
}

// ======================
//  Part1: 前端互動邏輯
// ======================

// DOM 元件綁定（依照你 orderadd.html 的名稱）
// ---- 若名稱與你的 HTML 不同，再告訴我調整 ----
const categorySelect = document.getElementById("category");
const productSelect = document.getElementById("product");
const priceInput = document.getElementById("price");
const amountInput = document.getElementById("amount");
const totalInput = document.getElementById("total");
const dateInput = document.getElementById("product_date");
const statusSelect = document.getElementById("status");

// ======================
// 1. 選取商品種類 → 更新商品選單
// ======================
function selectCategory() {
    const category = categorySelect.value;
    if (!category) return;

    fetch(`/product?category=${encodeURIComponent(category)}`)
        .then(res => {
            if (!res.ok) throw new Error("取得商品列表失敗");
            return res.json();
        })
        .then(data => {
            // 清空商品下拉選單
            productSelect.innerHTML = `<option value="">請選擇商品</option>`;

            if (Array.isArray(data.product)) {
                data.product.forEach(p => {
                    let opt = document.createElement("option");
                    opt.value = p;
                    opt.textContent = p;
                    productSelect.appendChild(opt);
                });
            }

            // 清空單價與小計
            priceInput.value = "";
            totalInput.value = 0;
        })
        .catch(err => {
            console.error(err);
            alert("取得商品列表失敗");
        });
}

// ======================
// 2. 選取商品 → 更新價格
// ======================
function selectProduct() {
    const product = productSelect.value;
    if (!product) {
        priceInput.value = "";
        totalInput.value = 0;
        return;
    }

    fetch(`/product?product=${encodeURIComponent(product)}`)
        .then(res => {
            if (!res.ok) throw new Error("取得商品價格失敗");
            return res.json();
        })
        .then(data => {
            priceInput.value = data.price ?? 0;
            countTotal();
        })
        .catch(err => {
            console.error(err);
            alert("取得商品價格失敗");
        });
}

// ======================
// 3. 計算小計：單價 × 數量
// ======================
function countTotal() {
    const price = parseFloat(priceInput.value) || 0;
    let amount = parseInt(amountInput.value) || 1;

    if (amount <= 0) {
        amount = 1;
        amountInput.value = 1;
    }

    const total = price * amount;
    totalInput.value = total.toFixed(2);
}

// ======================
// 4. 初始化預設值（日期、數量、狀態、小計）
// ======================
function initForm() {
    // 日期預設今天
    if (dateInput) {
        const today = new Date();
        const yyyy = today.getFullYear();
        const mm = String(today.getMonth() + 1).padStart(2, '0');
        const dd = String(today.getDate()).padStart(2, '0');
        dateInput.value = `${yyyy}-${mm}-${dd}`;
    }

    // 數量預設至少 1
    amountInput.value = 1;
    amountInput.min = 1;

    // 狀態預設「未付款」
    if (statusSelect) statusSelect.value = "未付款";

    totalInput.value = 0;
}

// ======================
// Event Listeners 綁定
// ======================
document.addEventListener("DOMContentLoaded", () => {
    initForm();

    if (categorySelect) categorySelect.addEventListener("change", selectCategory);
    if (productSelect) productSelect.addEventListener("change", selectProduct);
    if (amountInput) amountInput.addEventListener("input", countTotal);
    if (priceInput) priceInput.addEventListener("input", countTotal);
});
