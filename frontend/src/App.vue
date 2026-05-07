<template>
  <div class="app-container">

    <!-- =========================
         LANDING PAGE (MODE SELECT)
    ========================== -->
    <div v-if="mode === 'home'" class="landing">

      <h1>CareerPilot AI</h1>
      <p>Choose how you want to build your CV</p>

      <div class="mode-box">

        <button @click="mode = 'form'">
          ✍️ Manual CV Builder
        </button>

        <button @click="mode = 'voice'">
          🎙️ Voice CV Interview
        </button>

      </div>

    </div>

    <!-- =========================
         FORM MODE (YOUR ORIGINAL UI)
    ========================== -->
    <div v-if="mode === 'form'">

      <button class="back" @click="mode = 'home'">
        ← Back
      </button>

      <!-- 🔥 YOUR EXISTING FORM (UNCHANGED) -->
      <!-- PASTE YOUR FULL FORM HERE EXACTLY AS YOU SENT IT -->

      <!-- ACTION BUTTONS ONLY CONNECTED -->
      <div class="button-group">

        <button class="fill-btn" @click="fillDummyData">
          Fill Dummy Data
        </button>

        <button class="generate-btn" @click="generateCV" :disabled="loading">
          {{ loading ? "Generating CV..." : "Generate CV" }}
        </button>

      </div>

    </div>

    <!-- =========================
         VOICE MODE
    ========================== -->
    <div v-if="mode === 'voice'" class="voice-mode">

      <button class="back" @click="mode = 'home'">
        ← Back
      </button>

      <h2>AI Voice CV Interview</h2>

      <div class="chat-box">

        <div v-for="(msg, i) in messages" :key="i" :class="msg.role">
          {{ msg.text }}
        </div>

      </div>

      <button @click="startVoice">
        🎤 Speak
      </button>

    </div>

  </div>
</template>
<script setup>
import { reactive, ref } from "vue";

const mode = ref("home");
const loading = ref(false);

/* =========================
   FORM DATA (YOUR ORIGINAL)
========================= */
const formData = reactive({
  name: "",
  email: "",
  contact: "",
  github: "",
  province: "",
  city: "",
  target_role: "",
  technical_skills: "",
  soft_skills: "",
  education: "",
  certifications: "",
  professional_experience: "",
  projects: [
    { title: "", description: "" },
    { title: "", description: "" }
  ]
});

/* =========================
   FORM FUNCTIONS
========================= */
const fillDummyData = () => {

  formData.name = "John Doe";
  formData.email = "johndoe@gmail.com";
  formData.contact = "+27 71 234 5678";
  formData.github = "https://github.com/johndoe";
  formData.city = "Johannesburg";
  formData.province = "Gauteng";
  formData.target_role = "Frontend Developer";

  formData.technical_skills =
    "Vue.js, JavaScript, HTML, CSS, Flask, Python, REST APIs";

  formData.soft_skills =
    "Communication, Teamwork, Problem Solving";

  formData.education =
    "Diploma in IT - Boston City Campus";

  formData.certifications =
    "AWS Cloud Practitioner, Google AI Essentials";

  formData.professional_experience =
    "Built frontend apps using Vue and REST APIs";

  formData.projects = [
    {
      title: "AI Resume Generator",
      description: "Flask + Vue + Groq CV generator"
    },
    {
      title: "Hospital System",
      description: "Role-based management system"
    }
  ];
};

const generateCV = async () => {

  loading.value = true;

  try {

    const res = await fetch("http://127.0.0.1:5000/generate-cv", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(formData)
    });

    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.error);
    }

    const blob = await res.blob();

    const url = window.URL.createObjectURL(blob);

    const a = document.createElement("a");

    a.href = url;
    a.download = "CareerPilot_CV.pdf";

    a.click();

  } catch (err) {
    alert(err.message);
  } finally {
    loading.value = false;
  }
};


/* =========================
   VOICE MODE (SIMPLE VERSION)
========================= */
const messages = ref([]);

