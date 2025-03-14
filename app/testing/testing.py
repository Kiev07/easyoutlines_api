import requests

BASE_URL = "http://localhost:8000"
ADMIN_EMAIL = "admin@easyoutlays.com"
ADMIN_PASSWORD = "admin"
NEW_ADMIN_PASSWORD = "new_admin_password"

def login(email, password):
    response = requests.post(f"{BASE_URL}/auth/login", json={"email": email, "password": password})
    if response.status_code == 200:
        token = response.json()["access_token"]
        print(f"Login successful for {email}")
        return token
    else:
        print(f"Login failed for {email}: {response.json()}")
        return None

def change_password(token, new_password):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.put(f"{BASE_URL}/auth/change-password", json={"new_password": new_password}, headers=headers)
    if response.status_code == 200:
        print("Password changed successfully")
    else:
        print(f"Failed to change password: {response.json()}")

def delete_self(token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.delete(f"{BASE_URL}/admin/users/1", headers=headers)
    if response.status_code == 401:
        print("Admin cannot delete self: Test passed")
    else:
        print(f"Unexpected response: {response.json()}")

def create_user(token, email, role):
    headers = {"Authorization": f"Bearer {token}"}
    user_data = {
        "first_name": "Test",
        "last_name": "User",
        "email": email,
        "password": "password123",
        "role": role
    }
    response = requests.post(f"{BASE_URL}/admin/users", json=user_data, headers=headers)
    if response.status_code == 200:
        print(f"User {email} created successfully")
        return response.json()["user_id"]
    else:
        print(f"Failed to create user {email}: {response.json()}")
        return None

def update_user(token, user_id, new_email):
    headers = {"Authorization": f"Bearer {token}"}
    user_data = {
        "first_name": "Updated",
        "last_name": "User",
        "email": new_email,
        "role": "user",
        "status": "active"
    }
    response = requests.put(f"{BASE_URL}/admin/users/{user_id}", json=user_data, headers=headers)
    if response.status_code == 200:
        print(f"User {user_id} updated successfully")
    else:
        print(f"Failed to update user {user_id}: {response.json()}")

def delete_user(token, user_id):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.delete(f"{BASE_URL}/admin/users/{user_id}", headers=headers)
    if response.status_code == 200:
        print(f"User {user_id} deleted successfully")
    else:
        print(f"Failed to delete user {user_id}: {response.json()}")

def main():
    # Step 1: Login as admin
    admin_token = login(ADMIN_EMAIL, ADMIN_PASSWORD)
    if not admin_token:
        return

    # Step 2: Change admin password
    change_password(admin_token, NEW_ADMIN_PASSWORD)

    # Step 3: Attempt to delete self
    delete_self(admin_token)

    # Step 4: Create, update, and delete a normal user
    normal_user_email = "normal_user@example.com"
    normal_user_id = create_user(admin_token, normal_user_email, "user")
    if normal_user_id:
        update_user(admin_token, normal_user_id, "updated_normal_user@example.com")
        delete_user(admin_token, normal_user_id)

    # Step 5: Create, update, and delete an admin user
    admin_user_email = "new_admin@example.com"
    admin_user_id = create_user(admin_token, admin_user_email, "admin")
    if admin_user_id:
        update_user(admin_token, admin_user_id, "updated_admin@example.com")
        delete_user(admin_token, admin_user_id)

if __name__ == "__main__":
    main()