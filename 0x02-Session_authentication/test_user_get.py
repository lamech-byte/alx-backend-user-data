from models.user import User

user_id = "aa61b46b-61c4-40e9-9bb8-26419b2e2ac8"

user = User.get(user_id)

if user:
    print("User found:", user)
else:
    print("User not found")