const recognition = new (window.SpeechRecognition ||
  window.webkitSpeechRecognition)();

recognition.lang = "en-US";

const speak = (text) => {

  const utterance = new SpeechSynthesisUtterance(text);

  window.speechSynthesis.speak(utterance);
};

const sendVoice = async (text) => {

  const res = await fetch("http://127.0.0.1:5000/voice-chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      user_id: "user1",
      message: text
    })
  });

  const data = await res.json();

  messages.value.push({
    role: "bot",
    text: data.message
  });

  speak(data.message);

  if (data.done) {

    await fetch("http://127.0.0.1:5000/voice-generate-cv", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data.data)
    });

  }
};

const startVoice = () => {

  recognition.start();

};

recognition.onresult = (event) => {

  const text = event.results[0][0].transcript;

  messages.value.push({
    role: "user",
    text
  });

  sendVoice(text);
};
</script>
<style scoped>

* {
  box-sizing: border-box;
}

body {
  margin: 0;
  background: #f3f4f6;
}

.app-container {
  min-height: 100vh;
  padding: 40px 20px;
  font-family: Arial, sans-serif;
}

/* HERO */

.hero {
  text-align: center;
  margin-bottom: 40px;
}

.hero h1 {
  font-size: 44px;
  margin-bottom: 10px;
  color: #111827;
}

.hero p {
  color: #6b7280;
  font-size: 18px;
}

/* FORM */

.form-container {
  max-width: 1000px;
  margin: auto;
  background: white;
  padding: 35px;
  border-radius: 18px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.08);
}

/* SECTIONS */

.section {
  margin-bottom: 35px;
}

.section h2 {
  margin-bottom: 15px;
  color: #111827;
}

/* GRID */

.grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 15px;
}

/* INPUTS */

input,
textarea {
  width: 100%;
  padding: 14px;
  border-radius: 10px;
  border: 1px solid #d1d5db;
  font-size: 15px;
  outline: none;
}

input:focus,
textarea:focus {
  border-color: #2563eb;
}

textarea {
  min-height: 120px;
  resize: vertical;
}

/* PROJECT CARD */

.project-card {
  padding: 20px;
  border: 1px solid #e5e7eb;
  border-radius: 14px;
  margin-bottom: 20px;
}

/* BUTTONS */

.button-group {
  display: flex;
  gap: 15px;
}

.generate-btn,
.fill-btn,
.secondary-btn {
  border: none;
  border-radius: 10px;
  cursor: pointer;
  color: white;
  transition: 0.2s;
}

.generate-btn {
  flex: 1;
  padding: 16px;
  background: #111827;
  font-size: 16px;
}

.generate-btn:hover {
  background: #1f2937;
}

.fill-btn {
  padding: 16px 24px;
  background: #2563eb;
}

.fill-btn:hover {
  background: #1d4ed8;
}

.secondary-btn {
  padding: 12px 20px;
  background: #059669;
}

.secondary-btn:hover {
  background: #047857;
}

/* RESPONSIVE */

@media (max-width: 768px) {

  .grid {
    grid-template-columns: 1fr;
  }

  .button-group {
    flex-direction: column;
  }

  .hero h1 {
    font-size: 32px;
  }

  .form-container {
    padding: 20px;
  }

  .landing {
  text-align: center;
  padding: 100px;
}

.mode-box {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-top: 30px;
}

.mode-box button {
  padding: 20px;
  border: none;
  border-radius: 10px;
  background: #111827;
  color: white;
  cursor: pointer;
}

.back {
  margin-bottom: 20px;
  padding: 10px;
}

.voice-mode {
  text-align: center;
}

.chat-box {
  height: 300px;
  overflow-y: auto;
  background: #f3f4f6;
  padding: 20px;
  margin: 20px auto;
  width: 80%;
  border-radius: 10px;
}

.user {
  text-align: right;
  margin: 10px;
}

.bot {
  text-align: left;
  margin: 10px;
}

}

</style>

