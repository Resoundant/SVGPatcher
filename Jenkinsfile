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
        stage('STORE ARTIFACTS'){
            steps{
                script{
                    //Push package to pypiserver
                    withCredentials([usernamePassword(
                        credentialsId:'jenkins-pypiserver',
                        usernameVariable:'PYPI_USER',
                        passwordVariable:'PYPI_PASS')]){
                            sh """
                            ./"${env.VENV}"/bin/python3 -m twine upload --repository-url http://rpy.resoundant-hq.com:8081 -u "${PYPI_USER}" -p "${PYPI_PASS}" ./dist/*
                            """
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