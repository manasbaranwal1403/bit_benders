import React, { useState, useRef, useEffect } from 'react';
import {
  Container,
  Paper,
  TextField,
  IconButton,
  Typography,
  Box,
  CircularProgress,
} from '@mui/material';
import SendIcon from '@mui/icons-material/Send';
import axios from 'axios';

function Chatbot() {
  const [messages, setMessages] = useState([
    {
      type: 'bot',
      content: 'Hello! I can help you find information about government schemes. What would you like to know?',
    },
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    const userMessage = input.trim();
    setInput('');
    setMessages((prev) => [...prev, { type: 'user', content: userMessage }]);
    setLoading(true);

    try {
      const response = await axios.post('http://localhost:5000/api/chatbot', {
        message: userMessage,
        session_id: 'user-session', // In a real app, this would be unique per user
      });

      setMessages((prev) => [
        ...prev,
        { type: 'bot', content: response.data.response },
      ]);
    } catch (error) {
      console.error('Error sending message:', error);
      setMessages((prev) => [
        ...prev,
        {
          type: 'bot',
          content: 'Sorry, I encountered an error. Please try again later.',
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container maxWidth="md" sx={{ height: 'calc(100vh - 100px)' }}>
      <Paper
        elevation={3}
        sx={{
          height: '100%',
          display: 'flex',
          flexDirection: 'column',
          overflow: 'hidden',
        }}
      >
        <Box
          sx={{
            p: 2,
            bgcolor: 'primary.main',
            color: 'white',
          }}
        >
          <Typography variant="h6">Chat with Government Schemes Bot</Typography>
        </Box>

        <Box
          sx={{
            flex: 1,
            overflow: 'auto',
            p: 2,
            display: 'flex',
            flexDirection: 'column',
            gap: 2,
          }}
        >
          {messages.map((message, index) => (
            <Box
              key={index}
              sx={{
                alignSelf: message.type === 'user' ? 'flex-end' : 'flex-start',
                maxWidth: '70%',
              }}
            >
              <Paper
                elevation={1}
                sx={{
                  p: 2,
                  bgcolor: message.type === 'user' ? 'primary.light' : 'grey.100',
                  color: message.type === 'user' ? 'white' : 'text.primary',
                }}
              >
                <Typography>{message.content}</Typography>
              </Paper>
            </Box>
          ))}
          {loading && (
            <Box sx={{ alignSelf: 'flex-start' }}>
              <CircularProgress size={20} />
            </Box>
          )}
          <div ref={messagesEndRef} />
        </Box>

        <Box
          component="form"
          onSubmit={handleSend}
          sx={{
            p: 2,
            bgcolor: 'background.paper',
            borderTop: 1,
            borderColor: 'divider',
            display: 'flex',
            gap: 1,
          }}
        >
          <TextField
            fullWidth
            variant="outlined"
            placeholder="Type your message..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            disabled={loading}
            size="small"
          />
          <IconButton
            color="primary"
            type="submit"
            disabled={loading || !input.trim()}
          >
            <SendIcon />
          </IconButton>
        </Box>
      </Paper>
    </Container>
  );
}

export default Chatbot; 