# Habesha Plate 🍽️

Habesha Plate is a web application that allows users to explore and order traditional Ethiopian food from local restaurants. This project brings Ethiopian cuisine online, allowing users to experience the rich flavors of Ethiopian dishes by browsing menus, adding items to a cart, and placing orders with ease.

## Table of Contents

1. [Project Overview](#project-overview)
2. [Features](#features)
3. [Technologies Used](#technologies-used)
4. [Installation](#installation)
5. [Usage](#usage)
7. [License](#license)

---

### 1. Project Overview

The goal of Habesha Plate is to promote Ethiopian food by providing a platform for local restaurants to showcase their dishes and for users to explore and order them online. With features like menu browsing, cart management, and order placement, this application bridges the gap between traditional Ethiopian dining and modern technology.

### 2. Features

- **Menu Browsing**: View a variety of Ethiopian dishes with descriptions, prices, and preparation instructions.
- **Cart Management**: Add dishes to the cart and adjust quantities before placing an order.
- **Order Placement**: Seamless order experience with payment integration.
- **User Authentication**: Secure user registration and login system.
- **Admin Dashboard**: Admins can manage the menu, monitor orders, and update restaurant information.

### 3. Technologies Used

- **Frontend**: HTML, CSS, JavaScript, Bootstrap
- **Backend**: Django, Django REST Framework
- **Database**: PostgreSQL
- **Third-Party Integrations**: Chart.js for visualizing order statistics, authentication libraries for secure logins.

### 4. Installation

To set up the project locally, follow these steps:

1. **Clone the repository**
    ```bash
    git clone https://github.com/yourusername/habesha-plate.git
    cd habesha-plate
    ```

2. **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3. **Set up the database**
   - Ensure PostgreSQL is installed and running.
   - Configure your database settings in `settings.py`.

4. **Run migrations**
    ```bash
    python manage.py migrate
    ```

5. **Start the server**
    ```bash
    python manage.py runserver
    ```

### 5. Usage

1. Navigate to `http://127.0.0.1:8000` to view the home page.
2. Register or log in to your account.
3. Browse the menu, add items to your cart, and proceed with order placement.

### 6. License
This project is licensed under the MIT License.
