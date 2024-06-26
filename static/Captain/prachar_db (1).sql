-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jun 05, 2024 at 07:46 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `prachar_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `auth_group`
--

CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL,
  `name` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `auth_group`
--

INSERT INTO `auth_group` (`id`, `name`) VALUES
(1, 'sub admin group');

-- --------------------------------------------------------

--
-- Table structure for table `auth_group_permissions`
--

CREATE TABLE `auth_group_permissions` (
  `id` bigint(20) NOT NULL,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `auth_group_permissions`
--

INSERT INTO `auth_group_permissions` (`id`, `group_id`, `permission_id`) VALUES
(2, 1, 25),
(3, 1, 28),
(9, 1, 53),
(10, 1, 54),
(11, 1, 55),
(12, 1, 56),
(13, 1, 57),
(14, 1, 58),
(15, 1, 59),
(16, 1, 60),
(4, 1, 65),
(5, 1, 66),
(6, 1, 67),
(7, 1, 68),
(17, 1, 85),
(18, 1, 86),
(19, 1, 87),
(8, 1, 88);

-- --------------------------------------------------------

--
-- Table structure for table `auth_permission`
--

CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add log entry', 1, 'add_logentry'),
(2, 'Can change log entry', 1, 'change_logentry'),
(3, 'Can delete log entry', 1, 'delete_logentry'),
(4, 'Can view log entry', 1, 'view_logentry'),
(5, 'Can add permission', 2, 'add_permission'),
(6, 'Can change permission', 2, 'change_permission'),
(7, 'Can delete permission', 2, 'delete_permission'),
(8, 'Can view permission', 2, 'view_permission'),
(9, 'Can add group', 3, 'add_group'),
(10, 'Can change group', 3, 'change_group'),
(11, 'Can delete group', 3, 'delete_group'),
(12, 'Can view group', 3, 'view_group'),
(13, 'Can add user', 4, 'add_user'),
(14, 'Can change user', 4, 'change_user'),
(15, 'Can delete user', 4, 'delete_user'),
(16, 'Can view user', 4, 'view_user'),
(17, 'Can add content type', 5, 'add_contenttype'),
(18, 'Can change content type', 5, 'change_contenttype'),
(19, 'Can delete content type', 5, 'delete_contenttype'),
(20, 'Can view content type', 5, 'view_contenttype'),
(21, 'Can add session', 6, 'add_session'),
(22, 'Can change session', 6, 'change_session'),
(23, 'Can delete session', 6, 'delete_session'),
(24, 'Can view session', 6, 'view_session'),
(25, 'Can add two factor data', 7, 'add_twofactordata'),
(26, 'Can change two factor data', 7, 'change_twofactordata'),
(27, 'Can delete two factor data', 7, 'delete_twofactordata'),
(28, 'Can view two factor data', 7, 'view_twofactordata'),
(29, 'Can add area', 8, 'add_area'),
(30, 'Can change area', 8, 'change_area'),
(31, 'Can delete area', 8, 'delete_area'),
(32, 'Can view area', 8, 'view_area'),
(33, 'Can add city', 9, 'add_city'),
(34, 'Can change city', 9, 'change_city'),
(35, 'Can delete city', 9, 'delete_city'),
(36, 'Can view city', 9, 'view_city'),
(37, 'Can add campaign charge', 10, 'add_campaigncharge'),
(38, 'Can change campaign charge', 10, 'change_campaigncharge'),
(39, 'Can delete campaign charge', 10, 'delete_campaigncharge'),
(40, 'Can view campaign charge', 10, 'view_campaigncharge'),
(41, 'Can add agency information', 11, 'add_agencyinformation'),
(42, 'Can change agency information', 11, 'change_agencyinformation'),
(43, 'Can delete agency information', 11, 'delete_agencyinformation'),
(44, 'Can view agency information', 11, 'view_agencyinformation'),
(45, 'Can add client information', 12, 'add_clientinformation'),
(46, 'Can change client information', 12, 'change_clientinformation'),
(47, 'Can delete client information', 12, 'delete_clientinformation'),
(48, 'Can view client information', 12, 'view_clientinformation'),
(49, 'Can add campaign', 13, 'add_campaign'),
(50, 'Can change campaign', 13, 'change_campaign'),
(51, 'Can delete campaign', 13, 'delete_campaign'),
(52, 'Can view campaign', 13, 'view_campaign'),
(53, 'Can add driver basic information', 14, 'add_driverbasicinformation'),
(54, 'Can change driver basic information', 14, 'change_driverbasicinformation'),
(55, 'Can delete driver basic information', 14, 'delete_driverbasicinformation'),
(56, 'Can view driver basic information', 14, 'view_driverbasicinformation'),
(57, 'Can add device', 15, 'add_device'),
(58, 'Can change device', 15, 'change_device'),
(59, 'Can delete device', 15, 'delete_device'),
(60, 'Can view device', 15, 'view_device'),
(61, 'Can add banking information', 16, 'add_bankinginformation'),
(62, 'Can change banking information', 16, 'change_bankinginformation'),
(63, 'Can delete banking information', 16, 'delete_bankinginformation'),
(64, 'Can view banking information', 16, 'view_bankinginformation'),
(65, 'Can add auto kyc', 17, 'add_autokyc'),
(66, 'Can change auto kyc', 17, 'change_autokyc'),
(67, 'Can delete auto kyc', 17, 'delete_autokyc'),
(68, 'Can view auto kyc', 17, 'view_autokyc'),
(69, 'Can add manual kyc', 18, 'add_manualkyc'),
(70, 'Can change manual kyc', 18, 'change_manualkyc'),
(71, 'Can delete manual kyc', 18, 'delete_manualkyc'),
(72, 'Can view manual kyc', 18, 'view_manualkyc'),
(73, 'Can add payout configuration', 19, 'add_payoutconfiguration'),
(74, 'Can change payout configuration', 19, 'change_payoutconfiguration'),
(75, 'Can delete payout configuration', 19, 'delete_payoutconfiguration'),
(76, 'Can view payout configuration', 19, 'view_payoutconfiguration'),
(77, 'Can add state', 20, 'add_state'),
(78, 'Can change state', 20, 'change_state'),
(79, 'Can delete state', 20, 'delete_state'),
(80, 'Can view state', 20, 'view_state'),
(81, 'Can add business information', 21, 'add_businessinformation'),
(82, 'Can change business information', 21, 'change_businessinformation'),
(83, 'Can delete business information', 21, 'delete_businessinformation'),
(84, 'Can view business information', 21, 'view_businessinformation'),
(85, 'Can add vehicle license information', 22, 'add_vehiclelicenseinformation'),
(86, 'Can change vehicle license information', 22, 'change_vehiclelicenseinformation'),
(87, 'Can delete vehicle license information', 22, 'delete_vehiclelicenseinformation'),
(88, 'Can view vehicle license information', 22, 'view_vehiclelicenseinformation');

-- --------------------------------------------------------

--
-- Table structure for table `auth_user`
--

CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `auth_user`
--

INSERT INTO `auth_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`) VALUES
(1, 'pbkdf2_sha256$720000$AI8wZJ08cENg0hY9LrmkdU$tDs1iYd6ZNUhY2uFhn11kdTVq2TwUWAmG0V13Gaolus=', '2024-06-05 05:39:46.008498', 1, 'admin', '', '', '', 1, 1, '2024-05-30 09:04:27.247568'),
(2, 'pbkdf2_sha256$720000$Sndgo49wZmmKiGeCwptThT$m6zBi2ah8+C3CdA/oNhs19j4IDS99MPB835ZtKNMBZw=', '2024-06-05 04:39:03.954299', 0, 'root', '', '', '', 0, 1, '2024-05-31 07:34:58.000000'),
(3, 'pbkdf2_sha256$720000$EVcTGfpQRZFTHD8AXFhpq2$92V7/NvFHm1pGbwMmmdJ5ylOeaPWWTqsLzZFuxQ/GUA=', '2024-05-31 12:25:16.651721', 0, 'santu', 'santu', 'ss', 'rakshit4454.koffeekodes@gmail.com', 0, 1, '2024-05-31 09:07:37.000000');

-- --------------------------------------------------------

--
-- Table structure for table `auth_user_groups`
--

CREATE TABLE `auth_user_groups` (
  `id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `auth_user_groups`
