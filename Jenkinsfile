pipeline {
    agent any
    options {
    buildDiscarder(logRotator(numToKeepStr: '20', daysToKeepStr: '5'))
    }
    environment {
        username = credentials("username")
        password = credentials("password")
        dusername = credentials('dusername')
        dpassword = credentials('dpassword')
    }
    stages {
        stage('checkout') {
            steps {
                script {
                    properties([pipelineTriggers([pollSCM('*/30 * * * *')])])
                }
                git 'https://github.com/dor-solomon/courseProjectExtra.git'
            }
        }
        stage('run backend server') {
            steps {
                script {
                    if (isUnix()) {
                       sh 'nohup python rest_app.py ${username} ${password} ${host} &'
                     }
                     else {
                       bat 'start /min python rest_app.py %username% %password% %host%'
                     }
                 }
            }
        }
        stage('run backend_testing') {
            steps {
                script {
                    if (isUnix()) {
                       sh 'nohup python backend_testing.py ${username} ${password} ${host} &'
                     }
                     else {
                       bat 'python backend_testing.py %username% %password% %host%'
                     }
                 }
            }
        }
        stage('run clean_environment') {
            steps {
                script {
                    if (isUnix()) {
                       sh 'python clean_environment.py'
                     }
                     else {
                       bat 'python clean_environment.py'
                     }
                 }
            }
        }
        stage('build docker image') {
            steps {
                script {
                    if (isUnix()) {
                       sh 'docker build . -t ${dusername}/rest'
                     }
                     else {
                       bat 'docker build . -t %dusername%/rest'
                     }
                 }
            }
        }
        stage('push docker image') {
            steps {
                script {
                    if (isUnix()) {
                       sh 'docker login -u $dusername -p $dpassword'
                       sh 'docker push ${dusername}/rest'
                     }
                     else {
                       bat 'docker login -u %dusername% -p %dpassword%'
                       bat 'docker push %dusername%/rest'
                     }
                 }
            }
        }
        stage('set compose image version') {
            steps {
                script {
                    if (isUnix()) {
                       sh 'echo IMAGE_TAG=${BUILD_NUMBER} > .env'
                     }
                     else {
                       bat 'echo IMAGE_TAG=${BUILD_NUMBER} > .env'
                     }
                 }
            }
        }
        stage('docker-compose up') {
            steps {
                script {
                    if (isUnix()) {
                       sh 'docker-compose build --no-cache --build-arg username=${username} --build-arg password=${password} --build-arg host=${host}'
                       sh 'docker-compose up -d'
                     }
                     else {
                       bat 'docker-compose build --no-cache --build-arg username=%username% --build-arg password=%password% --build-arg host=%host%'
                       bat 'docker-compose up -d'
                     }
                 }
            }
        }
        stage('test docker container') {
            steps {
                script {
                    if (isUnix()) {
                       sh 'python docker_backend_testing.py ${username} ${password} ${host}'
                     }
                     else {
                       bat 'python docker_backend_testing.py %username% %password% %host%'
                     }
                 }
            }
        }
        stage('clean environment') {
            steps {
                script {
                    if (isUnix()) {
                       sh 'docker-compose down'
                       sh 'docker rmi rest:${BUILD_NUMBER}'
                     }
                     else {
                       bat 'docker-compose down'
                       bat 'docker rmi rest:${BUILD_NUMBER}'
                     }
                 }
            }
        }
        stage('deploy helm chart') {
            steps {
                script {
                    if (isUnix()) {
                       sh 'helm install rest-helm rest-helm --set image.repository=${dusername}/rest:${BUILD_NUMBER}'
                     }
                     else {
                       bat 'helm install rest-helm rest-helm --set image.repository=%dusername%/rest:${BUILD_NUMBER}'
                     }
                 }
            }
        }
        stage('service url') {
            steps {
                script {
                    if (isUnix()) {
                       sh 'minikube service rest-service --url > k8s_url.txt'
                     }
                     else {
                       bat 'minikube service rest-service --url > k8s_url.txt'
                     }
                 }
            }
        }
        stage('K8S_backend_testing') {
            steps {
                script {
                    if (isUnix()) {
                       sh 'python K8S_backend_testing.py ${username} ${password} ${host}'
                     }
                     else {
                       bat 'python K8S_backend_testing.py %username% %password% %host%'
                     }
                 }
            }
        }
        stage('Clean HELM environment') {
            steps {
                script {
                    if (isUnix()) {
                       sh 'helm delete rest-helm'
                     }
                     else {
                       bat 'helm delete rest-helm'
                     }
                 }
            }
        }
    }
}