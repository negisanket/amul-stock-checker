# check_stock.py
import requests

# Products in priority order
PRODUCTS = [
    "amul-high-protein-plain-lassi-200-ml-or-pack-of-30",
    "amul-high-protein-rose-lassi-200-ml-or-pack-of-30",
    "amul-high-protein-buttermilk-200-ml-or-pack-of-30"
]

NTFY_TOPIC = "amul-stock-alert"  # Subscribe at https://ntfy.sh/amul-stock-alert

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
        print(f"❌ Error checking {alias}: {e}")
    return False, None, None

def send_push_notification(title, message):
    ntfy_url = f"https://ntfy.sh/{NTFY_TOPIC}"
    headers = {"Title": title}
    requests.post(ntfy_url, data=message.encode(), headers=headers)
    print(f"📢 Notification sent: {title}")

def main():
    for alias in PRODUCTS:
        in_stock, name, alias_confirm = check_stock(alias)
        if in_stock:
            title = "🎉 Stock Available!"
            message = f"HUURRRRRRRRRay stock available!\n{name}\n🔗 https://shop.amul.com/en/product/{alias_confirm}"
            send_push_notification(title, message)
            return

    # No stock found in any
    title = "😞 Still Out of Stock"
    message = ":( Not yet available. We'll check again in an hour!"
    send_push_notification(title, message)

if __name__ == "__main__":
    main()
