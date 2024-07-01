<template>
    <div>
        <h1>Edit a category with id: {{ this.id }}</h1>
        <form>
            <input type="text" placeholder="name for the category" v-model="this.name"><br><br>
            <input type="text" placeholder="description for the category" v-model="this.desc"><br><br>
            <button type="button" @click="addCategory()">Submit</button> | <button onclick="history.back()"> cancel</button>
        </form>
        {{ this.message }}
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
        message: null,
        id: null        
       } 
    },
    created(){
        this.id = this.$route.params.id;
        this.token = localStorage.getItem('authToken')
        if(!this.token){
            this.$router.push('/login')
        }
        this.fetchCategory()
    },
    methods: {
        addCategory(){
            axios
            .put(`http://localhost:5000/api/category/${this.id}`,
                {
                    name: this.name,
                    description: this.desc
                },
                {headers :{Authorization: `${this.token}` },}  
            )
            .then(response => {
                this.message = response.data.message
                if (response.status == 201){
                   this.message = response.data;
                   if (response.data.status == 'SUCCESS'){
                    alert
                   }
                   this.$router.push('/') 
                }                
            })
            .catch(error => {
                console.log(error);
            })
        },
        fetchCategory(){
            axios
            .get(`http://localhost:5000/api/category/${this.id}`,
            {headers :{Authorization: `${this.token}`},}  
            )
            .then(response => {
                if (response.status == 200){
                   this.name = response.data.data.name,
                   this.desc = response.data.data.description,
                   console.log(response);
                    console.log('category: '+this.category);
            }                
        })
            .catch(error => {
                console.log(error);
            })
        },
    }
}
</script>