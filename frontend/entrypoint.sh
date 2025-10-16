#!/bin/sh

# Write REACT_APP_* variables to .env
echo "REACT_APP_BACKEND_URL=$REACT_APP_BACKEND_URL" > .env

# Start the React dev server
npm start
