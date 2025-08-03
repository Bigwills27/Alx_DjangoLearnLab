#!/usr/bin/env python3
"""
Test script for the API endpoints following ALX requirements
"""
import requests
import json

# Base URL for the API
BASE_URL = "http://127.0.0.1:8000/api"

def test_unauthenticated_access():
    """Test accessing endpoints without authentication"""
    print("=== Testing Unauthenticated Access ===")
    
    # Test BookList view (should work without authentication)
    try:
        response = requests.get(f"{BASE_URL}/books/")
        print(f"GET /api/books/ - Status: {response.status_code}")
        if response.status_code == 200:
            books = response.json()
            print(f"Found {len(books)} books")
            for book in books[:3]:  # Show first 3 books
                print(f"  - {book['title']} by {book['author']}")
    except Exception as e:
        print(f"Error testing BookList: {e}")
    
    # Test BookViewSet endpoints (should require authentication)
    try:
        response = requests.get(f"{BASE_URL}/books_all/")
        print(f"GET /api/books_all/ - Status: {response.status_code}")
        if response.status_code == 401:
            print("✓ Authentication required as expected")
        else:
            print("⚠ Expected authentication to be required")
    except Exception as e:
        print(f"Error testing BookViewSet: {e}")

def test_token_authentication():
    """Test token authentication"""
    print("\n=== Testing Token Authentication ===")
    
    # Get authentication token
    auth_data = {
        "username": "admin",
        "password": "adminpassword"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api-token-auth/", data=auth_data)
        print(f"POST /api/api-token-auth/ - Status: {response.status_code}")
        
        if response.status_code == 200:
            token_data = response.json()
            token = token_data.get('token')
            print(f"✓ Token obtained: {token[:20]}...")
            
            # Test authenticated access
            headers = {"Authorization": f"Token {token}"}
            
            # Test GET all books
            response = requests.get(f"{BASE_URL}/books_all/", headers=headers)
            print(f"GET /api/books_all/ (authenticated) - Status: {response.status_code}")
            if response.status_code == 200:
                books = response.json()
                print(f"✓ Found {len(books)} books with authentication")
            
            # Test POST new book
            new_book = {
                "title": "Test Book",
                "author": "Test Author"
            }
            response = requests.post(f"{BASE_URL}/books_all/", json=new_book, headers=headers)
            print(f"POST /api/books_all/ (create book) - Status: {response.status_code}")
            if response.status_code == 201:
                created_book = response.json()
                print(f"✓ Created book: {created_book['title']}")
                return created_book['id']  # Return ID for testing update/delete
            
        else:
            print("⚠ Failed to obtain token")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"Error testing authentication: {e}")
    
    return None

def test_crud_operations(token, book_id=None):
    """Test CRUD operations with authentication"""
    print("\n=== Testing CRUD Operations ===")
    
    if not token:
        print("⚠ No token available for CRUD testing")
        return
    
    headers = {"Authorization": f"Token {token}"}
    
    if book_id:
        # Test GET single book
        try:
            response = requests.get(f"{BASE_URL}/books_all/{book_id}/", headers=headers)
            print(f"GET /api/books_all/{book_id}/ - Status: {response.status_code}")
            if response.status_code == 200:
                book = response.json()
                print(f"✓ Retrieved book: {book['title']}")
        except Exception as e:
            print(f"Error testing GET single book: {e}")
        
        # Test PUT update book
        try:
            updated_book = {
                "title": "Updated Test Book",
                "author": "Updated Test Author"
            }
            response = requests.put(f"{BASE_URL}/books_all/{book_id}/", json=updated_book, headers=headers)
            print(f"PUT /api/books_all/{book_id}/ - Status: {response.status_code}")
            if response.status_code == 200:
                print("✓ Book updated successfully")
        except Exception as e:
            print(f"Error testing PUT update: {e}")
        
        # Test DELETE book
        try:
            response = requests.delete(f"{BASE_URL}/books_all/{book_id}/", headers=headers)
            print(f"DELETE /api/books_all/{book_id}/ - Status: {response.status_code}")
            if response.status_code == 204:
                print("✓ Book deleted successfully")
        except Exception as e:
            print(f"Error testing DELETE: {e}")

def main():
    """Run all tests"""
    print("Starting API Tests for ALX Django REST Framework Project")
    print("="*60)
    
    test_unauthenticated_access()
    
    # Get token and test authenticated operations
    auth_data = {"username": "admin", "password": "adminpassword"}
    try:
        response = requests.post(f"{BASE_URL}/api-token-auth/", data=auth_data)
        if response.status_code == 200:
            token = response.json().get('token')
            
            # Create a test book for CRUD operations
            headers = {"Authorization": f"Token {token}"}
            new_book = {"title": "CRUD Test Book", "author": "CRUD Test Author"}
            response = requests.post(f"{BASE_URL}/books_all/", json=new_book, headers=headers)
            if response.status_code == 201:
                book_id = response.json()['id']
                test_crud_operations(token, book_id)
            else:
                test_crud_operations(token)
        else:
            print("Could not obtain authentication token for CRUD testing")
    except Exception as e:
        print(f"Error in main test flow: {e}")
    
    print("\n" + "="*60)
    print("API Tests Complete!")

if __name__ == "__main__":
    main()
