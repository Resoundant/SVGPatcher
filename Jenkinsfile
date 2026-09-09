pipeline{
    agent{label 'build-lin3'}
    environment{
        START_TIME = new Date().format("YYYYMMddHHmm", TimeZone.getTimeZone('CST'))
        VENV = ".venv_build"
    }
    stages{
        stage('BUILD'){
            steps{
                script{
                    //Run build script
                    sh """
                    chmod +x ./build.sh
                    ./build.sh
                    """
                }
            }
        }
        stage('STORE ARTIFACTS') {
            steps {
                script {
                    def repo1Status = 1
                    def repo2Status = 1

                    // Upload to rpy
                    withCredentials([usernamePassword(
                        credentialsId: 'jenkins-pypiserver',
                        usernameVariable: 'PYPI_USER',
                        passwordVariable: 'PYPI_PASS'
                    )]) {
                        repo1Status = sh(
                            label: 'Upload package to rpy',
                            returnStatus: true,
                            script: '''
                                ./"$VENV"/bin/python3 -m twine upload \
                                    --repository-url http://rpy.resoundant-hq.com:8081 \
                                    -u "$PYPI_USER" \
                                    -p "$PYPI_PASS" \
                                    ./dist/*
                            '''
                        )
                    }

                    repo2Status = sh(
                        label: 'Upload package to cicd2',
                        returnStatus: true,
                        script: '''
                            ./"$VENV"/bin/python3 -m twine upload \
                                --repository-url http://cicd2.resoundant-hq.com:8081 \
                                --skip-existing \
                                -u anon \
                                -p anon \
                                ./dist/*
                        '''
                    )

                    if (repo1Status != 0) {
                        echo "Upload to rpy failed with exit code ${repo1Status}"
                    }

                    if (repo2Status != 0) {
                        echo "Upload to cicd2 failed with exit code ${repo2Status}"
                    }

                    if (repo1Status != 0 && repo2Status != 0) {
                        error('Artifact upload failed for both repositories')
                    }
                }
            }
        }
    }
    post{
        failure{
            script{
                //Send email notification
                emailext(attachLog:true,
                        body:"""Project: SVGPatcher
                               |DevOps Step: Build
                               |Build #: ${BUILD_NUMBER}
                               |Result: PIPELINE FAILURE
                               |Build Start Time: ${env.START_TIME}
                               |Branch: ${env.BRANCH_NAME}
                               |Commit: ${env.GIT_COMMIT}
                               |Please check the attached log.""".stripMargin(),
                        subject:"${JOB_NAME}: PIPELINE FAILURE, Build #${BUILD_NUMBER}",
                        to:'kkalutkiewicz@resoundant.com JHeilman@resoundant.com aalfayad@resoundant.com alfayad.abdulrahman@mayo.edu')
            }
        }
    }
}