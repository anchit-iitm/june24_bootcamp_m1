<template>
  <nav>
    <router-link to="/">Home</router-link> |
    <router-link to="/login">Login</router-link> |
    <router-link to="/register">Register</router-link> |
    <router-link :to="{name:'addCategory'}">addCategory</router-link> |
    <router-link :to="{name:'addProduct'}">addProduct</router-link> |
    <a @click="logout">Logout</a> |
    <router-link to="/about">About</router-link>

  </nav>
  <router-view/>
</template>

<script>
export default {
  methods: {
    logout() {
      // localStorage.removeItem('authtoken');
      // localStorage.removeItem('user_role');
      // localStorage.removeItem('user_email');
      // localStorage.removeItem('user_id');
      localStorage.clear();
    }
  }
  
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

nav {
  padding: 30px;
}

nav a {
  font-weight: bold;
  color: #2c3e50;
}

nav a.router-link-exact-active {
  color: #42b983;
}
</style>
