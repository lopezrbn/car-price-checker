import reflex as rx
import socket

front_port = 3002
back_port = 8002

config = rx.Config(
    app_name="car_price_checker",
    # api_url=("http://lopezrbn.sytes.net" if socket.gethostname() == "rubenlocalserver" else f"http://localhost:{back_port}"),
    # api_url=("http://car-price-checker.lopezrbn.com" if socket.gethostname() == "rubenlocalserver" else f"http://localhost:{back_port}"),
    frontend_port=front_port,
    backend_port=back_port,
)