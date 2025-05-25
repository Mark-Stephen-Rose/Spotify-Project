# Full-Stack Music Streaming Application

This is a full-featured music streaming web application built using Flask (Python) for the backend, a relational SQL database for persistent storage, and HTML, CSS, and JavaScript for a responsive and interactive frontend. The platform enables users to browse albums and playlists, stream music, manage their personal library, and perform account-level operations such as login and playlist creation.

## Tech Stack
- Frontend: HTML5, CSS3, JavaScript
- Backend: Python (Flask)
- Database: SQL with DAO (Data Access Object) architecture
- Audio Playback: HTML5 Audio API with custom JavaScript controls

## Features
- User authentication with registration and login
- Streaming support for songs organized into albums and playlists
- Playlist creation, editing, and deletion
- Liked songs library and user-specific music collections
- Real-time audio playback with autoplay, iteration, and dynamic controls
- Structured backend architecture with modular DAO design

## Project Structure
- `*.py` – Backend routes, data models, and DAO modules
- `/templates` – Jinja2 HTML templates rendered by Flask
- `/static` – JavaScript and CSS files for frontend behavior and styling
- `*.sql` – Database schema and test data scripts

## License
This project is licensed under the MIT License.
MIT License

Copyright (c) 2025 Mark Rose and Azia Koser

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
