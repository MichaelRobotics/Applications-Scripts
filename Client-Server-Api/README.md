# Robot Fleet Management System

## Project Overview
A distributed system for managing and monitoring a network of robots in real-time. This project consists of three interconnected components:

1. **Client**: Deployed on each robot to send telemetry data and receive commands
2. **Server**: Centralized communication hub handling client connections and data persistence
3. **API**: RESTful service providing programmatic access to robot data and management capabilities

The system uses a heartbeat mechanism to maintain connection status awareness, automated registration and deregistration of devices, and provides data persistence through a REST API.

## Technical Architecture

### Client Component
- Implemented in Python with TCP socket communication
- Sends periodic robot status and telemetry updates
- Receives and processes heartbeat messages from server
- Handles network disconnections with robust error recovery
- Automated retry and reconnection logic

### Server Component
- Multi-threaded TCP server with concurrent client connection handling
- Thread-safe communication across multiple robot connections
- Real-time heartbeat mechanism for connection monitoring
- Proxies data to persistent storage through the API
- Manages robot registration and deregistration

### API Component
- Flask and Flask-RESTx based RESTful service
- SQLAlchemy ORM for database interactions
- JSON serialization for cross-platform compatibility
- Complete CRUD operations for robot management
- Swagger UI documentation automatically generated

## Key Technical Features

- **Robust Socket Programming**: TCP/IP implementation with error handling
- **Concurrency Management**: Threaded server design for handling multiple connections
- **Data Persistence**: SQLite database with SQLAlchemy ORM
- **REST API Design**: Clean API with proper HTTP method usage and status codes
- **Serialization/Deserialization**: Pickle for socket comms, JSON for API
- **Heartbeat Mechanism**: Reliable connection status monitoring
- **Logging System**: Comprehensive logging for debugging and monitoring
- **Error Handling**: Graceful management of network issues and data conflicts
- **State Management**: Tracking and updating robot status
- **Swagger Documentation**: Auto-generated API docs

## Skills Demonstrated

- Distributed Systems Design
- Network Programming
- Concurrency and Parallelism
- RESTful API Development
- Database Design
- ORM Implementation
- Exception Handling
- Logging and Monitoring
- Scalable Architecture Design
- Resource Management

## Future Enhancements

- Authentication and authorization for secure robot management
- Data visualization dashboard for real-time monitoring
- WebSocket support for push notifications
- Command queueing for offline robots
- Geolocation tracking and mapping
- Metrics collection and analysis
- Containerization with Docker for easy deployment
- Horizontal scaling with load balancing

## Tools & Technologies

- **Languages**: Python
- **Networking**: TCP/IP, Socket Programming
- **Web Framework**: Flask
- **API Framework**: Flask-RESTx
- **ORM**: SQLAlchemy
- **Database**: SQLite
- **Documentation**: Swagger UI
- **Logging**: Python's logging module
- **Serialization**: Pickle, JSON

## How to Run the Project

### Prerequisites
- Python 3.6+
- pip package manager

### Installation
```bash
# Clone the repository
git clone https://github.com/yourusername/robot-fleet-management.git
cd robot-fleet-management

# Install dependencies
pip install -r requirements.txt

# Initialize the database
python -c "from Api.app.extensions import db; from Api.app import create_app; app = create_app(); app.app_context().push(); db.create_all()"
```

### Running the Components
```bash
# Terminal 1: Start the API
cd Api
flask run

# Terminal 2: Start the Server
python Server.py

# Terminal 3: Start a Client (robot simulator)
python Client.py
```

## Architecture Diagram

```
┌─────────────┐           ┌─────────────┐           ┌─────────────┐
│             │           │             │           │             │
│   Client    │◄─────────►│   Server    │◄─────────►│    API      │
│  (Robot)    │           │ (Heartbeat) │           │ (Database)  │
│             │           │             │           │             │
└─────────────┘           └─────────────┘           └─────────────┘
     * N                        * 1                       * 1
```

## License
MIT

## Contact
Your Name - your.email@example.com
