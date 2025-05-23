<script lang="ts">
import { defineComponent } from "vue";
import api from "@/services/api";

import { useAuthStore } from "@/store/authStore";

interface UserProfile {
  title_before_name: string;
  title_after_name: string;
  first_name: string;
  middle_name: string;
  last_name: string;
  user_email: string;
}

import TurnstileComponent from "@/components/TurnstileComponent.vue";

export default defineComponent({
  components: {
    TurnstileComponent,
  },
  data() {
    return {
      profileData: {
        title_before_name: "",
        title_after_name: "",
        first_name: "",
        middle_name: "",
        last_name: "",
        user_email: "",
      } as UserProfile,
      isEditing: false,
      message: "",
      error: "",
      passwordResetMessage: "",
      authStore: useAuthStore(),
      turnstileRef: null,
    };
  },
  methods: {
    toggleEdit() {
      this.isEditing = !this.isEditing;
      if (!this.isEditing) {
        this.loadUserProfile();
      }
    },

    async loadUserProfile() {
      try {
        const response = await api.get<UserProfile>("/authentication/me");
        this.profileData = {
          title_before_name: response.data.title_before_name || "",
          title_after_name: response.data.title_after_name || "",
          first_name: response.data.first_name || "",
          middle_name: response.data.middle_name || "",
          last_name: response.data.last_name || "",
          user_email: response.data.user_email || "",
        };
      } catch (err) {
        this.error = "Failed to load profile information";
        console.error(err);
      }
    },

    async updateProfile() {
      try {
        let withoutEmail = this.profileData;
        delete withoutEmail.user_email;
        await api.post("/authentication/update_profile", withoutEmail);
        this.message = "Profile updated successfully";
        this.isEditing = false;
        setTimeout(() => {
          this.message = "";
        }, 3000);
      } catch (err) {
        this.error = "Failed to update profile";
        console.error(err);
        setTimeout(() => {
          this.error = "";
        }, 3000);
      }
    },

    async requestPasswordReset() {
      try {
        const turnstileComponent = this.$refs.turnstileRef;
        if (!turnstileComponent?.hasToken && turnstileComponent?.siteKey) {
          this.error = "Please complete the CAPTCHA verification.";
          setTimeout(() => {
            this.error = "";
          }, 3000);
          return;
        }

        await api.post("/email/password_reset", {
          email: this.profileData.user_email,
          turnstile_token: turnstileComponent?.getToken() || "",
        });
        this.passwordResetMessage = "Password reset link sent to your email";
        setTimeout(() => {
          this.passwordResetMessage = "";
        }, 3000);
      } catch (err) {
        this.error = "Failed to send password reset link";
        console.error(err);
        setTimeout(() => {
          this.error = "";
        }, 3000);
      }
    },

    async deleteAccount() {
      if (
        !confirm(
          "Are you sure you want to delete your account? This action cannot be undone."
        )
      ) {
        return;
      }

      try {
        if (!this.authStore.token) {
          this.error = "Failed to get authentication token";
          return;
        }

        await api.delete("/user/me", {
          headers: {
            Authorization: `Bearer ${this.authStore.token}`,
          },
        });

        this.authStore.logout();
        this.message = "Your account has been successfully deleted";
        setTimeout(() => {
          window.location.href = "/";
        }, 2000);
      } catch (err: any) {
        console.error("Delete account error details:", {
          status: err.response?.status,
          data: err.response?.data,
          headers: err.response?.headers,
          config: err.config,
        });
        this.error = err.response?.data?.detail || "Error deleting account";
        setTimeout(() => {
          this.error = "";
        }, 3000);
      }
    },
  },
  mounted() {
    this.authStore.loadSavedToken();
    this.loadUserProfile();
  },
});
</script>

