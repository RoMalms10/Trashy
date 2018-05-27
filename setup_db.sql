-- Creating User and giving it permissions
CREATE DATABASE IF NOT EXISTS trashy_db;
GRANT USAGE ON *.* 
      TO 'trashy_dev'@'localhost'
      IDENTIFIED BY 'trashy_dev_pwd';
GRANT ALL PRIVILEGES ON trashy_db.*
      TO 'trashy_dev'@'localhost'
      IDENTIFIED BY 'trashy_dev_pwd';
GRANT SELECT ON performance_schema.*
      TO 'trashy_dev'@'localhost'
      IDENTIFIED BY 'trashy_dev_pwd';
FLUSH PRIVILEGES;
