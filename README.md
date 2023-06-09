# About
This solves the Solitaire minigame in MOLEK-SYNTEZ.

The script utilizes a method of screen capture and comparison against references images to identify the cards on screen.

Then, it explores the game's state space by identifying the legal moves from each game state.

Finally, it will try to find a set of moves that leads to a winning game state by a simple scoring mechanism, with a better score given for finished or empty columns.

# Requirements
* [Python 3](https://www.python.org/)
* [Pillow](https://pypi.org/project/Pillow/)
* [pynput](https://pypi.org/project/pynput/)

# Usage

Run `solver.py` while the game window is running.

Might not work for different monitor setups / screen resolutions.

# LICENSE

MIT License

Copyright (c) 2023 Kevin Liu

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
