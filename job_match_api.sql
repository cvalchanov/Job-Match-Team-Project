-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema job_match_api
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema job_match_api
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `job_match_api` DEFAULT CHARACTER SET latin1 ;
USE `job_match_api` ;

-- -----------------------------------------------------
-- Table `job_match_api`.`ad_states`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `job_match_api`.`ad_states` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE,
  UNIQUE INDEX `name_UNIQUE` (`name` ASC) VISIBLE)
ENGINE = InnoDB
AUTO_INCREMENT = 2
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `job_match_api`.`admins`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `job_match_api`.`admins` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(45) NOT NULL,
  `password` VARCHAR(1024) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE,
  UNIQUE INDEX `username_UNIQUE` (`username` ASC) VISIBLE)
ENGINE = InnoDB
AUTO_INCREMENT = 2
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `job_match_api`.`approvals`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `job_match_api`.`approvals` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `type` VARCHAR(45) NOT NULL,
  `name` VARCHAR(256) NOT NULL,
  `category_id` INT(11) NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE)
ENGINE = InnoDB
AUTO_INCREMENT = 5
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `job_match_api`.`cities`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `job_match_api`.`cities` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE,
  UNIQUE INDEX `name_UNIQUE` (`name` ASC) VISIBLE)
ENGINE = InnoDB
AUTO_INCREMENT = 3
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `job_match_api`.`companies`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `job_match_api`.`companies` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(45) NOT NULL,
  `password` VARCHAR(1024) NOT NULL,
  `name` VARCHAR(45) NOT NULL,
  `info` VARCHAR(1024) NOT NULL,
  `city_id` INT(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE,
  UNIQUE INDEX `username_UNIQUE` (`username` ASC) VISIBLE,
  INDEX `fk_companies_cities1_idx` (`city_id` ASC) VISIBLE,
  CONSTRAINT `fk_companies_cities1`
    FOREIGN KEY (`city_id`)
    REFERENCES `job_match_api`.`cities` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
AUTO_INCREMENT = 3
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `job_match_api`.`company_contacts`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `job_match_api`.`company_contacts` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `phone_number` VARCHAR(45) NOT NULL,
  `email` VARCHAR(45) NOT NULL,
  `website` VARCHAR(45) NULL DEFAULT NULL,
  `linkedin` VARCHAR(45) NULL DEFAULT NULL,
  `facebook` VARCHAR(45) NULL DEFAULT NULL,
  `twitter` VARCHAR(45) NULL DEFAULT NULL,
  `company_id` INT(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE,
  UNIQUE INDEX `email_UNIQUE` (`email` ASC) VISIBLE,
  UNIQUE INDEX `phone_number_UNIQUE` (`phone_number` ASC) VISIBLE,
  UNIQUE INDEX `website_UNIQUE` (`website` ASC) VISIBLE,
  UNIQUE INDEX `linkedin_UNIQUE` (`linkedin` ASC) VISIBLE,
  UNIQUE INDEX `facebook_UNIQUE` (`facebook` ASC) VISIBLE,
  UNIQUE INDEX `twitter_UNIQUE` (`twitter` ASC) VISIBLE,
  INDEX `fk_contacts_companies1_idx` (`company_id` ASC) VISIBLE,
  CONSTRAINT `fk_contacts_companies1`
    FOREIGN KEY (`company_id`)
    REFERENCES `job_match_api`.`companies` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
AUTO_INCREMENT = 2
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `job_match_api`.`job_ads`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `job_match_api`.`job_ads` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `min_salary` INT(11) NULL DEFAULT NULL,
  `max_salary` INT(11) NULL DEFAULT NULL,
  `description` VARCHAR(512) NOT NULL,
  `remote` TINYINT(4) NOT NULL DEFAULT 1,
  `status` TINYINT(4) NOT NULL DEFAULT 1,
  `company_id` INT(11) NOT NULL,
  `city_id` INT(11) NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_job_ads_companies_idx` (`company_id` ASC) VISIBLE,
  INDEX `fk_job_ads_cities1_idx` (`city_id` ASC) VISIBLE,
  CONSTRAINT `fk_job_ads_cities1`
    FOREIGN KEY (`city_id`)
    REFERENCES `job_match_api`.`cities` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_job_ads_companies`
    FOREIGN KEY (`company_id`)
    REFERENCES `job_match_api`.`companies` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
AUTO_INCREMENT = 10
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `job_match_api`.`professional_ads`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `job_match_api`.`professional_ads` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `min_salary` INT(11) NULL DEFAULT NULL,
  `max_salary` INT(11) NULL DEFAULT NULL,
  `description` VARCHAR(512) NOT NULL,
  `remote` TINYINT(4) NOT NULL DEFAULT 1,
  `professional_id` INT(11) NOT NULL,
  `city_id` INT(11) NULL DEFAULT NULL,
  `ad_state_id` INT(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE,
  INDEX `fk_professional_ads_professionals1_idx` (`professional_id` ASC) VISIBLE,
  INDEX `fk_professional_ads_cities1_idx` (`city_id` ASC) VISIBLE,
  INDEX `fk_professional_ads_ad_states1_idx` (`ad_state_id` ASC) VISIBLE,
  CONSTRAINT `fk_professional_ads_ad_states1`
    FOREIGN KEY (`ad_state_id`)
    REFERENCES `job_match_api`.`ad_states` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_professional_ads_cities1`
    FOREIGN KEY (`city_id`)
    REFERENCES `job_match_api`.`cities` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_professional_ads_professionals1`
    FOREIGN KEY (`professional_id`)
    REFERENCES `job_match_api`.`professionals` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
AUTO_INCREMENT = 3
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `job_match_api`.`professionals`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `job_match_api`.`professionals` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(45) NOT NULL,
  `password` VARCHAR(1024) NOT NULL,
  `first_name` VARCHAR(45) NOT NULL,
  `last_name` VARCHAR(45) NOT NULL,
  `info` VARCHAR(512) NULL DEFAULT NULL,
  `status` TINYINT(4) NOT NULL DEFAULT 0,
  `city_id` INT(11) NOT NULL,
  `main_ad_id` INT(11) NULL DEFAULT NULL,
  `hide_matches` TINYINT(4) NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE,
  UNIQUE INDEX `username_UNIQUE` (`username` ASC) VISIBLE,
  INDEX `fk_professionals_cities1_idx` (`city_id` ASC) VISIBLE,
  INDEX `fk_professionals_professional_ads1_idx` (`main_ad_id` ASC) VISIBLE,
  CONSTRAINT `fk_professionals_cities1`
    FOREIGN KEY (`city_id`)
    REFERENCES `job_match_api`.`cities` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_professionals_professional_ads1`
    FOREIGN KEY (`main_ad_id`)
    REFERENCES `job_match_api`.`professional_ads` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
AUTO_INCREMENT = 2
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `job_match_api`.`job_ads_match_requests`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `job_match_api`.`job_ads_match_requests` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `job_ad_id` INT(11) NOT NULL,
  `company_id` INT(11) NOT NULL,
  `professional_id` INT(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE,
  INDEX `fk_job_ads_match_requests_job_ads1_idx` (`job_ad_id` ASC) VISIBLE,
  INDEX `fk_job_ads_match_requests_companies1_idx` (`company_id` ASC) VISIBLE,
  INDEX `fk_job_ads_match_requests_professionals1_idx` (`professional_id` ASC) VISIBLE,
  CONSTRAINT `fk_job_ads_match_requests_companies1`
    FOREIGN KEY (`company_id`)
    REFERENCES `job_match_api`.`companies` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_job_ads_match_requests_job_ads1`
    FOREIGN KEY (`job_ad_id`)
    REFERENCES `job_match_api`.`job_ads` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_job_ads_match_requests_professionals1`
    FOREIGN KEY (`professional_id`)
    REFERENCES `job_match_api`.`professionals` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `job_match_api`.`skill_levels`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `job_match_api`.`skill_levels` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `level_name` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE,
  UNIQUE INDEX `level_UNIQUE` (`level_name` ASC) VISIBLE)
ENGINE = InnoDB
AUTO_INCREMENT = 5
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `job_match_api`.`skill_categories`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `job_match_api`.`skill_categories` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE)
ENGINE = InnoDB
AUTO_INCREMENT = 3
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `job_match_api`.`skills`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `job_match_api`.`skills` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  `skill_category_id` INT(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE,
  INDEX `fk_skills_skill_categories1_idx` (`skill_category_id` ASC) VISIBLE,
  CONSTRAINT `fk_skills_skill_categories1`
    FOREIGN KEY (`skill_category_id`)
    REFERENCES `job_match_api`.`skill_categories` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
AUTO_INCREMENT = 21
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `job_match_api`.`skills_skill_levels`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `job_match_api`.`skills_skill_levels` (
  `skill_id` INT(11) NOT NULL,
  `skill_level_id` INT(11) NOT NULL,
  PRIMARY KEY (`skill_id`, `skill_level_id`),
  INDEX `fk_skills_skill_levels_skill_levels1_idx` (`skill_level_id` ASC) VISIBLE,
  INDEX `fk_skills_skill_levels_skills1_idx` (`skill_id` ASC) VISIBLE,
  CONSTRAINT `fk_skills_skill_levels_skill_levels1`
    FOREIGN KEY (`skill_level_id`)
    REFERENCES `job_match_api`.`skill_levels` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_skills_skill_levels_skills1`
    FOREIGN KEY (`skill_id`)
    REFERENCES `job_match_api`.`skills` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `job_match_api`.`job_ads_skillsets`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `job_match_api`.`job_ads_skillsets` (
  `job_ad_id` INT(11) NOT NULL,
  `skill_id` INT(11) NOT NULL,
  `skill_level_id` INT(11) NOT NULL,
  PRIMARY KEY (`job_ad_id`, `skill_id`, `skill_level_id`),
  INDEX `fk_job_ads_skillsets_skill_levels_skills_skill_levels1_idx` (`skill_id` ASC, `skill_level_id` ASC) VISIBLE,
  INDEX `fk_job_ads_skillsets_skill_levels_job_ads1_idx` (`job_ad_id` ASC) VISIBLE,
  CONSTRAINT `fk_job_ads_skillsets_skill_levels_job_ads1`
    FOREIGN KEY (`job_ad_id`)
    REFERENCES `job_match_api`.`job_ads` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_job_ads_skillsets_skill_levels_skills_skill_levels1`
    FOREIGN KEY (`skill_id` , `skill_level_id`)
    REFERENCES `job_match_api`.`skills_skill_levels` (`skill_id` , `skill_level_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `job_match_api`.`professional_ads_match_requests`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `job_match_api`.`professional_ads_match_requests` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `professional_ad_id` INT(11) NOT NULL,
  `professional_id` INT(11) NOT NULL,
  `company_id` INT(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE,
  INDEX `fk_professional_ads_match_requests_professional_ads1_idx` (`professional_ad_id` ASC) VISIBLE,
  INDEX `fk_professional_ads_match_requests_professionals1_idx` (`professional_id` ASC) VISIBLE,
  INDEX `fk_professional_ads_match_requests_companies1_idx` (`company_id` ASC) VISIBLE,
  CONSTRAINT `fk_professional_ads_match_requests_companies1`
    FOREIGN KEY (`company_id`)
    REFERENCES `job_match_api`.`companies` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_professional_ads_match_requests_professional_ads1`
    FOREIGN KEY (`professional_ad_id`)
    REFERENCES `job_match_api`.`professional_ads` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_professional_ads_match_requests_professionals1`
    FOREIGN KEY (`professional_id`)
    REFERENCES `job_match_api`.`professionals` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
AUTO_INCREMENT = 2
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `job_match_api`.`professional_ads_skillsets`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `job_match_api`.`professional_ads_skillsets` (
  `professional_ad_id` INT(11) NOT NULL,
  `skill_id` INT(11) NOT NULL,
  `skill_level_id` INT(11) NOT NULL,
  PRIMARY KEY (`professional_ad_id`, `skill_id`, `skill_level_id`),
  INDEX `fk_professional_ads_skillsets_skill_levels_skills_skill_le_idx` (`skill_id` ASC, `skill_level_id` ASC) VISIBLE,
  INDEX `fk_professional_ads_skillsets_skill_levels_professional_ad_idx` (`professional_ad_id` ASC) VISIBLE,
  CONSTRAINT `fk_professional_ads_skillsets_skill_levels_professional_ads1`
    FOREIGN KEY (`professional_ad_id`)
    REFERENCES `job_match_api`.`professional_ads` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_professional_ads_skillsets_skill_levels_skills_skill_leve1`
    FOREIGN KEY (`skill_id` , `skill_level_id`)
    REFERENCES `job_match_api`.`skills_skill_levels` (`skill_id` , `skill_level_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `job_match_api`.`professional_contacts`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `job_match_api`.`professional_contacts` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `phone_number` VARCHAR(45) NOT NULL,
  `email` VARCHAR(45) NOT NULL,
  `website` VARCHAR(45) NULL DEFAULT NULL,
  `linkedin` VARCHAR(45) NULL DEFAULT NULL,
  `facebook` VARCHAR(45) NULL DEFAULT NULL,
  `twitter` VARCHAR(45) NULL DEFAULT NULL,
  `professional_id` INT(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE,
  UNIQUE INDEX `email_UNIQUE` (`email` ASC) VISIBLE,
  UNIQUE INDEX `phone_number_UNIQUE` (`phone_number` ASC) VISIBLE,
  UNIQUE INDEX `website_UNIQUE` (`website` ASC) VISIBLE,
  UNIQUE INDEX `linkedin_UNIQUE` (`linkedin` ASC) VISIBLE,
  UNIQUE INDEX `facebook_UNIQUE` (`facebook` ASC) VISIBLE,
  UNIQUE INDEX `twitter_UNIQUE` (`twitter` ASC) VISIBLE,
  INDEX `fk_professional_contacts_professionals1_idx` (`professional_id` ASC) VISIBLE,
  CONSTRAINT `fk_professional_contacts_professionals1`
    FOREIGN KEY (`professional_id`)
    REFERENCES `job_match_api`.`professionals` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `job_match_api`.`successfull_matches`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `job_match_api`.`successfull_matches` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `professional_id` INT(11) NOT NULL,
  `company_id` INT(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE,
  INDEX `fk_successfull_matches_professionals1_idx` (`professional_id` ASC) VISIBLE,
  INDEX `fk_successfull_matches_companies1_idx` (`company_id` ASC) VISIBLE,
  CONSTRAINT `fk_successfull_matches_professionals1`
    FOREIGN KEY (`professional_id`)
    REFERENCES `job_match_api`.`professionals` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_successfull_matches_companies1`
    FOREIGN KEY (`company_id`)
    REFERENCES `job_match_api`.`companies` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
