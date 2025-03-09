-- Crear la base de datos principal (ya definida en MYSQL_DATABASE)
CREATE DATABASE IF NOT EXISTS tokenizacion;
CREATE DATABASE IF NOT EXISTS anonimizacion;
CREATE DATABASE IF NOT EXISTS hsm;
CREATE DATABASE IF NOT EXISTS validacion;
CREATE DATABASE IF NOT EXISTS sagas;

-- Crear usuarios específicos para cada base de datos
CREATE USER IF NOT EXISTS 'usuario_tokenizacion'@'%' IDENTIFIED BY 'password_tokenizacion';
CREATE USER IF NOT EXISTS 'usuario_anonimizacion'@'%' IDENTIFIED BY 'password_anonimizacion';
CREATE USER IF NOT EXISTS 'usuario_hsm'@'%' IDENTIFIED BY 'password_hsm';
CREATE USER IF NOT EXISTS 'usuario_validacion'@'%' IDENTIFIED BY 'password_validacion';
CREATE USER IF NOT EXISTS 'usuario_sagas'@'%' IDENTIFIED BY 'password_sagas';

-- Otorgar permisos a los usuarios
GRANT ALL PRIVILEGES ON tokenizacion.* TO 'usuario_tokenizacion'@'%';
GRANT ALL PRIVILEGES ON anonimizacion.* TO 'usuario_anonimizacion'@'%';
GRANT ALL PRIVILEGES ON hsm.* TO 'usuario_hsm'@'%';
GRANT ALL PRIVILEGES ON validacion.* TO 'usuario_validacion'@'%';
GRANT ALL PRIVILEGES ON sagas.* TO 'usuario_sagas'@'%';

-- Aplicar los cambios
FLUSH PRIVILEGES;