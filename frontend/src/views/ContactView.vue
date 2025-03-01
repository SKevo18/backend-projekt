<template>
  <!-- header -->
  <div class="contact-header">
    <div class="contact-header-text">KONTAKT</div>
  </div>

  <!-- this is main container -->
  <div class="contact-container">
    <h2 class="contact-subheading">KONTAKTUJTE NÁS</h2>

    <!-- contact cards -->
    <div class="contact-cards">
      <div v-for="contact in contacts" :key="contact.name" class="contact-card">
        <img :src="contact.image" alt="Profile" class="contact-image" />
        <h3 class="contact-name">{{ contact.name }}</h3>
        <p class="contact-role">Organizátor</p>
        <p class="contact-phone">{{ contact.phone }}</p>
        <a :href="contact.email" class="contact-email">{{ contact.email }}</a>
      </div>
    </div>
  </div>


  <!-- Ak chceme používať Google Maps bez cookies (čo znamená, že nevyužívate dynamické zobrazenie mapy cez Google Maps JavaScript API),
    problémom môže byť niekoľko vecí. 
    Dostal som si: "Chrome is moving towards a new experience that allows users to choose to browse without third-party cookies." -->
  <div class="google-map">
    <iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d38630.23096179409!2d18.075449189646186!3d48.30802355207554!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x476b3ee583e728a7%3A0xe70919ee435d2989!2sSlovak%20University%20of%20Agriculture%20in%20Nitra!5e0!3m2!1sen!2ssk!4v1740863499661!5m2!1sen!2ssk" width="600" height="450" style="border:0;" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
  </div>

  <div class="footer">
  <FooterComponent />
  </div>
  
</template>

<script>
import FooterComponent from "../components/FooterComponent.vue";
import kevinImage from "@/assets/kevin.jpg";
import romiImage from "@/assets/romi.jpg";

export default {
  components: {
    FooterComponent,
  },
  data() {
    return {
      contacts: [
        {
          name: "Kevin Kevinovič",
          phone: "+421 134 170 111",
          email: "kkevinovic@ukf.sk",
          image: kevinImage,
        },
        {
          name: "Roman Romanovič",
          phone: "+421 132 222 999",
          email: "rromanovic@ukf.sk",
          image: romiImage,
        },
      ],
    };
  },
};
</script>

<style scoped>
.contact-header {
  background-color: #1a1a1a;
  width: 100%; 
  display: flex;
  justify-content: center; 
  align-items: center;
  height: 15em; 
  padding: 20px 0; 
}

.contact-header-text {
  color: white;
  font-size: 40px;
  font-weight: bold;
  text-align: left; 
  width: 100%; 
  padding-left: 20rem;
}

.contact-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  background-color: #f3f4f6;
  padding: 70px 20px;
}

.contact-subheading {
  font-size: 24px;
  font-weight: bold;
  margin-top: 2rem;
}

.contact-cards {
  display: flex;
  gap: 50px;
  justify-content: center;
  flex-wrap: wrap;
}

.contact-card {
  background: white;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.15);
  border-radius: 12px;
  padding: 25px;
  text-align: center;
  width: 280px;
  transition: transform 0.2s ease-in-out;
}

.contact-card:hover {
  transform: translateY(-5px);
}

.contact-image {
  width: 120px;
  height: 120px;
  border-radius: 8px;
  object-fit: cover;
  margin: 10px 0;
}

.contact-name {
  font-size: 22px;
  font-weight: bold;
}

.contact-role {
  color: #666;
  font-size: 16px;
  margin-bottom: 8px;
}

.contact-phone {
  font-size: 16px;
  font-weight: 500;
  color: #333;
}

.contact-email {
  font-size: 16px;
  color: #007bff;
  text-decoration: none;
}

.contact-email:hover {
  text-decoration: underline;
}


.google-map {
  width: 100%;
  height: 300px; 
}

.google-map iframe {
  width: 100%;
  height: 100%;
  border: 0;
  object-fit: cover;
}
</style>

