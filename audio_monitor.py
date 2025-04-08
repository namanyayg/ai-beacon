import pyaudio
import numpy as np
import threading
from typing import Callable
import time
class AudioMonitor:
    def __init__(self, 
                 chunk_size: int = 1024,
                 volume_threshold: float = 0.1):
        """
        Initialize the audio monitor with configuration parameters.
        
        Args:
            chunk_size: Number of frames per buffer
            volume_threshold: Volume level that triggers the callback (0.0 to 1.0)
        """
        self.chunk_size = chunk_size
        self.volume_threshold = volume_threshold
        self.callback = None
        self.is_running = False
        self.audio_thread = None

    def set_volume_callback(self, callback: Callable[[float], None]):
        """
        Set the callback function to be called when volume exceeds threshold.
        
        Args:
            callback: Function that takes a volume level (float) as argument
        """
        self.callback = callback

    def _monitor_audio(self):
        """Internal method to monitor audio in a separate thread."""
        p = pyaudio.PyAudio()
        
        # Find the VB-Audio Virtual Cable input device
        device_index = None
        for i in range(p.get_device_count()):
            device_info = p.get_device_info_by_index(i)
            if "CABLE Output" in device_info['name'] and device_info["maxInputChannels"] > 0:
                device_index = i
                break
        
        if device_index is None:
            print("Virtual Cable input device not found!")
            return

        try:
            # Open stream with VB-Audio Virtual Cable
            stream = p.open(
                format=pyaudio.paInt16,
                channels=2,
                rate=44100,
                input=True,
                input_device_index=device_index,
                frames_per_buffer=self.chunk_size
            )
            
            while self.is_running:
                try:
                    # Read audio data
                    data = stream.read(self.chunk_size, exception_on_overflow=False)
                    audio_data = np.frombuffer(data, dtype=np.int16)
                    
                    # Calculate volume using peak detection (most responsive)
                    volume = np.max(np.abs(audio_data)) / 32768.0
                    
                    # If volume exceeds threshold and callback is set, call it
                    if volume > self.volume_threshold and self.callback:
                        current_time = time.time()
                        if not hasattr(self, 'last_callback_time') or current_time - self.last_callback_time >= 1.0:
                            print(f"Detected Cursor completion, triggering blink...")
                            self.callback(volume)
                            self.last_callback_time = current_time
                except Exception as e:
                    print(f"Error reading audio: {e}")
                    break
                    
        except Exception as e:
            print(f"Error in audio monitoring: {e}")
        finally:
            if 'stream' in locals():
                stream.stop_stream()
                stream.close()
            p.terminate()

    def start(self):
        """Start the audio monitoring in a separate thread."""
        if not self.is_running:
            self.is_running = True
            self.audio_thread = threading.Thread(target=self._monitor_audio)
            self.audio_thread.daemon = True
            self.audio_thread.start()

    def stop(self):
        """Stop the audio monitoring."""
        self.is_running = False
        if self.audio_thread:
            self.audio_thread.join() 