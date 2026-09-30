pipeline {
    agent any

    environment {
        // 改成你自己的 Docker Hub 用户名
        IMAGE = 'xiaoxinagent/windriver-demo'
        // 改成你的 Harbor 地址（hostname 或 IP，不要带 http://）
        HARBOR_HOST = 'harbor.local:8088'
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
        stage('Push to Harbor') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'harbor',
                        usernameVariable: 'HARBOR_USER', passwordVariable: 'HARBOR_PASS')]) {
                    sh '''
                        echo "$HARBOR_PASS" | docker login "$HARBOR_HOST" -u "$HARBOR_USER" --password-stdin
                        docker tag "$IMAGE:$BUILD_NUMBER" "$HARBOR_HOST/library/windriver-demo:$BUILD_NUMBER"
                        docker push "$HARBOR_HOST/library/windriver-demo:$BUILD_NUMBER"
                    '''
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
