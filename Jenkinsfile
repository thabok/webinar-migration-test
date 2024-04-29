node {

    stage('preparations') {
        checkout scm
        bat 'pip install btc_embedded --upgrade'
    }

    stage('test') {
        bat 'python -u multi/test_all_models.py'
    }

    stage('wrap-up') {
        publishHTML([allowMissing: false,
            alwaysLinkToLastBuild: false,
            includes: '*.html',
            keepAll: false,
            reportDir: 'results',
            reportFiles: 'BTCMigrationTestSuite.html',
            reportName: 'BTC Migration Test Suite',
            reportTitles: '',
            useWrapperFileDirectly: true])
    }

}