import React, { useState, useEffect } from 'react';
import { Input, Button } from 'antd';
import '../styles/searchPageStyles.css';

const { Search } = Input;

const SearchPage = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState([]);

  const handleSearch = () => {
    if (!searchQuery.trim()) {
      setSearchResults([]);
      return;
    }

    fetch('/search', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ query: searchQuery }),
    })
      .then((response) => response.json())
      .then((data) => {
        setSearchResults(data.results || []);
      })
      .catch((error) => {
        console.error('Error searching:', error);
        setSearchResults([]);
      });
  };

  return (
    <div className="search-container">
      <h1>Search Videos</h1>
      <Search
        placeholder="Enter your search query"
        value={searchQuery}
        onChange={(e) => setSearchQuery(e.target.value)}
        onSearch={handleSearch}
        enterButton={<Button type="primary">Search</Button>}
        className="search-input"
      />

      <div className="video-grid">
        {searchResults.length > 0 ? (
          searchResults.map((video, index) => (
            <div key={index} className="video-item">
              <video controls>
                <source src={`/uploads/${video}`} type="video/mp4" />
                Your browser does not support the video tag.
              </video>
            </div>
          ))
        ) : (
          <p className="no-results">No videos found. Try a different query.</p>
        )}
      </div>
    </div>
  );
};

export default SearchPage;
