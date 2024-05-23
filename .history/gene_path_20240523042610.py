# constants.py
import os

WHISPER_CPP_DIR = "/Users/gene/audio_proj/whisper.cpp'"
AUDIO_FILE_PATH = "/Users/gene/briend/extracted_elements"

(env) (base) gene@genes-MBP briend % python transcription.py
Traceback (most recent call last):
  File "/Users/gene/briend/transcription.py", line 1, in <module>
    from whisper_cpp_python import Whisper
  File "/Users/gene/briend/env/lib/python3.11/site-packages/whisper_cpp_python/__init__.py", line 1, in <module>
    from .whisper import *
  File "/Users/gene/briend/env/lib/python3.11/site-packages/whisper_cpp_python/whisper.py", line 1, in <module>
    from . import whisper_cpp
  File "/Users/gene/briend/env/lib/python3.11/site-packages/whisper_cpp_python/whisper_cpp.py", line 54, in <module>
    _lib = _load_shared_library(_lib_base_name)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/gene/briend/env/lib/python3.11/site-packages/whisper_cpp_python/whisper_cpp.py", line 45, in _load_shared_library
    raise FileNotFoundError(
FileNotFoundError: Shared library with base name 'whisper' not found