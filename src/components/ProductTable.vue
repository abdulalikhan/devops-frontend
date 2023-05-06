<template>
  <div class="product-table-container">
    <table>
      <thead>
        <tr>
          <th>Name</th>
          <th>Description</th>
          <th>Price</th>
          <th>Quantity</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="product in paginatedProducts" :key="product.id">
          <td>{{ product.name }}</td>
          <td>
            {{ product.description }}
          </td>
          <td>{{ product.price }}</td>
          <td>
            <input type="number" v-model.number="product.quantity" @change="updateQuantity(product)">
          </td>
          <td>
            <button @click="deleteProduct(product)">Delete</button>
          </td>
        </tr>
      </tbody>
    </table>

    <div class="pagination-controls">
      <button class="prev-button" @click="prevPage" :disabled="currentPage === 1">Prev</button>
      <span>{{ currentPage }} / {{ totalPages }}</span>
      <button class="next-button" @click="nextPage" :disabled="currentPage === totalPages">Next</button>
    </div>

    <div class="add-product-container">
      <h2>New Product</h2>
      <form @submit.prevent="addProduct">
        <div>
          <label for="name">Name:</label>
          <input type="text" id="name" v-model="newProduct.name">
        </div>
        <div>
          <label for="description">Description:</label>
          <input type="text" id="description" v-model="newProduct.description">
        </div>
        <div>
          <label for="price">Price:</label>
          <input type="text" id="price" v-model="newProduct.price" pattern="\d+(\.\d{1,2})?">
        </div>
        <div>
          <label for="quantity">Quantity:</label>
          <input type="number" id="quantity" v-model.number="newProduct.quantity">
        </div>
        <button class="add-product-button" type="submit">Add Product</button>
      </form>
    </div>
  </div>
</template>

<style src="./ProductTable.css"></style>

<script>
import axios from 'axios';

export default {
  name: 'ProductTable',
  data() {
    return {
      products: [],
      currentPage: 1,
      perPage: 5,
      totalProducts: 0,
      newProduct: {
        name: '',
        description: '',
        quantity: 0,
        price: 0.0,
      },
    };
  },
  mounted() {
    this.loadProducts();
  },
  methods: {
    async loadProducts() {
      const response = await axios.get('https://devops-backend-staging.azurewebsites.net/products');
      this.products = response.data;
      this.totalProducts = this.products.length;
    },
    async addProduct() {
      const response = await axios.post('https://devops-backend-staging.azurewebsites.net/products', this.newProduct);
      this.products.push(response.data);
      this.newProduct = {
        name: '',
        description: '',
        quantity: 0,
        price: 0.0,
      };
      await this.loadProducts();
    },
    nextPage() {
    if (this.currentPage < this.totalPages) {
      this.currentPage += 1;
    }
  },

  prevPage() {
    if (this.currentPage > 1) {
      this.currentPage -= 1;
    }
  },
    async updateQuantity(product) {
      const payload = { quantity: product.quantity };
      const response = await axios.patch(`https://devops-backend-staging.azurewebsites.net/products/${product.id}`, payload);
      const index = this.products.findIndex((p) => p.id === response.data.id);
      this.products.splice(index, 1, response.data);
    },

    async deleteProduct(product) {
      await axios.delete(`https://devops-backend-staging.azurewebsites.net/products/${product.id}`);
      const index = this.products.indexOf(product);
      this.products.splice(index, 1);
      await this.loadProducts();
    },

    paginate(products) {
      const start = (this.currentPage - 1) * this.perPage;
      const end = start + this.perPage;
      return products.slice(start, end);
    },

  },
  computed: {
    paginatedProducts() {
      return this.paginate(this.products);
    },
    totalPages() {
      return Math.ceil(this.totalProducts / this.perPage);
    },
    pageNumbers() {
      const numbers = [];
      for (let i = 1; i <= this.totalPages; i += 1) {
        numbers.push(i);
      }
      return numbers;
    },
  },
};
</script>
