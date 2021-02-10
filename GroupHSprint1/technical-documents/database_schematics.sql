-- phpMyAdmin SQL Dump
-- version 5.0.4
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Feb 11, 2021 at 12:34 AM
-- Server version: 8.0.23
-- PHP Version: 7.4.15

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `project`
--

-- --------------------------------------------------------

--
-- Table structure for table `django_migrations`
--

CREATE TABLE `django_migrations` (
  `id` int NOT NULL,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2021-02-10 14:06:28.951228'),
(2, 'auth', '0001_initial', '2021-02-10 14:06:29.914650'),
(3, 'study_platform', '0001_initial', '2021-02-10 14:06:33.532710'),
(4, 'study_platform', '0002_auto_20210210_1358', '2021-02-10 14:06:37.992778'),
(5, 'study_platform', '0003_auto_20210210_1401', '2021-02-10 14:06:41.305916'),
(6, 'auth', '0002_alter_permission_name_max_length', '2021-02-10 14:25:20.971524'),
(7, 'auth', '0003_alter_user_email_max_length', '2021-02-10 14:25:21.080525'),
(8, 'auth', '0004_alter_user_username_opts', '2021-02-10 14:25:21.160967'),
(9, 'auth', '0005_alter_user_last_login_null', '2021-02-10 14:25:21.273420'),
(10, 'contenttypes', '0002_remove_content_type_name', '2021-02-10 14:25:57.170772'),
(11, 'auth', '0006_require_contenttypes_0002', '2021-02-10 14:25:57.224757'),
(12, 'auth', '0007_alter_validators_add_error_messages', '2021-02-10 14:25:57.295568'),
(13, 'auth', '0008_alter_user_username_max_length', '2021-02-10 14:25:57.421685'),
(14, 'auth', '0009_alter_user_last_name_max_length', '2021-02-10 14:25:57.554646'),
(15, 'auth', '0010_alter_group_name_max_length', '2021-02-10 14:25:57.701471'),
(16, 'auth', '0011_update_proxy_permissions', '2021-02-10 14:25:57.882662'),
(17, 'auth', '0012_alter_user_first_name_max_length', '2021-02-10 14:25:58.030077'),
(18, 'sessions', '0001_initial', '2021-02-10 14:28:14.557993'),
(19, 'admin', '0001_initial', '2021-02-10 14:28:56.822950'),
(20, 'admin', '0002_logentry_remove_auto_add', '2021-02-10 14:28:57.012157'),
(21, 'admin', '0003_logentry_add_action_flag_choices', '2021-02-10 14:28:57.082825');

-- --------------------------------------------------------

--
-- Table structure for table `study_platform_accessory`
--

CREATE TABLE `study_platform_accessory` (
  `id` int NOT NULL,
  `name` varchar(100) NOT NULL,
  `description` longtext NOT NULL,
  `graphic` varchar(100) NOT NULL,
  `has_mods` tinyint(1) NOT NULL,
  `target_id` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `study_platform_achievement`
--

CREATE TABLE `study_platform_achievement` (
  `id` int NOT NULL,
  `name` varchar(20) NOT NULL,
  `description` longtext NOT NULL,
  `user_id` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `study_platform_blog`
--

CREATE TABLE `study_platform_blog` (
  `id` int NOT NULL,
  `title` varchar(20) NOT NULL,
  `category` varchar(3) NOT NULL,
  `content` longtext NOT NULL,
  `updated_on` datetime(6) NOT NULL,
  `created_on` datetime(6) NOT NULL,
  `upvotes` int NOT NULL,
  `post_to_id` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `study_platform_blog_participants`
--

CREATE TABLE `study_platform_blog_participants` (
  `id` int NOT NULL,
  `blog_id` int NOT NULL,
  `userprofile_id` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `study_platform_college`
--

CREATE TABLE `study_platform_college` (
  `id` int NOT NULL,
  `name` varchar(20) NOT NULL,
  `score` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `study_platform_comment`
--

CREATE TABLE `study_platform_comment` (
  `id` int NOT NULL,
  `content` longtext NOT NULL,
  `created_on` datetime(6) NOT NULL,
  `author_id` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `study_platform_course`
--

CREATE TABLE `study_platform_course` (
  `id` int NOT NULL,
  `name` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `study_platform_mod`
--

CREATE TABLE `study_platform_mod` (
  `id` int NOT NULL,
  `name` varchar(20) NOT NULL,
  `description` longtext NOT NULL,
  `effect` varchar(20) NOT NULL,
  `accessory_id` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `study_platform_question`
--

CREATE TABLE `study_platform_question` (
  `id` int NOT NULL,
  `category` varchar(3) NOT NULL,
  `content` longtext NOT NULL,
  `answer` longtext NOT NULL,
  `course_id` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `study_platform_quiz`
--

CREATE TABLE `study_platform_quiz` (
  `is_welfare` tinyint(1) NOT NULL,
  `id` varchar(50) NOT NULL,
  `created_on` datetime(6) NOT NULL,
  `author_id` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `study_platform_reward`
--

CREATE TABLE `study_platform_reward` (
  `id` int NOT NULL,
  `name` varchar(20) NOT NULL,
  `is_tool` tinyint(1) NOT NULL,
  `description` longtext NOT NULL,
  `effect` varchar(3) NOT NULL,
  `graphic` varchar(100) NOT NULL,
  `user_id` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `study_platform_team`
--

CREATE TABLE `study_platform_team` (
  `id` int NOT NULL,
  `name` varchar(20) NOT NULL,
  `manager_id` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `study_platform_teamblog`
--

CREATE TABLE `study_platform_teamblog` (
  `id` int NOT NULL,
  `title` varchar(20) NOT NULL,
  `content` longtext NOT NULL,
  `updated_on` datetime(6) NOT NULL,
  `created_on` datetime(6) NOT NULL,
  `team_id` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `study_platform_teamblog_participants`
--

CREATE TABLE `study_platform_teamblog_participants` (
  `id` int NOT NULL,
  `teamblog_id` int NOT NULL,
  `userprofile_id` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `study_platform_usertitle`
--

CREATE TABLE `study_platform_usertitle` (
  `id` int NOT NULL,
  `content` varchar(20) NOT NULL,
  `user_id` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `study_platform_welfareresult`
--

CREATE TABLE `study_platform_welfareresult` (
  `id` int NOT NULL,
  `date` datetime(6) NOT NULL,
  `percentage` int NOT NULL,
  `quiz_id` varchar(50) DEFAULT NULL,
  `user_id` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `django_migrations`
--
ALTER TABLE `django_migrations`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `study_platform_accessory`
--
ALTER TABLE `study_platform_accessory`
  ADD PRIMARY KEY (`id`),
  ADD KEY `study_platform_acces_target_id_7f91f662_fk_study_pla` (`target_id`);

--
-- Indexes for table `study_platform_achievement`
--
ALTER TABLE `study_platform_achievement`
  ADD PRIMARY KEY (`id`),
  ADD KEY `study_platform_achie_user_id_d26ae769_fk_study_pla` (`user_id`);

--
-- Indexes for table `study_platform_blog`
--
ALTER TABLE `study_platform_blog`
  ADD PRIMARY KEY (`id`),
  ADD KEY `study_platform_blog_post_to_id_e1004186_fk_study_pla` (`post_to_id`);

--
-- Indexes for table `study_platform_blog_participants`
--
ALTER TABLE `study_platform_blog_participants`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `study_platform_blog_participants_blog_id_user_id_8f9a5a1d_uniq` (`blog_id`,`userprofile_id`),
  ADD KEY `study_platform_blog__userprofile_id_9d54db2a_fk_study_pla` (`userprofile_id`);

--
-- Indexes for table `study_platform_college`
--
ALTER TABLE `study_platform_college`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `study_platform_comment`
--
ALTER TABLE `study_platform_comment`
  ADD PRIMARY KEY (`id`),
  ADD KEY `study_platform_comme_author_id_2e37b77f_fk_study_pla` (`author_id`);

--
-- Indexes for table `study_platform_course`
--
ALTER TABLE `study_platform_course`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `study_platform_mod`
--
ALTER TABLE `study_platform_mod`
  ADD PRIMARY KEY (`id`),
  ADD KEY `study_platform_mod_accessory_id_513c9573_fk_study_pla` (`accessory_id`);

--
-- Indexes for table `study_platform_question`
--
ALTER TABLE `study_platform_question`
  ADD PRIMARY KEY (`id`),
  ADD KEY `study_platform_quest_course_id_4558447e_fk_study_pla` (`course_id`);

--
-- Indexes for table `study_platform_quiz`
--
ALTER TABLE `study_platform_quiz`
  ADD PRIMARY KEY (`id`),
  ADD KEY `study_platform_quiz_author_id_d32c5214_fk_study_pla` (`author_id`);

--
-- Indexes for table `study_platform_reward`
--
ALTER TABLE `study_platform_reward`
  ADD PRIMARY KEY (`id`),
  ADD KEY `study_platform_rewar_user_id_0c458640_fk_study_pla` (`user_id`);

--
-- Indexes for table `study_platform_team`
--
ALTER TABLE `study_platform_team`
  ADD PRIMARY KEY (`id`),
  ADD KEY `study_platform_team_manager_id_ab3e8016_fk_study_pla` (`manager_id`);

--
-- Indexes for table `study_platform_teamblog`
--
ALTER TABLE `study_platform_teamblog`
  ADD PRIMARY KEY (`id`),
  ADD KEY `study_platform_teamb_team_id_8a8690d1_fk_study_pla` (`team_id`);

--
-- Indexes for table `study_platform_teamblog_participants`
--
ALTER TABLE `study_platform_teamblog_participants`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `study_platform_teamblog__teamblog_id_user_id_c1912ae0_uniq` (`teamblog_id`,`userprofile_id`),
  ADD KEY `study_platform_teamb_userprofile_id_9dcbfac9_fk_study_pla` (`userprofile_id`);

--
-- Indexes for table `study_platform_usertitle`
--
ALTER TABLE `study_platform_usertitle`
  ADD PRIMARY KEY (`id`),
  ADD KEY `study_platform_usert_user_id_992874dc_fk_study_pla` (`user_id`);

--
-- Indexes for table `study_platform_welfareresult`
--
ALTER TABLE `study_platform_welfareresult`
  ADD PRIMARY KEY (`id`),
  ADD KEY `study_platform_welfa_quiz_id_3ea28d6a_fk_study_pla` (`quiz_id`),
  ADD KEY `study_platform_welfa_user_id_a6225981_fk_study_pla` (`user_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=22;

--
-- AUTO_INCREMENT for table `study_platform_accessory`
--
ALTER TABLE `study_platform_accessory`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `study_platform_achievement`
--
ALTER TABLE `study_platform_achievement`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `study_platform_blog`
--
ALTER TABLE `study_platform_blog`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `study_platform_blog_participants`
--
ALTER TABLE `study_platform_blog_participants`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `study_platform_college`
--
ALTER TABLE `study_platform_college`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `study_platform_comment`
--
ALTER TABLE `study_platform_comment`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `study_platform_course`
--
ALTER TABLE `study_platform_course`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `study_platform_mod`
--
ALTER TABLE `study_platform_mod`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `study_platform_question`
--
ALTER TABLE `study_platform_question`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `study_platform_reward`
--
ALTER TABLE `study_platform_reward`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `study_platform_team`
--
ALTER TABLE `study_platform_team`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `study_platform_teamblog`
--
ALTER TABLE `study_platform_teamblog`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `study_platform_teamblog_participants`
--
ALTER TABLE `study_platform_teamblog_participants`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `study_platform_usertitle`
--
ALTER TABLE `study_platform_usertitle`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `study_platform_welfareresult`
--
ALTER TABLE `study_platform_welfareresult`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `study_platform_accessory`
--
ALTER TABLE `study_platform_accessory`
  ADD CONSTRAINT `study_platform_acces_target_id_7f91f662_fk_study_pla` FOREIGN KEY (`target_id`) REFERENCES `study_platform_reward` (`id`);

--
-- Constraints for table `study_platform_achievement`
--
ALTER TABLE `study_platform_achievement`
  ADD CONSTRAINT `study_platform_achie_user_id_d26ae769_fk_study_pla` FOREIGN KEY (`user_id`) REFERENCES `study_platform_userprofile` (`id`);

--
-- Constraints for table `study_platform_blog`
--
ALTER TABLE `study_platform_blog`
  ADD CONSTRAINT `study_platform_blog_post_to_id_e1004186_fk_study_pla` FOREIGN KEY (`post_to_id`) REFERENCES `study_platform_college` (`id`);

--
-- Constraints for table `study_platform_blog_participants`
--
ALTER TABLE `study_platform_blog_participants`
  ADD CONSTRAINT `study_platform_blog__blog_id_3e5dd819_fk_study_pla` FOREIGN KEY (`blog_id`) REFERENCES `study_platform_blog` (`id`),
  ADD CONSTRAINT `study_platform_blog__userprofile_id_9d54db2a_fk_study_pla` FOREIGN KEY (`userprofile_id`) REFERENCES `study_platform_userprofile` (`id`);

--
-- Constraints for table `study_platform_comment`
--
ALTER TABLE `study_platform_comment`
  ADD CONSTRAINT `study_platform_comme_author_id_2e37b77f_fk_study_pla` FOREIGN KEY (`author_id`) REFERENCES `study_platform_userprofile` (`id`);

--
-- Constraints for table `study_platform_mod`
--
ALTER TABLE `study_platform_mod`
  ADD CONSTRAINT `study_platform_mod_accessory_id_513c9573_fk_study_pla` FOREIGN KEY (`accessory_id`) REFERENCES `study_platform_accessory` (`id`);

--
-- Constraints for table `study_platform_question`
--
ALTER TABLE `study_platform_question`
  ADD CONSTRAINT `study_platform_quest_course_id_4558447e_fk_study_pla` FOREIGN KEY (`course_id`) REFERENCES `study_platform_course` (`id`);

--
-- Constraints for table `study_platform_quiz`
--
ALTER TABLE `study_platform_quiz`
  ADD CONSTRAINT `study_platform_quiz_author_id_d32c5214_fk_study_pla` FOREIGN KEY (`author_id`) REFERENCES `study_platform_userprofile` (`id`);

--
-- Constraints for table `study_platform_reward`
--
ALTER TABLE `study_platform_reward`
  ADD CONSTRAINT `study_platform_rewar_user_id_0c458640_fk_study_pla` FOREIGN KEY (`user_id`) REFERENCES `study_platform_userprofile` (`id`);

--
-- Constraints for table `study_platform_team`
--
ALTER TABLE `study_platform_team`
  ADD CONSTRAINT `study_platform_team_manager_id_ab3e8016_fk_study_pla` FOREIGN KEY (`manager_id`) REFERENCES `study_platform_userprofile` (`id`);

--
-- Constraints for table `study_platform_teamblog`
--
ALTER TABLE `study_platform_teamblog`
  ADD CONSTRAINT `study_platform_teamb_team_id_8a8690d1_fk_study_pla` FOREIGN KEY (`team_id`) REFERENCES `study_platform_team` (`id`);

--
-- Constraints for table `study_platform_teamblog_participants`
--
ALTER TABLE `study_platform_teamblog_participants`
  ADD CONSTRAINT `study_platform_teamb_teamblog_id_fad1eab0_fk_study_pla` FOREIGN KEY (`teamblog_id`) REFERENCES `study_platform_teamblog` (`id`),
  ADD CONSTRAINT `study_platform_teamb_userprofile_id_9dcbfac9_fk_study_pla` FOREIGN KEY (`userprofile_id`) REFERENCES `study_platform_userprofile` (`id`);

--
-- Constraints for table `study_platform_usertitle`
--
ALTER TABLE `study_platform_usertitle`
  ADD CONSTRAINT `study_platform_usert_user_id_992874dc_fk_study_pla` FOREIGN KEY (`user_id`) REFERENCES `study_platform_userprofile` (`id`);

--
-- Constraints for table `study_platform_welfareresult`
--
ALTER TABLE `study_platform_welfareresult`
  ADD CONSTRAINT `study_platform_welfa_quiz_id_3ea28d6a_fk_study_pla` FOREIGN KEY (`quiz_id`) REFERENCES `study_platform_quiz` (`id`),
  ADD CONSTRAINT `study_platform_welfa_user_id_a6225981_fk_study_pla` FOREIGN KEY (`user_id`) REFERENCES `study_platform_userprofile` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
