<template>
    <div class="register">
      <h1>This is a register page</h1>
      <form>
        <label for="username">email:</label>
        <input type="text" id="username" name="username" v-model="this.email"><br>
        <label for="password">Password:</label>
        <input type="password" id="password" name="password" v-model="this.password"><br>
        <label for="roles">Choose a role:</label>

        <select name="roles" id="roles" v-model="this.role">
        <option value="manager">manager</option>
        <option value="customer">customer</option>
        </select>
        <button type="button" @click="register_fn">Login</button>
      </form>
    </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'register',
  data() {
    return {
      email: '',
      password: '',
      role: ''

    }
  },
  methods: {
    register_fn() {
      axios
      .post('http://localhost:5000/api/register', {
        email: this.email,
        password: this.password,
        role: this.role
      })
      .then(response => {
        console.log(response.data.message);
        console.log(response);
        if (response.status == 200) {
            this.$router.push('/login');
        }
        }
      )
      .catch(error => {
        console.log('catched error: '+ error);
      });

    }
}
}
</script>