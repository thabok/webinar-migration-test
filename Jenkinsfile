node {

    stage('preparations') {
        checkout scm
        // bat 'pip install btc_embedded --upgrade'
    }

    stage('test') {
        dir('multi') { bat 'python -u test_all_models.py' }
    }

    stage('wrap-up') {
        archiveArtifacts artifacts: 'results/*.epp', followSymlinks: false
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