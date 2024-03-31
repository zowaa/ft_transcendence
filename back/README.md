# Backend API Documentation

This README provides documentation for the backend APIs, including endpoints for user management, authentication, and two-factor authentication (2FA).

## Table of Contents
- [Authentication](#authentication)
  - [Register](#register)
  - [Login](#login)
  - [Logout](#logout)
- [User Profile](#user-profile)
  - [Profile](#profile)
  - [Change Password](#change-password)
- [Friends](#friends)
- [Avatar Upload](#avatar-upload)
- [Two-Factor Authentication (2FA)](#two-factor-authentication-2fa)
- [OAuth 42 Authentication](#oauth-42-authentication)

## Authentication

### Register
- **Endpoint:** `/register/`
- **Method:** POST
- **Description:** Registers a new user.
- **Body Parameters:** `username`, `email`, `password`

### Login
- **Endpoint:** `/login/`
- **Method:** POST
- **Description:** Authenticates a user and returns an access token.
- **Body Parameters:** `username`, `password`

### Logout
- **Endpoint:** `/logout/`
- **Method:** POST
- **Description:** Logs out the current user.

## User Profile

### Profile
- **Endpoint:** `/profile/`
- **Method:** GET/PUT
- **Description:** Retrieves or updates the profile information of the current user.
- **PUT Body Parameters:** Fields to update.

### Change Password
- **Endpoint:** `/change_password/`
- **Method:** PUT
- **Description:** Allows the user to change their password.
- **Body Parameters:** `old_password`, `new_password`

## Friends

- **Endpoint:** `/friends/`
- **Method:** GET/POST/PUT/DELETE
- **Description:** Manages friend relationships (list friends, send requests, accept/reject requests, remove friends).
- **POST Body Parameters:** `username` of the friend to add.
- **PUT Body Parameters:** `username` of the friend, `action` (accept/reject).

## Avatar Upload

- **Endpoint:** `/avatar/`
- **Method:** POST
- **Description:** Allows users to upload an avatar image.
- **Body Parameters:** File upload field.

## Two-Factor Authentication (2FA)

### Generate QR Code
- **Endpoint:** `/qr_code/`
- **Method:** GET
- **Description:** Generates a QR code for setting up 2FA.

### Verify 2FA Code
- **Endpoint:** `/double_factor/`
- **Method:** POST
- **Description:** Verifies the 2FA code entered by the user.
- **Body Parameters:** `code`

## OAuth 42 Authentication

### OAuth 42 Redirect
- **Endpoint:** `/auth42/`
- **Method:** GET
- **Description:** Redirects to the OAuth 42 authentication page.

### OAuth 42 Callback
- **Endpoint:** `/auth42_callback/`
- **Method:** GET
- **Description:** Handles the callback from OAuth 42 authentication.
