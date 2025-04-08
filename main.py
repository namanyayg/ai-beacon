import time
from audio_monitor import AudioMonitor
from led_controller import LEDController

def main():
    # Create LED controller
    led = LEDController(port='COM8')

    # await delay
    time.sleep(2)

    print("Starting Cursor monitoring...")
    
    # Create audio monitor
    audio_monitor = AudioMonitor()
    
    # Set up the callback to blink LED when volume threshold is exceeded
    audio_monitor.set_volume_callback(
        lambda volume: led.blink_async(times=3, delay=0.5)
    )
    
    try:
        # Start monitoring
        audio_monitor.start()
        
        # Keep the main thread alive
        while True:
            pass
            
    except KeyboardInterrupt:
        print("\nStopping audio monitoring...")
        audio_monitor.stop()
        led.close()

if __name__ == "__main__":
    main() 