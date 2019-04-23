-- phpMyAdmin SQL Dump
-- version 3.5.1
-- http://www.phpmyadmin.net
--
-- Servidor: localhost
-- Tiempo de generación: 12-04-2019 a las 14:15:50
-- Versión del servidor: 5.5.24-log
-- Versión de PHP: 5.4.3

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Base de datos: `labase`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `actualizaciones`
--

CREATE TABLE IF NOT EXISTS `actualizaciones` (
  `id_trabajo` int(11) NOT NULL,
  `id_vehiculo` varchar(8) NOT NULL COMMENT 'dato cambiado a matricula',
  `fecha` date NOT NULL,
  `hora` time NOT NULL,
  `servicios` text CHARACTER SET utf8 NOT NULL,
  `precios` text CHARACTER SET utf8 NOT NULL,
  `porcentaje_desc` float NOT NULL,
  `descuento` float NOT NULL,
  `porcentaje_iva` float NOT NULL,
  `iva` float NOT NULL,
  `descripcion` varchar(20) CHARACTER SET utf8 NOT NULL,
  `actualizacion` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`actualizacion`),
  KEY `id_trabajo` (`id_trabajo`),
  KEY `id_vehiculo` (`id_vehiculo`),
  KEY `id_vehiculo_2` (`id_vehiculo`),
  KEY `id_trabajo_2` (`id_trabajo`),
  KEY `id_vehiculo_3` (`id_vehiculo`),
  KEY `id_vehiculo_4` (`id_vehiculo`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `articulos`
--

CREATE TABLE IF NOT EXISTS `articulos` (
  `idArt` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(40) NOT NULL,
  `idCat` int(11) NOT NULL,
  `idProv` int(11) NOT NULL,
  `cantidad` float NOT NULL,
  `medida` int(11) NOT NULL,
  `costo` decimal(11,0) NOT NULL,
  PRIMARY KEY (`idArt`),
  UNIQUE KEY `nombre` (`nombre`),
  KEY `medida` (`medida`),
  KEY `idCat` (`idCat`),
  KEY `idProv` (`idProv`),
  KEY `nombre_2` (`nombre`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=6 ;

--
-- Volcado de datos para la tabla `articulos`
--

INSERT INTO `articulos` (`idArt`, `nombre`, `idCat`, `idProv`, `cantidad`, `medida`, `costo`) VALUES
(1, 'Trapos', 1, 1, 25, 1, '98'),
(2, 'Pintamax', 2, 1, 20, 3, '5600'),
(3, 'El solvente', 3, 2, 20, 3, '6400'),
(4, 'Cloro', 8, 1, 20, 3, '340'),
(5, 'Aquapura', 10, 2, 25, 3, '179');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `bajas_vehiculos`
--

CREATE TABLE IF NOT EXISTS `bajas_vehiculos` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `idV` int(11) NOT NULL COMMENT 'id vehiculo',
  `marca` varchar(30) NOT NULL,
  `modelo` varchar(50) NOT NULL,
  `matricula` varchar(8) NOT NULL,
  `idC` int(11) NOT NULL COMMENT 'id cliente',
  PRIMARY KEY (`id`),
  KEY `idC` (`idC`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COMMENT='almacena los vehiculos dados de baja ' AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `categorias`
--

CREATE TABLE IF NOT EXISTS `categorias` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(30) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nombre` (`nombre`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=12 ;

--
-- Volcado de datos para la tabla `categorias`
--

INSERT INTO `categorias` (`id`, `nombre`) VALUES
(10, 'Bebidas'),
(1, 'General'),
(4, 'Jabones'),
(7, 'Lijas'),
(8, 'Limpieza'),
(5, 'Lubricantes'),
(9, 'Oficina'),
(2, 'Pinturas'),
(3, 'Solventes'),
(6, 'Taladros'),
(11, 'Utensilios');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `datos_usuarios2`
--

CREATE TABLE IF NOT EXISTS `datos_usuarios2` (
  `id_cliente` int(11) NOT NULL AUTO_INCREMENT,
  `ingreso` date NOT NULL,
  `documento` varchar(15) NOT NULL,
  `nacimiento` date DEFAULT NULL,
  `nombre` varchar(15) NOT NULL,
  `apellido` varchar(15) NOT NULL,
  `apellido_dos` varchar(15) DEFAULT '',
  `telefono` varchar(15) NOT NULL,
  `direccion` varchar(30) DEFAULT '',
  `correo` varchar(80) NOT NULL DEFAULT '',
  `estado` int(1) NOT NULL DEFAULT '1',
  PRIMARY KEY (`id_cliente`),
  UNIQUE KEY `documento` (`documento`),
  UNIQUE KEY `correo` (`correo`),
  KEY `id_cliente` (`id_cliente`),
  KEY `id_cliente_2` (`id_cliente`),
  KEY `documento_2` (`documento`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8 AUTO_INCREMENT=2 ;

--
-- Volcado de datos para la tabla `datos_usuarios2`
--

INSERT INTO `datos_usuarios2` (`id_cliente`, `ingreso`, `documento`, `nacimiento`, `nombre`, `apellido`, `apellido_dos`, `telefono`, `direccion`, `correo`, `estado`) VALUES
(1, '2019-04-11', '45128013', '1984-02-24', 'Paola', 'Puchetta', 'Alves', '091816348', 'Austria 1423', 'paolapuchetta8@gmail.com', 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `egresos`
--

CREATE TABLE IF NOT EXISTS `egresos` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `articulo` int(11) NOT NULL,
  `costo` decimal(10,0) DEFAULT '0',
  `cantidad` float NOT NULL,
  `fecha` date NOT NULL,
  `usuario` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `articulo` (`articulo`),
  KEY `usuario` (`usuario`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=12 ;

--
-- Volcado de datos para la tabla `egresos`
--

INSERT INTO `egresos` (`id`, `articulo`, `costo`, `cantidad`, `fecha`, `usuario`) VALUES
(3, 1, '98', 6, '2019-04-10', 2),
(4, 3, '6400', 15, '2019-04-10', 2),
(5, 1, '98', 2, '2019-04-10', 1),
(6, 1, '98', 10, '2019-04-10', 1),
(7, 2, '5600', 3, '2019-04-11', 1),
(8, 2, '5600', 2, '2019-04-11', 1),
(9, 3, '6400', 5, '2019-04-11', 1),
(10, 3, '6400', 1, '2019-04-11', 1),
(11, 4, '340', 1, '2019-04-11', 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `existencias`
--

CREATE TABLE IF NOT EXISTS `existencias` (
  `id` int(11) NOT NULL,
  `existencias` float DEFAULT '0',
  `cantidad` varchar(15) NOT NULL,
  `minimo` int(11) DEFAULT '0',
  `maximo` int(11) DEFAULT '0',
  `ingreso` date DEFAULT '0000-00-00',
  `egreso` date DEFAULT '0000-00-00',
  UNIQUE KEY `id_2` (`id`),
  KEY `id` (`id`),
  KEY `id_3` (`id`),
  KEY `articulo` (`id`),
  KEY `id_4` (`id`),
  KEY `id_5` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Volcado de datos para la tabla `existencias`
--

INSERT INTO `existencias` (`id`, `existencias`, `cantidad`, `minimo`, `maximo`, `ingreso`, `egreso`) VALUES
(1, 14, '25 1', 5, 15, '2019-04-11', '2019-04-10'),
(2, 60, '20 3', 15, 30, '2019-04-11', '2019-04-11'),
(3, 2, '20 3', 10, 20, '2019-04-10', '2019-04-11'),
(4, 5, '20 3', 5, 10, '2019-04-11', '2019-04-11'),
(5, 10, '25 3', 5, 10, '2019-04-11', '0000-00-00');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `ingresos`
--

CREATE TABLE IF NOT EXISTS `ingresos` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `articulo` int(11) NOT NULL,
  `costo` decimal(10,0) DEFAULT '0',
  `cantidad` float NOT NULL,
  `fecha` date NOT NULL,
  `usuario` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `articulo` (`articulo`),
  KEY `usuario` (`usuario`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=15 ;

--
-- Volcado de datos para la tabla `ingresos`
--

INSERT INTO `ingresos` (`id`, `articulo`, `costo`, `cantidad`, `fecha`, `usuario`) VALUES
(1, 1, '98', 10, '2019-04-10', 2),
(2, 2, '0', 35, '2019-04-10', 1),
(3, 1, '98', 20, '2019-04-10', 1),
(4, 2, '5600', 4, '2019-04-10', 2),
(5, 3, '6400', 5, '2019-04-10', 1),
(6, 2, '5600', 5, '2019-04-10', 1),
(7, 2, '5600', 10, '2019-04-10', 1),
(8, 2, '5600', 4, '2019-04-10', 1),
(9, 2, '5600', 5, '2019-04-10', 1),
(10, 3, '6400', 15, '2019-04-10', 1),
(11, 2, '5600', 1, '2019-04-11', 1),
(12, 4, '340', 6, '2019-04-11', 1),
(13, 5, '179', 10, '2019-04-11', 1),
(14, 1, '98', 1, '2019-04-11', 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `iva`
--

CREATE TABLE IF NOT EXISTS `iva` (
  `id_iva` int(11) NOT NULL AUTO_INCREMENT,
  `porcentaje` float NOT NULL,
  PRIMARY KEY (`id_iva`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=3 ;

--
-- Volcado de datos para la tabla `iva`
--

INSERT INTO `iva` (`id_iva`, `porcentaje`) VALUES
(1, 22),
(2, 15);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `medidas`
--

CREATE TABLE IF NOT EXISTS `medidas` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `medida` varchar(15) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `medida` (`medida`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=6 ;

--
-- Volcado de datos para la tabla `medidas`
--

INSERT INTO `medidas` (`id`, `medida`) VALUES
(5, 'CC'),
(4, 'Gramos'),
(1, 'Kilos'),
(3, 'Litros'),
(2, 'Unidades');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `proveedores`
--

CREATE TABLE IF NOT EXISTS `proveedores` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `distribuidora` varchar(35) NOT NULL,
  `contacto` varchar(35) NOT NULL,
  `tel` varchar(15) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=4 ;

--
-- Volcado de datos para la tabla `proveedores`
--

INSERT INTO `proveedores` (`id`, `distribuidora`, `contacto`, `tel`) VALUES
(1, 'El tipo', 'Juan Gomez', '23447878'),
(2, 'Seriax', 'José Perez', '23336767'),
(3, 'Los chantas', 'Luis La calle', '22009090');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `seguros`
--

CREATE TABLE IF NOT EXISTS `seguros` (
  `id_seguro` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(20) CHARACTER SET utf8 NOT NULL,
  `direccion` varchar(35) CHARACTER SET utf8 NOT NULL,
  `telefono` varchar(12) CHARACTER SET utf8 NOT NULL,
  `persona_contacto` varchar(25) CHARACTER SET utf8 NOT NULL,
  PRIMARY KEY (`id_seguro`),
  UNIQUE KEY `nombre` (`nombre`),
  UNIQUE KEY `nombre_2` (`nombre`),
  UNIQUE KEY `nombre_3` (`nombre`),
  UNIQUE KEY `nombre_4` (`nombre`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=3 ;

--
-- Volcado de datos para la tabla `seguros`
--

INSERT INTO `seguros` (`id_seguro`, `nombre`, `direccion`, `telefono`, `persona_contacto`) VALUES
(1, 'BSE', 'Burgues 2323', '29003434', 'Susana Montero'),
(0, 'SURA', 'Av. Italia 1212', '29000909', 'José Perez');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `servicios`
--

CREATE TABLE IF NOT EXISTS `servicios` (
  `id_servicio` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(70) CHARACTER SET utf8 NOT NULL,
  PRIMARY KEY (`id_servicio`),
  UNIQUE KEY `nombre` (`nombre`) USING BTREE
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=10 ;

--
-- Volcado de datos para la tabla `servicios`
--

INSERT INTO `servicios` (`id_servicio`, `nombre`) VALUES
(1, 'Chapa'),
(2, 'Neumáticos y LLantas'),
(3, 'Mecánica'),
(4, 'Reparación y cambio de lunas'),
(5, 'Alineación'),
(6, 'Pintura'),
(7, 'Electricidad'),
(8, 'Inyección electrónica'),
(9, 'Cambio de aceite');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `trabajos`
--

CREATE TABLE IF NOT EXISTS `trabajos` (
  `fecha` date NOT NULL,
  `hora` time NOT NULL,
  `id_trabajo` int(11) NOT NULL AUTO_INCREMENT,
  `cliente_n` int(11) NOT NULL,
  `id_vehiculo` int(11) NOT NULL,
  `servicios` text CHARACTER SET utf8 NOT NULL,
  `precios` text CHARACTER SET utf8 NOT NULL,
  `descuento` float NOT NULL,
  `monto_descuento` float NOT NULL,
  `iva` float NOT NULL,
  `monto_iva` float NOT NULL,
  `presupuesto` float NOT NULL,
  `seguro` varchar(20) CHARACTER SET utf8 NOT NULL,
  `observaciones` varchar(100) CHARACTER SET utf8 DEFAULT NULL,
  `fecha_fin` varchar(15) CHARACTER SET utf8 DEFAULT NULL,
  `estado` varchar(30) CHARACTER SET utf8 NOT NULL,
  PRIMARY KEY (`id_trabajo`),
  UNIQUE KEY `id_trabajo_2` (`id_trabajo`),
  KEY `cliente_n` (`cliente_n`),
  KEY `id_trabajo` (`id_trabajo`),
  KEY `id_trabajo_3` (`id_trabajo`),
  KEY `id_vehiculo` (`id_vehiculo`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios_pass`
--

CREATE TABLE IF NOT EXISTS `usuarios_pass` (
  `numero` int(11) NOT NULL AUTO_INCREMENT,
  `usuario` varchar(15) DEFAULT NULL,
  `contra` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`numero`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=8 ;

--
-- Volcado de datos para la tabla `usuarios_pass`
--

INSERT INTO `usuarios_pass` (`numero`, `usuario`, `contra`) VALUES
(1, 'Paola', '1234'),
(2, 'Maxi', '2345'),
(3, 'Nacho', '3456'),
(4, 'Ana', '$2y$10$sJgvlrMKGD4qyu62i4SnyuUPjH3vKqEWkKWSA/uaHuPydmXDz/jE6'),
(6, 'Jose', '$2y$12$V.NwfnglcmrlNn2O6es9CeyluTA5T1cQSOKNQhoq95UdILCgfJcvC'),
(7, 'Juan', '$2y$12$uXNeiQ3Pd3NC8fkQz35uYO6PJmi6HKaVka93BV4P6kaw8PUzxT3dm');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `vehiculos`
--

CREATE TABLE IF NOT EXISTS `vehiculos` (
  `id_vehiculo` int(11) NOT NULL AUTO_INCREMENT,
  `cliente_n` int(11) NOT NULL,
  `marca` varchar(20) NOT NULL,
  `modelo` varchar(30) NOT NULL,
  `matricula` varchar(8) NOT NULL,
  PRIMARY KEY (`id_vehiculo`),
  UNIQUE KEY `matricula` (`matricula`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
