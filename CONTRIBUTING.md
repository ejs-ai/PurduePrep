# Contributing to PurduePrep

Thank you for your interest in contributing to PurduePrep! This project aims to help students find relevant exam-style questions to study effectively. We welcome contributions to improve the code, expand features, enhance documentation, and fix any issues. Specifically, we are interested in future expansion to create a caching feature which would allow PurduePrep to cache some frequently found exam questions.

## Project Architecture Overview
We developed the complete backend in Python with Flask as an API for frontend communication. Next.js was used a framework for a React frontend.
![System Design](docs/PurduePrep_system_components.png)

## How to Contribute

### 1. Clone the Repository
- Start by forking the repository to your own GitHub account.
- Clone your fork to your local machine.

### 2. Install Python and Poetry for dependency management
- PurduePrep runs on Python 3.12. Ensure this is installed.
- In your terminal, 'pip install poetry' which is our dependency manager.
- Once poetry is installed, run 'poetry install' and 'poetry update' to install and update PurduePrep's dependencies.

### 3. Running PurduePrep on localhost
- Ensure you have installed node modules (Node.js).
- Split your terminal. 'npm run dev' in one and 'python app.py' in the other to run the front and backends, respectively.
- Interact with the website by navigating to localhost in your .

### 4. Branch, commit changes, and submit a pull request
- Create a new feature branch for your changes.
- Submit a pull request in our repository and request review from our team (emmateff, skrichef, JPKamphuis).

## Contact Information

Email preppurdue@gmail.com for questions.
