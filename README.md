# 🐟 **Monkfish: A Smarter Alternative to Mobile Phones**

**Monkfish** is a secure, school-focused personal assistant that transforms the way students interact and navigate their environment. It’s built to combine robust software features with a purpose-designed hardware platform, delivering an experience that’s both innovative and dependable.

## 🚀 **Features & Details**

### 📩 **Secure Messaging**
- **Real-Time Chat**: 🔒 **Encrypted communication with a dynamic bad language filter that automatically censors inappropriate words.**
- **Lesson-Aware Scheduling**: ⏳ **Chat functionality is smartly integrated with the school timetable, ensuring it’s active only when appropriate.**

### 🏫 **Indoor Navigation**
- **QR Code Integration**: 📌 **Students input their current location using QR codes, enabling precise indoor tracking.**
- **A* Algorithm**: 🧭 **Utilizes an efficient path-finding algorithm to provide turn-by-turn navigation to classrooms, facilities, or even the nearest bathroom.**

### 🤝 **Friend Finder**
- **AI-Driven Matching**: 🧠 **Leverages facial recognition and interest-based profiling to help students connect with like-minded peers.**
- **Streamlined Connections**: 🔍 **Quickly identifies friends or study groups based on common interests and real-time data.**

### 🏆 **Rewards System**
- **Digital Badges**: 🏅 **Allows teachers to send pre-made or custom badges to recognize achievements, promoting positive behavior and engagement.**
- **Gamification**: 🎮 **Integrates rewards seamlessly to make school life more interactive and motivating.**

---

## 🖥️ **Technologies & Hardware**

### **Software**
- **Languages & Libraries**: 💻 **Developed in Python using AI, computer vision, and algorithmic path-finding.**
- **Server Architecture**: 🌐 **Runs on a local Raspberry Pi server, ensuring secure, offline operations within the school network.**

### **Hardware**
- **Design**: 🖥️ **A compact, durable device featuring a touchscreen and physical keyboard designed for ease-of-use.**
- **3D-Printed Case**: 🏗️ **Custom case for durability and ergonomics, combining a retro aesthetic with modern functionality.**
- **Battery Efficient**: 🔋 **Designed to last an entire school day, ensuring reliability.**

### **Required Hardware**
- 🖥️ **Raspberry Pi 4 or 5** (for running the application)
- 📟 **Touchscreen display** (for user interaction)
- ⌨️ **Mini physical keyboard** (for input convenience)
- 🔋 **Portable power supply** (for extended usability)
- 📸 **Oak D Lite** (for facial recognition and QR scanning)
- 📶 **WiFi or local network connectivity** (for secure communications)
- 🖨️ **3D-printed case** (for hardware protection and ease of handling)

---

## 🛠️ **Setup & Installation**

### **1️⃣ Prerequisites**
Before running the application, ensure you have:
- ✅ **Python 3.8+** installed ([Download here](https://www.python.org/downloads/))
- ✅ **pip** installed (`python -m ensurepip`)
- ✅ **Required dependencies (`requirements.txt`)**
- ✅ **(Optional) QR code scanner hardware for navigation features**

### **2️⃣ Installation**
#### 🔽 **Clone the repository:**
```bash
 git clone https://github.com/Nono123GitHub/Monkfish-School-Assistant.git
 cd Monkfish-School-Assistant
```

#### 🏗️ **Create a virtual environment (recommended):**
```bash
 python -m venv venv
 source venv/bin/activate   # On macOS/Linux
 venv\Scripts\activate      # On Windows
```

#### 📦 **Install dependencies:**
```bash
 pip install -r requirements.txt
```

#### ⚙️ **Configure the application:**
- **Rename `.env.example` to `.env`**
- **Edit `.env` to provide required values (e.g., API keys, database URLs)**

---

## ▶️ **Running the Application**

To start the application, run:
```bash
 cd Main Interface
 python main.py
```

For debugging mode:
```bash
 python main.py --debug
```

To stop the application:
```bash
 Ctrl + C
```

---

## 🛠️ **Troubleshooting**

❌ **ModuleNotFoundError?**
👉 **Run `pip install -r requirements.txt` again.**

❌ **Permission denied?**
👉 **Try running `chmod +x main.py` before executing.**

❌ **Errors related to missing `.env`?**
👉 **Ensure it is properly configured with required keys.**

---

## 📝 **Contributing**
We welcome contributions! Please **fork the repo, create a feature branch, and submit a pull request.**

---

## 📬 **Contact**
For any issues, **please open a GitHub issue or contact the repository maintainer.**

---

## 🔗 **Code & Design**

Explore the project details, source code, and hardware designs on [Tinkercad](https://www.tinkercad.com/things/e278IqMzMDa-case).

Experience how **Monkfish** redefines mobile technology for educational environments, combining state-of-the-art features with a focus on **safety, efficiency, and student connectivity.**

