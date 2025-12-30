# Jenkins Pipeline Report

**GitHub Repository:** [https://github.com/manog95/flaskapp](https://github.com/manog95/flaskapp)

This report provides a brief explanation of each stage in the Jenkins pipeline defined for the Flask application.

## Pipeline Stages

### 1. Clone
- **Purpose**: Retrieves the source code from the GitHub repository.
- **Action**: Uses the `checkout scm` command to check out the branch configured in the Jenkins job (e.g., `main`). This ensures the build uses the latest code.
- **Success Criteria**: The repository files are successfully downloaded to the Jenkins workspace.

### 2. Install Dependencies
- **Purpose**: Prepares the runtime environment by creating a secure, isolated virtual environment.
- **Action**:
    - Creates a Python virtual environment (`venv`).
    - Activates the virtual environment.
    - Installs all required libraries listed in `requirements.txt` (e.g., Flask, pytest, Flask-SQLAlchemy).
- **Success Criteria**: All dependencies are installed without errors.

### 3. Run Unit Tests
- **Purpose**: Verifies the application's functionality before building.
- **Action**: Executes the unit tests defined in `tests/test_app.py` using the `pytest` framework within the virtual environment.
- **Success Criteria**: All defined tests (Home, Login, Register, 404) pass.

### 4. Build
- **Purpose**: Packages the application for deployment.
- **Action**: Compresses the application files into a zip archive (`flaskapp.zip`). It intelligently excludes development artifacts like the virtual environment (`venv`, `env`), git metadata (`.git`), and cache files (`__pycache__`) to keep the build clean.
- **Success Criteria**: A `flaskapp.zip` artifact is created in the workspace.

### 5. Deploy
- **Purpose**: Deploys the application to the target environment.
- **Action**: This stage is configured to unpack the build artifact.
    - **Windows**: Extracts `flaskapp.zip` to `C:\Users\Malik Inam\Desktop\flask_deploy`.
    - **Linux**: Configured to extract to `/var/www/flaskapp`.
- **Success Criteria**: The application files are successfully extracted to the target directory.
