import React, { useState, useEffect } from 'react';
import {
  Container,
  Grid,
  Card,
  CardContent,
  Typography,
  TextField,
  Box,
  Chip,
  CircularProgress,
  Alert,
  Button,
} from '@mui/material';
import SearchIcon from '@mui/icons-material/Search';
import axios from 'axios';

function SchemeDirectory() {
  const [schemes, setSchemes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [page, setPage] = useState(1);
  const [hasMore, setHasMore] = useState(true);

  const fetchSchemes = async (query = '') => {
    try {
      setLoading(true);
      const url = query
        ? `http://localhost:5000/api/schemes/search?q=${query}`
        : `http://localhost:5000/api/schemes?page=${page}&limit=10`;
      
      const response = await axios.get(url);
      const newSchemes = response.data.data;
      
      if (query) {
        setSchemes(newSchemes);
      } else {
        setSchemes((prev) => [...prev, ...newSchemes]);
      }
      
      setHasMore(newSchemes.length === 10);
      setError(null);
    } catch (error) {
      console.error('Error fetching schemes:', error);
      setError('Failed to load schemes. Please try again later.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchSchemes();
  }, [page]);

  const handleSearch = (e) => {
    e.preventDefault();
    setPage(1);
    fetchSchemes(searchQuery);
  };

  const handleLoadMore = () => {
    setPage((prev) => prev + 1);
  };

  return (
    <Container maxWidth="lg">
      <Box sx={{ my: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          Government Schemes Directory
        </Typography>

        <Box
          component="form"
          onSubmit={handleSearch}
          sx={{ mb: 4, display: 'flex', gap: 1 }}
        >
          <TextField
            fullWidth
            variant="outlined"
            placeholder="Search schemes..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            size="small"
          />
          <Button
            type="submit"
            variant="contained"
            startIcon={<SearchIcon />}
            disabled={loading}
          >
            Search
          </Button>
        </Box>

        {error && (
          <Alert severity="error" sx={{ mb: 2 }}>
            {error}
          </Alert>
        )}

        <Grid container spacing={3}>
          {schemes.map((scheme) => (
            <Grid item xs={12} md={6} key={scheme._id}>
              <Card>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    {scheme.name}
                  </Typography>
                  <Typography
                    variant="body2"
                    color="text.secondary"
                    paragraph
                  >
                    {scheme.description}
                  </Typography>
                  <Box sx={{ mb: 2 }}>
                    <Chip
                      label={scheme.category}
                      size="small"
                      sx={{ mr: 1 }}
                    />
                    <Chip
                      label={scheme.status}
                      size="small"
                      color={scheme.status === 'active' ? 'success' : 'default'}
                    />
                  </Box>
                  <Typography variant="body2" color="text.secondary">
                    <strong>Eligibility:</strong> {scheme.eligibility}
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>

        {loading && (
          <Box sx={{ display: 'flex', justifyContent: 'center', my: 4 }}>
            <CircularProgress />
          </Box>
        )}

        {!loading && hasMore && !searchQuery && (
          <Box sx={{ display: 'flex', justifyContent: 'center', my: 4 }}>
            <Button
              variant="outlined"
              onClick={handleLoadMore}
              disabled={loading}
            >
              Load More
            </Button>
          </Box>
        )}

        {!loading && schemes.length === 0 && (
          <Alert severity="info">
            No schemes found. Try a different search query or check back later.
          </Alert>
        )}
      </Box>
    </Container>
  );
}

export default SchemeDirectory; 