--

INSERT INTO `auth_user_groups` (`id`, `user_id`, `group_id`) VALUES
(2, 2, 1),
(1, 3, 1);

-- --------------------------------------------------------

--
-- Table structure for table `auth_user_user_permissions`
--

CREATE TABLE `auth_user_user_permissions` (
  `id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `django_admin_log`
--

CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) UNSIGNED NOT NULL CHECK (`action_flag` >= 0),
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `django_admin_log`
--

INSERT INTO `django_admin_log` (`id`, `action_time`, `object_id`, `object_repr`, `action_flag`, `change_message`, `content_type_id`, `user_id`) VALUES
(1, '2024-05-31 06:11:02.991448', '1', 'TwoFactorData object (1)', 3, '', 7, 1),
(2, '2024-05-31 07:09:03.477270', '2', 'TwoFactorData object (2)', 3, '', 7, 1),
(3, '2024-05-31 07:35:35.611288', '2', 'root', 1, '[{\"added\": {}}]', 4, 1),
(4, '2024-05-31 07:36:47.671620', '2', 'root', 2, '[{\"changed\": {\"fields\": [\"Staff status\"]}}]', 4, 1),
(5, '2024-05-31 07:48:06.891641', '2', 'root', 2, '[{\"changed\": {\"fields\": [\"Staff status\"]}}]', 4, 1),
(6, '2024-05-31 07:49:19.179221', '2', 'root', 2, '[{\"changed\": {\"fields\": [\"Password\"]}}]', 4, 1),
(7, '2024-05-31 09:07:24.295420', '1', 'sub admin group', 1, '[{\"added\": {}}]', 3, 1),
(8, '2024-05-31 09:08:26.175601', '3', 'santu', 1, '[{\"added\": {}}]', 4, 1),
(9, '2024-05-31 09:15:46.512329', '1', 'sub admin group', 2, '[{\"changed\": {\"fields\": [\"Permissions\"]}}]', 3, 1),
(10, '2024-05-31 11:05:25.767220', '4', 'TwoFactorData object (4)', 3, '', 7, 1),
(11, '2024-05-31 11:31:05.220919', '2', 'root', 2, '[{\"changed\": {\"fields\": [\"Groups\"]}}]', 4, 1),
(12, '2024-05-31 11:32:30.447267', '2', 'root', 2, '[{\"changed\": {\"fields\": [\"Password\"]}}]', 4, 1),
(13, '2024-06-04 12:12:49.339516', '1', 'sub admin group', 2, '[{\"changed\": {\"fields\": [\"Permissions\"]}}]', 3, 1),
(14, '2024-06-05 04:35:55.147284', '1', 'State object (1)', 1, '[{\"added\": {}}]', 20, 1),
(15, '2024-06-05 04:36:12.103708', '1', 'City object (1)', 1, '[{\"added\": {}}]', 9, 1),
(16, '2024-06-05 04:37:48.245987', '1', 'Area object (1)', 1, '[{\"added\": {}}]', 8, 1),
(17, '2024-06-05 04:38:23.633060', '2', 'Area object (2)', 1, '[{\"added\": {}}]', 8, 1),
(18, '2024-06-05 04:41:18.910739', '1', 'DriverBasicInformation object (1)', 1, '[{\"added\": {}}]', 14, 2);

-- --------------------------------------------------------

--
-- Table structure for table `django_content_type`
--

CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(1, 'admin', 'logentry'),
(3, 'auth', 'group'),
(2, 'auth', 'permission'),
(4, 'auth', 'user'),
(5, 'contenttypes', 'contenttype'),
(11, 'p_app', 'agencyinformation'),
(8, 'p_app', 'area'),
(17, 'p_app', 'autokyc'),
(16, 'p_app', 'bankinginformation'),
(21, 'p_app', 'businessinformation'),
(13, 'p_app', 'campaign'),
(10, 'p_app', 'campaigncharge'),
(9, 'p_app', 'city'),
(12, 'p_app', 'clientinformation'),
(15, 'p_app', 'device'),
(14, 'p_app', 'driverbasicinformation'),
(18, 'p_app', 'manualkyc'),
(19, 'p_app', 'payoutconfiguration'),
(20, 'p_app', 'state'),
(7, 'p_app', 'twofactordata'),
(22, 'p_app', 'vehiclelicenseinformation'),
(6, 'sessions', 'session');

-- --------------------------------------------------------

--
-- Table structure for table `django_migrations`
--

CREATE TABLE `django_migrations` (
  `id` bigint(20) NOT NULL,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2024-05-30 07:22:29.024008'),
(2, 'auth', '0001_initial', '2024-05-30 07:22:29.706008'),
(3, 'admin', '0001_initial', '2024-05-30 07:22:29.860136'),
(4, 'admin', '0002_logentry_remove_auto_add', '2024-05-30 07:22:29.873177'),
(5, 'admin', '0003_logentry_add_action_flag_choices', '2024-05-30 07:22:29.883171'),
(6, 'contenttypes', '0002_remove_content_type_name', '2024-05-30 07:22:29.954232'),
(7, 'auth', '0002_alter_permission_name_max_length', '2024-05-30 07:22:30.058473'),
(8, 'auth', '0003_alter_user_email_max_length', '2024-05-30 07:22:30.113471'),
(9, 'auth', '0004_alter_user_username_opts', '2024-05-30 07:22:30.128513'),
(10, 'auth', '0005_alter_user_last_login_null', '2024-05-30 07:22:30.186705'),
(11, 'auth', '0006_require_contenttypes_0002', '2024-05-30 07:22:30.190714'),
(12, 'auth', '0007_alter_validators_add_error_messages', '2024-05-30 07:22:30.204713'),
(13, 'auth', '0008_alter_user_username_max_length', '2024-05-30 07:22:30.227702'),
(14, 'auth', '0009_alter_user_last_name_max_length', '2024-05-30 07:22:30.250766'),
(15, 'auth', '0010_alter_group_name_max_length', '2024-05-30 07:22:30.271975'),
(16, 'auth', '0011_update_proxy_permissions', '2024-05-30 07:22:30.285025'),
(17, 'auth', '0012_alter_user_first_name_max_length', '2024-05-30 07:22:30.308973'),
(18, 'sessions', '0001_initial', '2024-05-30 07:22:30.345080'),
(19, 'p_app', '0001_initial', '2024-05-31 06:07:18.309284'),
(20, 'p_app', '0002_area_alter_twofactordata_id_city_campaigncharge_and_more', '2024-06-04 04:51:32.693015'),
(21, 'p_app', '0003_alter_state_options_alter_agencyinformation_ai_email_and_more', '2024-06-04 09:04:26.623652'),
(22, 'p_app', '0004_alter_state_options', '2024-06-04 09:06:40.393703'),
(23, 'p_app', '0005_alter_agencyinformation_ai_address_2_and_more', '2024-06-04 11:56:10.634905'),
(24, 'p_app', '0006_remove_clientinformation_ci_agency_and_more', '2024-06-04 11:56:16.690892'),
(25, 'p_app', '0007_area_city_campaigncharge_agencyinformation_and_more', '2024-06-04 11:59:47.148840'),
(26, 'p_app', '0008_alter_agencyinformation_ai_address_2_and_more', '2024-06-04 12:04:13.560618');

-- --------------------------------------------------------

--
-- Table structure for table `django_session`
--

CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `django_session`
--

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('9w8jb2mz7hsq09p026qclqwf45cdjnrs', '.eJxVjMEOwiAQRP-FsyFQ7G7Xo_d-Q7MsVKoGktKejP-uJD3ocea9mZeaeN_StNe4TktQF2XV6bfzLI-YGwh3zreipeRtXbxuij5o1WMJ8Xk93L-DxDW1NUXyjEgSaMaz9FaMp2-MAoHQmoCdByDsh1lcNxAbA84xRHYAgOr9AfJ3N50:1sEN9w:U9amU1om8Vylb5i26wMoWiJqMpCKbViRHzAU1PeBiac', '2024-06-18 05:56:36.277867'),
('jv2te6sgkpd8208k6v43ju9qk8tsb4w3', '.eJxVjjsOwyAQRO9CHRAssOCU6XMGBAvE-chI_lRR7h4juUiqkWZGb-bNQtzWMWxLmcM9szMDdvr1UqRnmXqQH3G6NUFtWud7Er0ijnQR15bL63J0_wBjXMaOBazGSU1akvGqaLOrs1gMIfqcPCgqueahFrBeO0jOEiYDaBPa6HYo1BjWti_0M2A1IBL3UipujFF8KFXxVBMOSiuK1bLPFyOsRL4:1sD0VN:U1zy9pYHtw6ycDgtR6TSvIOfs7SSZt9RB-PtuaGfdc8', '2024-06-14 11:33:05.672275'),
('mcxpofdja3z45ye76ys9qzps5y8vm5rs', '.eJxVjMEOwiAQRP-FsyFQ7G7Xo_d-Q7MsVKoGktKejP-uJD3ocea9mZeaeN_StNe4TktQF2XV6bfzLI-YGwh3zreipeRtXbxuij5o1WMJ8Xk93L-DxDW1NUXyjEgSaMaz9FaMp2-MAoHQmoCdByDsh1lcNxAbA84xRHYAgOr9AfJ3N50:1sE2KN:a52n-OMDhppmrhPt4D4YxMr_7eZ9mmFLaBMLFjKvgGc', '2024-06-17 07:41:59.056695'),
('n1dulbkpdsdu98zbxjphiphfea3gfvek', '.eJxVjckOwyAMRP-Fc4lYEoN77L3fgIyBpouClOVU9d9LpBzai6XxzLx5i0DbOoZtyXO4J3EWWpx-f5H4mafdSA-abrXjOq3zPXZ7pDvcpbvWlF-XI_sHGGkZ9zZmjOQccsLieh40q4hNZoaETqvkTARAN_jC1ngkpcBagkwWAFyDmkJhrW2h4TB67AtraYqKsi9Gy8g5ydyud9aXorz4fAF_UUZE:1sEjNY:x75_oexsc3KLdyZ1xB9WN0Lt6Wb3sgsRRdkWNTA8T2M', '2024-06-19 05:40:08.537229'),
('n5ou9a8ik1afazy5x07913hqm8p6sitd', '.eJxVjMEOwiAQRP-FsyFQ7G7Xo_d-Q7MsVKoGktKejP-uJD3ocea9mZeaeN_StNe4TktQF2XV6bfzLI-YGwh3zreipeRtXbxuij5o1WMJ8Xk93L-DxDW1NUXyjEgSaMaz9FaMp2-MAoHQmoCdByDsh1lcNxAbA84xRHYAgOr9AfJ3N50:1sD182:xUN0ozX_r0IAEonQOoARqz7fFLXf41occthWdP58v0Q', '2024-06-14 12:13:02.560149');

-- --------------------------------------------------------

--
-- Table structure for table `p_app_agencyinformation`
--

CREATE TABLE `p_app_agencyinformation` (
  `ai_id` int(11) NOT NULL,
  `ai_name` varchar(100) NOT NULL,
  `ai_Email` varchar(254) NOT NULL,
  `ai_contact_number` int(11) NOT NULL,
  `ai_second_contact_number` int(11) DEFAULT NULL,
  `ai_address_1` varchar(100) NOT NULL,
  `ai_address_2` varchar(100) DEFAULT NULL,
  `ai_pincode` int(11) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `ai_city_id` int(11) NOT NULL,
  `ai_state_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `p_app_area`
--

CREATE TABLE `p_app_area` (
  `a_id` int(11) NOT NULL,
  `a_name` varchar(50) NOT NULL,
  `a_latitude` double NOT NULL,
  `a_longitude` double NOT NULL,
  `created_at` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `p_app_area`
--

INSERT INTO `p_app_area` (`a_id`, `a_name`, `a_latitude`, `a_longitude`, `created_at`) VALUES
(1, 'vasu', 21.121, 72.742, '2024-06-05 04:37:48.242991'),
(2, 'piplod', 22.819, 73.911, '2024-06-05 04:38:23.631054');

-- --------------------------------------------------------

--
-- Table structure for table `p_app_autokyc`
--

CREATE TABLE `p_app_autokyc` (
  `ak_id` int(11) NOT NULL,
  `ak_aadhar_card` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`ak_aadhar_card`)),
  `ak_kyc_token` varchar(100) NOT NULL,
  `ak_thumb_print` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`ak_thumb_print`)),
  `created_at` datetime(6) NOT NULL,
  `ak_driver_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `p_app_bankinginformation`
--

CREATE TABLE `p_app_bankinginformation` (
  `bki_id` int(11) NOT NULL,
  `bki_name` varchar(50) NOT NULL,
  `bki_account_holder_name` varchar(100) NOT NULL,
  `bki_account_number` int(11) NOT NULL,
  `bki_ifsc_code` varchar(20) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `bki_driver_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `p_app_businessinformation`
