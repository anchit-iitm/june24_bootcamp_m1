#!/bin/bash

# Start temp_security.py in the background and get its PID
python temp_security.py &
SERVER_PID=$!

# Function to terminate server and exit script
function cleanup_and_exit {
    kill $SERVER_PID
    exit $1
}

# Wait for the server to start
sleep 5

# Test login for admin and user, capture tokens
ADMIN_TOKEN=$(curl -s -X POST -H "Content-Type: application/json" -d '{"email":"admin@a.com","password":"admin"}' http://localhost:5000/test1 | jq -r '.token')
USER_TOKEN=$(curl -s -X POST -H "Content-Type: application/json" -d '{"email":"user@a.com","password":"user"}' http://localhost:5000/test1 | jq -r '.token')

# Check if tokens are captured
if [ -z "$ADMIN_TOKEN" ] || [ -z "$USER_TOKEN" ]; then
    echo "Failed to obtain tokens"
    cleanup_and_exit 1
fi

# Test admin and user access
ADMIN_ACCESS=$(curl -s -H "Authorization:$ADMIN_TOKEN" http://localhost:5000/test2 | jq -r '.message')
USER_ACCESS=$(curl -s -H "Authorization:$USER_TOKEN" http://localhost:5000/test3 | jq -r '.message')

# Verify access
if [ "$ADMIN_ACCESS" != "admin only" ] || [ "$USER_ACCESS" != "public" ]; then
    echo "Access test failed"
    cleanup_and_exit 1
fi

# Create a new user via test4
NEW_USER_RESPONSE=$(curl -s -X POST -H "Content-Type: application/json" -d '{"email":"newuser@a.com","password":"newuser"}' http://localhost:5000/test4)

# Repeat login and role testing for the new user
NEW_USER_TOKEN=$(curl -s -X POST -H "Content-Type: application/json" -d '{"email":"newuser@a.com","password":"newuser"}' http://localhost:5000/test1 | jq -r '.token')

# Verify new user token
if [ -z "$NEW_USER_TOKEN" ]; then
    echo "Failed to obtain new user token"
    cleanup_and_exit 1
fi

# Test new user access
NEW_USER_ACCESS=$(curl -s -H "Authorization:$NEW_USER_TOKEN" http://localhost:5000/test3)
if echo "$NEW_USER_ACCESS" | jq -e .message > /dev/null; then
    NEW_USER_ACCESS_MSG=$(echo "$NEW_USER_ACCESS" | jq -r '.message')
else
    echo "Failed to parse JSON response: $NEW_USER_ACCESS"
    cleanup_and_exit 1
fi

# Verify new user access
if [ "$NEW_USER_ACCESS" != "public" ]; then
    echo "New user access test failed"
    cleanup_and_exit 1
fi

# If everything went right, terminate the server
cleanup_and_exit 0