pipeline {
    agent any
    environment {
        SONAR_AUTH_TOKEN = credentials('SONAR_AUTH_TOKEN')
    }
    stages {
        stage('Build') {
            steps {
                echo 'Building...'
            }
        }
        stage('SAST - SonarQube Scan') {
            steps {
                withSonarQubeEnv('SonarLocal') {
                    bat """
                        sonar-scanner ^
                        -Dsonar.projectKey=MyProject ^
                        -Dsonar.sources=src ^
                        -Dsonar.host.url=http://localhost:9000 ^
                        -Dsonar.login=%SONAR_AUTH_TOKEN%
                    """
                }
            }
        }
        stage('Test') {
            steps { echo 'Testing...' }
        }
        stage('Deploy') {
            steps { echo 'Deploying...' }
        }
    }
}
