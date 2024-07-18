<template>
    <div class="photo-gallery">
      <div v-for="(photo, index) in photos" :key="index" class="photo-item">
        <img :src="photo.url" :alt="photo.alt" @click="openLightbox(index)">
      </div>
      <div v-if="lightboxIndex !== -1" class="lightbox">
        <img :src="photos[lightboxIndex].url" :alt="photos[lightboxIndex].alt">
        <button @click="closeLightbox">Close</button>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        photos: [
          { url: 'path/to/photo1.jpg', alt: 'Photo 1 Description' },
          { url: 'path/to/photo2.png', alt: 'Photo 2 Description' },
          // Add more photos here...
        ],
        lightboxIndex: -1 // -1 indicates lightbox is closed
      };
    },
    methods: {
      openLightbox(index) {
        this.lightboxIndex = index;
      },
      closeLightbox() {
        this.lightboxIndex = -1;
      }
    }
  };
  </script>
  
  <style>
  .photo-gallery {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
  }
  
  .photo-item {
    margin: 10px;
    width: 200px;
  }
  
  .photo-item img {
    width: 100%;
    height: auto;
    cursor: pointer;
  }
  
  .lightbox {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.8);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
  }
  
  .lightbox img {
    max-width: 80%;
    max-height: 80%;
  }
  </style>