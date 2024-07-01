<template>
    <div>
        <h1>Create a product</h1>
        <form>
            <input type="text" placeholder="name for the Product" v-model="this.name"><br><br>
            <input type="text" placeholder="description for the Product" v-model="this.desc"><br><br>
            <input type="number" placeholder="price for the Product" v-model="this.price"><br><br>
            <input type="number" placeholder="stock for the Product" v-model="this.stock"><br><br>
            <label for="cars">Choose a category:</label>
            <select name="cars" id="cars" v-model="this.category_id">
                <option v-for="cate in category" :key="cate.id" :value="cate.id">{{ cate.name }}</option>
            </select><br><br>

            <input type="file" @change="addFile">

            <button type="button" @click="addProduct">Submit</button>
        </form>
        <!-- {{ this.category }} -->
    </div>
</template>

<script>
import axios from 'axios';
export default{
    name: 'addProduct',
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
        img: null       
       } 
    },
    created(){
        this.token = localStorage.getItem('authToken')
        if(!this.token){
            this.$router.push('/login')
        }else{
          this.fetchCategory();  
        }
        
    },
    methods: {
        addFile(e) {
            this.img = e.target.files[0];
            console.log(this.img);
        },
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
        addProduct(){
            let formData = new FormData();
            formData.append('name', this.name)
            formData.append('description', this.desc)
            formData.append('stock', this.stock)
            formData.append('price', this.price) 
            formData.append('category_id', this.category_id)
            formData.append('img', this.img)
            axios
            .post('http://localhost:5000/api/product', formData,
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