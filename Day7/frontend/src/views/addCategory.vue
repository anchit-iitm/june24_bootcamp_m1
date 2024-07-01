<template>
    <div>
        <h1>Create a category</h1>
        <form>
            <input type="text" placeholder="name for the category" v-model="this.name"><br><br>
            <input type="text" placeholder="description for the category" v-model="this.desc"><br><br>
            <input type="file" name="" id="" >
            <button type="button" @click="addCategory">Submit</button>
        </form>
    </div>    
</template>

<script>
import axios from 'axios';
export default{
    name: 'addCategory',
    data() {
       return{
        name: null,
        desc: null,
        token: null,
        message: null        
       } 
    },
    created(){
        this.token = localStorage.getItem('authToken')
        if(!this.token){
            this.$router.push('/login')
        }
    },
    methods: {
        addCategory(){
            axios
            .post('http://localhost:5000/api/category',
                {
                    name: this.name,
                    description: this.desc
                },
                {headers :{Authorization: `${this.token}` },}  
            )
            .then(response => {
                if (response.status == 201){
                   this.message = response.data,
                   this.$router.push('/') 
                }                
            })
            .catch(error => {
                console.log(error);
            })
        }
    }
}
</script>