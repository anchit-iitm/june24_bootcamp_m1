<template>
    <div class="login">
      <h1>This is a login page</h1>
      <form>
        <label for="username">email:</label>
        <input type="text" id="username" name="username" v-model="this.email"><br>
        <label for="password">Password:</label>
        <input type="password" id="password" name="password" v-model="this.password"><br>
        
        <button type="button" @click="login_fn">Login</button>
      </form>
    </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'login',
  data() {
    return {
      email: '',
      password: ''
    }
  },
  methods: {
    login_fn() {
      console.log('Username: ' + this.email);
      console.log('Password: ' + this.password);
      axios
      .post('http://localhost:5000/api/login', {
        email: this.email,
        password: this.password
      })
      .then(response => {
        console.log(response.data.message);
        console.log(response);
        if (response.status == 200) {
          localStorage.setItem('authtoken', response.data.token);
          localStorage.setItem('user_role', response.data.role);
          localStorage.setItem('user_email', response.data.email);
          localStorage.setItem('user_id', response.data.id);
        }
        else {
          console.log('Login failed');
        }
      })
      .catch(error => {
        console.log(' catched error: '+ error);
      });
    }
}

}
</script>