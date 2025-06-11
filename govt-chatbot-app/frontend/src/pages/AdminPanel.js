import React, { useState, useEffect } from 'react';
import {
  Container,
  Typography,
  Box,
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  Grid,
  Paper,
  IconButton,
  Alert,
  CircularProgress,
} from '@mui/material';
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/Delete';
import AddIcon from '@mui/icons-material/Add';
import axios from 'axios';

function AdminPanel() {
  const [schemes, setSchemes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [openDialog, setOpenDialog] = useState(false);
  const [editingScheme, setEditingScheme] = useState(null);
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    eligibility: '',
    benefits: '',
    documents_required: '',
    application_process: '',
    website: '',
    contact_info: '',
    category: '',
    status: 'active',
  });

  useEffect(() => {
    fetchSchemes();
  }, []);

  const fetchSchemes = async () => {
    try {
      setLoading(true);
      const response = await axios.get('http://localhost:5000/api/schemes');
      setSchemes(response.data.data);
      setError(null);
    } catch (error) {
      console.error('Error fetching schemes:', error);
      setError('Failed to load schemes. Please try again later.');
    } finally {
      setLoading(false);
    }
  };

  const handleOpenDialog = (scheme = null) => {
    if (scheme) {
      setEditingScheme(scheme);
      setFormData(scheme);
    } else {
      setEditingScheme(null);
      setFormData({
        name: '',
        description: '',
        eligibility: '',
        benefits: '',
        documents_required: '',
        application_process: '',
        website: '',
        contact_info: '',
        category: '',
        status: 'active',
      });
    }
    setOpenDialog(true);
  };

  const handleCloseDialog = () => {
    setOpenDialog(false);
    setEditingScheme(null);
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (editingScheme) {
        await axios.put(
          `http://localhost:5000/api/schemes/${editingScheme._id}`,
          formData
        );
      } else {
        await axios.post('http://localhost:5000/api/schemes', formData);
      }
      handleCloseDialog();
      fetchSchemes();
    } catch (error) {
      console.error('Error saving scheme:', error);
      setError('Failed to save scheme. Please try again.');
    }
  };

  const handleDelete = async (schemeId) => {
    if (window.confirm('Are you sure you want to delete this scheme?')) {
      try {
        await axios.delete(`http://localhost:5000/api/schemes/${schemeId}`);
        fetchSchemes();
      } catch (error) {
        console.error('Error deleting scheme:', error);
        setError('Failed to delete scheme. Please try again.');
      }
    }
  };

  return (
    <Container maxWidth="lg">
      <Box sx={{ my: 4 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 4 }}>
          <Typography variant="h4" component="h1">
            Admin Panel
          </Typography>
          <Button
            variant="contained"
            startIcon={<AddIcon />}
            onClick={() => handleOpenDialog()}
          >
            Add New Scheme
          </Button>
        </Box>

        {error && (
          <Alert severity="error" sx={{ mb: 2 }}>
            {error}
          </Alert>
        )}

        {loading ? (
          <Box sx={{ display: 'flex', justifyContent: 'center', my: 4 }}>
            <CircularProgress />
          </Box>
        ) : (
          <Grid container spacing={3}>
            {schemes.map((scheme) => (
              <Grid item xs={12} key={scheme._id}>
                <Paper sx={{ p: 2 }}>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                    <Typography variant="h6">{scheme.name}</Typography>
                    <Box>
                      <IconButton
                        color="primary"
                        onClick={() => handleOpenDialog(scheme)}
                      >
                        <EditIcon />
                      </IconButton>
                      <IconButton
                        color="error"
                        onClick={() => handleDelete(scheme._id)}
                      >
                        <DeleteIcon />
                      </IconButton>
                    </Box>
                  </Box>
                  <Typography color="text.secondary" paragraph>
                    {scheme.description}
                  </Typography>
                  <Typography variant="body2">
                    <strong>Category:</strong> {scheme.category}
                  </Typography>
                  <Typography variant="body2">
                    <strong>Status:</strong> {scheme.status}
                  </Typography>
                </Paper>
              </Grid>
            ))}
          </Grid>
        )}

        <Dialog open={openDialog} onClose={handleCloseDialog} maxWidth="md" fullWidth>
          <DialogTitle>
            {editingScheme ? 'Edit Scheme' : 'Add New Scheme'}
          </DialogTitle>
          <DialogContent>
            <Box component="form" onSubmit={handleSubmit} sx={{ mt: 2 }}>
              <Grid container spacing={2}>
                <Grid item xs={12}>
                  <TextField
                    fullWidth
                    label="Scheme Name"
                    name="name"
                    value={formData.name}
                    onChange={handleInputChange}
                    required
                  />
                </Grid>
                <Grid item xs={12}>
                  <TextField
                    fullWidth
                    label="Description"
                    name="description"
                    value={formData.description}
                    onChange={handleInputChange}
                    multiline
                    rows={3}
                    required
                  />
                </Grid>
                <Grid item xs={12} md={6}>
                  <TextField
                    fullWidth
                    label="Eligibility"
                    name="eligibility"
                    value={formData.eligibility}
                    onChange={handleInputChange}
                    required
                  />
                </Grid>
                <Grid item xs={12} md={6}>
                  <TextField
                    fullWidth
                    label="Category"
                    name="category"
                    value={formData.category}
                    onChange={handleInputChange}
                    required
                  />
                </Grid>
                <Grid item xs={12}>
                  <TextField
                    fullWidth
                    label="Benefits"
                    name="benefits"
                    value={formData.benefits}
                    onChange={handleInputChange}
                    multiline
                    rows={2}
                    required
                  />
                </Grid>
                <Grid item xs={12}>
                  <TextField
                    fullWidth
                    label="Documents Required"
                    name="documents_required"
                    value={formData.documents_required}
                    onChange={handleInputChange}
                    multiline
                    rows={2}
                    required
                  />
                </Grid>
                <Grid item xs={12}>
                  <TextField
                    fullWidth
                    label="Application Process"
                    name="application_process"
                    value={formData.application_process}
                    onChange={handleInputChange}
                    multiline
                    rows={3}
                    required
                  />
                </Grid>
                <Grid item xs={12} md={6}>
                  <TextField
                    fullWidth
                    label="Website"
                    name="website"
                    value={formData.website}
                    onChange={handleInputChange}
                  />
                </Grid>
                <Grid item xs={12} md={6}>
                  <TextField
                    fullWidth
                    label="Contact Info"
                    name="contact_info"
                    value={formData.contact_info}
                    onChange={handleInputChange}
                  />
                </Grid>
              </Grid>
            </Box>
          </DialogContent>
          <DialogActions>
            <Button onClick={handleCloseDialog}>Cancel</Button>
            <Button onClick={handleSubmit} variant="contained">
              {editingScheme ? 'Update' : 'Create'}
            </Button>
          </DialogActions>
        </Dialog>
      </Box>
    </Container>
  );
}

export default AdminPanel; 