# check_stock.py
import requests

PRODUCTS = [
    "amul-high-protein-plain-lassi-200-ml-or-pack-of-30",
    "amul-high-protein-rose-lassi-200-ml-or-pack-of-30",
    "amul-high-protein-buttermilk-200-ml-or-pack-of-30"
]

NTFY_TOPIC = "amul-stock-alert"  # You can change this

def check_stock(alias):
    url = f"https://shop.amul.com/api/1/entity/ms.products?q={{\"alias\":\"{alias}\"}}&limit=1"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        if data["data"]:
            product = data["data"][0]
            available = product.get("available", 0)
            return available > 0, product["name"], product["alias"]
    except Exception as e:
        print("❌ Error:", e)
    return False, None, None

def send_push_notification(product_name, product_alias):
    message = f"🛒 {product_name} is now in stock!\n🔗 https://shop.amul.com/en/product/{product_alias}"
    ntfy_url = f"https://ntfy.sh/{NTFY_TOPIC}"
    headers = {"Title": "Amul Stock Alert"}
    response = requests.post(ntfy_url, data=message.encode(), headers=headers)
    print("✅ Notification sent via ntfy.sh")

# Run for all products
for alias in PRODUCTS:
    in_stock, name, alias_confirm = check_stock(alias)
    if in_stock:
        print(f"✅ {name} is available!")
        send_push_notification(name, alias_confirm)
        break
    else:
        print(f"❌ {alias} still out of stock.")
