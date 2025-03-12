<template>
  <aside class="sidebar">
    <ul>
      <li>
        <router-link to="/">International Conference 2021</router-link>
      </li>
      <li>
        <router-link to="/">International Conference 2022</router-link>
      </li>
      <li>
        <router-link to="/">International Conference 2023</router-link>
      </li>
      <li>
        <router-link to="/">International Conference 2024</router-link>
      </li>
      <li>
        <router-link to="/">International Conference 2025</router-link>
      </li>
    </ul>
  </aside>
</template>

<style scoped>
.sidebar {
  width: 250px;
  height: 100vh;
  background: linear-gradient(to bottom, #2c3e50, #1a252f);
  color: white;
  display: flex;
  flex-direction: column;
  padding-top: 80px;
  /* anti nav bar */
  box-shadow: 3px 0 10px rgba(0, 0, 0, 0.2);
  left: 0;
  top: 0;
  overflow-y: auto;
  z-index: 999;
}

.sidebar ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.sidebar li {
  padding: 15px 20px;
  font-size: 1.1rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  transition: background 0.3s ease;
}

.sidebar li:hover {
  background: rgba(255, 255, 255, 0.1);
  cursor: pointer;
}

.sidebar a {
  text-decoration: none;
  color: white;
  display: flex;
  align-items: center;
  gap: 10px;
  font-weight: 500;
}

.sidebar a:hover {
  color: #f39c12;
}

.sidebar-icon {
  font-size: 1.3rem;
}
</style>
