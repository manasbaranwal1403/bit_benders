import React, { useState } from 'react';
import {
    Dialog,
    DialogTitle,
    DialogContent,
    DialogActions,
    TextField,
    Button,
    Alert,
    Box,
    Link
} from '@mui/material';
import axios from 'axios';
import PasswordReset from './PasswordReset';

const Login = ({ open, onClose, onLogin }) => {
    const [mode, setMode] = useState('login');
    const [formData, setFormData] = useState({
        username: '',
        email: '',
        password: ''
    });
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);
    const [showPasswordReset, setShowPasswordReset] = useState(false);

    const handleInputChange = (e) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value
        });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        setLoading(true);

        try {
            if (mode === 'login') {
                const response = await axios.post('/api/auth/login', {
                    email: formData.email,
                    password: formData.password
                });
                onLogin(response.data);
                onClose();
            } else {
                await axios.post('/api/auth/register', formData);
                setMode('login');
                setFormData({ username: '', email: '', password: '' });
            }
        } catch (err) {
            setError(err.response?.data?.message || 'An error occurred. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    const toggleMode = () => {
        setMode(mode === 'login' ? 'register' : 'login');
        setError('');
        setFormData({ username: '', email: '', password: '' });
    };

    return (
        <>
            <Dialog open={open} onClose={onClose} maxWidth="sm" fullWidth>
                <DialogTitle>
                    {mode === 'login' ? 'Login' : 'Register'}
                </DialogTitle>
                <DialogContent>
                    <Box component="form" onSubmit={handleSubmit} sx={{ mt: 2 }}>
                        {error && (
                            <Alert severity="error" sx={{ mb: 2 }}>
                                {error}
                            </Alert>
                        )}
                        
                        {mode === 'register' && (
                            <TextField
                                fullWidth
                                label="Username"
                                name="username"
                                value={formData.username}
                                onChange={handleInputChange}
                                required
                                margin="normal"
                            />
                        )}
                        <TextField
                            fullWidth
                            label="Email"
                            name="email"
                            type="email"
                            value={formData.email}
                            onChange={handleInputChange}
                            required
                            margin="normal"
                        />
                        <TextField
                            fullWidth
                            label="Password"
                            name="password"
                            type="password"
                            value={formData.password}
                            onChange={handleInputChange}
                            required
                            margin="normal"
                        />
                        {mode === 'login' && (
                            <Box sx={{ mt: 1, textAlign: 'right' }}>
                                <Link
                                    component="button"
                                    variant="body2"
                                    onClick={() => setShowPasswordReset(true)}
                                >
                                    Forgot Password?
                                </Link>
                            </Box>
                        )}
                    </Box>
                </DialogContent>
                <DialogActions>
                    <Button onClick={toggleMode}>
                        {mode === 'login' ? 'Need an account? Register' : 'Already have an account? Login'}
                    </Button>
                    <Button
                        onClick={handleSubmit}
                        variant="contained"
                        disabled={loading}
                    >
                        {loading ? 'Processing...' : mode === 'login' ? 'Login' : 'Register'}
                    </Button>
                </DialogActions>
            </Dialog>

            <PasswordReset
                open={showPasswordReset}
                onClose={() => setShowPasswordReset(false)}
                mode="request"
            />
        </>
    );
};

export default Login; 