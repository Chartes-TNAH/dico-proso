-- -----------------------------------------------------
-- Schema hoozhoo
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `hoozhoo` ;


CREATE SCHEMA IF NOT EXISTS `hoozhoo` DEFAULT CHARACTER SET utf8 ;
USE `hoozhoo` ;

-- -----------------------------------------------------
-- Table `hoozhoo`.`person`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `hoozhoo`.`person` ;

CREATE TABLE IF NOT EXISTS `hoozhoo`.`person` (
  `person_id` SMALLINT NOT NULL AUTO_INCREMENT COMMENT '	',
  `person_name` TINYTEXT NULL,
  `person_firstname` TINYTEXT NULL,
  `person_nickname` TINYTEXT NULL,
  `person_birthdate`VARCHAR(12) NULL,
  `person_deathdate` VARCHAR(12) NULL,
  `person_gender` ENUM('Femme','Homme', 'Inconnu') NOT NULL,
  `person_description` TEXT NOT NULL,
  `person_country` TINYTEXT NULL,
  `person_language` TINYTEXT NULL,
  `person_occupations` TINYTEXT NULL,
  `person_nativename` TINYTEXT NULL,
  `person_external_id` VARCHAR(12) NOT NULL,
  PRIMARY KEY (`person_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `hoozhoo`.`user`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `hoozhoo`.`user` ;

CREATE TABLE IF NOT EXISTS `hoozhoo`.`user` (
  `user_id` SMALLINT NOT NULL AUTO_INCREMENT,
  `user_name` TINYTEXT NOT NULL,
  `user_login` VARCHAR(45) NOT NULL,
  `user_email` TINYTEXT NOT NULL,
  `user_password` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE INDEX `user_login_UNIQUE` (`user_login` ASC))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `hoozhoo`.`authorship_person`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `hoozhoo`.`authorship_person` ;

CREATE TABLE IF NOT EXISTS `hoozhoo`.`authorship_person` (
  `authorship_person_id` SMALLINT NOT NULL AUTO_INCREMENT,
  `authorship_person_user_id` SMALLINT NOT NULL,
  `authorship_person_person_id` SMALLINT NOT NULL,
  `authorship_person_date` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`authorship_person_id`),
  INDEX `fk_authorship_person_1_idx` (`authorship_person_person_id` ASC),
  INDEX `fk_authorship_person_2_idx` (`authorship_person_user_id` ASC),
  CONSTRAINT `fk_authorship_person_1`
    FOREIGN KEY (`authorship_person_person_id`)
    REFERENCES `hoozhoo`.`person` (`person_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_authorship_person_2`
    FOREIGN KEY (`authorship_person_user_id`)
    REFERENCES `hoozhoo`.`user` (`user_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `hoozhoo`.`relation_type`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `hoozhoo`.`relation_type` ;

CREATE TABLE IF NOT EXISTS `hoozhoo`.`relation_type` (
  `relation_type_id` SMALLINT NOT NULL AUTO_INCREMENT,
  `relation_type_name`  VARCHAR(45) NOT NULL,
  `relation_type_code` VARCHAR(45) NOT NULL,
  `relation_type_first_snap` VARCHAR(45),
  `relation_type_second_snap` VARCHAR(45),
  `relation_type_third_snap` VARCHAR(45),
  `relation_type_fourth_snap` VARCHAR(45), 
  PRIMARY KEY (`relation_type_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `hoozhoo`.`link`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `hoozhoo`.`link` ;

CREATE TABLE IF NOT EXISTS `hoozhoo`.`link` (	
  `link_id` SMALLINT NOT NULL AUTO_INCREMENT,
  `link_person1_id` SMALLINT NOT NULL,
  `link_person2_id` SMALLINT NOT NULL,
  `link_relation_type_id` SMALLINT NOT NULL,
  PRIMARY KEY (`link_id`),
  INDEX `fk_link_1_idx` (`link_person1_id` ASC),
  INDEX `fk_link_2_idx` (`link_person2_id` ASC),
  INDEX `fk_link_3_idx` (`link_relation_type_id` ASC),
  
  CONSTRAINT `fk_link_1`
    FOREIGN KEY (`link_person1_id`)
    REFERENCES `hoozhoo`.`person` (`person_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_link_2`
    FOREIGN KEY (`link_person2_id`)
    REFERENCES `hoozhoo`.`person` (`person_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
CONSTRAINT `fk_link_3`
    FOREIGN KEY (`link_relation_type_id`)
    REFERENCES `hoozhoo`.`relation_type` (`relation_type_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `hoozhoo`.`authorship_link`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `hoozhoo`.`authorship_link` ;

CREATE TABLE IF NOT EXISTS `hoozhoo`.`authorship_link` (
  `authorship_link_id` SMALLINT NOT NULL AUTO_INCREMENT,
  `authorship_link_user_id` SMALLINT NOT NULL,
  `authorship_link_link_id` SMALLINT NOT NULL,
  `authorship_link_date` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`authorship_link_id`),
  INDEX `fk_authorship_link_1_idx` (`authorship_link_link_id` ASC),
  INDEX `fk_authorship_link_2_idx` (`authorship_link_user_id` ASC),
  CONSTRAINT `fk_authorship_link_1`
    FOREIGN KEY (`authorship_link_link_id`)
    REFERENCES `hoozhoo`.`link` (`link_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_authorship_link_2`
    FOREIGN KEY (`authorship_link_user_id`)
    REFERENCES `hoozhoo`.`user` (`user_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;



DROP USER IF EXISTS hoozhoo_user;
CREATE USER 'hoozhoo_user' IDENTIFIED BY 'password';
GRANT INSERT, SELECT, UPDATE, DELETE ON `hoozhoo`.* TO 'hoozhoo_user';


INSERT INTO `relation_type` (`relation_type_name`,`relation_type_code`,`relation_type_first_snap`,`relation_type_second_snap`,`relation_type_third_snap`,`relation_type_fourth_snap`) VALUES ('tante de','#AuntOf','#Bond','#ExtendedFamilyOf','#SiblingOfParentOf','');
INSERT INTO `relation_type` (`relation_type_name`,`relation_type_code`,`relation_type_first_snap`,`relation_type_second_snap`,`relation_type_third_snap`,`relation_type_fourth_snap`) VALUES ('oncle de','#UncleOf','#Bond','#ExtendedFamilyOf','#SiblingOfParentOf','');
INSERT INTO `relation_type` (`relation_type_name`,`relation_type_code`,`relation_type_first_snap`,`relation_type_second_snap`,`relation_type_third_snap`,`relation_type_fourth_snap`) VALUES ('neveu de','#NephewOf','#Bond','#ExtendedFamilyOf','#ChildOfSiblingOf','');
INSERT INTO `relation_type` (`relation_type_name`,`relation_type_code`,`relation_type_first_snap`,`relation_type_second_snap`,`relation_type_third_snap`,`relation_type_fourth_snap`) VALUES ('nièce de','#NieceOf','#Bond','#ExtendedFamilyOf','#ChildOfSiblingOf','');
INSERT INTO `relation_type` (`relation_type_name`,`relation_type_code`,`relation_type_first_snap`,`relation_type_second_snap`,`relation_type_third_snap`,`relation_type_fourth_snap`) VALUES ('cousine ou cousin de','#CousinOf','#Bond','#ExtendedFamilyOf','','');
INSERT INTO `relation_type` (`relation_type_name`,`relation_type_code`,`relation_type_first_snap`,`relation_type_second_snap`,`relation_type_third_snap`,`relation_type_fourth_snap`) VALUES ('petite-fille de','#GranddaughterOf','#Bond','#ExtendedFamilyOf','#DescendentOf','#GrandchildOf');
INSERT INTO `relation_type` (`relation_type_name`,`relation_type_code`,`relation_type_first_snap`,`relation_type_second_snap`,`relation_type_third_snap`,`relation_type_fourth_snap`) VALUES ('petit-fils de','#GrandsonOf','#Bond','#ExtendedFamilyOf','#DescendentOf','#GrandchildOf');
INSERT INTO `relation_type` (`relation_type_name`,`relation_type_code`,`relation_type_first_snap`,`relation_type_second_snap`,`relation_type_third_snap`,`relation_type_fourth_snap`) VALUES ('grand-père de','#GrandfatherOf','#Bond','#ExtendedFamilyOf','#AncestorOf','#GrandparentOf');
INSERT INTO `relation_type` (`relation_type_name`,`relation_type_code`,`relation_type_first_snap`,`relation_type_second_snap`,`relation_type_third_snap`,`relation_type_fourth_snap`) VALUES ('grand-mère de','#GrandmotherOf','#Bond','#ExtendedFamilyOf','#AncestorOf','#GrandparentOf');
INSERT INTO `relation_type` (`relation_type_name`,`relation_type_code`,`relation_type_first_snap`,`relation_type_second_snap`,`relation_type_third_snap`,`relation_type_fourth_snap`) VALUES ('arrière-grand-père de','#GreatGrandfatherOf','#Bond','#ExtendedFamilyOf','#AncestorOf','#GreatGrandparentOf');
INSERT INTO `relation_type` (`relation_type_name`,`relation_type_code`,`relation_type_first_snap`,`relation_type_second_snap`,`relation_type_third_snap`,`relation_type_fourth_snap`) VALUES ('arrière-grand-mère de','#GreatGrandmotherOf','#Bond','#ExtendedFamilyOf','#AncestorOf','#GreatGrandparentOf');
INSERT INTO `relation_type` (`relation_type_name`,`relation_type_code`,`relation_type_first_snap`,`relation_type_second_snap`,`relation_type_third_snap`,`relation_type_fourth_snap`) VALUES ('frère de','#BrotherOf','#Bond','#HereditaryFamilyOf','#SiblingOf','');
INSERT INTO `relation_type` (`relation_type_name`,`relation_type_code`,`relation_type_first_snap`,`relation_type_second_snap`,`relation_type_third_snap`,`relation_type_fourth_snap`) VALUES ('soeur de','#SisterOf','#Bond','#HereditaryFamilyOf','#SiblingOf','');
INSERT INTO `relation_type` (`relation_type_name`,`relation_type_code`,`relation_type_first_snap`,`relation_type_second_snap`,`relation_type_third_snap`,`relation_type_fourth_snap`) VALUES ('fille de','#DaughterOf','#Bond','#HereditaryFamilyOf','#ParentOf','');
INSERT INTO `relation_type` (`relation_type_name`,`relation_type_code`,`relation_type_first_snap`,`relation_type_second_snap`,`relation_type_third_snap`,`relation_type_fourth_snap`) VALUES ('fils de','#SonOf','#Bond','#HereditaryFamilyOf','#ParentOf','');
INSERT INTO `relation_type` (`relation_type_name`,`relation_type_code`,`relation_type_first_snap`,`relation_type_second_snap`,`relation_type_third_snap`,`relation_type_fourth_snap`) VALUES ('mère de','#MotherOf','#Bond','#HereditaryFamilyOf','#ParentOf','');
INSERT INTO `relation_type` (`relation_type_name`,`relation_type_code`,`relation_type_first_snap`,`relation_type_second_snap`,`relation_type_third_snap`,`relation_type_fourth_snap`) VALUES ('père de','#FatherOf','#Bond','#HereditaryFamilyOf','#ParentOf','');
INSERT INTO `relation_type` (`relation_type_name`,`relation_type_code`,`relation_type_first_snap`,`relation_type_second_snap`,`relation_type_third_snap`,`relation_type_fourth_snap`) VALUES ('esclave de','#SlaveOf','#Bond','#ExtendedHouseholdOf','','');
INSERT INTO `relation_type` (`relation_type_name`,`relation_type_code`,`relation_type_first_snap`,`relation_type_second_snap`,`relation_type_third_snap`,`relation_type_fourth_snap`) VALUES ('esclave libéré(e) de','#FreedSlaveOf','#Bond','#ExtendedHouseholdOf','','');
INSERT INTO `relation_type` (`relation_type_name`,`relation_type_code`,`relation_type_first_snap`,`relation_type_second_snap`,`relation_type_third_snap`,`relation_type_fourth_snap`) VALUES ('homme libéré de','#FreedmanOf','#Bond','#ExtendedHouseholdOf','','');
INSERT INTO `relation_type` (`relation_type_name`,`relation_type_code`,`relation_type_first_snap`,`relation_type_second_snap`,`relation_type_third_snap`,`relation_type_fourth_snap`) VALUES ('femme libérée de','#FreedwomanOf','#Bond','#ExtendedHouseholdOf','','');
INSERT INTO `relation_type` (`relation_type_name`,`relation_type_code`,`relation_type_first_snap`,`relation_type_second_snap`,`relation_type_third_snap`,`relation_type_fourth_snap`) VALUES ('relation intime occasionnelle avec','#CasualIntimateRelationshipWith','#Bond','#IntimateRelationshipWith','','');
INSERT INTO `relation_type` (`relation_type_name`,`relation_type_code`,`relation_type_first_snap`,`relation_type_second_snap`,`relation_type_third_snap`,`relation_type_fourth_snap`) VALUES ('relation intime sérieuse avec','#SeriousIntimateRelationshipWith','#Bond','#IntimateRelationshipWith','','');
INSERT INTO `relation_type` (`relation_type_name`,`relation_type_code`,`relation_type_first_snap`,`relation_type_second_snap`,`relation_type_third_snap`,`relation_type_fourth_snap`) VALUES ('ennemi(e) de','#EnmityFor','#Bond','','','');
INSERT INTO `relation_type` (`relation_type_name`,`relation_type_code`,`relation_type_first_snap`,`relation_type_second_snap`,`relation_type_third_snap`,`relation_type_fourth_snap`) VALUES ('ami(e) avec','#FriendshipFor','#Bond','#AllianceWith','','');
