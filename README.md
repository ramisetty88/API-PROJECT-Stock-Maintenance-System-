Stock Maintenance System
📌 Project Content
This is a web-based Stock maintenance system that allows users to place orders,view their orders and view their products,And admins can add products,view products,view orders and view list of customers.
Admin Dashboard:

Register (via API)
Login (JWT or Session-based authentication)
Add Products (API: POST /products)
View Products (API: GET /products)
View Customers (API: GET /users)
View Order Details (API: GET /orders)

User Dashboard:

View Products (API: GET /products)
Place Order (API: POST /orders)
View My Orders (API: GET /orders/<user_id>)

Project code:

🛠️ Tech Stack
Frontend: HTML, CSS, JavaScript
Backend: Node.js, Express.js
Database: MySQL
Hosting: Render / InfinityFree (for database)
📂 Project Structure
/FixMyStay
│── /images             # Stores images used in the project
│── /models             # Database models
│── /node_modules       # Dependencies installed via npm
│── /routes             # Backend API routes
│── /scripts            # Additional scripts for functionality
│── /styles             # CSS and styling files
│── .env                # Environment variables (database config, secrets)
│── .gitattributes      # Git attributes file
│── announcements.html  # Announcements page
│── complaint-form.html # Complaint submission page
│── complaints.html     # Complaints listing page
│── contacts.html       # Contact management page
│── dashboard.html      # Dashboard for students & admins
│── database.sql        # SQL file for database schema
│── db.js               # Database connection script
│── home.html           # Homepage of the system
│── index.html          # Main entry page
│── package.json        # Dependencies & scripts
│── package-lock.json   # Lock file for dependencies
│── server.js           # Main backend server file
│── signup.html         # Signup page

🚀 Setup & Installation
1️⃣ Clone the Repository
git clone https://github.com/saathvikb2005/hostel-complaint-system
cd hostel-complaint-system
2️⃣ Install Dependencies
npm install
3️⃣ Configure Environment Variables
Create a .env file in the root directory and add:

PORT=3001
DB_HOST=your-database-host
DB_USER=your-database-username
DB_PASSWORD=your-database-password
DB_NAME=your-database-name
4️⃣ Start the Server
node server.js
The backend will run on http://localhost:3001

🌐 Deployment
Frontend Hosting: Can be deployed on Netlify, Vercel
Backend Hosting: Can be hosted on Render
Database Hosting: Using InfinityFree MySQL
