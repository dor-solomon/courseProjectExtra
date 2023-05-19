pipeline {
    agent any
    options {
    buildDiscarder(logRotator(numToKeepStr: '20', daysToKeepStr: '5'))
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
                bat 'start /min python rest_app.py %username% %password%'
            }
        }
        stage('run frontend server') {
            steps {
                bat 'start /min python web_app.py %username% %password%'
            }
        }
        stage('run backend_testing') {
            steps {
                bat 'python backend_testing.py %username% %password%'
            }
        }
        stage('run frontend_testing') {
            steps {
                bat 'python frontend_testing.py %username% %password%'
            }
        }
        stage('run combined_testing') {
            steps {
                bat 'python combined_testing.py %username% %password%'
            }
        }
        stage('run clean_environment') {
            steps {
                bat 'python clean_environment.py'
            }
        }
    }
}