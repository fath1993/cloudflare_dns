# Python Django Service to Change Cloudflare DNS Automatically

This project is a Django-based web application that provides a service to automatically change DNS settings on Cloudflare. Users can manage their DNS records efficiently through a user-friendly interface, simplifying the process of updating and maintaining DNS configurations.

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Automatic DNS Updates**: Change Cloudflare DNS records programmatically with ease.
- **User Authentication**: Secure user accounts with authentication and role-based access control.
- **DNS Record Management**: Add, update, and delete DNS records through a web interface.
- **Real-time Updates**: Instantly apply DNS changes and view updates in real time.
- **Logging and Notifications**: Keep track of DNS changes and notify users of updates.

## Installation

To run this project locally, follow these steps:

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/cloudflare-dns-service.git
    ```

2. Navigate into the project directory:
    ```bash
    cd cloudflare-dns-service
    ```

3. Create a virtual environment:
    ```bash
    python -m venv venv
    ```

4. Activate the virtual environment:
    - On Windows:
      ```bash
      venv\Scripts\activate
      ```
    - On macOS/Linux:
      ```bash
      source venv/bin/activate
      ```

5. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

6. Set up your database:
    ```bash
    python manage.py migrate
    ```

7. Create a superuser for the admin interface (optional):
    ```bash
    python manage.py createsuperuser
    ```

8. Start the development server:
    ```bash
    python manage.py runserver
    ```

## Usage

Once the server is running, visit `http://127.0.0.1:8000/` in your browser to access the Cloudflare DNS management service.

- **Authenticate**: Log in or create a new account to manage your DNS settings.
- **Manage DNS Records**: Use the interface to add, update, or delete DNS records as needed.
- **View Logs**: Check the logs for any DNS changes made for transparency.

## Contributing

Contributions are welcome! If you’d like to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/new-feature`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature/new-feature`).
5. Open a Pull Request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