--

CREATE TABLE `p_app_businessinformation` (
  `bi_id` int(11) NOT NULL,
  `bi_name` varchar(100) NOT NULL,
  `bi_email` varchar(254) NOT NULL,
  `bi_connect_number` int(11) NOT NULL,
  `bi_second_connect_number` int(11) DEFAULT NULL,
  `bi_address_1` varchar(100) NOT NULL,
  `bi_address_2` varchar(100) DEFAULT NULL,
  `bi_pincode` int(11) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `bi_city_id` int(11) NOT NULL,
  `bi_client_id` int(11) NOT NULL,
  `bi_state_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `p_app_campaign`
--

CREATE TABLE `p_app_campaign` (
  `c_id` int(11) NOT NULL,
  `c_video_files` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`c_video_files`)),
  `c_number_of_repetition` int(11) NOT NULL,
  `c_start_date` date NOT NULL,
  `c_tenure` date NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `c_area_id` int(11) NOT NULL,
  `c_client_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `p_app_campaigncharge`
--

CREATE TABLE `p_app_campaigncharge` (
  `cc_id` int(11) NOT NULL,
  `cc_range` varchar(10) NOT NULL,
  `cc_amount` int(11) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `cc_city_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `p_app_city`
--

CREATE TABLE `p_app_city` (
  `city_id` int(11) NOT NULL,
  `city_name` varchar(50) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `created_by_id` int(11) NOT NULL,
  `state_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `p_app_city`
--

INSERT INTO `p_app_city` (`city_id`, `city_name`, `created_at`, `created_by_id`, `state_id`) VALUES
(1, 'Surat', '2024-06-05 04:36:12.099715', 1, 1);

-- --------------------------------------------------------

--
-- Table structure for table `p_app_clientinformation`
--

CREATE TABLE `p_app_clientinformation` (
  `ci_id` int(11) NOT NULL,
  `ci_name` varchar(100) NOT NULL,
  `ci_email` varchar(254) NOT NULL,
  `ci_contact_number` int(11) NOT NULL,
  `ci_second_contact_number` int(11) DEFAULT NULL,
  `ci_address_1` varchar(100) NOT NULL,
  `ci_address_2` varchar(100) DEFAULT NULL,
  `ci_pincode` int(11) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `ci_agency_id` int(11) DEFAULT NULL,
  `ci_city_id` int(11) NOT NULL,
  `ci_state_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `p_app_device`
--

CREATE TABLE `p_app_device` (
  `d_id` int(11) NOT NULL,
  `d_brand_name` varchar(50) NOT NULL,
  `d_model_number` varchar(50) NOT NULL,
  `d_mac_address` varchar(50) NOT NULL,
  `d_status` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `d_driver_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `p_app_driverbasicinformation`
--

CREATE TABLE `p_app_driverbasicinformation` (
  `dbi_id` int(11) NOT NULL,
  `dbi_name` varchar(100) NOT NULL,
  `dbi_email` varchar(254) NOT NULL,
  `dbi_mobile_number` int(11) NOT NULL,
  `dbi_address_1` varchar(100) NOT NULL,
  `dbi_address_2` varchar(100) DEFAULT NULL,
  `dbi_pincode` int(11) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `dbi_city_id` int(11) NOT NULL,
  `dbi_employee_id` int(11) NOT NULL,
  `dbi_state_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `p_app_driverbasicinformation`
--

INSERT INTO `p_app_driverbasicinformation` (`dbi_id`, `dbi_name`, `dbi_email`, `dbi_mobile_number`, `dbi_address_1`, `dbi_address_2`, `dbi_pincode`, `created_at`, `dbi_city_id`, `dbi_employee_id`, `dbi_state_id`) VALUES
(1, 'Mohan', 'mohan@gmail.com', 1234567891, 'A-31, Radhe Krupa society', 'punagam', 395010, '2024-06-05 04:41:18.907022', 1, 2, 1);

-- --------------------------------------------------------

--
-- Table structure for table `p_app_manualkyc`
--

CREATE TABLE `p_app_manualkyc` (
  `mk_id` int(11) NOT NULL,
  `mk_aadhar_card` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`mk_aadhar_card`)),
  `mk_pan_card` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`mk_pan_card`)),
  `created_at` datetime(6) NOT NULL,
  `mk_driver_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `p_app_payoutconfiguration`
--

CREATE TABLE `p_app_payoutconfiguration` (
  `pc_id` int(11) NOT NULL,
  `pc_range` varchar(50) NOT NULL,
  `pc_amount` int(11) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `pc_city_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `p_app_state`
--

CREATE TABLE `p_app_state` (
  `state_id` int(11) NOT NULL,
  `state_name` varchar(50) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `created_by_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `p_app_state`
--

INSERT INTO `p_app_state` (`state_id`, `state_name`, `created_at`, `created_by_id`) VALUES
(1, 'Gujarat', '2024-06-05 04:35:55.142274', 1);

-- --------------------------------------------------------

--
-- Table structure for table `p_app_twofactordata`
--

CREATE TABLE `p_app_twofactordata` (
  `id` int(11) NOT NULL,
  `otp_secret` varchar(255) NOT NULL,
  `session_identifier` char(32) DEFAULT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `p_app_twofactordata`
--

INSERT INTO `p_app_twofactordata` (`id`, `otp_secret`, `session_identifier`, `user_id`) VALUES
(3, '5FM7WAHGHLL7ACB4BBY47IEVMXZNOGHK', '9b894fc12f0b4f21bcedebce8738ff08', 1),
(5, 'I34EKJ5SD3CTPAF6UFCYEU6OLZZ5KYRQ', 'a4757249ec764917b2945a7371a35a65', 3),
(6, 'FNZIMMQUQFJVJFMFKPQZILFFKJ3AJAAE', '3e89adfab5bf41158f7f4ba455558d7f', 2);

-- --------------------------------------------------------

--
-- Table structure for table `p_app_vehiclelicenseinformation`
--

CREATE TABLE `p_app_vehiclelicenseinformation` (
  `vli_id` int(11) NOT NULL,
  `vi_number` varchar(10) NOT NULL,
  `vi_photo` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`vi_photo`)),
  `vi_rc_photo` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`vi_rc_photo`)),
  `li_number` varchar(50) NOT NULL,
  `li_photo` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`li_photo`)),
  `created_at` datetime(6) NOT NULL,
  `vli_driver_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `auth_group`
--
ALTER TABLE `auth_group`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  ADD KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`);

