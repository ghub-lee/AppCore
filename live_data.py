from fyers_apiv3.FyersWebsocket import data_ws, order_ws
from AppCore import fyers_login


fyers_instance = fyers_login.FyeresLogin()
session, access_token_fyers = fyers_instance.login()
access_token_pin = fyers_instance.ACCESS_TOKEN_PIN


class LiveDataHandler:

    def __init__(self):
        self.fyers_data_socket = None

        # Replace the sample access token with your actual access token obtained from Fyers
        access_token_data = fyers_instance.FY_ID+"-"+fyers_instance.APP_TYPE+":"+access_token_fyers

        self.fyers_data_socket = data_ws.FyersDataSocket(
            access_token=access_token_data,  # Access token in the format "appid:accesstoken"
            log_path="./data/live_data_log/",
            # Lite mode disabled
            # if litemode is true you get only LTP else complete info.
            litemode=False,
            write_to_file=True,  # Save response in a log file instead of printing it.
            reconnect=True,  # Enable auto-reconnection to WebSocket on disconnection.
            on_connect=self.on_open_data,  # Callback function to subscribe to data upon connection.
            on_close=self.on_close,  # Callback function to handle WebSocket connection close events.
            on_error=self.on_error,  # Callback function to handle WebSocket errors.
            on_message=self.on_message  # Callback function to handle incoming messages from the WebSocket.
        )

        # Establish a connection to the Fyers WebSocket
        self.fyers_data_socket.connect()

    def on_open_data(self):

        data_type = "SymbolUpdate"
        # data_type = "DepthUpdate"

        # Subscribe to the specified symbols and data type
        # you can give index symbols and stock symbols also
        symbols = ['NSE:SBIN-EQ']

        self.fyers_data_socket.subscribe(symbols=symbols, data_type=data_type)

        # Keep the socket running to receive real-time data
        self.fyers_data_socket.keep_running()

    def on_message(self, message):
        """
        Callback function to handle incoming messages from the FyersDataSocket WebSocket.

        Parameters:
            message (dict): The received message from the WebSocket.

        """
        print("Response:", message)

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
    live_data_handler_instance = LiveDataHandler()