pipeline {
    agent any

    stages {
        stage('Clone') {
            steps {
                echo 'Cloning repository...'
                // Use 'checkout scm' to use the repository configured in the Jenkins job
                // This correctly handles branches (like 'main') and credentials automatically.
                checkout scm
                echo 'Clone stage successfully completed'
            }
        }

        stage('Install Dependencies') {
            steps {
                echo 'Installing dependencies...'
                // Using 'sh' for Linux/Mac agents. If running on Windows, replace 'sh' with 'bat'
                // and 'python3' with 'python'.
                script {
                    if (isUnix()) {
                        sh 'python3 -m venv venv'
                        sh '. venv/bin/activate && pip install -r requirements.txt'
                    } else {
                        bat 'python -m venv venv'
                        bat 'call venv\\Scripts\\activate.bat && pip install -r requirements.txt'
                    }
                }
                echo 'Install Dependencies stage successfully completed'
            }
        }

        stage('Run Unit Tests') {
            steps {
                echo 'Running unit tests...'
                script {
                     if (isUnix()) {
                        sh '. venv/bin/activate && python3 -m pytest'
                    } else {
                        bat 'call venv\\Scripts\\activate.bat && python -m pytest'
                    }
                }
                echo 'Run Unit Tests stage successfully completed'
            }
        }

        stage('Build') {
            steps {
                echo 'Building application...'
                // Example build step: Create a zip file of the application
                script {
                    if (isUnix()) {
                        sh 'zip -r flaskapp.zip . -x "venv/*" -x ".git/*" -x "__pycache__/*"'
                    } else {
                        // Requires 7zip or standard powershell compression if available. 
                        // Using a simple echo for now or standard powershell command
                        powershell 'Get-ChildItem -Exclude "venv","env",".git","__pycache__","*.zip" | Compress-Archive -DestinationPath flaskapp.zip -Force'
                    }
                }
                archiveArtifacts artifacts: 'flaskapp.zip', allowEmptyArchive: true
                echo 'Build stage successfully completed'
            }
        }

        stage('Deploy') {
            steps {
                echo 'Deploying application...'
                script {
                    if (isUnix()) {
                         echo "Deploying to production server at /var/www/flaskapp..."
                         // Example: unzip flaskapp.zip -d /var/www/flaskapp
                         // sh 'unzip -o flaskapp.zip -d /var/www/flaskapp'
                    } else {
                         echo "Deploying to local Desktop folder..."
                         // Expand to specific Desktop folder
                         powershell 'Expand-Archive -Path flaskapp.zip -DestinationPath "C:\\Users\\Malik Inam\\Desktop\\flask_deploy" -Force'
                    }
                }
                echo 'Deploy stage successfully completed'
            }
        }
    }
}
