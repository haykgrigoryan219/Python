import requests

# Base URL for the JSONPlaceholder API
BASE_URL = "https://jsonplaceholder.typicode.com"

# GET Request
def get_filtered_posts():
    # Fetch posts
    response = requests.get(f"{BASE_URL}/posts")
    if response.status_code == 200:
        posts = response.json()
        
        # Filter posts by title length and body content
        filtered_posts = [
            post for post in posts
            if len(post['title'].split()) <= 6 and post['body'].count('\n') <= 3
        ]
        
        return filtered_posts
    else:
        print(f"Failed to fetch posts: {response.status_code}")
        return []

# POST Request
def create_new_post():
    # Data for the new post
    new_post = {
        "title": "New Post Title",
        "body": "This is the body of the new post.",
        "userId": 1
    }
    
    response = requests.post(f"{BASE_URL}/posts", json=new_post)
    
    if response.status_code == 201:
        print("Post created successfully.")
        print(response.json())
    else:
        print(f"Failed to create post: {response.status_code}")

# PUT Request
def update_post(post_id):
    # Data to update the post
    updated_post = {
        "title": "Updated Post Title",
        "body": "This is the updated body of the post.",
        "userId": 1
    }
    
    response = requests.put(f"{BASE_URL}/posts/{post_id}", json=updated_post)
    
    if response.status_code == 200:
        print("Post updated successfully.")
        print(response.json())
    else:
        print(f"Failed to update post: {response.status_code}")

# DELETE Request
def delete_post(post_id):
    response = requests.delete(f"{BASE_URL}/posts/{post_id}")
    
    if response.status_code == 200:
        print(f"Post {post_id} deleted successfully.")
        print(response.json())
    else:
        print(f"Failed to delete post: {response.status_code}")


#GET request and filtering
filtered_posts = get_filtered_posts()
for i in filtered_posts:
  print(i)

# POST request to create a new post
create_new_post()

# PUT request to update a post with ID 1
update_post(1)

# DELETE request to delete a post with ID 1
delete_post(1)
