import requests

NTFY_TOPIC = "amul-stock-alert"
PRODUCTS = [
    "amul-kool-protein-milkshake-or-chocolate-180-ml-or-pack-of-30",  # ✅ confirmed in-stock
    "amul-high-protein-plain-lassi-200-ml-or-pack-of-30",
    "amul-high-protein-rose-lassi-200-ml-or-pack-of-30",
    "amul-high-protein-buttermilk-200-ml-or-pack-of-30"
]

def check_stock(alias):
    try:
        url = f"https://shop.amul.com/api/1/entity/ms.products?q={{\"alias\":\"{alias}\"}}&limit=1"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        if data.get("data"):
            product = data["data"][0]
            inventory = product.get("inventory_quantity", 0)
            return inventory > 0, product["name"], product["alias"]
    except Exception as e:
        print(f"❌ Error checking stock for {alias}: {e}")
    return False, None, None

def send_push_notification(title, message):
    try:
        requests.post(
            f"https://ntfy.sh/{NTFY_TOPIC}",
            data=message.encode("utf-8"),
            headers={"Title": title}
        )
    except Exception as e:
        print(f"Error sending notification: {e}")

def main():
    for alias in PRODUCTS:
        in_stock, name, alias_url = check_stock(alias)
        if in_stock:
            msg = f"HUURRRRRRRRRay stock available!\n{name}\n🔗 https://shop.amul.com/en/product/{alias_url}"
            send_push_notification("🎉 Stock Available!", msg)
            return
    send_push_notification("SAAAAADDD Still Out of Stock", ":( None of the products are available yet.")

if __name__ == "__main__":
    main()