--
-- Indexes for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`);

--
-- Indexes for table `auth_user`
--
ALTER TABLE `auth_user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Indexes for table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  ADD KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`);

--
-- Indexes for table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  ADD KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`);

--
-- Indexes for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  ADD KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`);

--
-- Indexes for table `django_content_type`
--
ALTER TABLE `django_content_type`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`);

--
-- Indexes for table `django_migrations`
--
ALTER TABLE `django_migrations`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `django_session`
--
ALTER TABLE `django_session`
  ADD PRIMARY KEY (`session_key`),
  ADD KEY `django_session_expire_date_a5c62663` (`expire_date`);

--
-- Indexes for table `p_app_agencyinformation`
--
ALTER TABLE `p_app_agencyinformation`
  ADD PRIMARY KEY (`ai_id`),
  ADD UNIQUE KEY `ai_Email` (`ai_Email`),
  ADD KEY `p_app_agencyinformat_ai_state_id_6c886503_fk_p_app_sta` (`ai_state_id`),
  ADD KEY `p_app_agencyinformat_ai_city_id_4d02227b_fk_p_app_cit` (`ai_city_id`);

--
-- Indexes for table `p_app_area`
--
ALTER TABLE `p_app_area`
  ADD PRIMARY KEY (`a_id`);

--
-- Indexes for table `p_app_autokyc`
--
ALTER TABLE `p_app_autokyc`
  ADD PRIMARY KEY (`ak_id`),
  ADD KEY `p_app_autokyc_ak_driver_id_84da7e8d_fk_p_app_dri` (`ak_driver_id`);

