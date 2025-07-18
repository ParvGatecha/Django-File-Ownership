Of course. Here is the complete and final `README.md` file.

You just need to replace the placeholder paths like `path/to/your/screenshot.png` with the actual links to your images.

---

# Django File Ownership Transfer API

This project is a Django REST API system that allows users to securely upload files, transfer ownership of those files to other users, and revoke those transfers. All ownership changes are tracked in a history log for audit purposes.

This system is built to fulfill the requirements of the project brief, demonstrating proficiency in Django, Django REST Framework, database modeling, and API testing.

## Table of Contents

- [Project Overview](#project-overview)
- [Core Functionality](#core-functionality)
- [Setup and Installation](#setup-and-installation)
- [API Endpoints](#api-endpoints)
- [Postman API Testing Walkthrough](#postman-api-testing-walkthrough)
  - [Step 1: User A Uploads a File](#step-1-user-a-uploads-a-file)
  - [Step 2: User A Transfers the File to User B](#step-2-user-a-transfers-the-file-to-user-b)
  - [Step 3: User A Revokes the Transfer](#step-3-user-a-revokes-the-transfer)
- [Database State Verification](#database-state-verification)
  - [State 1: After Transfer](#state-1-after-transfer)
  - [State 2: After Revocation](#state-2-after-revocation)
  - [State 3: The Complete Audit Trail](#state-3-the-complete-audit-trail)

## Project Overview

The system allows a user (`User A`) to upload a resource. `User A` can then transfer ownership of this resource to `User B`. Later, `User A` (the original owner) retains the right to revoke this transfer, taking back ownership of the resource. The entire lifecycle of ownership changes is logged for auditing.

## Core Functionality

*   **File Transfer**: An owner can transfer a file to another user, changing the file's `owner` field.
*   **Transfer Revocation**: The **original owner** of a file can revoke a transfer, returning ownership to themselves.
*   **History Tracking**: All transfer and revoke actions are logged with timestamps in a `TransferHistory` model.
*   **Secure API**: Endpoints are protected, requiring token authentication.

## Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/your-repo-name.git
    cd your-repo-name
    ```
2.  **Create and activate a virtual environment:**
    ```bash
    # Create a virtual environment
    python -m venv venv

    # Activate it
    # On Windows:
    venv\Scripts\activate
    # On macOS/Linux:
    source venv/bin/activate
    ```
3.  **Install dependencies from `requirements.txt`:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Run database migrations:**
    ```bash
    python manage.py migrate
    ```
5.  **Create users (admin, and test users `UserA`, `UserB`):**
    ```bash
    python manage.py createsuperuser
    python manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_user(username='UserA', password='password123'); User.objects.create_user(username='UserB', password='password123')"
    ```
6.  **Run the server:**
    ```bash
    python manage.py runserver
    ```

## API Endpoints

| Endpoint                          | Method | Purpose                                     |
| --------------------------------- | ------ | ------------------------------------------- |
| `/api/get-token/`                 | `POST` | Get an authentication token.                |
| `/api/files/`                     | `POST` | Upload a new file.                          |
| `/api/files/`                     | `GET`  | List files owned by the authenticated user. |
| `/api/transfer/`                  | `POST` | Transfer a file to another user.            |
| `/api/revoke/`                    | `POST` | Revoke a transfer (original owner only).    |
| `/api/files/<file_id>/history/`   | `GET`  | View a file's ownership history.            |

---

## Postman API Testing Walkthrough

This section demonstrates the core API functionality using Postman screenshots.

### Step 1: User A Uploads a File

`UserA` authenticates and uploads a new file named "PropertyPapers.pdf". The API responds with the new file object, showing that `UserA` is both the `owner` and `original_owner`.

![User A uploads a file](/images/Screenshot4.png)

### Step 2: User A Transfers the File to User B

`UserA` makes a `POST` request to the `/api/transfer/` endpoint, specifying the `file_id` and the `to_user_id` (User B's ID). The API confirms the successful transfer.

![User A transfers file to User B](/images/Screenshot5.png)

### Step 3: User A Revokes the Transfer

Even though `UserB` is the current owner, `UserA` (as the **original owner**) can revoke the transfer. `UserA` makes a `POST` request to the `/api/revoke/` endpoint. The API confirms that ownership has been successfully returned.

![User A revokes the transfer](/images/Screenshot2.png)

---

## Database State Verification

The following screenshots are from the Django Admin panel, showing how the database state changes during the workflow.

### State 1: After Transfer

After `UserA` transfers the file to `UserB`, the `File` model shows that the **owner** has been updated to `UserB`, while the **original_owner** correctly remains `UserA`.

![File state after transfer](/images/Screenshot3.png)

### State 2: After Revocation

After `UserA` revokes the transfer, the `File` model is updated again. Both the **owner** and **original_owner** are now correctly set back to `UserA`.

![File state after revocation](/images/Screenshot6.png)

### State 3: The Complete Audit Trail

The `TransferHistory` table provides a clear audit trail. It logs both the initial `TRANSFER` from `UserA` to `UserB` and the subsequent `REVOKE` action, which shows ownership returning from `UserB` to `UserA`.

![Complete audit history in database](/images/Screenshot7.png)