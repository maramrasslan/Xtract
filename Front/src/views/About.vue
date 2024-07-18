<template>
  <div class="about-us">
    <h1>About Us</h1>
    <div class="qa-section">
      <div class="qa" v-for="(item, index) in questions" :key="index">
        <h2 class="question" @click="toggleAnswer(index)">Q: {{ item.question }}</h2>
        <p v-if="item.visible" class="answer">A: {{ item.answer }}</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AboutUs',
  data() {
    return {
      questions: [
        {
          question: "What is Xtract?",
          answer: "Xtract is your go-to platform for making open-source intelligence a breeze! We focus on collecting public data from social media to help you find all the juicy details you're looking for. Think of it as your personal detective assistant, but way cooler and digital!",
          visible: false
        },
        {
          question: "How does Xtract work?",
          answer: "It's simple! Just type in a name, and we'll fetch all possible accounts with that name from various social media platforms. You can then decide whether to collect all available data or use filters to grab only the most valuable bits. It's like shopping, but for data!",
          visible: false
        },
        {
          question: "What kind of data can I collect?",
          answer: "You can collect a wide range of public data, including profile information, posts, photos, and more. Whether you want everything or just specific details, Xtract has got you covered.",
          visible: false
        },
        {
          question: "Why did we create Xtract?",
          answer: "With millions of users on social media platforms generating heaps of valuable data every day, we saw an opportunity to make data collection easier and more efficient. Existing tools were either too complicated or didn't combine data from multiple platforms. So, we took matters into our own hands and built Xtract!",
          visible: false
        },
        {
          question: "How can Xtract help me?",
          answer: "Whether you're a researcher, investigator, or just curious, Xtract helps you gather the information you need from social media quickly and efficiently. Our user-friendly interface ensures you spend less time figuring things out and more time discovering insights.",
          visible: false
        },
        {
          question: "Is it easy to use Xtract?",
          answer: "Absolutely! Our intuitive design and straightforward process make it easy for anyone to start collecting data. Plus, we’re always here to help if you need any assistance.",
          visible: false
        },
        {
          question: "Can I customize the data collection process?",
          answer: "Yes, Xtract allows you to use filters to customize the data you collect. You can choose to gather all available data or narrow it down to the most relevant information based on your needs.",
          visible: false
        },
        {
          question: "How do you ensure the data collected is accurate?",
          answer: "We use sophisticated algorithms and up-to-date technology to ensure the data we collect is as accurate and relevant as possible. However, we always recommend cross-referencing information to confirm its validity.",
          visible: false
        },
        {
          question: "Can I export the collected data?",
          answer: "Yes, you can easily export the collected data in various formats, such as CSV or JSON, allowing you to analyze and use the data offline or in other applications.",
          visible: false
        },
        {
          question: "What makes Xtract unique?",
          answer: "Xtract stands out by aggregating data from multiple platforms into one easy-to-use application. No more juggling between different tools or websites – Xtract does it all for you in one place!",
          visible: false
        }
      ]
    };
  },
  methods: {
    toggleAnswer(index) {
      this.questions[index].visible = !this.questions[index].visible;
      console.log(this.questions[index].visible); // Debugging: Log the visibility state
    }
  }
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;700&display=swap');

.about-us {
  font-family: 'Open Sans', sans-serif;
  padding: 20px;
  max-width: 800px;
  margin: auto;
  color: rgba(8, 60, 44);
}

h1 {
  text-align: center;
  margin-bottom: 30px;
}

.qa-section {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.qa {
  border-bottom: 1px solid #ddd;
  padding-bottom: 10px;
  cursor: pointer;
}

.question {
  font-weight: 700;
  color: black;
}

.answer {
  font-weight: 400;
  color: black;
  margin-top: 5px;
  transition: max-height 0.3s ease-out, opacity 0.3s ease-out;
  overflow: hidden;
}
</style>
