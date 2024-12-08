# audio_system.py

import pygame, random, threading
from pygame import mixer
from settings import AUDIO

# Initialize the Pygame mixer
mixer.init()

class AudioSystem:
    _playing_sfx = {}  # Tracks currently playing SFX by ID
    _looping_sfx_threads = {}  # Tracks threads for looping SFX by ID
    
    @staticmethod
    def _get_random_path(audio_paths):
        # Randomly select a path from a list
        if isinstance(audio_paths, list):
            return random.choice(audio_paths)
        return audio_paths
    
    @staticmethod
    def play_music(music_id, should_loop, offset=0.0):
        # Play the specified music track
        if music_id not in AUDIO['music']:
            raise ValueError(f"Music ID '{music_id}' not found in AUDIO['music'].")
        
        # Stop any currently playing music
        mixer.music.stop()
        
        # Get a random path for the music
        music_path = AudioSystem._get_random_path(AUDIO['music'][music_id])
        mixer.music.load(music_path)
        loop_flag = -1 if should_loop else 0
        mixer.music.play(loops=loop_flag, start=offset)
    
    @staticmethod
    def stop_music():
        # Stop the currently playing music
        mixer.music.stop()
    
    @staticmethod
    def play_sfx(sfx_id, offset=0.0, should_loop=False, duration_range=(0.0, 0.0)):
        # Play the specified sound effect
        if sfx_id not in AUDIO['sfx']:
            raise ValueError(f"SFX ID '{sfx_id}' not found in AUDIO['sfx'].")
        
        # Check if the SFX is already playing
        if sfx_id in AudioSystem._playing_sfx:
            print(f"SFX '{sfx_id}' is already playing and will be ignored.")
            return

        # Get a random path for the sound effect
        sfx_path = AudioSystem._get_random_path(AUDIO['sfx'][sfx_id])
        sound = mixer.Sound(sfx_path)

        def loop_sfx():
            # Handle looping SFX with random durations
            while sfx_id in AudioSystem._looping_sfx_threads:
                channel = sound.play()
                duration = random.uniform(*duration_range) if duration_range else sound.get_length()
                pygame.time.delay(int(duration * 1000))
                channel.stop()

        if should_loop:
            if not duration_range:
                raise ValueError("Duration range must be provided for looping SFX.")
            # Start a thread for looping the SFX
            AudioSystem._looping_sfx_threads[sfx_id] = threading.Thread(target=loop_sfx, daemon=True)
            AudioSystem._looping_sfx_threads[sfx_id].start()
        else:
            # Play the sound effect once
            channel = sound.play()
            AudioSystem._playing_sfx[sfx_id] = channel
            if offset > 0.0:
                duration = sound.get_length()
                if offset < duration:
                    pygame.time.delay(int(offset * 1000))
                    channel.stop()

    @staticmethod
    def stop_sfx(sfx_id: str):
        # Stop the specified SFX from playing
        if sfx_id in AudioSystem._looping_sfx_threads:
            del AudioSystem._looping_sfx_threads[sfx_id]
        if sfx_id in AudioSystem._playing_sfx:
            channel = AudioSystem._playing_sfx.pop(sfx_id)
            channel.stop()

    @staticmethod
    def stop_all_sfx():
        # Stops all currently playing SFX
        for sfx_id in list(AudioSystem._looping_sfx_threads.keys()):
            AudioSystem.stop_sfx(sfx_id)
        for sfx_id in list(AudioSystem._playing_sfx.keys()):
            AudioSystem.stop_sfx(sfx_id)