
  # CurhatBuddy Mobile App Design

  This is a code bundle for CurhatBuddy Mobile App Design. The original project is available at https://www.figma.com/design/KQz6yiCYBNZJgqoE1JLWty/CurhatBuddy-Mobile-App-Design.

  ## Running the code

  Run `npm i` to install the dependencies.

  Run `npm run dev` to start the development server.

  ## Backend integration

  This UI is designed to work with the Flask chatbot backend in the parent folder.

  1. Install backend dependencies in the root folder:
     ```bash
     pip install -r ../requirements.txt
     ```
  2. Start the backend from the root folder:
     ```bash
     python ../web_app.py
     ```
  3. Start the UI frontend in this folder:
     ```bash
     npm run dev
     ```

  During development, the Vite dev server proxies `/api` requests to `http://127.0.0.1:5000`.
  