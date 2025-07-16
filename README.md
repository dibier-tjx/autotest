# autotest

sudo apt install openjdk-11-jdk

sudo apt install ./allure_2.34.1-1_all.deb

allure generate ./result -o ./report --clean

allure open -h 127.0.0.1 -p 8883 ./report