#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

function print_usage() {
    echo "Usage: $0 [major | minor | patch]"
    echo "  major: Increment the major version (e.g., v1.2.3 -> v2.0.0)"
    echo "  minor: Increment the minor version (e.g., v1.2.3 -> v1.3.0)"
    echo "  patch: Increment the patch version (e.g., v1.2.3 -> v1.2.4)"
    echo "Latest tag: ${LATEST_TAG}"
    exit 1
}

# Get the latest tag, or default to v0.0.0 if no tags exist
# The `git describe` command finds the most recent tag from the current commit.
LATEST_TAG=$(git describe --tags --abbrev=0 2>/dev/null || echo "v0.0.0")

# Ensure an argument is provided
if [ -z "$1" ]; then
    print_usage
fi

# Remove the 'v' prefix for arithmetic processing
VERSION=${LATEST_TAG#v}

# Split the version string into an array
IFS='.' read -r -a VERSION_PARTS <<< "$VERSION"
MAJOR=${VERSION_PARTS[0]}
MINOR=${VERSION_PARTS[1]}
PATCH=${VERSION_PARTS[2]}

case "$1" in
    major)
        NEW_MAJOR=$((MAJOR + 1))
        NEW_MINOR=0
        NEW_PATCH=0
        ;;
    minor)
        NEW_MAJOR=$MAJOR
        NEW_MINOR=$((MINOR + 1))
        NEW_PATCH=0
        ;;
    patch)
        NEW_MAJOR=$MAJOR
        NEW_MINOR=$MINOR
        NEW_PATCH=$((PATCH + 1))
        ;;
    *)
        print_usage
        ;;
esac

# Create the new version string
NEW_VERSION="v$NEW_MAJOR.$NEW_MINOR.$NEW_PATCH"

echo "Current version: $LATEST_TAG"
echo "New version: $NEW_VERSION"

# Create and push the new annotated tag
read -p "Do you want to create and push the new tag '$NEW_VERSION'? (y/n) " -n 1 -r
echo # Add a newline
if [[ $REPLY =~ ^[Yy]$ ]]
then
    git tag -a "$NEW_VERSION" -m "Release version $NEW_VERSION"
    git push origin "$NEW_VERSION"
    echo "New tag '$NEW_VERSION' created and pushed."
fi


