### 접속 ROOT/mysql 계정으로 접속

### 데이터베이스 생성
CREATE DATABASE KODB3

### 사용자 생성 local 및 외부 '%'
CREATE USER kopo3@'localhost' IDENTIFIED BY 'kopo3'

CREATE USER kopo3@'%' IDENTIFIED BY 'kopo3'

### 사용자 조회
SELECT HOST, USER
FROM MYSQL.USER

### 사용자 권한 부여 ON *.* 은 모든 데이터베이스 권한 부여
###              ON KODB2.* 은 KODB2에만 모든 권한 부여
GRANT ALL PRIVILEGES ON *.* TO kopo3@'localhost'

GRANT ALL PRIVILEGES ON *.* TO kopo3@'%'

### MYSQL 접속
