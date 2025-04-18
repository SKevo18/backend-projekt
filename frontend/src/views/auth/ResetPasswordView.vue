<script lang="ts" setup>
import { ref } from "vue";
import { useRoute, useRouter } from "vue-router";
import api from "@/services/api";

const route = useRoute();
const router = useRouter();

const password = ref<string>("");
const confirmPassword = ref<string>("");
const message = ref<string>("");
const error = ref<string>("");

const token = route.query.token as string;

const handlePasswordReset = async () => {
    message.value = "";
    error.value = "";

    if (!password.value || !confirmPassword.value) {
        error.value = "Zadajte prosím obe heslá.";
        return;
    }

    if (password.value !== confirmPassword.value) {
        error.value = "Heslá sa nezhodujú.";
        return;
    }

    try {
        await api.post("/email/password_update", {
            token,
            new_password: password.value,
        }, {
            headers: {
                'Content-Type': 'application/json',
            }
        });

        message.value = "Heslo bolo úspešne zmenené.";
        setTimeout(() => {
            router.push("/login");
        }, 2000);
    } catch (err: any) {
        error.value = err.response?.data?.detail || "Chyba pri zmene hesla.";
    }
};
</script>

<template>
    <div class="auth-form-container">
        <form @submit.prevent="handlePasswordReset" class="auth-form">
            <fieldset>
                <legend>Zmena hesla</legend>

                <div class="form-group">
                    <label for="password">Heslo</label>
                    <input type="password" id="password" v-model="password" />
                </div>

                <div class="form-group">
                    <label for="confirmPassword">Potvrdenie hesla</label>
                    <input type="password" id="confirmPassword" v-model="confirmPassword" />
                </div>

                <button type="submit" class="button button-green">Zmeniť heslo</button>

                <p v-if="message" class="text-green-600 mt-2">{{ message }}</p>
                <p v-if="error" class="text-red-600 mt-2">{{ error }}</p>
            </fieldset>
        </form>
    </div>
</template>

<style>
@import "./auth_form.css";
</style>
