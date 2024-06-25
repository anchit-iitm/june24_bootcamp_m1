<template>
 <h1>admin dashboard</h1>
 <table>
    <thead>
        <tr>
            <th>id</th>
            <th>name</th>
            <th>description</th>
            <th>status</th>
            <th>Actions</th>
        </tr>       
    </thead>
    <tbody>
        <tr v-for="cate in category" :key="cate.id">
            <td>{{ cate.id }}</td>
            <td>{{ cate.name }}</td>
            <td>{{ cate.description }}</td>
            <td>{{ cate.status }} | {{ cate.delete }}</td>         
            <td><router-link :to="{name:'updateCategory', params: {id: cate.id}}">Update</router-link> | <button v-if="!cate.delete" type="button" @click="deletecate(cate.id)">delete</button></td>

        </tr>        
    </tbody>    
 </table>
 <table>
    <thead>
        <tr>
            <th>id</th>
            <th>name</th>
            <th>description</th>
            <th>status</th>
        </tr>       
    </thead>
    <tbody>
        <tr v-for="cate in products" :key="cate.id">
            <td>{{ cate.id }}</td>
            <td>{{ cate.name }}</td>
            <td>{{ cate.description }}</td>
            <td>{{ cate.status }}</td>
            <td><img :src="`http://localhost:8000/${cate.id}.jpg`" alt="" weidth="20" height="20"></td>
        </tr>        
    </tbody>    
 </table>
</template>

<script>
import axios from 'axios';
export default{
    name: 'admindashboard',
    data() {
       return{
        name: null,
        desc: null,
        price: null,
        stock: null,
        token: null,
        message: null,
        category: [],
        category_id: null,
        products: []       
       } 
    },
    created(){
        this.token = localStorage.getItem('authToken')
        if(!this.token){
            this.$router.push('/login')
        }else{
          this.fetchCategory(); 
          this.fetchProduct(); 
        }
        
    },
    methods: {
        fetchCategory(){
            axios
            .get('http://localhost:5000/api/category',
            {headers :{Authorization: `${this.token}`},}  
            )
            .then(response => {
                if (response.status == 200){
                   this.category = response.data.data,
                   console.log(response);
                    console.log('category: '+this.category);
            }                
        })
            .catch(error => {
                console.log(error);
            })
        },
        fetchProduct(){
            axios
            .get('http://localhost:5000/api/product',
            {headers :{Authorization: `${this.token}`},}  
            )
            .then(response => {
                if (response.status == 200){
                   this.products = response.data.data,
                   console.log(response);
                    console.log('category: '+this.products);
            }                
        })
            .catch(error => {
                console.log(error);
            })
        },
        deletecate(id){
            axios
            .delete(`http://localhost:5000/api/category/${id}`,
            {headers :{Authorization: `${this.token}`},}  
            )
            .then(response => {
                if (response.status == 201){
                   console.log(response);
                   this.fetchCategory()
            }                
        })
            .catch(error => {
                console.log(error);
            }) 
        }
    }
}
</script>
