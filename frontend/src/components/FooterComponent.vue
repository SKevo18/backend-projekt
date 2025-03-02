<template>
  <footer class="footer">
    <div class="container">
      <div class="footer-section">
        <img
          src="@/assets/logo-nconnect.png"
          alt="nConnect Logo - Connecting IT Communities"
          class="logo"
        />
        <p class="tagline">Spájame IT komunity</p>
        <div class="social-links">
          <a href="#" class="icon"><i class="fab fa-facebook"></i></a>
          <a href="#" class="icon"><i class="fab fa-instagram"></i></a>
          <a href="#" class="icon"><i class="fab fa-linkedin"></i></a>
        </div>
      </div>
      <div class="footer-section">
        <p class="title">Študentské centrum UKF</p>
        <p>Dražovská 2 | Nitra</p>
        <p><a href="https://nconnect.sk/" class="link">info@nconnect.sk</a></p>
      </div>
      <div class="footer-section">
        <p class="title">Fakulta prírodných vied a informatiky</p>
        <p>Univerzita Konštantína Filozofa v Nitre</p>
        <p><a href="#" class="link">Ochrana osobných údajov</a></p>
      </div>
    </div>
    <div class="copyright">
      © 2025 nConnect | <a href="#" class="link">Terms of Service</a> |
      <a href="#" class="link">Privacy Policy</a>
    </div>
  </footer>
</template>

<script>
export default {
  name: "FooterComponent",
};
</script>

<style scoped>
.footer {
  background-color: #1e1e1e;
  color: white;
  padding: 40px 0;
  font-size: 16px;
  font-family: "Arial", "Helvetica", sans-serif;
}

.container {
  max-width: 1100px;
  margin: 0 auto;
  padding: 0 20px;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  flex-wrap: wrap;
}

.footer-section {
  flex: 1;
  min-width: 250px;
  text-align: left;
  margin-bottom: 20px;
}

.logo {
  height: 50px;
  margin-bottom: 15px;
  object-fit: contain;
}

.tagline {
  font-size: 20px;
  font-weight: 500;
  margin-bottom: 15px;
  font-style: italic;
  color: #bbb;
}

.social-links {
  display: flex;
  justify-content: flex-start;
  gap: 20px;
  margin-top: 15px;
}

.icon {
  color: white;
  font-size: 22px;
  text-decoration: none;
  transition: color 0.3s ease, transform 0.3s ease;
}

.icon:hover {
  color: #4a90e2;
  transform: scale(1.1);
}

.title {
  font-weight: 600;
  font-size: 20px;
  margin-bottom: 10px;
  color: #aaa;
}

.link {
  color: #4a90e2;
  text-decoration: none;
  font-size: 16px;
  font-weight: 500;
}

.link:hover {
  text-decoration: underline;
  color: #5c8fd0;
}

.copyright {
  text-align: center;
  font-size: 14px;
  margin-top: 30px;
  padding: 20px 0;
  border-top: 1px solid #444;
  color: #777;
}

.copyright a {
  color: #4a90e2;
  text-decoration: none;
}

.copyright a:hover {
  text-decoration: underline;
}

/* Mobile responsiveness */
@media (max-width: 768px) {
  .container {
    flex-direction: column;
    align-items: center;
  }
  .footer-section {
    text-align: center;
    margin-bottom: 15px;
  }
}
</style>