--
-- Indexes for table `p_app_bankinginformation`
--
ALTER TABLE `p_app_bankinginformation`
  ADD PRIMARY KEY (`bki_id`),
  ADD KEY `p_app_bankinginforma_bki_driver_id_44178ad1_fk_p_app_dri` (`bki_driver_id`);

--
-- Indexes for table `p_app_businessinformation`
--
ALTER TABLE `p_app_businessinformation`
  ADD PRIMARY KEY (`bi_id`),
  ADD UNIQUE KEY `bi_email` (`bi_email`),
  ADD KEY `p_app_businessinform_bi_city_id_f451a1cf_fk_p_app_cit` (`bi_city_id`),
  ADD KEY `p_app_businessinform_bi_client_id_e62fb88e_fk_p_app_cli` (`bi_client_id`),
  ADD KEY `p_app_businessinform_bi_state_id_21bdcd2e_fk_p_app_sta` (`bi_state_id`);

--
-- Indexes for table `p_app_campaign`
--
ALTER TABLE `p_app_campaign`
  ADD PRIMARY KEY (`c_id`),
  ADD KEY `p_app_campaign_c_area_id_4d5f5337_fk_p_app_area_a_id` (`c_area_id`),
  ADD KEY `p_app_campaign_c_client_id_ce9441ef_fk_p_app_cli` (`c_client_id`);

