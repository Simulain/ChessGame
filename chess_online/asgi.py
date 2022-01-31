import os
from channels import routing
import django
from django.core.asgi import get_asgi_application
from chess.consumers import GameConsumer
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

django.setup()

application = ProtocolTypeRouter({
  "websocket": AuthMiddlewareStack(
        URLRouter([
            path(r'game/<int:game_id>', GameConsumer.as_asgi())
        ])
    ),
})
