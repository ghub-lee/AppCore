from fyers_apiv3.FyersWebsocket import data_ws, order_ws
from AppCore import fyers_login


fyers_instance = fyers_login.FyeresLogin()
session, access_token_fyers = fyers_instance.login()
access_token_pin = fyers_instance.ACCESS_TOKEN_PIN


class LiveOrderHandler:

    def __init__(self):
        self.fyers_order_socket = None

        # Replace the sample access token with your actual access token obtained from Fyers
        access_token_order = access_token_pin

        self.fyers_order_socket = order_ws.FyersOrderSocket(
            access_token=access_token_order,  # Your access token for authenticating with the Fyers API.
            write_to_file=True,  # A boolean flag indicating whether to write data to a log file or not.
            log_path="./data/live_data_log/",
            on_connect=self.on_open_order,  # Callback function to be executed upon successful WebSocket connection.
            on_close=self.on_close,  # Callback function to be executed when the WebSocket connection is closed.
            on_error=self.on_error,  # Callback function to handle any WebSocket errors that may occur.
            on_general=self.on_general,  # Callback function to handle general events from the WebSocket.
            on_orders=self.on_order,  # Callback function to handle order-related events from the WebSocket.
            on_positions=self.on_position,  # Callback function to handle position-related events from the WebSocket.
            on_trades=self.on_trade,  # Callback function to handle trade-related events from the WebSocket.
            reconnect=self.on_reconnect
        )

        # Establish a connection to the Fyers WebSocket
        self.fyers_order_socket.connect()

    def on_open_order(self):
        # Specify the data type and symbols you want to subscribe to
        # data_type = "OnOrders"
        # data_type = "OnTrades"
        # data_type = "OnPositions"
        # data_type = "OnGeneral"

        data_type = "OnOrders,OnTrades,OnPositions,OnGeneral"
        self.fyers_order_socket.subscribe(data_type=data_type)

        # Keep the socket running to receive real-time data
        self.fyers_order_socket.keep_running()

    def on_message(self, message):
        """
        Callback function to handle incoming messages from the FyersDataSocket WebSocket.

        Parameters:
            message (dict): The received message from the WebSocket.

        """
        print("Response:", message)

    def on_trade(self, message):
        """
        Callback function to handle incoming messages from the FyersDataSocket WebSocket.

        Parameters:
            message (dict): The received message from the WebSocket.

        """
        print("Trade Response:", message)

    def on_order(self, message):
        """
        Callback function to handle incoming messages from the FyersDataSocket WebSocket.

        Parameters:
            message (dict): The received message from the WebSocket.

        """
        print("Order Response:", message)

    def on_position(self, message):
        """
        Callback function to handle incoming messages from the FyersDataSocket WebSocket.

        Parameters:
            message (dict): The received message from the WebSocket.

        """
        print("Position Response:", message)

    def on_general(self, message):
        """
        Callback function to handle incoming messages from the FyersDataSocket WebSocket.

        Parameters:
            message (dict): The received message from the WebSocket.

        """
        print("General Response:", message)

    def on_error(self, message):
        """
        Callback function to handle WebSocket errors.

        Parameters:
            message (dict): The error message received from the WebSocket.


        """
        print("Error:", message)

    def on_reconnect(self, message):
        """
        Callback function to handle WebSocket errors.

        Parameters:
            message (dict): The error message received from the WebSocket.


        """
        print("Error:", message)

    def on_close(self, message):
        print("Connection closed:", message)


if __name__ == "__main__":
    live_order_handler_instance = LiveOrderHandler()
