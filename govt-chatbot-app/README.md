# Government Scheme Chatbot Application

A full-stack web application with a chatbot interface for government scheme information.

## Features

- **Scheme Directory**: Browse and search government schemes
- **Interactive Chatbot**: Get information about schemes through a conversational interface
- **Admin Panel**: Manage schemes (add, update, delete)
- **Responsive Design**: Works on desktop and mobile devices

## Tech Stack

### Backend
- Python with Flask
- MongoDB for database
- RESTful API architecture

### Frontend
- React.js
- Modern UI with responsive design
- Axios for API communication

## Getting Started

### Prerequisites
- Python 3.8+
- Node.js 14+
- MongoDB

### Installation

1. Clone the repository
```
git clone https://github.com/yourusername/govt-chatbot-app.git
cd govt-chatbot-app
```

2. Install dependencies
```
npm run install
```
This will install both backend and frontend dependencies.

3. Set up environment variables
- Rename `.env.example` to `.env` in the backend directory
- Update the values with your MongoDB and SMTP settings

4. Start the development servers
```
npm run dev
```
This will start both backend and frontend servers.

- Backend: http://localhost:5000
- Frontend: http://localhost:3000

## Project Structure

```
govt-chatbot-app/
├── backend/                 # Python Flask server
│   ├── config/              # Database configuration
│   ├── controllers/         # Request handlers
│   ├── models/              # Database models
│   ├── routes/              # API endpoints
│   ├── utils/               # Utility functions
│   ├── chatbot/             # Chatbot logic
│   ├── app.py               # Main application
│   └── requirements.txt     # Python dependencies
│
├── frontend/                # React.js client
│   ├── public/              # Static files
│   ├── src/                 # React components
│   │   ├── components/      # Reusable components
│   │   ├── pages/           # Page components
│   │   └── styles/          # CSS files
│   └── package.json         # JS dependencies
│
└── README.md                # Project documentation
```

## API Endpoints

- `GET /api/schemes`: Get all schemes with pagination
- `GET /api/schemes/:id`: Get scheme by ID
- `GET /api/schemes/search?q=query`: Search schemes
- `POST /api/schemes`: Create a new scheme
- `PUT /api/schemes/:id`: Update a scheme
- `DELETE /api/schemes/:id`: Delete a scheme
- `POST /api/chatbot`: Send message to chatbot

## License

This project is licensed under the ISC License.
