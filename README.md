# github-runners

helm upgrade gha-runner-scale-set ./gha-runner-scale-set --values gha-runner-scale-set/values.yaml

helm pull jenkins/jenkins --version 5.7.15 --untar

helm install jenkins ./jenkins --values jenkins/plugins.yaml