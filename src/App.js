import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import './App.css';
import Database from './components/Database/Database'; // Ensure this path is correct



function App() {
  return (
    <Router>
      <div className="App">
        <header className="App-header">
          <h1 className="App-title">DatabaseGenie</h1>
        </header>
        <div className="App-content">  {/* Ensure this div wraps around the Routes */}
          <Database />
        </div>
      </div>
    </Router>
  );
}


export default App;
