-- Crear la base de datos principal (ya definida en MYSQL_DATABASE)
CREATE DATABASE IF NOT EXISTS tokenizacion;
CREATE DATABASE IF NOT EXISTS usuarios;

-- Crear usuarios específicos para cada base de datos
CREATE USER IF NOT EXISTS 'usuario_tokenizacion'@'%' IDENTIFIED BY 'password_tokenizacion';
CREATE USER IF NOT EXISTS 'usuario_usuarios'@'%' IDENTIFIED BY 'password_usuarios';

-- Otorgar permisos a los usuarios
GRANT ALL PRIVILEGES ON tokenizacion.* TO 'usuario_tokenizacion'@'%';
GRANT ALL PRIVILEGES ON usuarios.* TO 'usuario_usuarios'@'%';

-- Aplicar los cambios
FLUSH PRIVILEGES;