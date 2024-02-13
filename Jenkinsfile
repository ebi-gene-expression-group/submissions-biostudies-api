pipeline {
    agent {
        kubernetes {
            cloud 'atlas-admin-2'
            defaultContainer 'jnlp'
            yamlFile 'jenkins-k8s-pod.yaml'
        }
    }

    environment {
        DOCKER_REGISTRY = 'quay.io'
        DOCKER_REPO = 'ebigxa/submissions-biostudies-api' // Replace with your Quay repository
        DOCKER_IMAGE_TAG = "${DOCKER_REPO}:${BUILD_NUMBER}"
        DOCKER_IMAGE_LATEST = "${DOCKER_REPO}:latest"
    }

    stages {
        stage('Build Docker Image') {
            steps {
                script {
                    sh "docker build -t ${DOCKER_IMAGE_TAG} -f Dockerfile ."
                    sh "docker tag ${DOCKER_IMAGE_TAG} ${DOCKER_IMAGE_LATEST}"
                }
            }
        }

        stage('Push Docker Image to Quay') {
            steps {
                container('docker') {
                    script {
                        docker.withRegistry('https://quay.io', 'EBIGXA_QUAY_IO_TOKEN') {
                            docker.push(DOCKER_IMAGE_TAG)
                            docker.push(DOCKER_IMAGE_LATEST)
                        }
                    }
                }
            }
        }
    }

    post {
        success {
            echo "Docker image build and push succeeded"
        }
        failure {
            echo "Docker image build and push failed"
        }
    }
}
