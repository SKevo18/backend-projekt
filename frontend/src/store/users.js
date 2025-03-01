import { defineStore } from 'pinia';

export const useUsersStore = defineStore('users', {
    state: () => ({
        first_name: localStorage.getItem('first_name') || '',
        second_name: localStorage.getItem('second_name') || '',
        user_email: localStorage.getItem('user_email') || '',
        user_password: sessionStorage.getItem('user_password') || '',
}),

    actions: {
        setUsersData(data) {
            console.log('Setting user data:', data); // Логирование для отладки
        Object.keys(data).forEach((key) => {
            if (key in this) {
                this[key] = data[key];

            if (key === 'user_password') {
                sessionStorage.setItem(key, data[key]);
        } else {
            localStorage.setItem(key, data[key]);
        }
        }
    });
    },

    clearUsersData() {
      console.log('Clearing user data'); // Логирование для отладки
        Object.assign(this, {
            first_name: '',
            second_name: '',
            user_email: '',
            user_password: '',
        });

        ['first_name', 'second_name', 'user_email'].forEach(key => localStorage.removeItem(key));
        sessionStorage.removeItem('user_password');
    }
    }
});
