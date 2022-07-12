pipeline {
    agent any
    triggers {
        pollSCM('')
    }
    stages {
        stage('Build Application') {
            steps {
                echo '== Building Python-Flask Application =='
                // sh "pip install -r requirements.txt"
                sh 'pip install flask'
            }
        }
        stage('Run Application') {
            steps {
                echo '=== Running Python-Flask Application ==='
                sh 'python app.py'
            }
        }
        // stage('Build Docker Image') {
        //     when {
        //         branch 'main'
        //     }
        //     steps {
        //         echo '=== Building Petclinic Docker Image ==='
        //         script {
        //             app = docker.build('aravindsirivelli/flaskimg')
        //         }
        //     }
        // }
        // stage('Push Docker Image') {
        //     when {
        //         branch 'main'
        //     }
        //     steps {
        //         echo '=== Pushing Flask App Docker Image ==='
        //         script {
        //             GIT_COMMIT_HASH = sh (script: "git log -n 1 --pretty=format:'%H'", returnStdout: true)
        //             SHORT_COMMIT = "${GIT_COMMIT_HASH[0..7]}"
        //             docker.withRegistry('https://registry.hub.docker.com/u/aravindsirivelli', 'dockerHubCredentials') {
        //                 app.push("$SHORT_COMMIT")
        //                 app.push('latest')
        //             }
        //         }
        //     }
        // }