--
-- Indexes for table `p_app_campaigncharge`
--
ALTER TABLE `p_app_campaigncharge`
  ADD PRIMARY KEY (`cc_id`),
  ADD KEY `p_app_campaigncharge_cc_city_id_d12d2a50_fk_p_app_city_city_id` (`cc_city_id`);

--
-- Indexes for table `p_app_city`
--
ALTER TABLE `p_app_city`
  ADD PRIMARY KEY (`city_id`),
  ADD KEY `p_app_city_state_id_df1bff5d_fk_p_app_state_state_id` (`state_id`),
  ADD KEY `p_app_city_created_by_id_fff7ca24_fk_auth_user_id` (`created_by_id`);

--
-- Indexes for table `p_app_clientinformation`
--
ALTER TABLE `p_app_clientinformation`
  ADD PRIMARY KEY (`ci_id`),
  ADD UNIQUE KEY `ci_email` (`ci_email`),
  ADD KEY `p_app_clientinformat_ci_state_id_9073044e_fk_p_app_sta` (`ci_state_id`),
  ADD KEY `p_app_clientinformat_ci_agency_id_802bddeb_fk_p_app_age` (`ci_agency_id`),
  ADD KEY `p_app_clientinformat_ci_city_id_39959c6b_fk_p_app_cit` (`ci_city_id`);

--
-- Indexes for table `p_app_device`
--
ALTER TABLE `p_app_device`
  ADD PRIMARY KEY (`d_id`),
  ADD KEY `p_app_device_d_driver_id_11705181_fk_p_app_dri` (`d_driver_id`);

