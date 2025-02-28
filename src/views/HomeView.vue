<template>
    <div class="home">
      <div class="hero">
        <h1>Welcome to MyApp!</h1>
        <p>Super-Duper-2025-Backend-Project-Initial-GitHub-Europe-Herous-Commit.</p>
        <router-link to="/login" class="btn">Login</router-link>
        <router-link to="/register" class="btn btn-alt">Registration</router-link>
      </div>
    </div>
  </template>
  
  <script setup>
  </script>
  
  <style scoped>
  .home {
    display: flex;
    justify-content: center;
    align-items: center;
    height: calc(100vh);
    text-align: center;
    background: linear-gradient(to right, #007bff, #00c6ff);
    color: white;
  }
  
  .hero {
    max-width: 600px;
    padding: 20px;
  }
  
  h1 {
    font-size: 2.5rem;
    margin-bottom: 10px;
  }
  
  p {
    font-size: 1.2rem;
    margin-bottom: 20px;
  }
  
  .btn {
    display: inline-block;
    margin: 10px;
    padding: 10px 20px;
    font-size: 1.2rem;
    color: white;
    background: #28a745;
    border-radius: 5px;
    text-decoration: none;
    transition: 0.3s;
  }
  
  .btn-alt {
    background: #ff9800;
  }
  
  .btn:hover {
    opacity: 0.8;
  }
  </style>
  