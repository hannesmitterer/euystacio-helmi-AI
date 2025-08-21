## Euystacio Full Package Automated Deployment

To deploy the full Euystacio package into this repository, use the provided shell script:

### Steps

1. **Ensure you have cloned this repository and have the Euystacio_Full_Package directory available.**
2. **Run the deployment script:**

    ```bash
    ./deploy-euystacio.sh /path/to/Euystacio_Full_Package
    ```

3. **The script will:**
   - Copy all files from the package into the repo
   - Stage all changes
   - Commit with a unified pulse message
   - Push to the main branch

> **Note:** You must have Git installed and configured, and push permissions for the repository.