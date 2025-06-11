import React, { useState } from 'react';
import { AppBar, Toolbar, Typography, Button, IconButton, Menu, MenuItem } from '@mui/material';
import { AccountCircle } from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import Login from './Login';

function Navbar() {
  const navigate = useNavigate();
  const [anchorEl, setAnchorEl] = useState(null);
  const [loginOpen, setLoginOpen] = useState(false);
  const [user, setUser] = useState(null);

  const handleMenu = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  const handleLogin = (userData) => {
    setUser(userData);
    setLoginOpen(false);
  };

  const handleLogout = () => {
    setUser(null);
    handleClose();
  };

  return (
    <>
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            Govt Scheme Chatbot
          </Typography>
          <Button color="inherit" onClick={() => navigate('/')}>Home</Button>
          <Button color="inherit" onClick={() => navigate('/chatbot')}>Chatbot</Button>
          <Button color="inherit" onClick={() => navigate('/schemes')}>Schemes</Button>
          {user?.role === 'admin' && (
            <Button color="inherit" onClick={() => navigate('/admin')}>Admin</Button>
          )}
          {user ? (
            <>
              <IconButton
                size="large"
                onClick={handleMenu}
                color="inherit"
              >
                <AccountCircle />
              </IconButton>
              <Menu
                anchorEl={anchorEl}
                open={Boolean(anchorEl)}
                onClose={handleClose}
              >
                <MenuItem onClick={handleLogout}>Logout</MenuItem>
              </Menu>
            </>
          ) : (
            <Button color="inherit" onClick={() => setLoginOpen(true)}>Login</Button>
          )}
        </Toolbar>
      </AppBar>
      <Login open={loginOpen} onClose={() => setLoginOpen(false)} onLogin={handleLogin} />
    </>
  );
}

export default Navbar; 