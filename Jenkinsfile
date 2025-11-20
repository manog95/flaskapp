pipeline {
agent any
stages {
stage('Build') {
steps {
echo 'Building..'
// Here you can define commands for your build
}
}
stage('SAST - SonarQube Scan') {
            steps {
                withSonarQubeEnv('SonarLocal') {
                    bat '''
                        sonar-scanner ^
                        -Dsonar.projectKey=MyProject ^
                        -Dsonar.sources=src ^
                        -Dsonar.host.url=http://localhost:9000 ^
                        -Dsonar.login=%SONAR_AUTH_TOKEN%
                    '''
                }
            }
      }
stage('Test') {
steps {
echo 'Testing..'
// Here you can define commands for your tests
}
}
stage('Deploy') {
steps {
echo 'Deploying....'
// Here you can define commands for your deployment
}
}
}
}
