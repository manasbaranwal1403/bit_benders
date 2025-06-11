import React from 'react';
import { Container, Typography, Box, Button } from '@mui/material';
import { useNavigate } from 'react-router-dom';

function Home() {
  const navigate = useNavigate();

  return (
    <Container maxWidth="md">
      <Box sx={{ mt: 8, textAlign: 'center' }}>
        <Typography variant="h2" component="h1" gutterBottom>
          Welcome to Government Scheme Chatbot
        </Typography>
        <Typography variant="h5" component="h2" gutterBottom color="text.secondary">
          Your one-stop solution for government scheme information
        </Typography>
        <Box sx={{ mt: 4 }}>
          <Button
            variant="contained"
            color="primary"
            size="large"
            onClick={() => navigate('/chatbot')}
            sx={{ mr: 2 }}
          >
            Start Chat
          </Button>
          <Button
            variant="outlined"
            color="primary"
            size="large"
            onClick={() => navigate('/schemes')}
          >
            Browse Schemes
          </Button>
        </Box>
      </Box>
    </Container>
  );
}

export default Home; 