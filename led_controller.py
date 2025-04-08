import serial
import time
import threading
from typing import Optional

class LEDController:
    def __init__(self, 
                 port: str = 'COM8',
                 baud_rate: int = 9600,
                 connection_timeout: float = 2.0):
        """
        Initialize the LED controller with configuration parameters.
        
        Args:
            port: Serial port for Arduino connection
            baud_rate: Baud rate for serial communication
            connection_timeout: Time to wait for connection to establish (seconds)
        """
        self.port = port
        self.baud_rate = baud_rate
        self.connection_timeout = connection_timeout
        self.serial_connection: Optional[serial.Serial] = None

    def _ensure_connection(self) -> bool:
        """
        Ensure serial connection is established.
        
        Returns:
            bool: True if connection is established, False otherwise
        """
        if self.serial_connection is None or not self.serial_connection.is_open:
            try:
                self.serial_connection = serial.Serial(
                    self.port, 
                    self.baud_rate, 
                    timeout=1
                )
                time.sleep(self.connection_timeout)
                return True
            except Exception as e:
                print(f"Error establishing serial connection: {e}")
                return False
        return True

    def turn_on(self):
        """Turn the LED on."""
        if self._ensure_connection():
            try:
                self.serial_connection.write(b'1')
                print("LED ON")
            except Exception as e:
                print(f"Error turning LED on: {e}")

    def turn_off(self):
        """Turn the LED off."""
        if self._ensure_connection():
            try:
                self.serial_connection.write(b'0')
                print("LED OFF")
            except Exception as e:
                print(f"Error turning LED off: {e}")

    def blink(self, times: int = 3, delay: float = 0.5):
        """
        Blink the LED a specified number of times with a given delay.
        
        Args:
            times: Number of times to blink
            delay: Delay between blinks in seconds
        """
        if self._ensure_connection():
            try:
                for _ in range(times):
                    self.turn_on()
                    time.sleep(delay)
                    self.turn_off()
                    time.sleep(delay)
            except Exception as e:
                print(f"Error during LED blink sequence: {e}")

    def blink_async(self, times: int = 3, delay: float = 0.5):
        """
        Blink the LED asynchronously in a separate thread.
        
        Args:
            times: Number of times to blink
            delay: Delay between blinks in seconds
        """
        threading.Thread(target=self.blink, args=(times, delay)).start()

    def close(self):
        """Close the serial connection."""
        if self.serial_connection and self.serial_connection.is_open:
            try:
                self.serial_connection.close()
            except Exception as e:
                print(f"Error closing serial connection: {e}") 