from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from tracking.consumers import TrackingConsumer

application = ProtocolTypeRouter({
    "websocket": URLRouter([
        path("ws/tracking/", TrackingConsumer.as_asgi()),
    ])
})
