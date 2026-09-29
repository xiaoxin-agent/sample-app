pipeline {
    agent any

    environment {
        // 改成你自己的 Docker Hub 用户名
        IMAGE = 'YOUR_DOCKERHUB_USER/windriver-demo'
    }

    stages {
        stage('Build') {
            steps {
                // 用 venv 隔离依赖：Debian 系系统 Python 受 PEP 668 保护，
                // pip 不允许直接装包（--user 也一样），必须走虚拟环境
                sh '''
                    python3 -m venv .venv
                    .venv/bin/pip install -r requirements.txt
                '''
            }
        }
        stage('Test') {
            steps {
                sh 'mkdir -p reports && .venv/bin/pytest --junitxml=reports/junit.xml'
            }
            post {
                always {
                    junit 'reports/junit.xml'
                }
            }
        }
        stage('Package') {
            steps {
                sh 'docker build -t $IMAGE:$BUILD_NUMBER .'
            }
        }
        stage('Push') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub',
                        usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh 'echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin'
                    sh 'docker push $IMAGE:$BUILD_NUMBER'
                }
            }
        }
    }

    post {
        success {
            echo "构建成功：$IMAGE:$BUILD_NUMBER 已推送"
        }
        failure {
            echo '构建失败：去上面变红的 stage 看日志定位'
        }
    }
}
