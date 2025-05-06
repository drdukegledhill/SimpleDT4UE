#!/bin/bash

# Create parent directory for separated repositories
mkdir -p ../SimpleDT4UE_Repos

# Function to copy a component to its new repository
copy_component() {
    local component=$1
    local target="../SimpleDT4UE_Repos/$component"
    
    echo "Copying $component to $target..."
    mkdir -p "$target"
    cp -r "$component"/* "$target/"
    cp "$component/.gitignore" "$target/" 2>/dev/null || true
    cp "$component/README.md" "$target/" 2>/dev/null || true
}

# Copy each component
copy_component "UnityDemo"
copy_component "MacOSDemo"
copy_component "iOSDemo"
copy_component "PiServer"
copy_component "PythonDemo"

# Copy main README
cp README.md ../SimpleDT4UE_Repos/

echo "Repository separation complete!"
echo "New repositories are located in: ../SimpleDT4UE_Repos/"
echo "Please initialize git repositories in each component directory." 