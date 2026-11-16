import json
import time
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
channel = connection.channel()

channel.queue_declare(queue="freshcart_orders", durable=True)
channel.basic_qos(prefetch_count=1)

total_revenue = 0.0
processed_count = 0


def callback(ch, method, properties, body):
    global total_revenue, processed_count
    event = json.loads(body)
    processed_count += 1
    total_revenue += event["total"]

    print(
        f"[Consumer] Processed {event['order_id']} | "
        f"{event['product']} x{event['quantity']} = ${event['total']:.2f} | "
        f"Running Revenue: ${total_revenue:.2f}"
    )
    time.sleep(0.2)
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_consume(queue="freshcart_orders", on_message_callback=callback)

print("[Consumer] Waiting for messages on 'freshcart_orders'. Press Ctrl+C to stop.")
try:
    channel.start_consuming()
except KeyboardInterrupt:
    print(f"\n[Consumer] Stopped. Total orders: {processed_count}, Total revenue: ${total_revenue:.2f}")
    connection.close()
