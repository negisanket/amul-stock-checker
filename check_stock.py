import requests

NTFY_TOPIC = "amul-stock-alert"  # Replace with your actual ntfy topic name

def send_push_notification(title, message):
    try:
        requests.post(
            f"https://ntfy.sh/{NTFY_TOPIC}",
            data=message.encode("utf-8"),
            headers={"Title": title}
        )
        print(f"✅ Notification sent: {title}")
    except Exception as e:
        print(f"❌ Error sending notification: {e}")

def get_all_protein_products():
    try:
        url = 'https://shop.amul.com/api/1/entity/ms.products?q={"categories":"protein"}&limit=100'
        print(f"🔍 Requesting: {url}")
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        return resp.json().get("data", [])
    except Exception as e:
        print(f"❌ Failed to fetch protein products: {e}")
        return []

def main():
    products = get_all_protein_products()
    for product in products:
        name = product.get("name", "").lower()
        alias = product.get("alias", "")
        quantity = product.get("inventory_quantity", 0)

        if any(kw in name for kw in ["lassi", "buttermilk", "milkshake"]) and quantity > 0:
            msg = f"HUURRRRRRRRRay stock available!\n{name.title()}\n🔗 https://shop.amul.com/en/product/{alias}"
            send_push_notification("🎉 Stock Available!", msg)
            return

    send_push_notification("Still Out of Stock", ":( None of the protein drinks are available yet.")

if __name__ == "__main__":
    main()
