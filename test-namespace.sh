#!/bin/bash

NAMESPACE=$1
TEST_IMAGE=$2

echo ${TEST_IMAGE}

cp "${AWS_CONFIG_FILE}" ./aws_config
cp "${AWS_SHARED_CREDENTIALS_FILE}" ./aws_shared_credentials

set -x
docker run  --name system-tests --cap-add=NET_ADMIN --device /dev/net/tun:/dev/net/tun  --network=host  --volumes-from="$(docker ps -q)" -e AWS_CONFIG_FILE="$(pwd)/aws_config" -e AWS_SHARED_CREDENTIALS_FILE="$(pwd)/aws_shared_credentials" -i "${TEST_IMAGE}" "signalFlowSanityTests" "signalbox" "${NAMESPACE}"

docker cp system-tests:junit-report "${CI_PROJECT_DIR}/" || echo "junit-report copy failed"

docker cp system-tests:system-tests-status.txt "." || echo "system-tests-status copy failed"

docker rm system-tests

if grep -q "SYSTEM_TESTS_FAILED=true" system-tests-status.txt
then
    echo "System-tests failed"
    exit 1
elif grep -q "SYSTEM_TESTS_FAILED=false" system-tests-status.txt 
then
    echo "System-tests passed"
else
    echo "System-tests run-time error"
    exit 1
fi