--
-- Indexes for table `p_app_driverbasicinformation`
--
ALTER TABLE `p_app_driverbasicinformation`
  ADD PRIMARY KEY (`dbi_id`),
  ADD UNIQUE KEY `dbi_email` (`dbi_email`),
  ADD KEY `p_app_driverbasicinf_dbi_state_id_5b6ed01f_fk_p_app_sta` (`dbi_state_id`),
  ADD KEY `p_app_driverbasicinf_dbi_city_id_adfe87b6_fk_p_app_cit` (`dbi_city_id`),
  ADD KEY `p_app_driverbasicinf_dbi_employee_id_6131c5d3_fk_auth_user` (`dbi_employee_id`);

--
-- Indexes for table `p_app_manualkyc`
--
ALTER TABLE `p_app_manualkyc`
  ADD PRIMARY KEY (`mk_id`),
  ADD KEY `p_app_manualkyc_mk_driver_id_e8783529_fk_p_app_dri` (`mk_driver_id`);

--
-- Indexes for table `p_app_payoutconfiguration`
--
ALTER TABLE `p_app_payoutconfiguration`
  ADD PRIMARY KEY (`pc_id`),
  ADD KEY `p_app_payoutconfigur_pc_city_id_4c9e7784_fk_p_app_cit` (`pc_city_id`);

--
-- Indexes for table `p_app_state`
--
ALTER TABLE `p_app_state`
  ADD PRIMARY KEY (`state_id`),
  ADD KEY `p_app_state_created_by_id_36284342_fk_auth_user_id` (`created_by_id`);

--
-- Indexes for table `p_app_twofactordata`
--
ALTER TABLE `p_app_twofactordata`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `user_id` (`user_id`);

