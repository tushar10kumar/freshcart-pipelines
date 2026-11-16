import json
import time
import random
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
channel = connection.channel()

channel.queue_declare(queue="freshcart_orders", durable=True)

products = [
    {"sku": "FC-101", "name": "Organic Apples", "price": 3.50},
    {"sku": "FC-102", "name": "Whole Milk 1L", "price": 1.80},
    {"sku": "FC-103", "name": "Sourdough Bread", "price": 4.25},
    {"sku": "FC-104", "name": "Free-Range Eggs", "price": 5.00},
]

for order_id in range(1, 11):
    item = random.choice(products)
    qty = random.randint(1, 5)
    event = {
        "order_id": f"ORD-{1000 + order_id}",
        "sku": item["sku"],
        "product": item["name"],
        "quantity": qty,
        "total": round(item["price"] * qty, 2),
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }

    channel.basic_publish(
        exchange="",
        routing_key="freshcart_orders",
        body=json.dumps(event),
        properties=pika.BasicProperties(delivery_mode=2),
    )
    print(f"[Producer] Sent {event['order_id']}: {event['quantity']}x {event['product']} (${event['total']})")
    time.sleep(0.5)

connection.close()
print("[Producer] Finished streaming 10 orders.")
