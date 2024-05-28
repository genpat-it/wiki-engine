IMAGE_NAME = "${DOCKER_REPO}/bioinfo/${BRANCH_NAME}"
TOOL_VERSION = "1.2.4"

node("${DOCKER_BUILD_NODE}") {
    stage('SCM Checkout') { 
         scmVars = checkout scm
         IMAGE_ID = scmVars.GIT_COMMIT.take(10) 
    }
    stage("Docker build") {
        sh "docker build . -t ${IMAGE_NAME}:${TOOL_VERSION}--${IMAGE_ID}"
        sh "docker tag ${IMAGE_NAME}:${TOOL_VERSION}--${IMAGE_ID} ${IMAGE_NAME}:latest"        
    }
    stage("Docker push") {
        sh "docker push ${IMAGE_NAME}:${TOOL_VERSION}--${IMAGE_ID}"
        sh "docker push ${IMAGE_NAME}:latest"
    }
}