<template>
  <div class="profile-container">
    <h1 class="profile-title">Your Profile</h1>

    <div class="profile-section">
      <div class="actions-row">
        <button
          @click="toggleEdit"
          class="button"
          :class="isEditing ? 'button-red' : 'button-green'"
        >
          {{ isEditing ? "Cancel" : "Edit Profile" }}
        </button>
      </div>

      <form @submit.prevent="updateProfile" class="profile-form">
        <fieldset>
          <legend>Personal Information</legend>

          <div class="form-group">
            <label for="title_before_name">Title before name</label>
            <input
              type="text"
              id="title_before_name"
              v-model="profileData.title_before_name"
              :disabled="!isEditing"
            />
          </div>

          <div class="form-group">
            <label for="title_after_name">Title after name</label>
            <input
              type="text"
              id="title_after_name"
              v-model="profileData.title_after_name"
              :disabled="!isEditing"
            />
          </div>

          <div class="form-group">
            <label for="first_name">First Name</label>
            <input
              type="text"
              id="first_name"
              v-model="profileData.first_name"
              :disabled="!isEditing"
            />
          </div>

          <div class="form-group">
            <label for="middle_name">Middle Name</label>
            <input
              type="text"
              id="middle_name"
              v-model="profileData.middle_name"
              :disabled="!isEditing"
            />
          </div>

          <div class="form-group">
            <label for="last_name">Last Name</label>
            <input
              type="text"
              id="last_name"
              v-model="profileData.last_name"
              :disabled="!isEditing"
            />
          </div>

          <div class="form-group">
            <label for="user_email">Email</label>
            <input
              type="email"
              id="user_email"
              v-model="profileData.user_email"
              disabled
            />
          </div>

          <button v-if="isEditing" type="submit" class="button button-green">
            Save Changes
          </button>
        </fieldset>
      </form>

      <div v-if="message" class="message success">{{ message }}</div>
      <div v-if="error" class="message error">{{ error }}</div>

      <div class="password-reset-section">
        <h2>Password Management</h2>
        <p class="mb-4">Want to change your password?</p>
        <TurnstileComponent ref="turnstileRef" />
        <button @click="requestPasswordReset" class="button button-yellow mt-4">
          Send Password Reset Link
        </button>
        <div v-if="passwordResetMessage" class="message success mt-4">
          {{ passwordResetMessage }}
        </div>
      </div>

      <div class="account-deletion-section">
        <h2>Account Management</h2>
        <p class="mb-4 text-red-600">
          Warning: Account deletion is an irreversible process.
        </p>
        <div class="flex justify-center">
          <button @click="deleteAccount" class="button button-red">
            Delete My Account
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style>
@import "tailwindcss";

.profile-container {
  @apply max-w-3xl mx-auto p-4;
}

.profile-title {
  @apply text-2xl font-bold text-green-800 mb-4;
}

.profile-section {
  @apply bg-white p-6 rounded shadow;
}

.profile-form {
  @apply mb-8;
}

.actions-row {
  @apply flex justify-end mb-4;
}

.form-group {
  @apply mb-4;
}

.form-group label {
  @apply block text-gray-700 mb-1;
}

.form-group input {
  @apply w-full p-2 border border-gray-300 rounded;
}

.form-group input:disabled {
  @apply bg-gray-100;
}

.button {
  @apply px-4 py-2 font-bold rounded cursor-pointer;
}

.button-green {
  @apply bg-green-600 text-white hover:bg-green-700;
}

.button-red {
  @apply bg-red-600 text-white hover:bg-red-700;
}

.button-yellow {
  @apply bg-yellow-500 text-white hover:bg-yellow-600;
}

.message {
  @apply p-2 mb-4 rounded;
}

.success {
  @apply bg-green-100 text-green-800 border border-green-200;
}

.error {
  @apply bg-red-100 text-red-800 border border-red-200;
}

.password-reset-section {
  @apply mt-8 pt-4 border-t;
}

.password-reset-section h2 {
  @apply text-xl font-bold text-green-800 mb-2;
}

.account-deletion-section {
  @apply mt-8 pt-4 border-t;
}

.account-deletion-section h2 {
  @apply text-xl font-bold text-red-800 mb-2;
}
</style>
