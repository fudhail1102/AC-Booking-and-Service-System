# AC-Booking-and-Service-System

## Project Description

This project is an AC Reservation and Service System built using Python, Tkinter, and MySQL. The system allows customers to sign up, log in, and manage their AC reservations and service bookings. It provides functionalities to book and cancel orders and services for air conditioners, with options to customize preferences based on price, brand, type, system, and cooling power.

## Features

- **User Authentication**: Sign up and log in with credentials.
- **Book Orders**: Select and customize AC options to place orders.
- **Book Services**: Book services like servicing, repair, installation, and uninstallation for ACs.
- **Cancel Orders and Services**: Allows users to cancel their bookings if needed.
- **View Orders and Services**: Users can view their booking history and details.
- **Interactive GUI**: User-friendly interface developed with Tkinter.

## Requirements

To run this project, you need the following Python packages:

- `mysql-connector==2.2.9`
- `mysql-connector-python==9.0.0`
- `python-dotenv==1.0.1`

You can install these packages using the following command:

```sh
pip install -r requirements.txt
```
## Setting up Environment Variables

- Create a .env file in the root directory of your project and add the following environment variables with your MySQL database credentials:

- DB_HOST=your_database_host
- DB_USER=your_database_user
- DB_PASSWORD=your_database_password
- DB_NAME=your_database_name

