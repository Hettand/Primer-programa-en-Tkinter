-- phpMyAdmin SQL Dump
-- version 3.5.1
-- http://www.phpmyadmin.net
--
-- Servidor: localhost
-- Tiempo de generación: 23-04-2019 a las 13:38:03
-- Versión del servidor: 5.5.24-log
-- Versión de PHP: 5.4.3

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Base de datos: `taller`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `bases`
--

CREATE TABLE IF NOT EXISTS `bases` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `idTaller` int(11) NOT NULL,
  `nombre` varchar(15) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `idTaller` (`idTaller`,`nombre`),
  KEY `idTaller_2` (`idTaller`),
  KEY `nombre` (`nombre`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=2 ;

--
-- Volcado de datos para la tabla `bases`
--

INSERT INTO `bases` (`id`, `idTaller`, `nombre`) VALUES
(1, 1, 'labase');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `clientes`
--

CREATE TABLE IF NOT EXISTS `clientes` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `email` varchar(35) NOT NULL,
  `bases` varchar(20) NOT NULL,
  `id_cliente` varchar(20) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  KEY `email_2` (`email`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=7 ;

--
-- Volcado de datos para la tabla `clientes`
--

INSERT INTO `clientes` (`id`, `email`, `bases`, `id_cliente`) VALUES
(6, 'paolapuchetta8@gmail.com', '1,', '1,');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `talleres`
--

CREATE TABLE IF NOT EXISTS `talleres` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(30) NOT NULL,
  `direccion` varchar(40) NOT NULL,
  `correo` varchar(35) NOT NULL,
  `contacto` varchar(60) NOT NULL,
  `tel` varchar(12) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  UNIQUE KEY `nombre` (`nombre`),
  UNIQUE KEY `correo` (`correo`),
  KEY `id_2` (`id`),
  KEY `nombre_2` (`nombre`),
  KEY `id_3` (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=2 ;

--
-- Volcado de datos para la tabla `talleres`
--

INSERT INTO `talleres` (`id`, `nombre`, `direccion`, `correo`, `contacto`, `tel`) VALUES
(1, 'labase', 'Austria 1423', 'positivarse@gmail.com', 'Paola', '91816348');

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
