# AI Beacon

_A physical notification light for Cursor AI_

https://github.com/user-attachments/assets/0d2e827e-6966-493e-bc95-f7070afb9e80

When I started using AI like Cursor, I noticed a troubling pattern: I'd set the AI to work on a task, switch to Twitter "just for a minute," and suddenly find myself wasting 20 minutes.

By the time I remembered to check back, my focus was completely shattered. This context-switching was undermining my  efficiency gains. 

Rather than trying to develop better discipline *(a losing battle)*, I decided to create an environmental solution — a physical light that would pull me back to work.

## Building the Solution

I borrowed a Raspberry Pi Pico 2 from a friend, and found some LEDs, a breadboard, and jumper cables. Within two hours, I had a working prototype.

An interesting challenge was figuring out how to detect when Cursor had completed a task. A recent Cursor update had added sound notifications when tasks completed, which gave me the hook I needed.

My solution was admittedly hacky but effective. I installed [VB-Audio Virtual Cable](https://vb-audio.com/Cable/) and configured Windows to route Cursor's audio output through this virtual device. Then I wrote a Python script to monitor this audio channel and trigger the LED whenever it detected sound — since nothing else would be outputting to this channel, any sound would mean Cursor had finished its task.

The code itself isn't complex. The Arduino sketch (listen-blink.ino) simply listens for commands over the serial port and controls the LED accordingly. The Python script (audio_monitor.py) monitors the virtual audio device and sends the appropriate command to the serial port when it detects audio.

## The Difference

The first time my blue light started blinking while I was deep in a Twitter hole, I was amazed at how effectively it pulled me back. 

There's something about a physical change in your environment that cuts through digital distraction in a way that on-screen notifications never could.

## Making Your Own

If you're experiencing similar focus issues with AI, here's how you can create your own system:

Any microcontroller with digital outputs will work — an Arduino, any Raspberry Pi model, or even an ESP8266 if you want to make it wireless. The key components are:

- A way to detect when your AI task is complete (sound, API events, or even screen monitoring)
- A physical notification method (LED, small buzzer, or even a servo that moves a flag)
- Code to connect the two

## Looking Forward

What I find most interesting is that the solution bridges the gap between the digital and physical world.

The future of productive human-AI collaboration might be less about chat interfaces and more about ambient computing that respects our attention and cognitive limitations.

My little blinking light is a crude first step in that direction, but it's made a world of difference in my daily work. Sometimes the simplest solutions are the most effective.

* My writing about AI: https://nmn.gl/blog
* Stop AI hallucinations in your code: https://gigamind.dev/
