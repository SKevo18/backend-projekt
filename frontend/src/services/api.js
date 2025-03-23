import axios from 'axios'

const instance = axios.create({
  baseURL: 'https://some-domain.com/api/',
    headers: {
        'Content-Type': 'aplication/json'
    },
    timeout: 10000

});

