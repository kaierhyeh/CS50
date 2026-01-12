# Pong Game - Ultimate Platform
#### Video Demo: [URL](https://youtu.be/Hw04NfGSgFw)

## Description
**Pong Game** is a comprehensive online gaming platform centered around the classic arcade game Pong.

While Pong may appear to be a simple arcade game, this project reveals that a robust, modern implementation is far from trivial. Under the hood, it requires a complex orchestration of microservices, real-time synchronization, and secure data handling. It is a full-stack Single Page Application (SPA) that demonstrates mastery of modern web technologies, microservices architecture, and even Web3 integration.

### Key Features
- **Real-time Multiplayer**: Play Pong against friends or strangers with low-latency WebSocket connections.
- **Game Modes**:
    - **Classic 1v1**: The standard experience.
    - **4-Player Chaos**: A custom mode for larger groups.
    - **AI Opponent**: A challenging bot for solo practice.
- **Tournament System**: Organize brackets for up to 8 players.
- **Blockchain Integration**: Tournament results are permanently recorded on the **Avalanche** blockchain (Fuji Testnet) using a custom Solidity smart contract, ensuring immutable history.
- **User Management**: Secure authentication via Google OAuth, Two-Factor Authentication (2FA) using TOTP, and detailed user profiles with stats.
- **Social Features**: Real-time chat, friend lists, and online status tracking.

## Technology Stack
The project is built using a microservices architecture to ensure scalability and maintainability:
- **Frontend**: Vanilla TypeScript with a custom component-based framework (no React/Vue/Angular used, to demonstrate deep understanding of DOM manipulation).
- **Backend**: Node.js with Fastify.
- **Database**: SQLite (User data & Game history).
- **Blockchain**: Solidity (Smart Contract) and Ethers.js (Frontend integration).
- **Infrastructure**: Docker & Docker Compose for orchestration.

## File Structure & Implementation Details
The project is organized into a monorepo structure, with distinct directories for each microservice and the frontend. Here is a breakdown of the key components and files:

### Backend Microservices (`srcs/backend/`)
Each service is a standalone Fastify application with its own `Dockerfile`, `package.json`, and source code.

- **`auth/` (Authentication Service)**
    - `src/index.ts`: The entry point. It initializes the Fastify server and registers routes.
    - `src/routes/auth.ts`: Handles Google OAuth callbacks and JWT generation.
    - `src/routes/2fa.ts`: Manages Two-Factor Authentication using TOTP (Time-based One-Time Password). It generates QR codes and validates user tokens.
    - `src/middleware/`: Contains JWT verification logic to protect private routes.

- **`game/` (Game Logic Service)**
    - `src/game/GameSession.ts`: The core game engine. It runs the physics loop (60 FPS) on the server side to prevent cheating. It calculates ball movement, collision detection with paddles/walls, and score updates.
    - `src/game/GameManager.ts`: Manages active game sessions and routes WebSocket messages to the correct session.
    - `src/websocket/`: Handles real-time communication with clients, receiving input (paddle movements) and broadcasting game state (ball position).

- **`users/` (User Management Service)**
    - `src/routes/profile.ts`: Handles user profile updates (avatar, nickname).
    - `src/db/`: Contains SQLite database schemas and migration scripts for storing user data.

- **`chat/` (Chat Service)**
    - `src/gateway/`: Manages WebSocket connections for the global chat and direct messages.
    - `src/db/`: Stores chat history in a separate SQLite database.

- **`stats/` (Statistics Service)**
    - Aggregates match results from the Game Service and updates user rankings and history.

### Frontend (`srcs/frontend/`)
The frontend is a Single Page Application (SPA) built without frameworks.

- **`src/index.html`**: The single HTML entry point. It contains the main container where different "pages" are dynamically rendered.
- **`src/scripts/router.ts`**: A custom client-side router. It listens for URL changes and renders the appropriate component (e.g., Dashboard, Game, Profile) without reloading the page.
- **`src/scripts/game/`**:
    - `GameRenderer.ts`: Uses the HTML5 Canvas API to draw the game state (paddles, ball, score) received from the server.
    - `InputController.ts`: Captures keyboard events (W/S, Arrow Keys) and sends them to the backend via WebSocket.