--
-- Indexes for table `p_app_vehiclelicenseinformation`
--
ALTER TABLE `p_app_vehiclelicenseinformation`
  ADD PRIMARY KEY (`vli_id`),
  ADD KEY `p_app_vehiclelicense_vli_driver_id_8625d879_fk_p_app_dri` (`vli_driver_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `auth_group`
--
ALTER TABLE `auth_group`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;

--
-- AUTO_INCREMENT for table `auth_permission`
--
ALTER TABLE `auth_permission`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=89;

--
-- AUTO_INCREMENT for table `auth_user`
--
ALTER TABLE `auth_user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=19;

--
-- AUTO_INCREMENT for table `django_content_type`
--
ALTER TABLE `django_content_type`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=23;

--
-- AUTO_INCREMENT for table `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=27;

--
-- AUTO_INCREMENT for table `p_app_agencyinformation`
--
ALTER TABLE `p_app_agencyinformation`
  MODIFY `ai_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `p_app_area`
--
ALTER TABLE `p_app_area`
  MODIFY `a_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `p_app_autokyc`
--
ALTER TABLE `p_app_autokyc`
  MODIFY `ak_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `p_app_bankinginformation`
--
ALTER TABLE `p_app_bankinginformation`
  MODIFY `bki_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `p_app_businessinformation`
--
ALTER TABLE `p_app_businessinformation`
  MODIFY `bi_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `p_app_campaign`
--
ALTER TABLE `p_app_campaign`
  MODIFY `c_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `p_app_campaigncharge`
--
ALTER TABLE `p_app_campaigncharge`
  MODIFY `cc_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `p_app_city`
--
ALTER TABLE `p_app_city`
  MODIFY `city_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `p_app_clientinformation`
--
ALTER TABLE `p_app_clientinformation`
  MODIFY `ci_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `p_app_device`
--
ALTER TABLE `p_app_device`
  MODIFY `d_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `p_app_driverbasicinformation`
--
ALTER TABLE `p_app_driverbasicinformation`
  MODIFY `dbi_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `p_app_manualkyc`
--
ALTER TABLE `p_app_manualkyc`
  MODIFY `mk_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `p_app_payoutconfiguration`
--
ALTER TABLE `p_app_payoutconfiguration`
  MODIFY `pc_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `p_app_state`
--
ALTER TABLE `p_app_state`
  MODIFY `state_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `p_app_twofactordata`
--
ALTER TABLE `p_app_twofactordata`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `p_app_vehiclelicenseinformation`
--
ALTER TABLE `p_app_vehiclelicenseinformation`
  MODIFY `vli_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- Constraints for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

--
-- Constraints for table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  ADD CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  ADD CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `p_app_agencyinformation`
--
ALTER TABLE `p_app_agencyinformation`
  ADD CONSTRAINT `p_app_agencyinformat_ai_city_id_4d02227b_fk_p_app_cit` FOREIGN KEY (`ai_city_id`) REFERENCES `p_app_city` (`city_id`),
  ADD CONSTRAINT `p_app_agencyinformat_ai_state_id_6c886503_fk_p_app_sta` FOREIGN KEY (`ai_state_id`) REFERENCES `p_app_state` (`state_id`);

--
-- Constraints for table `p_app_autokyc`
--
ALTER TABLE `p_app_autokyc`
  ADD CONSTRAINT `p_app_autokyc_ak_driver_id_84da7e8d_fk_p_app_dri` FOREIGN KEY (`ak_driver_id`) REFERENCES `p_app_driverbasicinformation` (`dbi_id`);

--
-- Constraints for table `p_app_bankinginformation`
--
ALTER TABLE `p_app_bankinginformation`
  ADD CONSTRAINT `p_app_bankinginforma_bki_driver_id_44178ad1_fk_p_app_dri` FOREIGN KEY (`bki_driver_id`) REFERENCES `p_app_driverbasicinformation` (`dbi_id`);

--
-- Constraints for table `p_app_businessinformation`
--
ALTER TABLE `p_app_businessinformation`
  ADD CONSTRAINT `p_app_businessinform_bi_city_id_f451a1cf_fk_p_app_cit` FOREIGN KEY (`bi_city_id`) REFERENCES `p_app_city` (`city_id`),
  ADD CONSTRAINT `p_app_businessinform_bi_client_id_e62fb88e_fk_p_app_cli` FOREIGN KEY (`bi_client_id`) REFERENCES `p_app_clientinformation` (`ci_id`),
  ADD CONSTRAINT `p_app_businessinform_bi_state_id_21bdcd2e_fk_p_app_sta` FOREIGN KEY (`bi_state_id`) REFERENCES `p_app_state` (`state_id`);

--
-- Constraints for table `p_app_campaign`
--
ALTER TABLE `p_app_campaign`
  ADD CONSTRAINT `p_app_campaign_c_area_id_4d5f5337_fk_p_app_area_a_id` FOREIGN KEY (`c_area_id`) REFERENCES `p_app_area` (`a_id`),
  ADD CONSTRAINT `p_app_campaign_c_client_id_ce9441ef_fk_p_app_cli` FOREIGN KEY (`c_client_id`) REFERENCES `p_app_clientinformation` (`ci_id`);

--
-- Constraints for table `p_app_campaigncharge`
--
ALTER TABLE `p_app_campaigncharge`
  ADD CONSTRAINT `p_app_campaigncharge_cc_city_id_d12d2a50_fk_p_app_city_city_id` FOREIGN KEY (`cc_city_id`) REFERENCES `p_app_city` (`city_id`);

--
-- Constraints for table `p_app_city`
--
ALTER TABLE `p_app_city`
  ADD CONSTRAINT `p_app_city_created_by_id_fff7ca24_fk_auth_user_id` FOREIGN KEY (`created_by_id`) REFERENCES `auth_user` (`id`),
  ADD CONSTRAINT `p_app_city_state_id_df1bff5d_fk_p_app_state_state_id` FOREIGN KEY (`state_id`) REFERENCES `p_app_state` (`state_id`);

--
-- Constraints for table `p_app_clientinformation`
--
ALTER TABLE `p_app_clientinformation`
  ADD CONSTRAINT `p_app_clientinformat_ci_agency_id_802bddeb_fk_p_app_age` FOREIGN KEY (`ci_agency_id`) REFERENCES `p_app_agencyinformation` (`ai_id`),
  ADD CONSTRAINT `p_app_clientinformat_ci_city_id_39959c6b_fk_p_app_cit` FOREIGN KEY (`ci_city_id`) REFERENCES `p_app_city` (`city_id`),
  ADD CONSTRAINT `p_app_clientinformat_ci_state_id_9073044e_fk_p_app_sta` FOREIGN KEY (`ci_state_id`) REFERENCES `p_app_state` (`state_id`);

--
-- Constraints for table `p_app_device`
--
ALTER TABLE `p_app_device`
  ADD CONSTRAINT `p_app_device_d_driver_id_11705181_fk_p_app_dri` FOREIGN KEY (`d_driver_id`) REFERENCES `p_app_driverbasicinformation` (`dbi_id`);

--
-- Constraints for table `p_app_driverbasicinformation`
--
ALTER TABLE `p_app_driverbasicinformation`
  ADD CONSTRAINT `p_app_driverbasicinf_dbi_city_id_adfe87b6_fk_p_app_cit` FOREIGN KEY (`dbi_city_id`) REFERENCES `p_app_city` (`city_id`),
  ADD CONSTRAINT `p_app_driverbasicinf_dbi_employee_id_6131c5d3_fk_auth_user` FOREIGN KEY (`dbi_employee_id`) REFERENCES `auth_user` (`id`),
  ADD CONSTRAINT `p_app_driverbasicinf_dbi_state_id_5b6ed01f_fk_p_app_sta` FOREIGN KEY (`dbi_state_id`) REFERENCES `p_app_state` (`state_id`);

--
-- Constraints for table `p_app_manualkyc`
--
ALTER TABLE `p_app_manualkyc`
  ADD CONSTRAINT `p_app_manualkyc_mk_driver_id_e8783529_fk_p_app_dri` FOREIGN KEY (`mk_driver_id`) REFERENCES `p_app_driverbasicinformation` (`dbi_id`);

--
-- Constraints for table `p_app_payoutconfiguration`
--
ALTER TABLE `p_app_payoutconfiguration`
  ADD CONSTRAINT `p_app_payoutconfigur_pc_city_id_4c9e7784_fk_p_app_cit` FOREIGN KEY (`pc_city_id`) REFERENCES `p_app_city` (`city_id`);

--
-- Constraints for table `p_app_state`
--
ALTER TABLE `p_app_state`
  ADD CONSTRAINT `p_app_state_created_by_id_36284342_fk_auth_user_id` FOREIGN KEY (`created_by_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `p_app_twofactordata`
--
ALTER TABLE `p_app_twofactordata`
  ADD CONSTRAINT `p_app_twofactordata_user_id_65cf998c_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `p_app_vehiclelicenseinformation`
--
ALTER TABLE `p_app_vehiclelicenseinformation`
  ADD CONSTRAINT `p_app_vehiclelicense_vli_driver_id_8625d879_fk_p_app_dri` FOREIGN KEY (`vli_driver_id`) REFERENCES `p_app_driverbasicinformation` (`dbi_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
