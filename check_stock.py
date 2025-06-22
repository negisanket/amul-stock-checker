import requests

PRODUCTS = [
    "amul-kool-protein-milkshake-or-kesar-180-ml-or-pack-of-30",
    "amul-high-protein-plain-lassi-200-ml-or-pack-of-30",
    "amul-high-protein-rose-lassi-200-ml-or-pack-of-30",
    "amul-high-protein-buttermilk-200-ml-or-pack-of-30"
]

NTFY_TOPIC = "amul-stock-alert"  # change as needed

def check_stock(alias):
    try:
        url = f"https://shop.amul.com/api/1/entity/ms.products?q={{\"alias\":\"{alias}\"}}&limit=1"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        if data.get("data"):
            product = data["data"][0]

            # ✅ The real stock count
            inventory_quantity = product.get("inventory_quantity", 0)

            return inventory_quantity > 0, product["name"], product["alias"]
    except Exception as e:
        print(f"❌ Error checking {alias}: {e}")
    return False, None, None


def send_push_notification(title, message):
    try:
        url = f"https://ntfy.sh/{NTFY_TOPIC}"
        headers = {"Title": title}
        response = requests.post(url, data=message.encode(), headers=headers)
        if response.status_code == 200:
            print(f"✅ Notification sent: {title}")
        else:
            print(f"❌ Failed to send notification: {response.status_code}")
    except Exception as e:
        print(f"Error sending notification: {e}")

def main():
    for alias in PRODUCTS:
        in_stock, name, alias_confirm = check_stock(alias)
        if in_stock:
            message = f"HUURRRRRRRRRay stock available!\n{name}\n🔗 https://shop.amul.com/en/product/{alias_confirm}"
            send_push_notification("🎉 Stock Available!", message)
            return

    # If no stock found
    send_push_notification("SAAADDDD Still Out of Stock", ":( Not yet available. We'll check again in an hour!")

if __name__ == "__main__":
    main()
