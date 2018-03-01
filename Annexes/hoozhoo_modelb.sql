-- -----------------------------------------------------
-- Schema hoozhoo
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `hoozhoo` ;


CREATE SCHEMA IF NOT EXISTS `hoozhoo` DEFAULT CHARACTER SET utf8 ;
USE `hoozhoo` ;

-- -----------------------------------------------------
-- Table `hoozhoo`.`personne`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `hoozhoo`.`personne` ;

CREATE TABLE IF NOT EXISTS `hoozhoo`.`personne` (
  `personne_id` SMALLINT NOT NULL AUTO_INCREMENT COMMENT '	',
  `personne_nom` TINYTEXT NOT NULL,
  `personne_prenom` TINYTEXT NULL,
  `personne_surnom` TINYTEXT NULL,
  `personne_description` TEXT NOT NULL,
  `personne_date_naissance`VARCHAR(10) NULL,
  `personne_date_mort` VARCHAR(10) NULL,
  `personne_genre` ENUM('F','M', 'Inconnu') NOT NULL,
  `personne_identifiant` VARCHAR(45) NULL,
  PRIMARY KEY (`personne_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `hoozhoo`.`user`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `hoozhoo`.`user` ;

CREATE TABLE IF NOT EXISTS `hoozhoo`.`user` (
  `user_id` SMALLINT NOT NULL AUTO_INCREMENT,
  `user_nom` TINYTEXT NOT NULL,
  `user_login` VARCHAR(45) NOT NULL,
  `user_email` TINYTEXT NOT NULL,
  `user_password` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE INDEX `user_login_UNIQUE` (`user_login` ASC))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `hoozhoo`.`authorship`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `hoozhoo`.`authorship` ;

CREATE TABLE IF NOT EXISTS `hoozhoo`.`authorship` (
  `authorship_id` SMALLINT NOT NULL AUTO_INCREMENT,
  `authorship_user_id` SMALLINT NOT NULL,
  `authorship_personne_id` SMALLINT NOT NULL,
  `authorship_date` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`authorship_id`),
  INDEX `fk_authorship_1_idx` (`authorship_personne_id` ASC),
  INDEX `fk_authorship_2_idx` (`authorship_user_id` ASC),
  CONSTRAINT `fk_authorship_1`
    FOREIGN KEY (`authorship_personne_id`)
    REFERENCES `hoozhoo`.`personne` (`personne_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_authorship_2`
    FOREIGN KEY (`authorship_user_id`)
    REFERENCES `hoozhoo`.`user` (`user_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `hoozhoo`.`typeRelation`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `hoozhoo`.`typeRelation` ;

CREATE TABLE IF NOT EXISTS `hoozhoo`.`typeRelation` (
  `typeRelation_id` SMALLINT NOT NULL AUTO_INCREMENT,
  `typeRelation_nom`  VARCHAR(45) NOT NULL,
  `typeRelation_code` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`typeRelation_id`))
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `hoozhoo`.`relationship`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `hoozhoo`.`relationship` ;

CREATE TABLE IF NOT EXISTS `hoozhoo`.`relationship` (
  `relationship_id` SMALLINT NOT NULL AUTO_INCREMENT,
  `relationship_user_id` SMALLINT NOT NULL,
  `relationship_typeRelation_id` SMALLINT NOT NULL,
  `relationship_date` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`relationship_id`),
  INDEX `fk_relationship_1_idx` (`relationship_typeRelation_id` ASC),
  INDEX `fk_relationship_2_idx` (`relationship_user_id` ASC),
  CONSTRAINT `fk_relationship_1`
    FOREIGN KEY (`relationship_typeRelation_id`)
    REFERENCES `hoozhoo`.`typeRelation` (`typeRelation_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_relationship_2`
    FOREIGN KEY (`relationship_user_id`)
    REFERENCES `hoozhoo`.`user` (`user_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `hoozhoo`.`lienPersonnes`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `hoozhoo`.`lienPersonnes` ;

CREATE TABLE IF NOT EXISTS `hoozhoo`.`lienPersonnes` (	
  `lienPersonnes_id` SMALLINT NOT NULL AUTO_INCREMENT,
  `lienPersonnes_personne1_id` SMALLINT NOT NULL,
  `lienPersonnes_personne2_id` SMALLINT NOT NULL,
  `lienPersonnes_typeRelation_id` SMALLINT NOT NULL,
  PRIMARY KEY (`lienPersonnes_id`),
  INDEX `fk_lienPersonnes_1_idx` (`lienPersonnes_personne1_id` ASC),
  INDEX `fk_lienPersonnes_2_idx` (`lienPersonnes_personne2_id` ASC),
  INDEX `fk_lienPersonnes_3_idx` (`lienPersonnes_typeRelation_id` ASC),
  
  CONSTRAINT `fk_lienPersonnes_1`
    FOREIGN KEY (`lienPersonnes_personne1_id`)
    REFERENCES `hoozhoo`.`personne` (`personne_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_lienPersonnes_2`
    FOREIGN KEY (`lienPersonnes_personne2_id`)
    REFERENCES `hoozhoo`.`personne` (`personne_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
CONSTRAINT `fk_lienPersonnes_3`
    FOREIGN KEY (`lienPersonnes_typeRelation_id`)
    REFERENCES `hoozhoo`.`typeRelation` (`typeRelation_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE = '';
GRANT USAGE ON *.* TO hoozhoo_user;
 DROP USER hoozhoo_user;
SET SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';
CREATE USER 'hoozhoo_user' IDENTIFIED BY 'password';

GRANT ALL ON `hoozhoo`.* TO 'hoozhoo_user';
GRANT SELECT ON TABLE `hoozhoo`.* TO 'hoozhoo_user';
GRANT SELECT, INSERT, TRIGGER ON TABLE `hoozhoo`.* TO 'hoozhoo_user';
GRANT SELECT, INSERT, TRIGGER, UPDATE, DELETE ON TABLE `hoozhoo`.* TO 'hoozhoo_user';
GRANT EXECUTE ON ROUTINE `hoozhoo`.* TO 'hoozhoo_user';

