import React, { useState } from 'react';
import {
    Dialog,
    DialogTitle,
    DialogContent,
    DialogActions,
    TextField,
    Button,
    Alert,
    Box
} from '@mui/material';
import api from '../utils/api';

const PasswordReset = ({ open, onClose, mode = 'request' }) => {
    const [email, setEmail] = useState('');
    const [token, setToken] = useState('');
    const [newPassword, setNewPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    const [error, setError] = useState('');
    const [success, setSuccess] = useState('');
    const [loading, setLoading] = useState(false);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        setSuccess('');
        setLoading(true);

        try {
            if (mode === 'request') {
                await api.post('/auth/request-reset', { email });
                setSuccess('If an account exists with this email, you will receive a password reset link.');
                setEmail('');
            } else {
                if (newPassword !== confirmPassword) {
                    setError('Passwords do not match!');
                    return;
                }
                await api.post('/auth/reset-password', {
                    token,
                    new_password: newPassword
                });
                setSuccess('Password has been reset successfully!');
                setToken('');
                setNewPassword('');
                setConfirmPassword('');
                setTimeout(() => onClose(), 2000);
            }
        } catch (err) {
            setError(err.response?.data?.message || 'An error occurred. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <Dialog open={open} onClose={onClose} maxWidth="sm" fullWidth>
            <DialogTitle>
                {mode === 'request' ? 'Request Password Reset' : 'Reset Password'}
            </DialogTitle>
            <DialogContent>
                <Box component="form" onSubmit={handleSubmit} sx={{ mt: 2 }}>
                    {error && (
                        <Alert severity="error" sx={{ mb: 2 }}>
                            {error}
                        </Alert>
                    )}
                    {success && (
                        <Alert severity="success" sx={{ mb: 2 }}>
                            {success}
                        </Alert>
                    )}
                    
                    {mode === 'request' ? (
                        <TextField
                            fullWidth
                            label="Email"
                            type="email"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            required
                            margin="normal"
                        />
                    ) : (
                        <>
                            <TextField
                                fullWidth
                                label="Reset Token"
                                value={token}
                                onChange={(e) => setToken(e.target.value)}
                                required
                                margin="normal"
                            />
                            <TextField
                                fullWidth
                                label="New Password"
                                type="password"
                                value={newPassword}
                                onChange={(e) => setNewPassword(e.target.value)}
                                required
                                margin="normal"
                            />
                            <TextField
                                fullWidth
                                label="Confirm Password"
                                type="password"
                                value={confirmPassword}
                                onChange={(e) => setConfirmPassword(e.target.value)}
                                required
                                margin="normal"
                            />
                        </>
                    )}
                </Box>
            </DialogContent>
            <DialogActions>
                <Button onClick={onClose}>Cancel</Button>
                <Button
                    onClick={handleSubmit}
                    variant="contained"
                    disabled={loading}
                >
                    {loading ? 'Processing...' : mode === 'request' ? 'Send Reset Link' : 'Reset Password'}
                </Button>
            </DialogActions>
        </Dialog>
    );
};

export default PasswordReset; 