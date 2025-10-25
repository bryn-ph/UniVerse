# UniVerse
The study discussion board connecting Australian university students for cross-campus academic support.

---

# PART A: Project Responses

## Team Name / Members
**Team Universe**
- Bryn Phillips
- Joshua Santosa
- Dhiwa Kusumah
- Sri Sai Suhaas Mavuri
- Emily Murphy

---
## Project Scope (A1, A2, A3)
### **A1. Problem Relevance (10 pts)**
Australian university students often face **fragmented academic communities**, limited to campus-specific platforms or private group chats.  
This makes it difficult for students from different universities to share resources, collaborate, and support each other academically.  

**UniVerse** directly addresses this by:
- Creating a **cross-university academic platform** for collaboration and discussion.  
- Enabling **smarter visibility** across universities with our *Class-Signature-Engine (CSE)* algorithm.  



### **A2. Project Desirability (10 pts)**
**Technical Feasibility:**  
Built using a modern, lightweight, and scalable stack. Initial proof of concept developed with rapid prototpying in mind, but more hardy and structured alternatives were considered for the future.

**Mitigation of Risks:**  
- Offline-safe and deployable locally (minimal dependencies).  
- Schema-based OpenAPI definitions ensure frontend and backend consistency.  
- Modular architecture allows future upgrades (e.g. PostgreSQL, user auth, or ML-powered grouping).  

**Development Plan:**  
1. Establish REST API and models for users, classes, universities, discussions.  
2. Build frontend views with auto-generated API types.  
3. Integrate *CSE* for automatic class grouping.  
4. Deploy with persistent database and production configuration.  

### **A3. Target Users (5 pts)**
**Primary Users:**  
- University students seeking peer help, discussion context, or collaboration.  

**Secondary Users:**  
- Tutors or teaching assistants engaging across multiple institutions.  
- Educational institutions exploring inter-campus cooperation.  

**Personas:**  
- *Alice* — a CS student at RMIT who wants to discuss a more generic “Machine Learning” topic with students at Monash, as she was interested in their specific areas of study and context.  
- *Ben* — a biology student looking for shared class/topic discussions with other universities as a means to supplement respective course material to provide a broader learning pathway.  

---

## Design Intentions (C1, C2)
###  **C1. User Interface (10 pts)**
- **Consistent design system:** Shadcn UI + TailwindCSS for clarity and modern appeal.  
- **Accessible and readable typography:** Fira Sans with high contrast ratios.  
- **Clear information hierarchy:** group → class → discussion → replies.  
- **Responsive layout:** works across desktop, tablet, and mobile seamlessly.  

### **C2. User Experience (10 pts)**
- **Intuitive navigation:** navbar containing user profile, main cntent feed, and exploration, discussion pages for replies and content.  
- **Cross-university feed:** powered by the *CSE*, exposing related topics dynamically.  
- **Feedback mechanisms:** loading spinners, present escape options, and button state transitions.  
- **Future accessibility roadmap:** keyboard navigation and semantic ARIA tags.  


---

## Development Solutions (D2)

### **D2. Back-End Complexity (10 pts)**
**Chosen Features:**
1. Provide an example of a well-designed backend function or module
that demonstrates efficient time complexity, clean logic, and
integration with other components.

    ### Justification:

    **Class-Signature-Engine Algorithm (CSE):** the bulk of our logic for this engine is located in the `group_classes_by_signature()` function. The algorithm runs in *O(n²)* pairwise comparisons but scales efficiently for particularly smaller datasets.

    **Integration & Maintainability:** The function ties directly into the class creation route, automatically re-grouping classes in real-time without user input. This improves project utility significantly, as time goes on. 

    **Iterative Development Support:** The modular structure supports incremental enhancements (e.g., ML-based similarity in future versions) without requiring architectural refactoring. 
    
2. Demonstrate meaningful use of an API and explain why it is well-
suited to the project, showing a reusable function (not hard-coded API requests).

    ### Justification:

    **Centralised API Architecture:** We have implemented a backend driven OpenAPI architecture. So rather than manually writing request logic or type definitions, this approach provides a single source of truth between frontend and backend, eliminating redundancy and ensuring schema and type consistency.

    **Improves Iterative & Modular Development:** Building on the above point, when new endpoints or fields are added in Flask, they propagate into the frontend via re-generated types — enabling rapid, modular iteration without refactoring or introducing breaking changes.

---

## Technologies Used (D3)
### **D3. Documentation (10 pts)**

### **Base Versions**
- **Node.js** v22.21.0
- **npm** 11.6.2
- **Python** 3.11.9

### **Tech Stack**
| Layer | Technologies |
|-------|---------------|
| **Frontend** | React, TypeScript, Vite, Shadcn UI, TailwindCSS |
| **Backend** | Flask, Flask-Smorest, SQLAlchemy, Flask-CORS |
| **Database** | SQLite |
| **Dev Tools** | Node.js, npm, Python, OpenAPI Type Generator |

---

## PART B: Setup and User Guide

### 1. Clone the Repository

```bash
git clone https://github.com/bryn-ph/UniVerse.git
cd universe
```

### 2. Backend Setup

```bash
cd backend

# Setup and activate venv
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python -m venv venv
source venv/bin/activate

# Install requirements
pip install -r requirements.txt

# Run backend
python app.py

# (OPTIONAL - With backend running) Seed the database
python seed.py
```

### 3. Frontend Setup

```bash
cd frontend

# Install npm packages
npm install

# Ensure backend api types/hooks are up to date
npm run generate-api

# Run frontend
npm run dev
```

---

> **Default Backend Port:** http://127.0.0.1:5001

> **Local Backend Swagger:** http://127.0.0.1:5001/swagger
>

> **Default Frontend Port:** http://localhost:5173
>

> **Note:** Run `npm run start-all` to start both the frontend and backend in one command.
> Generate api.ts based off schemas.py with `npm run generate-api`