- **`src/scripts/components/`**: Reusable UI components like the Navigation Bar, Chat Window, and Toast Notifications.
- **`src/style/`**: Custom CSS files. We used CSS Variables for theming (Dark/Light mode) and Flexbox/Grid for responsive layout.

## Design Choices

### Why Microservices?
We debated between a Monolithic and Microservices architecture. A Monolith would have been easier to set up initially. However, we chose Microservices to mimic a real-world scalable system.
- **Decoupling**: If the Chat Service crashes, the Game Service continues to run uninterrupted.
- **Scalability**: We can deploy multiple instances of the Game Service to handle thousands of concurrent matches without affecting the Auth Service.
- **Technology Agnostic**: Although we used Node.js for everything, this architecture allows us to rewrite a specific service (e.g., the Game Engine) in a faster language like Go or Rust in the future without touching the rest of the system.

### Why Server-Side Game Logic?
In many simple browser games, logic runs on the client. We chose to run the physics engine entirely on the server (`GameSession.ts`).
- **Fairness**: Clients only send inputs (e.g., "Move Up"). The server decides the result. This makes it impossible for a user to cheat by modifying their local ball position or speed.
- **Synchronization**: All players see the exact same game state, regardless of their internet speed or computer power.

### Why No Frontend Framework?
Using React or Vue would have simplified state management. However, building a SPA from scratch using Vanilla TypeScript (`router.ts`, `component` system) forced us to understand the fundamental Web APIs:
- **History API**: For client-side routing.
- **DOM Manipulation**: Efficiently updating the UI without a Virtual DOM.
- **WebSockets**: Managing raw socket connections and event listeners manually.
This choice significantly deepened our understanding of how browsers actually work.

### Blockchain for Tournaments
Instead of just storing tournament results in a standard database, we integrated a blockchain solution. This serves as a "Proof of Victory" – once a tournament is won, the result is written to the blockchain and cannot be altered by server admins or hackers. It adds a layer of prestige and permanence to competitive play.

## Installation & Usage
### Prerequisites
- Docker & Docker Compose
(sudo apt install docker-compose-plugin)
- Make

### Quick Start
1. **Clone the repository**:


2. **Setup Credentials**:
   Create `secret/google-oauth.env`:
   ```
   GOOGLE_CLIENT_ID=your_client_id
   GOOGLE_CLIENT_SECRET=your_client_secret
   GOOGLE_REDIRECT_URI=https://localhost:4443/auth/google/callback
   ```
(Google API credentials and proper blockchain setup are needed if you want to fully test both features. Without them, the game works normally.)


3. **Launch**: (It could take around 15 minutes to build on CS50.dev.)
   ```bash
   make up_separately
   ```


4. **Access**:
   - If you've built it on your PC:<br>
   [**Localhost**] Open [https://localhost:4443](https://localhost:4443)<br>
   - If you've built it on CS50.dev:<br>
   [**CS50 Codespace**] Forward port 4443 and set it to HTTPS.Then open [https://cuddly-goldfish-j4j94jv7gww2p9jr-4443.app.github.dev/](https://cuddly-goldfish-j4j94jv7gww2p9jr-4443.app.github.dev/)
   - **LAN / Remote Play**: To play from another computer on the same network:
     1. Find your host computer's local IP address (e.g., `ipconfig` on Windows or `ip addr` on Linux).
     2. On the second computer, open `https://<YOUR_LOCAL_IP>:4443`.
     3. *Note: You may see a browser security warning because of the self-signed certificate. This is normal for development; simply proceed to the site.*
     4. *Note: For Google Login to work on the second computer, you must add `https://<YOUR_LOCAL_IP>:4443/auth/google/callback` to your Authorized Redirect URIs in the Google Cloud Console.*


5. **Clean up**:
   ```bash
   make clean
   # Do **NOT** use make fclean. It'll break your CS50.dev codespace.
   # But if you know what you're doing, I'm not stopping you.
   ```


## Collaborators
This project was a collaborative effort. Special thanks to all contributors:
- [`Alexej`](github.com/ku-alexej)
- [`Kilfen`](github.com/kbaridon)
- [`Marine`](github.com/ma-pierre)
- [`Steven`](github.com/s-t-e-v)
