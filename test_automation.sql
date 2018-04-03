-- MySQL dump 10.13  Distrib 5.5.55, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: test_automation
-- ------------------------------------------------------
-- Server version	5.5.55-0ubuntu0.14.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `BalanceSheet_companybalancesheetdata`
--

DROP TABLE IF EXISTS `BalanceSheet_companybalancesheetdata`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `BalanceSheet_companybalancesheetdata` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `gbc_name_id` int(11) NOT NULL,
  `lrq_id` int(11) DEFAULT NULL,
  `q1_id` int(11) DEFAULT NULL,
  `q2_id` int(11) DEFAULT NULL,
  `q3_id` int(11) DEFAULT NULL,
  `q4_id` int(11) DEFAULT NULL,
  `s2section_id` int(11) DEFAULT NULL,
  `section_id` int(11) DEFAULT NULL,
  `subsection_id` int(11) DEFAULT NULL,
  `tlm_id` int(11) DEFAULT NULL,
  `y1_id` int(11) DEFAULT NULL,
  `y2_id` int(11) DEFAULT NULL,
  `y3_id` int(11) DEFAULT NULL,
  `y4_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `BalanceShe_gbc_name_id_b16ce8a2_fk_DataExtraction_companylist_id` (`gbc_name_id`),
  KEY `BalanceSheet_g_lrq_id_d60dfb2e_fk_DataExtraction_quarter_data_id` (`lrq_id`),
  KEY `BalanceSheet_gb_q1_id_25e2646c_fk_DataExtraction_quarter_data_id` (`q1_id`),
  KEY `BalanceSheet_gb_q2_id_70e0e41f_fk_DataExtraction_quarter_data_id` (`q2_id`),
  KEY `BalanceSheet_gb_q3_id_c3d79b9e_fk_DataExtraction_quarter_data_id` (`q3_id`),
  KEY `BalanceSheet_gb_q4_id_7d11ab56_fk_DataExtraction_quarter_data_id` (`q4_id`),
  KEY `BalanceShee_s2section_id_b3f5d998_fk_DataExtraction_s2section_id` (`s2section_id`),
  KEY `BalanceSheet_gb_section_id_a25c8d8e_fk_DataExtraction_section_id` (`section_id`),
  KEY `BalanceSh_subsection_id_00178286_fk_DataExtraction_subsection_id` (`subsection_id`),
  KEY `BalanceSheet_gbcd_tlm_id_c83ab809_fk_DataExtraction_year_data_id` (`tlm_id`),
  KEY `BalanceSheet_gbcda_y1_id_6e8a6913_fk_DataExtraction_year_data_id` (`y1_id`),
  KEY `BalanceSheet_gbcda_y2_id_ee6229fc_fk_DataExtraction_year_data_id` (`y2_id`),
  KEY `BalanceSheet_gbcda_y3_id_0387887b_fk_DataExtraction_year_data_id` (`y3_id`),
  KEY `BalanceSheet_gbcda_y4_id_356bd22c_fk_DataExtraction_year_data_id` (`y4_id`),
  CONSTRAINT `BalanceSheet_gbcda_y1_id_6e8a6913_fk_DataExtraction_year_data_id` FOREIGN KEY (`y1_id`) REFERENCES `DataExtraction_year_data` (`id`),
  CONSTRAINT `BalanceSheet_gbcda_y2_id_ee6229fc_fk_DataExtraction_year_data_id` FOREIGN KEY (`y2_id`) REFERENCES `DataExtraction_year_data` (`id`),
  CONSTRAINT `BalanceSheet_gbcda_y3_id_0387887b_fk_DataExtraction_year_data_id` FOREIGN KEY (`y3_id`) REFERENCES `DataExtraction_year_data` (`id`),
  CONSTRAINT `BalanceSheet_gbcda_y4_id_356bd22c_fk_DataExtraction_year_data_id` FOREIGN KEY (`y4_id`) REFERENCES `DataExtraction_year_data` (`id`),
  CONSTRAINT `BalanceSheet_gbcd_tlm_id_c83ab809_fk_DataExtraction_year_data_id` FOREIGN KEY (`tlm_id`) REFERENCES `DataExtraction_year_data` (`id`),
  CONSTRAINT `BalanceSheet_gb_q1_id_25e2646c_fk_DataExtraction_quarter_data_id` FOREIGN KEY (`q1_id`) REFERENCES `DataExtraction_quarter_data` (`id`),
  CONSTRAINT `BalanceSheet_gb_q2_id_70e0e41f_fk_DataExtraction_quarter_data_id` FOREIGN KEY (`q2_id`) REFERENCES `DataExtraction_quarter_data` (`id`),
  CONSTRAINT `BalanceSheet_gb_q3_id_c3d79b9e_fk_DataExtraction_quarter_data_id` FOREIGN KEY (`q3_id`) REFERENCES `DataExtraction_quarter_data` (`id`),
  CONSTRAINT `BalanceSheet_gb_q4_id_7d11ab56_fk_DataExtraction_quarter_data_id` FOREIGN KEY (`q4_id`) REFERENCES `DataExtraction_quarter_data` (`id`),
  CONSTRAINT `BalanceSheet_gb_section_id_a25c8d8e_fk_DataExtraction_section_id` FOREIGN KEY (`section_id`) REFERENCES `DataExtraction_section` (`id`),
  CONSTRAINT `BalanceSheet_g_lrq_id_d60dfb2e_fk_DataExtraction_quarter_data_id` FOREIGN KEY (`lrq_id`) REFERENCES `DataExtraction_quarter_data` (`id`),
  CONSTRAINT `BalanceShee_s2section_id_b3f5d998_fk_DataExtraction_s2section_id` FOREIGN KEY (`s2section_id`) REFERENCES `DataExtraction_s2section` (`id`),
  CONSTRAINT `BalanceShe_gbc_name_id_b16ce8a2_fk_DataExtraction_companylist_id` FOREIGN KEY (`gbc_name_id`) REFERENCES `DataExtraction_companylist` (`id`),
  CONSTRAINT `BalanceSh_subsection_id_00178286_fk_DataExtraction_subsection_id` FOREIGN KEY (`subsection_id`) REFERENCES `DataExtraction_subsection` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `BalanceSheet_companybalancesheetdata`
--

LOCK TABLES `BalanceSheet_companybalancesheetdata` WRITE;
/*!40000 ALTER TABLE `BalanceSheet_companybalancesheetdata` DISABLE KEYS */;
/*!40000 ALTER TABLE `BalanceSheet_companybalancesheetdata` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `DataExtraction_companylist`
--

DROP TABLE IF EXISTS `DataExtraction_companylist`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `DataExtraction_companylist` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `company_name` varchar(200) NOT NULL,
  `y_end` varchar(200) NOT NULL,
  `c_ticker` varchar(200) DEFAULT NULL,
  `ditname_id` int(11) NOT NULL,
  `country` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `DataExtraction_companylist_3e7c3345` (`ditname_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `DataExtraction_companylist`
--

LOCK TABLES `DataExtraction_companylist` WRITE;
/*!40000 ALTER TABLE `DataExtraction_companylist` DISABLE KEYS */;
/*!40000 ALTER TABLE `DataExtraction_companylist` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `DataExtraction_quarter_data`
--

DROP TABLE IF EXISTS `DataExtraction_quarter_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `DataExtraction_quarter_data` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `quarter_date` varchar(200) DEFAULT NULL,
  `q1` varchar(200) DEFAULT NULL,
  `description` varchar(1000) DEFAULT NULL,
  `pdf_image_path` varchar(1000) DEFAULT NULL,
  `pdf_page` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `DataExtraction_quarter_data`
--

LOCK TABLES `DataExtraction_quarter_data` WRITE;
/*!40000 ALTER TABLE `DataExtraction_quarter_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `DataExtraction_quarter_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `DataExtraction_s2section`
--

DROP TABLE IF EXISTS `DataExtraction_s2section`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `DataExtraction_s2section` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `item` varchar(2000) NOT NULL,
  `i_synonyms` varchar(2000) DEFAULT NULL,
  `i_breakdown` varchar(5000) DEFAULT NULL,
  `i_keyword` varchar(1000) DEFAULT NULL,
  `added_date` datetime NOT NULL,
  `subsection_id` int(11) NOT NULL,
  `i_deduction` varchar(2000) DEFAULT NULL,
  `added_by_id` int(11) DEFAULT NULL,
  `modified_by_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `DataExtraction_s2section_57a29e66` (`subsection_id`),
  KEY `DataExtraction_s2section_0c5d7d4e` (`added_by_id`),
  KEY `DataExtraction_s2section_b3da0983` (`modified_by_id`),
  CONSTRAINT `DataExtraction_s2section_added_by_id_29848b74_fk_auth_user_id` FOREIGN KEY (`added_by_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `DataExtraction_s2section_modified_by_id_58e3eea3_fk_auth_user_id` FOREIGN KEY (`modified_by_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `DataExtra_subsection_id_45d8ff42_fk_DataExtraction_subsection_id` FOREIGN KEY (`subsection_id`) REFERENCES `DataExtraction_subsection` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `DataExtraction_s2section`
--

LOCK TABLES `DataExtraction_s2section` WRITE;
/*!40000 ALTER TABLE `DataExtraction_s2section` DISABLE KEYS */;
INSERT INTO `DataExtraction_s2section` VALUES (1,'Restricted Cash (Current)','Restricted deposits ## Restricted Cash','refundable deposits ## minimum balances on bank accounts ## funds held in escrow ## Pledged bank deposits ## Pledged time deposits','restricted','2017-11-21 12:10:27',5,'',NULL,NULL),(2,'Other Short-Term Receivables (Non-Trade)','\'\'','Claims for losses or damages ## Claims for tax refunds ## Dividends or interest receivable ## Advances to employee ## Sales of property other than inventory ## Deposits with creditors or utilities ## Operating Lease Receivables ## Finance Lease Receivables ## Finance Lease Receivables ## Loans to Related Parties ## Loans to Other Entities ## Reversal on Impairment on Other Short-Term Receivables (Non-Trade) ## Miscellaneous receivables ## Non trade receivables ## Lease receivable ## Finance and Interest receivable ## Rent Receivable ## Interest Receivable ## Due from Employees','non-trade','2017-11-21 12:10:50',5,'',NULL,NULL),(3,'Prepaid Expenses & Advances (Current)','Prepaid Expenses & Advances','Rent ## Prepaid Insurance ## Prepaid Advertising and Office Supplies ##  insurance premiums  ## Advances/Downpayment/Deposit for Property, Plant and Equipment ## Advances/Downpayment/Deposit for Long Term Financial Assets ## Prepaid lease payments ## Advances to Suppliers ## Security Deposit ## Advances to Employees ## Prepaid Inventory ## Prepaid Expenses ## Prepaid Rent ## Loans to employees ## Rental Deposit','prepaid, advances, expenses','2017-11-21 12:11:19',5,'',NULL,NULL),(4,'Tax Assets (Current)','Current corporate tax receivables ## Current tax assets','Tax Recoverable ## Deferred Tax Assets ## Prepaid Tax ## Deferred Expenses (Current) ## Refundable Income Taxes ## Claim for Tax Refund ## Taxation recoverable ## Income tax receivable ## Tax receivable ## Current tax assets ## Current tax receivables ## Deferred taxes – net ## Current deferred income tax benefits ## Deferred income tax assets ## Deferred income taxes ## Deferred income taxes, net ## Deferred tax assets-current  Advance Tax','income tax','2017-11-28 07:05:57',5,'',NULL,NULL),(5,'Deferred Expenses (Current)','Deferred costs##Deferred Expenses','Deferred Compensation Plan Assets ## Deferred Subscriber Acquisition Costs ## Deferred financing costs','','2017-11-21 12:12:18',5,'',NULL,NULL),(6,'Current Financial Assets','Current Financial Assets##Financial Assets','Derivatives Financial Assets for Hedging ## Foreign Currency Forward Contracts ## Interest Rate Swaps ## Currency Swaps ## Non-Derivative Financial Assets Held for Trading ## Held-to-Maturity Investments ## Held-to-Maturity Bills of Exchange/Promissory Notes ## Held-to-Maturity Debentures/Notes/Bonds ## Available-for-Sales Financial Assets ## Available-for-Sales Redeemable Notes/Bonds ## Available-for-Sale Shares in Third Party Entities ## Financial Assets and Liabilities at Fair Value Through Profit or Loss ## Financial assets held under resale agreements ## Derivatives Financial Assets ## Derivative financial instruments ## Financial derivative assets ## Financial Instrument at fair value through profit or loss','derivatives , contracts , hedges','2017-11-21 12:12:57',5,'',NULL,NULL),(7,'Other Current Assets (not listed above)','Other Current Assets','Current Assets Classified as Held for Sale ## Current Assets Classified as Held for Sale Revaluation Reserve ## Restricted Assets ## Warranty Reserve, Amounts due from joint ventures ## Amount due from ultimate holding company## Other current interest-bearing receivables ## Current Assets Classified as Held for Sale ## Assets classified as held for sale ##  Assets held for sale, net','','2017-11-21 12:13:21',5,'',NULL,NULL),(8,'Restricted Cash (Non-Current)','Restricted deposits ## Restricted Cash','Restricted Cash (Non-Current) ## Restricted investments and deposits ## escrow deposit (Non-Current) ## refundable deposits ## minimum balances on bank accounts ## funds held in escrow','restricted','2017-11-21 12:17:10',12,'',NULL,NULL),(9,'Other Long-Term Receivables (Non-Trade)','Other Long-Term Receivables','Finance Lease Receivables ## Loans to Related Parties ## Loans to Other Entities ## Reversal on Impairment on Long Short-Term Receivables (Non-Trade) ## Land Lease Agreement ## Amount due from an associate ## Government funding receivable ## Construction funding receivable ## Receivables on disposals of assets ## Amounts due from other related companies ## Amount due from a joint venture ## Amount due from an investee company ## Advances to subsidiary companies ## Loan due to significant shareholder ## Amount due to significant shareholder ## Amount due to associate ## Amount due to subsidiaries ## Loans due from a subsidiary Long term interest receivables','non trade','2017-11-21 12:17:28',12,'',NULL,NULL),(10,'Prepaid Expenses & Advances (Non-Current)','Non-current prepayments and deposits','Prepaid Rent ## Prepaid Insurance ## Advances for Property, Plant and Equipment ## Advances for Long Term Financial Assets ## Prepayments for acquisition of land use right and property, plant and equipment ## Advances to subsidiary companies ## Prepaid Lease Payment##Deposits and other##Downpayment for Property, Plant and Equipment## Deposit  for Property, Plant and Equipment##Downpayment  for Long Term Financial Assets## Deposit  for Long Term Financial Assets','prepaid,advances,expenses','2017-11-28 05:34:48',12,'',NULL,NULL),(11,'Tax Assets (Non-Current)','Tax Assets##  Non-Current corporate tax receivables ## Non-Current tax assets','Tax Recoverable ## Withholding Tax Deducted at Source ## Deferred Income Tax Assets ## Prepaid Tax ## Claim for Tax Refund ## Tax receivable  ## Deferred tax assets non current ## Deferred income taxes ## Deferred income tax benefits ## Deferred tax receivables ## Advance Tax','income tax','2017-11-28 07:06:07',12,'',NULL,NULL),(12,'Deferred Expenses (Non-Current)','Deferred costs','Deferred Compensation Plan Assets ## Deferred Subscriber Acquisition Costs ## Deferred financing costs','','2017-11-21 12:19:20',12,'',NULL,NULL),(13,'Other Non-Current Assets (not listed above)','Other Non-Current Assets##Other long-term assets','Non-Current Assets Classified as Held for Sale ## Non-Current Assets Classified as Held for Sale Revaluation Reserve ## Non-Current Deposit ## Assets Retirement Benefits ## Long term trade receivables ## Retention money ## Retirement benefit asset ## Long-term deposits paid ## Available for sale investments ## Non-current assets held for sale','','2017-11-21 12:19:56',12,'',NULL,NULL),(14,'Other Short-Term Payables (Non-Trade)','Other Short-Term Payables','Operating Lease Payables ## Deferred Liabilities (Current) ## Deferred Rent (Current) ## System-wide Payables ## Other payables and accrued expenses ## Other Short Term Acquisition Payable ## Government funding payable ## Interest Payable ## Accounts Payable – Non-Trade ## Land Lease Agreement Liability ## Interest Payable ## Rent Payable ## dividends payable ## Long-term lease payments (current portion)','non-trade','2017-11-21 12:22:30',16,'',NULL,NULL),(15,'Deferred Income Tax Liabilities (Current)','Provision for Tax ## Income Tax Payable ## Deferred Tax Liabilities (Net) ## Deferred Tax Liabilities ## Current income tax liabilities ## Income Taxes Payable ## Current income tax payable ## Deferred income taxes ## Current Tax liabilities','\'\'','income tax','2017-11-21 12:22:50',16,'',NULL,NULL),(16,'Accrued Expenses (Current)','\'\'','Accrued Interest (Current) ## Accrued Wage ## Accrued Insurance ## Other accrued expenses ## accrued fringe benefits ## accrued management bonuses ## accrued advertising and promotion ## accrued product warranty costs ## accrued interest on loans payable ## Interest Accrued but not due ## Accrued Salaries ## Accrued insurance and other taxes ## Accrued Management Incentives  Accrued payroll ## Accrued compensation and benefits ## Other creditors and accrued liabilities ## Other payables and accruals ## Accrued Expenses ## minor repairs ## electrical installations ## purchase of office supplies','accrued','2017-11-21 12:23:08',16,'',NULL,NULL),(17,'Pension & Post Retirement Liabilities (Current)','Employee Benefits Obligation ## Provision for Defined Benefit Plan ## Post Retirement Benefits ## Pension and other post-retirement benefit obligations ## Post-employment and other','Equity-Settled Employee Benefits Reserve (Current)','pension, retirement','2017-11-21 12:23:36',16,'',NULL,NULL),(18,'Sales Advances (Current)','Deferred Revenue ## Unearned Revenues ## Unearned Franchise Fee ## Liabilities for Guest Loyalty Program ## Deferred revenue-current ## Revenue received in advance ## Deferred income ## Prepayments from customers ## Deferred income from monthly dues ## Deferred revenues ## Deferred income-current','\'\'','deferred,unearned,revenue','2017-11-21 12:23:58',16,'',NULL,NULL),(19,'Other Current Liabilities (not listed above)','Other Current Liabilities','Other Provisions (Current) ## Allowance for Future Sales ## Severance and Relocation Provisions ## Liabilities Classified as Held for Sale ## Deposit Received ## Assets Retirement Obligations ## Amount due to a joint venture ## Amount due to a related party ## Amounts due to non-controlling owners of subsidiaries, Other liabilities, Other taxes payable ## Financial assets sold under repurchase agreements ## Liabilities associated with assets classified as held for sale ## Provision for dividend ## Proposed Dividend ## Unclaimed dividend','','2017-11-21 12:24:23',16,'',NULL,NULL),(20,'Other long-term Payables (Non-Trade)','Other long-term Payables','Operating Lease Payables ## Deferred Liabilities (Non-Current) ## Deferred Rent (Non-Current) ## Deferred Lease Credits ## Other Long Term Acquisition Payable ## Deferred government grants ## Deferred credits and other noncurrent liabilities','lease,non-trade','2017-11-21 12:26:25',19,'',NULL,NULL),(21,'Deferred Income Tax Liabilities (Non-Current)','Deferred tax liabilities-noncurrent ## Noncurrent deferred income taxes ## Provision for Tax ## Income Tax Payable ## Deferred Tax Liabilities ## Non-Current income tax liabilities ## Income Taxes Payable ## Non-Current income tax payable Non-Current Tax liabilities','\'\'','income tax','2017-11-21 12:26:38',19,'',NULL,NULL),(22,'Accrued Expenses (Non-Current)','\'\'','Accrued Interest (Non-Current) ## Accrued Wage ## Accrued Insurance ## Other accrued expenses ## accrued fringe benefits ## accrued management bonuses ## accrued advertising and promotion ## accrued product warranty costs ## accrued interest on loans payable ## Interest Accrued but not due ## Accrued Salaries ## Accrued insurance and other taxes ## Accrued Management Incentives ## Accrued payroll ## Accrued compensation and benefits##Deferred compensation','accrued','2017-11-28 05:38:04',19,'',NULL,NULL),(23,'Pension & Post Retirement Liabilities (Non-Current)','Employee Benefits Obligation ## Retirement benefit liabilities ## Employee benefits ## Pension liability ## Pension and other post-retirement benefit obligations','Equity-Settled Employee Benefits Reserve (Non-Current) ## Pension fund liability ## Defined benefit obligations','pension,retirement','2017-11-21 12:28:19',19,'',NULL,NULL),(24,'Sales Advances (Non-Current)','Deferred Revenue ## Unearned Revenues ## Unearned Franchise Fee ## Liabilities for Guest Loyalty Program ## Deferred income - net of current portion ## Deferred revenue-noncurrent','\'\'','deferred,unearned,revenue','2017-12-01 10:01:30',19,'',NULL,NULL),(25,'Other Non-Current Liabilities (not listed above)','\'\'','Other Provisions (Non-Current) ## Negative Goodwill ## Non-Current Liabilities Classified as Held for Sale ## Redeemable noncontrolling interests ## Other non-current deposit or payable ## Other long-term non interest-bearing liabilities ## Liabilities associated with assets classified as held for sale ## Provision for dividend ## Proposed Dividend ## Unclaimed dividend##Other Non-Current Liabilities','','2017-11-21 12:29:01',19,'',NULL,NULL);
/*!40000 ALTER TABLE `DataExtraction_s2section` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `DataExtraction_section`
--

DROP TABLE IF EXISTS `DataExtraction_section`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `DataExtraction_section` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `item` varchar(2000) NOT NULL,
  `i_synonyms` varchar(200) DEFAULT NULL,
  `added_date` datetime NOT NULL,
  `i_related` varchar(200) NOT NULL,
  `added_by_id` int(11) DEFAULT NULL,
  `modified_by_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `DataExtraction_section_0c5d7d4e` (`added_by_id`),
  KEY `DataExtraction_section_b3da0983` (`modified_by_id`),
  CONSTRAINT `DataExtraction_section_added_by_id_c8864ede_fk_auth_user_id` FOREIGN KEY (`added_by_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `DataExtraction_section_modified_by_id_e4f1ddc6_fk_auth_user_id` FOREIGN KEY (`modified_by_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `DataExtraction_section`
--

LOCK TABLES `DataExtraction_section` WRITE;
/*!40000 ALTER TABLE `DataExtraction_section` DISABLE KEYS */;
INSERT INTO `DataExtraction_section` VALUES (1,'Current Assets','Net Current Assets, Total Current Assets','2018-02-22 12:36:42','Balance Sheet',NULL,NULL),(2,'Non-Current Assets','Net Non Current Assets','2017-12-04 06:00:44','Balance Sheet',NULL,NULL),(3,'Current Liabilities','Net Current Liabilities','2017-12-04 06:00:21','Balance Sheet',NULL,NULL),(4,'Non-Current Liabilities','Net Non Current Liabilities##Long-term liabilities','2017-12-04 06:00:25','Balance Sheet',NULL,NULL),(5,'Shareholder Equity','Shareholders Funds##Capital Stock','2017-12-04 06:00:32','Balance Sheet',NULL,NULL),(6,'Revenue','Net Revenue','2018-02-22 12:37:06','Profit and Loss',NULL,NULL),(7,'Cost of Revenue','Net Cost of revenue','2018-02-22 12:37:25','Profit and Loss',NULL,NULL),(8,'Other Operating Income','Total Other Operating Income','2018-02-22 12:37:42','Profit and Loss',NULL,NULL),(9,'Operating Expenses','Total Operating Expenses','2018-02-22 12:38:19','Profit and Loss',NULL,NULL),(10,'Non-Operating Income/(Expenses)','Total Non operating Expenses','2018-02-22 12:38:44','Profit and Loss',NULL,NULL),(11,'Net Profit/(Loss) for the Year','Net Profit, Net Loss','2018-02-22 12:40:34','Profit and Loss',NULL,NULL),(12,'Depreciation & Dividend','Total Depreciation','2018-02-22 12:40:49','Profit and Loss',NULL,NULL),(13,'Income Tax Expense','Net income tax expense, Total income tax expense','2018-02-22 12:41:09','Profit and Loss',NULL,NULL),(14,'Profit/(Loss) from Discontinued Operations','net profit from discontinued operations,Total profit from discontinued opeartions','2018-02-22 12:41:47','Profit and Loss',NULL,NULL),(15,'Gross Profit/(Loss)','Gross Profit##Gross Loss##Gross income##Gross Profit/(Loss)','2018-02-23 05:43:03','Profit and Loss',NULL,NULL),(16,'Pretax Profit/(Loss)','Profit Before Income Tax##Profit before tax##Income (loss) before provision for income taxes##Income  before provision for income taxes ##loss before provision for income taxes##Earnings before income','2018-02-23 07:39:27','Profit and Loss',NULL,NULL),(18,'Extra PNL Keywords','\'\'','2018-03-05 07:29:29','Profit and Loss',NULL,NULL);
/*!40000 ALTER TABLE `DataExtraction_section` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `DataExtraction_sector`
--

DROP TABLE IF EXISTS `DataExtraction_sector`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `DataExtraction_sector` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `sector_name` varchar(1000) NOT NULL,
  `copy_main` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=35 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `DataExtraction_sector`
--

LOCK TABLES `DataExtraction_sector` WRITE;
/*!40000 ALTER TABLE `DataExtraction_sector` DISABLE KEYS */;
INSERT INTO `DataExtraction_sector` VALUES (1,'Aviation Services',1),(2,'B2B Manufacturing Sector',0),(3,'Commercial Services Sector',1),(4,'Commercial Services Sector/Consumer Services Sector',1),(5,'Communications Sector',1),(6,'Construction Sector',1),(7,'Consumer Services Sector',1),(8,'Distributors',1),(9,'Entertainment Sector',1),(10,'Farming and Processing',1),(11,'Financial Services',1),(12,'Health Care Sector',1),(13,'Hospitality, Recreation & Entertainment Sector',1),(14,'Infrastructure Developer',1),(15,'Manufacturing Sector',1),(16,'Power Generation',1),(17,'Rail and Road Services',1),(18,'Real Estate Sector',1),(19,'Retail Sector',1),(20,'Software Development',1),(21,'Textile & Apparels Manufacturing',1),(32,'Shipping Services',1),(33,'Mining and Processing',1),(34,'Oil and Gas Sector',0);
/*!40000 ALTER TABLE `DataExtraction_sector` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `DataExtraction_sectordit`
--

DROP TABLE IF EXISTS `DataExtraction_sectordit`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `DataExtraction_sectordit` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `dit_name` varchar(1000) NOT NULL,
  `dit_code` varchar(200) NOT NULL,
  `sector_id` int(11) NOT NULL,
  `copy_Sector` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=269 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `DataExtraction_sectordit`
--

LOCK TABLES `DataExtraction_sectordit` WRITE;
/*!40000 ALTER TABLE `DataExtraction_sectordit` DISABLE KEYS */;
INSERT INTO `DataExtraction_sectordit` VALUES (1,'Rice Milling','01010105',10,1),(2,'Oil Palm Planting and Processing','01010201',10,1),(3,'Tree Nuts Farming','01010305',10,1),(4,'Sugarcane Farming & Processing','01010401',10,1),(5,'Poultry Farming & Processing','01020101',10,1),(6,'Cattle & Cow Farming & Dairy Products Production','01020202',10,1),(7,'Farm Animal Slaughtering & Processing Operators (Fresh Meat)','01020203',10,1),(8,'Hog & Pig Farming & Processing','01020205',10,1),(9,'Aquaculture Farming & Processing','01020302',10,1),(10,'Seafood Product Preparation & Packaging Services','01020303',10,1),(11,'Fruits & Vegetable Farming and Processing','01010307',10,1),(12,'Fruit & Vegetable Processing','02010502',10,1),(13,'Tea Manufacturing','02020104',10,1),(14,'Brewers','02020201',15,1),(15,'Wineries','02020202',10,1),(16,'Cigars & Cigarette Manufacturing','02030201',15,1),(17,'Convenience Stores without Fuel Station','03010301',19,1),(18,'Convenience Stores with Fuel Station','03010302',19,1),(19,'Supermarkets','03010404',19,1),(20,'Mass Merchants - Warehouse Clubs/Wholesale Stores','03010502',19,1),(21,'Pharmacy Drugstores & Online Pharmacy','03010701',19,1),(22,'Mid-Tier Department Stores','03020101',19,1),(23,'Discount Retail Department Stores','03020103',19,1),(24,'High-Tier/Specialty Department Stores','03020105',19,1),(25,'Jewelry Retailers','03020401',19,1),(26,'Watch Retailers','03020402',19,1),(27,'Luxury Watch Retailers','03020403',19,1),(28,'Single Brand Apparel & Accessories Store Retailers (mid-end)','03020404',19,1),(29,'Children & Infants Clothing Retailers','03020405',19,1),(30,'Sportwear Retailers','03020406',19,1),(31,'Luxury Fashion Houses','03020407',19,1),(32,'Beauty Products Retailers','03020501',19,1),(33,'Optical Goods Retailers','03020502',19,1),(34,'Toys & Games Retailers','03020603',19,1),(35,'Book & Magazine Retailers','03020604',19,1),(36,'Pet & Pet Supplies Retailers','03020608',19,1),(37,'Consumer Electronics & Home Appliance Retailers','03020902',19,1),(38,'Online Consumer Product Retailers','03020205',19,1),(39,'Nonwoven Fabric Mills','04010201',21,1),(40,'Yarn Spinning Mills','04010303',21,1),(41,'Home Furnishings Textile and Soft Furnishings (inc. carpets and rugs)','04010403',21,1),(42,'Apparel Brand Licensing (brand management)','04020101',3,1),(43,'Ready Made Garment Manufacturing','04020102',21,1),(44,'Undergarment Manufacturing','04020103',21,1),(45,'Footwear Manufacturing','04020309',15,1),(46,'Luggage & Briefcase Manufacturing','04020402',15,1),(47,'Jewelry Manufacturing(exclude costume jewelry)','04020501',15,1),(48,'Eyewear & Eyewear Accessories Manufacturing','04020601',15,1),(49,'Sportswear and Accessories Manufacturing','04020310',15,1),(50,'Ceramic Wall & Floor Tiles Manufacturing','05020201',15,1),(51,'Bathroom Fixtures& Sanitary Ware Manufacturing','05020403',15,1),(52,'Point of Sale Systems Manufacturing','05030205',15,1),(53,'Household Electric Appliances Manufacturing (inc. air cooler and fans)','     06010107',15,1),(54,'Bicycle Manufacturers','06030201',15,1),(55,'Motorhomes, Trailers & Campers','06030302',15,1),(56,'Kitchen Utensils, Flatware and Glassware Manufacturing','06010209',15,1),(57,'Fitness & Sport Centers Operators','07010101',13,1),(58,'Golf Courses Operators','07010104',13,1),(59,'Professional Soccer Teams','07010201',13,1),(60,'Cruise Lines Operators','07020102',13,1),(61,'Bars & Taverns Operators','07020201',13,1),(62,'Movie Theaters Operators','07030101',13,1),(63,'Event Promoters','07030112',13,1),(64,'Museum Operators','07030113',13,1),(65,'Amusement and Theme Park (include Arcade) Operators','07030114',13,1),(66,'Casinos Operators','07030203',13,1),(67,'Mobile & Online Gambling Operators','07030204',13,1),(68,'Race Track Management Operators','07030207',13,1),(69,'Lottery Operators','07030208',13,1),(70,'Retail Travel Agencies','07030302',13,1),(71,'Internet Based Travel Info & Booking Services','07030304',13,1),(72,'Hotels & Resorts Operators (exclude Casino Hotel)','07020105',13,1),(73,'Restaurant, Snack and Juice Bar Operators (include cafÃ©)','07020207',13,1),(74,'Amusement and Theme Park (include Arcade) Operators','07030114',13,1),(75,'Medical Supplies Distributors','08030102',8,1),(76,'Rubber Gloves Manufacturers','08030202',15,1),(77,'Pharmaceutical Distributors','08030301',8,1),(78,'Behavioral Health Facilities','08040102',12,1),(79,'Medical & Diagnostic Laboratories Testing Services','08040301',12,1),(80,'Radiology & Diagnostic Imaging Services','08040302',12,1),(81,'Home Health Care & Hospice Services','08040307',12,1),(82,'Veterinary Treatment Facilities','08050101',12,1),(83,'Hospitals, Clinics & Primary Care Service Providers','08040101',12,1),(84,'Funeral Home & Service Providers','09010104',7,1),(85,'Pawn Shops Services','09010107',7,1),(86,'Beauty Salons & Spa Operators','09010201',7,1),(87,'Hair Salons Operators','09010202',7,1),(88,'Private University, College & Professional School Operators','09010302',7,1),(89,'Private Elementary & High School Operators','09010303',7,1),(90,'Tuition Centres (Cram or Preparatory School) Operators','09010304',7,1),(91,'Language School Operators','09010305',7,1),(92,'Internet Based Restaurant Reservation & Food Delivery Services','09010307',7,1),(93,'Dating Services Web','09010402',7,1),(94,'Tax Preparation Service ','09020204',3,1),(95,'Security Services Providers','09020304',3,1),(96,'Internet Based Recruitment Services','09020403',3,1),(97,'Exhibition & Conference Services ','09020602',3,1),(98,'Auction Houses & Art Dealers (non-online)','09020603',3,1),(99,'Domain Register Services','09020606',3,1),(100,'Industry Data & Analytic Services','09020702',3,1),(101,'Technology Data & Analytics Services','09020704',3,1),(102,'Consumer & Commercial Services Sector','09020705',3,1),(103,'Engineered Wood Products Manufacturing','10010201',15,1),(104,'Pulp Mills','10020102',15,1),(105,'Paper Mills','10020103',15,1),(106,'Glass Containers & Packaging Materials Manufacturing','10030201',15,1),(107,'Metal Containers & Packaging Materials Manufacturing','10030202',15,1),(108,'Plastic Containers & Packaging Materials Manufacturing','10030204',15,1),(109,'Plastic Bag & Pouch Manufacturing','10030205',15,1),(110,'Plastic Film & Sheet Manufacturing','10030206',15,1),(111,'Logging and Timberland Services','10010103',15,1),(112,'Paper Packaging Materials Manufacturing','10030106',15,1),(113,'Aircraft Leasing Services','11010104',11,1),(114,'Motorcycles & Scooters Manufacturing','11020101',15,1),(115,'Motor Vehicle Wheel Manufacturing','11020218',15,1),(116,'Auto Parts & Accessories Store Retailers','11020309',19,1),(117,'Automobile Rental & Leasing Companies','11020312',11,1),(118,'Low Cost (Budget) Passenger Airlines (incl. short & long haul)','     12010207',1,1),(119,'Full Service Passenger Airlines (inc. short & long haul)','12010208',1,1),(120,'Dry Bulk Shipping Services','12020203',32,1),(121,'Chemical Tankers Chartering Services','12020207',32,1),(122,'LPG & LNG Tankers Chartering Services','12020208',32,1),(123,'Oil Tankers Chartering Services','12020209',32,1),(124,'Rail Freight Services','12020301',17,1),(125,'Truckload Transportation Services','12020501',17,1),(126,'Storage & Warehousing Services','12020603',3,1),(127,'Dredging Services','12020705',6,1),(128,'Air-conditioning, Freezing & Heating Equipment Manufacturing','13010101',2,1),(129,'Light Fixture Manufacturing and Lights Production','13010201',2,1),(130,'Fire Detection & Fighting Equipment Manufacturing','13010301',2,1),(131,'Security System Manufacturing','13010302',2,1),(132,'Elevator & Moving Stairway for Commerical & Residential Building Industry - Manufacturing','13010401',2,1),(133,'Electronic Measuring Instrument Manufacturing','13010502',2,1),(134,'Power Cable Manufacturing','13010604',2,1),(135,'Fluid Control Device Manufacturing','13010804',2,1),(136,'Pump & Pumping Equipment Manufacturing','13010805',2,1),(137,'Power Transmission Products Manufacturing','13020102',2,1),(138,'Engine Manufacturing','13020104',2,1),(139,'Construction & Mining Machinery Manufacturing','13020204',2,1),(140,'Commerical Farm Machinery Manufacturing','13020301',2,1),(141,'Lawn & Garden Equipment Manufacturing','13020304',2,1),(142,'Food Processing Machinery - Manufacturing','13020501',2,1),(143,'Cleaning Machinery Manufacturing','13020602',2,1),(144,'Sawmill & Woodworking Machinery Manufacturing','13021301',2,1),(145,'Glass & Stone Processing Equipment & Machinery Manufacturing','13021403',2,1),(146,'Convey & Conveying Equipment & Machinery Manufacturing','13021601',2,1),(147,'Industrial Lifting Trucks & Stackers Manufacturing','13021602',2,1),(148,'Packaging Equipment & Machinery Manufacturing','13021604',2,1),(149,'Welding & Solder Equipment Manufacturing','13021707',2,1),(150,'Air & Liquids Filtration Products Manufacturing (eg filter bag)','13030102',2,1),(151,'Water Purification Products Manufacturing','13030103',2,1),(152,'Waste Recycling Products Manufacturing (excl secondary metal smelters & refiners)','13030302',2,1),(153,'Waste Collection, Treatment & Disposal Services','13030305',3,1),(154,'Electrical Contractors','13040101',6,1),(155,'Civil Engineering Services','13040201',6,1),(156,'Construction & Mining Machinery & equipment Distribution','13050101',8,1),(157,'Air Heat & A/C Equipment & Supplies Distribution','13050201',8,1),(158,'Electrical Supplies Distribution','13050202',8,1),(159,'Electronic components Distribution','13050203',8,1),(160,'Machinery & Equipment Renting Services','13050301',3,1),(161,'Printing Machinery & Equipment Manufacturing','13050601',2,1),(162,'Minerals & Metal Processing Industry Machinery Manufacturing','13021404',2,1),(163,'Environmental Control and Monitoring System Manufacturing','13030105',2,1),(164,'Water & Wastewater Treatment Facilities Services','13030306',6,1),(165,'Overhead Crane Manufacturing (Including Material Handling Equipment)','13021606',2,1),(166,'','',0,1),(167,'Precious Metals Smelting & Refining','14010206',33,1),(168,'Rare Earth Minerals Mining','14010207',33,1),(169,'Secondary Copper Smelting & Refining ','14020103',33,1),(170,'Secondary Aluminum Smelting & Refining','14020203',33,1),(171,'Tin Mining','14020601',33,1),(172,'Iron Ore Mining & Processing','14020704',33,1),(173,'Silica Mining & products manufacturing','14020906',33,1),(174,'Uranium Mining & Processing','14021102',33,1),(175,'Thermal Coal Mining & Processing','14030101',33,1),(176,'Coking Coal Mining & Processing','14030102',33,1),(177,'Diamond Mining & Processing','14060104',33,1),(178,'Gold Mining & Processing','14010106',33,1),(179,'Heavy Minerals Mining & Processing','14020612',33,1),(180,'Long, Pipe & Tubular Products','14040109',15,1),(181,'Nickel Mining & Processing','14020504',33,1),(182,'Silver Mining & Processing','14010104',33,1),(183,'Aluminium Mining (Bauxite) & Processing','14020204',33,1),(184,'Metal Forging','14080305',15,1),(185,'Platinum Group Mining & Processing','14010105',33,1),(186,'Steel Products Manufacturer','14040110',15,1),(187,'Zinc Mining & Processing','14020404',33,1),(188,'Steel Producers','14040111',15,1),(189,'Metal casting','14020710',15,1),(190,'Copper Mining & Processing','14020106',33,1),(191,'Ferro Alloy Manufacturer','14020711',15,1),(192,'Aluminum Products Manufacturer','14020205',15,1),(193,'Chlor Alkali Products Manufacturing','15010101',15,1),(194,'Industrial Gas Mfg','15010102',15,1),(195,'GraphiteElectrodeManufacturing','15020105',15,1),(196,'Traditional Ceramics (Excluding Tiles)','15020109',15,1),(197,'Printing Ink','15020202',15,1),(198,'Synthetic Dye & Pigments','15020205',15,1),(199,'Adhesives and Sealants Manufacturing','15020501',15,1),(200,'Flavors and FragranceManufacturing','15020601',15,1),(201,'Explosives Chemicals Manufacturing','15020901',15,1),(202,'Nitrogenous Fertilizers (ammonia & urea)','15030101',15,1),(203,'Rubber Planting and Processing','15040402',10,1),(204,'Oil & Gas Explorers & Producers','16010102',34,1),(205,'Petroleum Refining','16010401',34,1),(206,'Biodiesel Production','16020101',16,1),(207,'Ethanol Fuel Production','16020102',16,1),(208,'Coal Power Generation','16030101',16,1),(209,'Gas Power Generation ','16030102',16,1),(210,'Oil Power Generation','16030103',16,1),(211,'Solar Power Generation','16030301',16,1),(212,'Wind Power Generation','16030302',16,1),(213,'Hydro Power Generation','16030304',16,1),(214,'Natural Gas Distributors','16040203',34,1),(215,'Photovoltaic Cells, Modules, Wafers & Thin Film Manufacturers','16070103',15,1),(216,'Wind Turbine Manufacturers','16070201',15,1),(217,'Foundation & Structure Contractors','17010102',6,1),(218,'Airport Developers and Operators','17010402',14,1),(219,'Roads and Highways Developers and Operators','17010403',14,1),(220,'Construction Aggregates Producers (crushed stones , sand & gravel)','17010601',15,1),(221,'Cement Manufacturing ','17010602',15,1),(222,'Commerical Properties Developers (Office and Industrial)','18010105',18,1),(223,'Retail Properties Developers (Regional mall and Shopping Centers)','18010106',18,1),(224,'Residential Properties Developers (for sales mainly)','18010201',18,1),(225,'Residential Properties Developers (for rental mainly)','18010202',18,1),(226,'Student Housing Developers','18010203',18,1),(227,'Manufactured Housing Developers','18010205',18,1),(228,'Self-Storage Developers','18010302',14,1),(229,'Real Estate Brokerage and Consultancy Services','18020103',4,1),(230,'Financial Transaction Processing Services','19010204',11,1),(231,'Investment Banking - Financial Advisory Services','19020101',11,1),(232,'Telecommunications Devices Manufacturing','20010203',15,1),(233,'Telecommunication Tower Leasing Operators','20010302',5,1),(234,'Wired/Wireless Telecommunications Carriers','20020101',5,1),(235,'VOIP Services (Cloud Based Communications) Providers','20020102',5,1),(236,'Local TV Broadcasting','20030101',9,1),(237,'Radio Broadcasting Providers','20030102',9,1),(238,'Cable TV Networks Operators','20030103',9,1),(239,'Satellite TV Operators','20030104',9,1),(240,'Advertising Agencies','20040101',3,1),(241,'Outdoor Advertising Agencies','20040102',3,1),(242,'Market Research & Public Opinion Poll Providers','20040106',3,1),(243,'Newspaper Publishers','20050201',7,1),(244,'Online Movie & Music Download','20050302',7,1),(245,'Communication & Broadcasting Equipment Manufacturing','20010106',15,1),(246,'Multimedia, Film & Television Production House','20050111',9,1),(247,'Computer Peripherals Manufacturing','21010102',15,1),(248,'Display Panels Manufacturing','21010105',15,1),(249,'Light Emitting Diode (LED) Manufacturing','21020205',15,1),(250,'Laser Optical Components Manufacturing','21020215',15,1),(251,'Graphic Software Development','21030103',20,1),(252,'Engineering Software Development','21030104',20,1),(253,'Accounting Software Development','21030105',20,1),(254,'Productivity Software Development','21030107',20,1),(255,'Enterprise Resource Planning (ERP) Software Development','21030108',20,1),(256,'Communications Software Development','21030202',20,1),(257,'Education Software Development','21030203',20,1),(258,'Online Games Software Development','21030207',20,1),(259,'Database Software Development','21030301',20,1),(260,'Technology Consulting Services','21040104',20,1),(261,'Transaction Based Software Solutions','21040106',20,1),(262,'IT Services for Government Sector','21040201',20,1),(263,'Semiconductor Foundries & Integrated Circuits Design & Manufacturing','21020106',15,1),(264,'Business Process Outsourcing Services','21040107',3,1),(265,'Technology Supply Chain Products Distribution','21040303',20,1),(266,'Memory Drives, Chips & Components Manufacturing','21010206',15,1),(267,'Digital Security Solutions Provider','21030304',20,1),(268,'Online & Social Games Developer','21030209',20,1);
/*!40000 ALTER TABLE `DataExtraction_sectordit` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `DataExtraction_subsection`
--

DROP TABLE IF EXISTS `DataExtraction_subsection`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `DataExtraction_subsection` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `item` varchar(2000) NOT NULL,
  `i_synonyms` varchar(2000) DEFAULT NULL,
  `i_breakdown` varchar(5000) DEFAULT NULL,
  `i_keyword` varchar(1000) DEFAULT NULL,
  `added_date` datetime NOT NULL,
  `section_id` int(11) NOT NULL,
  `i_deduction` varchar(2000) DEFAULT NULL,
  `added_by_id` int(11) DEFAULT NULL,
  `modified_by_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `DataExtraction__section_id_7e236ea0_fk_DataExtraction_section_id` (`section_id`),
  KEY `DataExtraction_subsection_0c5d7d4e` (`added_by_id`),
  KEY `DataExtraction_subsection_b3da0983` (`modified_by_id`),
  CONSTRAINT `DataExtraction_subsection_added_by_id_8b87730f_fk_auth_user_id` FOREIGN KEY (`added_by_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `DataExtraction_subsectio_modified_by_id_d32f8c11_fk_auth_user_id` FOREIGN KEY (`modified_by_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `DataExtraction__section_id_7e236ea0_fk_DataExtraction_section_id` FOREIGN KEY (`section_id`) REFERENCES `DataExtraction_section` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=52 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `DataExtraction_subsection`
--

LOCK TABLES `DataExtraction_subsection` WRITE;
/*!40000 ALTER TABLE `DataExtraction_subsection` DISABLE KEYS */;
INSERT INTO `DataExtraction_subsection` VALUES (1,'Cash & Near Cash Items','Cash & Cash Equivalents','bills ## coins ##  funds for current purposes ## checks ## cash in bank ## bank accounts ##  marketable securities ## checks received but not yet deposited ##checking accounts ## petty cash ##  savings accounts ## money market accounts ## Fixed Deposit, Government Securities ## Cash in transit ## Other cash equivalents ## Trading securities ## Bank balances and cash ## Cash and bank balances ## Cash at bank and on hand ## marketable equity##Cash and equivalents##cash','','2017-11-30 04:33:50',1,'',NULL,NULL),(2,'Short-Term Investments','temporary investments ## Current Investments ## short-term inverstments','debt securities ## short-term paper ## Treasury bills and commercial paper ## preferred stock, mutual funds ## Bank deposits with maturity over three months ## Other current investments ## Held for trading investments ## Bank balances held on behalf of customers ## Liquid investments ## Available-for-sale investments ## Time deposits with original maturity over three months ## Short-term bank deposits','short-term','2017-11-21 12:08:07',1,'',NULL,NULL),(3,'Trade Receivable','Accounts Receivable,net ## Accounts receivable, less allowance for doubtful accounts ## Trade debtors and bills receivable ## Accounts receivable, net of allowance for doubtful accounts and sales returns ## Trade Receivable##Accounts receivable','Notes Receivable ## Trade Receivable - 3rd parties ## Trade Receivable - related parties ## Reversal on Impairment on Trade Receivable ## Unbilled Revenue ## Amounts due from related parties ## Unbilled accounts receivable','','2017-11-29 16:15:44',1,'',NULL,NULL),(4,'Inventories','Inventories, net ## Merchandise inventories ## Inventories and supplies ## Raw materials and supplies## inventory, net','Spare parts and servicing equipment ## Provision for dismantlement ## removal or restoration ## raw materials ## work in progress ## WIP, finished goods ## manufacturing cost ## Spare Parts ## Finished Products ## Goods in transit ## Stock ## stock in trade','inventories, raw, stock, goods, material','2017-11-29 09:53:18',1,'Less: Impairment on Inventories,Impairment on Inventories',NULL,NULL),(5,'Other Current Assets','\'\'','\'\'','','2017-10-04 07:09:44',1,'',NULL,NULL),(6,'Property, Plant & Equipment','Net Fixed Assets ## Property, plant and equipment, net ## Tangible assets##Total property, plant and equipment, net','Land ## Buildings ## Plant and Equipment ## Equipment under Finance Lease ## Furniture ## Other Property, Plant & Equipment ## Construction in Progress ##  Asset Revaluation Deficit ## Capital Work-In-Progress ## Subscriber System Assets ## Vehicles physical assets ## tangible fixed assets ##  Land and land improvements ## Land, buildings and improvements ## Land and buildings ## Property, plant and equipment in progress ## Construction work in progress ## Fixed assets (including Capital work in progress) ## Office equipment ## Furniture and other equipment ## Other fixtures and fittings, tools and equipment ## Equipment , Machinery and equipment ## Computer equipment and capitalized software ## Plant and machinery ## Plant, property and equipment, net ## Rental equipment ## Building ## Buildings and building equipment ## Building & improvements ##  Motor Vehicles##Construction in process','equipment, land, machinery, plant, property, buildings, vehicles, fleet, warehouses','2017-11-30 10:37:38',2,'',NULL,NULL),(7,'Intangible Assets','Intangible Assets','Goodwill ## Patents ,Trademarks ## Copyrights ## Land Use Rights, Licenses ## Acquired intangible assets, net ##  Permits and other intangible assets  ## Other intangible assets ## Definite-lived intangible assets, net ## Indefinite-lived intangible assets ## Broadcasting Rights ## Customer Relationships ## Goodwill on acquisition ## Goodwill and intangible assets, net ##  Trademarks and trade names ## Permits and other intangible assets  ##  Other intangible assets, net ## brand recognition ## Brand, ##software','intangible','2017-11-21 12:14:37',2,'',NULL,NULL),(8,'Investment Properties','\'\'','Land Held for Property Development ## Buildings Held for Leasing ## Office Units Held for Leasing ## Residential Units Held for Leasing ## Commercial Units Held for Leasing ## Investment Property Construction in Progress ## Reversal on Impairment on Investment Properties ## Investment Properties Revaluation Reserve ## Long Term Investment ## Shares in co-operative property ## investment in stocks bonds, and properties ## funds set up for long-term purposes ## Investments in subsidiaries ## Long-term investments ## Other investments and non-current accounts receivable joint ventures and associated companies','investment','2017-11-21 12:15:24',2,'',NULL,NULL),(9,'Investment in Associated Companies/Joint Ventures','Equity and Cost Method Investments ## Equity in investees ## Investments in associates and joint ventures ## Investments accounted for using the equity method ## Participations in affiliated companies and joint ventures ## Equity method investments ## Equity interests in associates','Investments in associates ## Investments in joint ventures ## Investments in unconsolidated subsidiaries ## Interests in associates , Joint ventures ## Investment in an associate ## Investments in joint ventures and associates ## Interests in joint ventures ## Associated companies','joint ventures, Investments in associates','2017-11-21 12:15:56',2,'',NULL,NULL),(10,'Biological Assets','\'\'','Mature Plantations ## Immature Plantations ## Nursery, Plantation Expenditure ## Biological Assets Revaluation Reserve ## Plantation assets ## Animals and Livestock ## plants and animals','','2017-11-21 12:16:11',2,'',NULL,NULL),(11,'Long-Term Financial Assets','\'\'','Derivatives Financial Assets for Hedging ## Foreign Currency Forward Contracts ## Interest Rate Swaps ## Currency Swaps ## Non-Derivative Financial Assets Held for Trading ## Held-to-Maturity Investments ## Held-to-Maturity Bills of Exchange/Promissory Notes ## Held-to-Maturity Debentures/Notes/Bonds ## Available-for-Sales Financial Assets ## Available-for-Sales Redeemable Notes/Bonds ## Available-for-Sale Shares in Third Party Entities ## Financial Assets Revaluation Reserve ## Financial assets at fair value through profit or loss ## Available-for-Sale Investment ## Held-to-maturity financial asset ## Held for Trading Investments ## Interest rate swap contract','','2017-11-21 12:16:40',2,'',NULL,NULL),(12,'Other Non-Current Assets','\'\'','\'\'','','2017-11-21 12:19:50',2,'',NULL,NULL),(13,'Trade Payables','Accounts Payable ## Trade and bills payables ## Trade creditors and bills payable ## Trade accounts payable','Trade Payables - 3rd parties ## Trade Payables - related parties ## Accounts payable, client accounts ## Supplier Credit ## Notes Payable ## Trade and other payables','trade','2017-11-21 12:20:51',3,'',NULL,NULL),(14,'Short-Term Borrowings','Short-Term Debt Obligations ## Bank borrowings ## Bank borrowings, secured ##  Short-term debt including current maturities of long-term debt','Short-Term Bank Loans and Overdraft ## Short-Term Loan from Related Parties ## Short-Term Loan from Third Party Entities ## Short-Term Loan from Government ## Current Portion of Long-Term Bank Loans ## Current Liability Component of Convertible Debt/Notes/Bonds ## Current Portion of Notes/Bonds ## Current Portion of Perpetual Debt/Notes/Bonds ## Current Portion of Long-Term Loan from Related Parties ## Current Portion of Long-Term Loan from Third Party Entities ## Current Portion of Long-Term Loan from Government ## Current Portion of Redeemable Preference Share ## Current portion of finance leases ## Revolving credit agreements ## Current portion – capital leases ## Current portion of closure ## post-closure and remedial liabilities ## Short-term debt ## short-term loan ## Interest-bearing loans and borrowings ## Notes payable to banks ## Short-term debt and current maturities of long-term debt ## Interest-bearing loans ## borrowings and other financial liabilities ## Short-term Bank indebtedness ## Short-term borrowings and current maturities of long-term debt ## Bank overdraft ## Loan from significant shareholder ## Amount due to associate ## Current portion of bank loans ## Current portion of long-term debt ## Current portion of borrowings and short-term bank loans## Current maturities of long-term debt ## Current maturities of long-term debt and short-term facilities ## Short term bonds ## Senior notes , current portion ## Loans from shareholders ## Financial institutions and other loans ## Loans from financial institutions (current portion) ## Capital Lease Obligations - Short-Term Portion ## Short-term financing note payable ## Notes payable to banks ## Financial Lease Payables ## Capital Lease Payables ## Obligations under finance leases','borrowings, debt, loans, bonds','2017-11-21 12:21:24',3,'',NULL,NULL),(15,'Current Financial Liabilities','\'\'','Financial Guarantee Contracts ## Derivatives Financial Liabilities for Hedging ## Foreign Currency Forward Contracts ## Interest Rate Swaps ## Currency Swaps ## Non-Derivative Financial Liabilities Held for Trading ## Interest rate swap contract ## Financial Guarantee Contract','derivative','2017-11-21 12:21:45',3,'',NULL,NULL),(16,'Other Current Liabilities','\'\'','\'\'','','2017-09-26 04:40:29',3,NULL,NULL,NULL),(17,'Long-Term Borrowings','Long-Term Debt Obligations ## Long-term debt ## Long-term debt ## less current portion ##Long-Term Borrowings','Long-Term Bank Loans ## Liability Component of Convertible Debt/Notes/Bonds, Notes/Bonds ## Perpetual Debt/Notes/Bonds ## Long-Term Loan from Related Parties ## Long-Term Loan from Third Party Entities ## Long-Term Loan from Government ## Redeemable Preference Share ## Building Financing Arrangement ## Senior unsecured debentures ## Long-term capital-lease obligation ## debentures ## loans ## Bank borrowings ## Medium and long-term borrowings ## Convertible bonds ## Convertible debentures ## Senior notes ## Residents loan ## Loans from shareholders','debt, borrowing, loans, debentures, bonds, senior notes','2017-11-21 12:25:19',4,'',NULL,NULL),(18,'Long-Term Financial Liabilities','Medium-/long-term financial liabilities','Financial Guarantee Contracts ## Derivatives Financial Liabilities for Hedging ## Foreign Currency Forward Contracts ## Interest Rate Swaps ## Currency Swaps ## Non-Derivative Financial Liabilities Held for Trading ## Financial Liabilities Revaluation Reserve ## Long-Term Interest rate derivative liability ## Other Long-Term financial obligations ## Interest rate swap contract ## Derivative financial instruments','Derivative','2017-11-21 12:25:44',4,'',NULL,NULL),(19,'Other Non-Current Liabilities','Other long-term liabilities','\'\'','\'\'','2017-09-26 04:57:04',4,NULL,NULL,NULL),(20,'Shareholder Equity','Shareholders Funds##Capital Stock','\'\'','','2017-09-26 12:26:57',5,NULL,NULL,NULL),(21,'Share Capital & Additional Paid-In Capital','\'\'','Common Share Issued and Paid-Up ##Common stock and additional paid-in capital##Common Stock##Common stock, no par value##Common shares##Issued capital##Additional Paid In Capital##Paid-in capital##Additional paid-in-capital##Share Premium##Capital in excess of par value##Treasury Shares##Treasury Stock, at cost##Cost of shares held in treasury##Treasury stock##Distributions in Excess of Earnings##Shares held under employee participation plan##Contributed surplus','','2017-11-29 03:04:22',5,'',NULL,NULL),(22,'Non-Redeemable Preference Share','Preferred Stock','Non-Redeemable Participating Preference Share##Non-Redeemable Convertible Non-Participating Preference Share','','2017-09-26 12:27:51',5,NULL,NULL,NULL),(23,'Retained Earnings/(Losses)','Retained Earnings##Retained Losses','\'\'','','2017-09-26 12:28:24',5,NULL,NULL,NULL),(24,'Reserves','\'\'','Currency Translation Reserve##Statutory Reserve##Surplus Reserve##Capital Reserve##Accumulated Other Comprehensive Gain##Accumulated Other Comprehensive Loss##Share Option Reserve##Merger Reserve##Unearned Compensation##Equity Contribution Reserve##Warrants reserve##Revaluation reserve##Other equity reserves##Hedging reserves##Available-for-sale reserve##Cash flow hedging reserve##Hedging, translation and fair value reserves##Revluation reserve from measurement of financial instruments##Capital redemption reserve##Foreign currency translation reserve##Foreign exchange reserve##Exchange differences from the translation of foreign operations statement','','2017-09-26 12:28:47',5,NULL,NULL,NULL),(26,'Other Equity','\'\'','Equity Component of Convertible Notes & Bonds##Differences Arising from Restructuring Transactions##Income Tax Benefits/(Liabilities) Credited to Equity##Money Received against Share Warrants##Convertible equity instrument##Mandatory convertible securities','','2017-09-26 12:30:19',5,NULL,NULL,NULL),(27,'Other Current Assets Deduction','\'\'','\'\'','','2017-10-04 06:40:26',1,'',NULL,NULL),(28,'Other Non-Current Assets Deduction','\'\'','\'\'','','2017-10-04 06:42:18',2,'',NULL,NULL),(29,'Other Current Liabilities Deduction','\'\'','\'\'','','2017-10-04 09:11:48',3,'',NULL,NULL),(30,'Other Non-Current Liabilities Deduction','\'\'','\'\'','','2017-10-04 06:41:40',4,'',NULL,NULL),(31,'Other Equity Deduction','\'\'','\'\'','','2017-10-04 06:42:09',5,'',NULL,NULL),(32,'Revenue','Revenue from Operations## Revenue ## Net Sales ## Operating Revenues ## Sales to Customers ## Net Revenue from Operations ## Operating sales revenue ## Total revenues ## Sales revenue ## Net Sale of products ## Net revenues ## Turnover','\'\'','','2017-11-27 05:06:23',6,'',NULL,NULL),(33,'Cost of Revenue','Cost of Revenue ## Cost of Goods Sold ## Cost of Products Sold ## Cost of Sales ## Cost of Services Provided ## Total cost of revenues ## Cost of sales and services provided ## Cost of Operations ## Cost of Revenues ## Cost of merchandise sales ## Cost of services','Direct Materials Used ## Cost of Materials Consumed ## Raw materials and consumables used ## Material costs,Purchases used in the business ## Purchases of stock-in-trade ## Purchase of Finished Goods Inventory to be Sold ## Direct Labour for Manufacturing ## Labor ## Manufacturing Overhead Expense ## Production Equipment Depreciation Expense ## Depreciation Expenses allocated to Cost of Revenue  ## Cost of Power Purchased ## Power and fuel ## Electricity and other fuel purchases ## Cost of Fuel ## less: Cash Discount ## Purchases of Stock in Trade ## Changes in Inventory ## Changes in inventories of finished goods ## work in progress and stock-in- trade ## Vessel Operating Costs ## Shipping and loading costs( freight inward costs) ## Amortization of Content Rights ##Any direct intangible pre publication costs ## Broadcasting rights specific to the industry ## Primary Packaging Costs ## Sub-contracting Expenses ## Third Party Services','','2017-11-27 05:08:19',7,'',NULL,NULL),(34,'Royalty Income','\'\'','\'\'','','2017-11-27 05:08:53',8,'',NULL,NULL),(35,'Other Operating Revenue','Other Operating Income##Other Revenue ## Other income ## Services and others ## Franchise royalties and fees ## Other sales ## Other revenues','Reversal on Impairment Loss on Property ,Plant and Equipment ## Reversal on impairment on land and buildings ## Reversal on Impariment Loss on Inventory ## Reversal on Provision for Doubtful Trade Receivables ## Reversal on Provision for Other Doubtful Receivables ## Reversal on Provision for Inventory ## Gain on disposal of operating assets ( excluding PPE and intangible assets, operating assets include inventory, trade receivables (like factoring) etc) ## Subsidy or Grants from Government ## Change in valuation of any other current asset','','2018-02-22 12:38:05',8,'',NULL,NULL),(36,'Selling & Marketing Expenses','Direct and Selling ## Selling, marketing and distribution ## Selling and promotion expenses','Delivery Charges ## Marketing Expenses ## Marketing and distribution expenses ## Marketing and promotional expenses ## Advertising and Promotion ## Freight outward Charges## Freight and forwarding expenses ## Freight expenses ## Transportation costs ## Warranty Claims## Selling and distribution costs ## Distribution costs ## Secondary Packaging Costs##other s,g&a expenses## Freight outward Shipping Charges','','2018-02-22 12:45:43',9,'',NULL,NULL),(37,'General & Administrative Expenses','General and Administrative Expenses','General and Administrative ##Employee Benefits Expenses##Personnel costs##Employee Related Expenses##Staff costs##Salaries and employees benefits##Employee Wages## Pensions and other Benefits##Pension settlement expense##Professional Fees Incurred for Operation##Traveling and Accommodation Expenses##Licenses and Permits Charges##Amortization of Intangible Assets##Intangible amortisation##Rental Expenses##Research and development##Product development##Communication Expenses##Insurance##Donations##Repair and Maintenance Expenses##Legal Fees##Consultant Fees##Secretarial Fees##Audit Fees##Office Supplies##Office Refreshment##Utility##Training Expenses##Services and utilities##Travel & Transportation##Postage##Property Taxes## Depreciation and Amortisation ##Royalties expense##Bank Charges##Auditor Renumeration##Selling, general and Administrative expenses##Director\'s Sitting Fees##Bank Admin Fees##Commission Expense ## Entertainment Expenses','','2018-03-07 11:16:54',9,'',NULL,NULL),(38,'Other Operating Expenses','Other Operating Expenses','Impairment Loss on Property, Plant and Equipment ## Impairment of long-lived assets ## Impariment Loss on Inventory ## Provision for Doubtful Trade Receivables ## Bad Debt Expense ## Provision for Other Doubtful Receivables ## Provision for Inventory ## Impairment Losses ## Goodwill impairment charge ## Impairment charges ## Asset impairment and exit costs ## Restructuring and redundancy ## Restructuring related impairment ## Restructuring expenses ## Plant restructuring ## Restructuring Charges ##  Impairment loss on acquired intangible assets ## Impairment loss on other intangible assets ## Exploration and evaluation ## Exploration expenses ## Exploration and evaluation expenses ## Write-down of non-current assets ## Impairment reversal/(charge) in associate ## Accretion of environmental liabilities ## Fulfillment costs ## Acquisition Costs (Administrative Cost incurred due to mergers or acquisitions)','','2017-11-27 05:12:11',9,'',NULL,NULL),(39,'Financial Income','Financial Income','interest from Bank Deposits ## Interest from Available-for-Sale Investments ## Interest and investment income ## Interest from Held-to-Maturity Investments ## Interest from Other Loans and Receivables ## Other financial income (expense), net','','2017-11-27 05:12:48',10,'',NULL,NULL),(40,'Financial Expenses','Finance Costs ## Finance charges##Financial Expenses','Interest on Bank Loans and Overdrafts (other than those from related parties) ## Interest expense ## Interest on Loans from Related Parties ## Interest on Finance Leases ## Interest on Convertible Debt/Notes/Bonds ## Interest on Notes/Bonds ## Interest on Perpetual Debt/Notes/Bonds ## Preferred Dividends on Mandatory Redeemable Preferred and Trust Preferred Securities ## Professional Fees Incurred for Debt Issuance/Repayment ## Loan Facility Fees ## Amortization of Loan Facility Fees ## Amortization of Debt Discount or Premium ## Professional Fees Incurred for Equity Issuance/Buyback ## Non-Cash Interest Expenses ## Amortization of Deferred Financing Fees,Refinancing Costs ## Net financial income/(expense) from derivatives ## Merger termination fees, net','','2017-11-27 05:13:26',10,'',NULL,NULL),(41,'Share of results of associated companies, net of tax','Share of Profit and Loss of Associated Companies ## Gain/(Loss) from equity method investments ## Equity in Earnings (Losses) from Unconsolidated Affiliates ## Equity in gain (loss) of associates ## Share of profits less losses of associates and joint ventures ## Share of income/(losses) of equity investments ## Shares in earnings of affiliated companies and joint ventures after tax ## Result of equity investments ## Shares in earnings in subsidiaries','\'\'','','2017-11-27 05:13:47',10,'',NULL,NULL),(42,'Share of results of joint ventures, net of tax','Share of Profit and Loss of Joint Ventures ## Share of profit of a jointly controlled entity','\'\'','','2017-11-27 05:14:06',10,'',NULL,NULL),(43,'Foreign Exchange Gain/(Loss), net','Net foreign exchange gains','Realized Foreign Exchange Gain or Loss ## Unrealized Foreign Exchange Gain or Loss','','2017-11-27 05:14:31',10,'',NULL,NULL),(44,'Other Non-Operating Income/(Expenses)','Miscellaneous income (expense)## Other Non-Operating Income(Expenses)','Gain/(Loss) on Disposal of Property, Plant and Equipment ## Gain/(Loss) on sales of real estate ## Loss on asset dispositions and impairments ## Exceptional item - Profit on sale of residential flats ## Loss on disposal of real estate and property and equipment, net ## Gain/(Loss) on Investment Properties ## Gain/(Loss) from Disposal of Equity Interest in Subsidiaries/Associates/Joint Ventures ## Gain on disposal of subsidiaries ## Loss on disposal of business ## Net gain (loss) on liquidation of non-operating subsidiaries ## Gain on sale of business ## Gain/(loss) on acquisition and disposal of consolidated entities ## Gain on revaluation of investment to fair value upon discontinuation of equity method ## Gain/(Loss) on Disposal of Financial Assets ## Net (gain) loss on disposals of assets ## Change in Value of Investment Properties ## Change in Value of Financial Assets ## Change in Value ofInterest expense Financial Liabilities ## Change in Value of Assets Classified as Held for Sale ## Change in Pension & Post Retirement Liabilities ## Change in Employee Benefits Obligation ## Actuarial gain on defined benefit plans## \r\nChange in Value of Biological Assets ## Insurance Claims Received ## Business interruption insurance recovery ## Gain/(Loss) on Changes in Fair Values ## Gain/(Loss) on Disposal of Non-Current Assets ## Gain/(Loss) on Debt Extinguishment/Retirement ## Exchange Offer Costs ## Recovery from Legal Settlement/Expenses related to Litigation ## Gain/(Loss) on Real Estate Sales ## Gain/(Loss) on derivative instruments ## Investment Income from Investment Property ## Rental Income from Investment Property ## Reversal on Impairment Loss on Investment Properties ## Securities investment gains ## Impairment Loss on Investment Properties ## Impairment loss on investment securities ## De- recognition of foreign currency translation reserve ## Provision/Reversal for Contingencies ## Dividend Income ##Impairment loss on goodwill ## Goodwill impairment','','2017-11-27 05:15:25',10,'',NULL,NULL),(45,'Income Tax Expense','Taxation ## Income tax expense ##Income tax  benefit ## Tax on the profit for the year,Tax expense ##Tax charge on profit on ordinary activities','Income Tax Expenses of current period ## Current Tax ## Deferred Income Taxes ## Deferred Tax Expenses ## Deferred Tax Credit ## Deferred tax,Provision for Taxes of prior periods ## Current Tax Expense relating to Prior Years ## Provision for Income Taxes ## Provision benefit for income taxes ## Tax Credit Entitlement ## Zakat ## Benefit for Income Taxes ## Income tax provision benefit ## MAT Credit ## MAT credit entitlement ## Tax credit ## Income tax credit ## Income tax recovery##Provision for benefit from income taxes##interest income expense','','2018-03-07 11:19:18',13,'',NULL,NULL),(46,'Profit/(Loss) from Discontinued Operations','Profit/(Loss) from discontinued operations, net of tax','\'\'','','2018-02-22 12:16:46',14,'',NULL,NULL),(47,'Minority Interest','Minority Interest##non controlling interest','\'\'','','2017-11-27 05:17:00',11,'',NULL,NULL),(48,'Depreciation & Amortization','Depreciation & Amortization','depreciation##amortization','','2017-11-27 05:17:29',12,'',NULL,NULL),(49,'Dividend Paid','Dividend Paid','Dividend','','2017-11-27 05:17:45',12,'',NULL,NULL),(50,'less: Export Taxes, Sales Tax','Excise Duty##Business Tax and Surcharges##Less: Excise Duty##Excise taxes and royalties##Excise taxes on products##Special gaming tax, special levy and gaming premium##Service tax or any other indirect tax on sales##less excise taxes','\'\'','\'\'','2018-03-05 07:24:16',6,'',NULL,NULL),(51,'Extra PNL Keywords','\'\'','\'\'','\'\'','2018-03-05 07:29:50',18,'',NULL,NULL);
/*!40000 ALTER TABLE `DataExtraction_subsection` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `DataExtraction_year_data`
--

DROP TABLE IF EXISTS `DataExtraction_year_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `DataExtraction_year_data` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `year_date` varchar(200) DEFAULT NULL,
  `y1` varchar(200) DEFAULT NULL,
  `description` varchar(1000) DEFAULT NULL,
  `pdf_image_path` varchar(1000) DEFAULT NULL,
  `pdf_page` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `DataExtraction_year_data`
--

LOCK TABLES `DataExtraction_year_data` WRITE;
/*!40000 ALTER TABLE `DataExtraction_year_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `DataExtraction_year_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `PNL_companypnldata`
--

DROP TABLE IF EXISTS `PNL_companypnldata`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `PNL_companypnldata` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `gbc_name_id` int(11) NOT NULL,
  `lrq_id` int(11) DEFAULT NULL,
  `q1_id` int(11) DEFAULT NULL,
  `q2_id` int(11) DEFAULT NULL,
  `q3_id` int(11) DEFAULT NULL,
  `q4_id` int(11) DEFAULT NULL,
  `s2section_id` int(11) DEFAULT NULL,
  `section_id` int(11) DEFAULT NULL,
  `subsection_id` int(11) DEFAULT NULL,
  `tlm_id` int(11) DEFAULT NULL,
  `y1_id` int(11) DEFAULT NULL,
  `y2_id` int(11) DEFAULT NULL,
  `y3_id` int(11) DEFAULT NULL,
  `y4_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `PNL_compan_gbc_name_id_9ffc47dd_fk_DataExtraction_companylist_id` (`gbc_name_id`),
  KEY `PNL_companypnl_lrq_id_3c56f2a2_fk_DataExtraction_quarter_data_id` (`lrq_id`),
  KEY `PNL_companypnld_q1_id_d4019884_fk_DataExtraction_quarter_data_id` (`q1_id`),
  KEY `PNL_companypnld_q2_id_5ab90a6f_fk_DataExtraction_quarter_data_id` (`q2_id`),
  KEY `PNL_companypnld_q3_id_1c67f8f8_fk_DataExtraction_quarter_data_id` (`q3_id`),
  KEY `PNL_companypnld_q4_id_10e0ff1c_fk_DataExtraction_quarter_data_id` (`q4_id`),
  KEY `PNL_company_s2section_id_7b583f3d_fk_DataExtraction_s2section_id` (`s2section_id`),
  KEY `PNL_companypnld_section_id_129f6492_fk_DataExtraction_section_id` (`section_id`),
  KEY `PNL_compa_subsection_id_a704a326_fk_DataExtraction_subsection_id` (`subsection_id`),
  KEY `PNL_companypnldat_tlm_id_f597e563_fk_DataExtraction_year_data_id` (`tlm_id`),
  KEY `PNL_companypnldata_y1_id_0149676b_fk_DataExtraction_year_data_id` (`y1_id`),
  KEY `PNL_companypnldata_y2_id_74b82f36_fk_DataExtraction_year_data_id` (`y2_id`),
  KEY `PNL_companypnldata_y3_id_3c98e246_fk_DataExtraction_year_data_id` (`y3_id`),
  KEY `PNL_companypnldata_y4_id_348ce33f_fk_DataExtraction_year_data_id` (`y4_id`),
  CONSTRAINT `PNL_companypnldata_y1_id_0149676b_fk_DataExtraction_year_data_id` FOREIGN KEY (`y1_id`) REFERENCES `DataExtraction_year_data` (`id`),
  CONSTRAINT `PNL_companypnldata_y2_id_74b82f36_fk_DataExtraction_year_data_id` FOREIGN KEY (`y2_id`) REFERENCES `DataExtraction_year_data` (`id`),
  CONSTRAINT `PNL_companypnldata_y3_id_3c98e246_fk_DataExtraction_year_data_id` FOREIGN KEY (`y3_id`) REFERENCES `DataExtraction_year_data` (`id`),
  CONSTRAINT `PNL_companypnldata_y4_id_348ce33f_fk_DataExtraction_year_data_id` FOREIGN KEY (`y4_id`) REFERENCES `DataExtraction_year_data` (`id`),
  CONSTRAINT `PNL_companypnldat_tlm_id_f597e563_fk_DataExtraction_year_data_id` FOREIGN KEY (`tlm_id`) REFERENCES `DataExtraction_year_data` (`id`),
  CONSTRAINT `PNL_companypnld_q1_id_d4019884_fk_DataExtraction_quarter_data_id` FOREIGN KEY (`q1_id`) REFERENCES `DataExtraction_quarter_data` (`id`),
  CONSTRAINT `PNL_companypnld_q2_id_5ab90a6f_fk_DataExtraction_quarter_data_id` FOREIGN KEY (`q2_id`) REFERENCES `DataExtraction_quarter_data` (`id`),
  CONSTRAINT `PNL_companypnld_q3_id_1c67f8f8_fk_DataExtraction_quarter_data_id` FOREIGN KEY (`q3_id`) REFERENCES `DataExtraction_quarter_data` (`id`),
  CONSTRAINT `PNL_companypnld_q4_id_10e0ff1c_fk_DataExtraction_quarter_data_id` FOREIGN KEY (`q4_id`) REFERENCES `DataExtraction_quarter_data` (`id`),
  CONSTRAINT `PNL_companypnld_section_id_129f6492_fk_DataExtraction_section_id` FOREIGN KEY (`section_id`) REFERENCES `DataExtraction_section` (`id`),
  CONSTRAINT `PNL_companypnl_lrq_id_3c56f2a2_fk_DataExtraction_quarter_data_id` FOREIGN KEY (`lrq_id`) REFERENCES `DataExtraction_quarter_data` (`id`),
  CONSTRAINT `PNL_company_s2section_id_7b583f3d_fk_DataExtraction_s2section_id` FOREIGN KEY (`s2section_id`) REFERENCES `DataExtraction_s2section` (`id`),
  CONSTRAINT `PNL_compan_gbc_name_id_9ffc47dd_fk_DataExtraction_companylist_id` FOREIGN KEY (`gbc_name_id`) REFERENCES `DataExtraction_companylist` (`id`),
  CONSTRAINT `PNL_compa_subsection_id_a704a326_fk_DataExtraction_subsection_id` FOREIGN KEY (`subsection_id`) REFERENCES `DataExtraction_subsection` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `PNL_companypnldata`
--

LOCK TABLES `PNL_companypnldata` WRITE;
/*!40000 ALTER TABLE `PNL_companypnldata` DISABLE KEYS */;
/*!40000 ALTER TABLE `PNL_companypnldata` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `PNL_ditsectorsection`
--

DROP TABLE IF EXISTS `PNL_ditsectorsection`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `PNL_ditsectorsection` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `item` varchar(2000) NOT NULL,
  `i_synonyms` varchar(400) DEFAULT NULL,
  `added_date` datetime NOT NULL,
  `added_by_id` int(11) DEFAULT NULL,
  `dit_id` int(11) NOT NULL,
  `modified_by_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `PNL_ditsectorsection_added_by_id_f916850a_fk_auth_user_id` (`added_by_id`),
  KEY `PNL_ditsectorsect_dit_id_4baaf404_fk_DataExtraction_sectordit_id` (`dit_id`),
  KEY `PNL_ditsectorsection_modified_by_id_257b9d66_fk_auth_user_id` (`modified_by_id`),
  CONSTRAINT `PNL_ditsectorsection_added_by_id_f916850a_fk_auth_user_id` FOREIGN KEY (`added_by_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `PNL_ditsectorsection_modified_by_id_257b9d66_fk_auth_user_id` FOREIGN KEY (`modified_by_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `PNL_ditsectorsect_dit_id_4baaf404_fk_DataExtraction_sectordit_id` FOREIGN KEY (`dit_id`) REFERENCES `DataExtraction_sectordit` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `PNL_ditsectorsection`
--

LOCK TABLES `PNL_ditsectorsection` WRITE;
/*!40000 ALTER TABLE `PNL_ditsectorsection` DISABLE KEYS */;
/*!40000 ALTER TABLE `PNL_ditsectorsection` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `PNL_ditsectorsubsection`
--

DROP TABLE IF EXISTS `PNL_ditsectorsubsection`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `PNL_ditsectorsubsection` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `item` varchar(2000) NOT NULL,
  `neg_ro` tinyint(1) NOT NULL,
  `i_synonyms` varchar(2000) DEFAULT NULL,
  `i_breakdown` varchar(5000) DEFAULT NULL,
  `i_keyword` varchar(1000) DEFAULT NULL,
  `i_deduction` varchar(2000) DEFAULT NULL,
  `added_date` datetime NOT NULL,
  `added_by_id` int(11) DEFAULT NULL,
  `dit_id` int(11) NOT NULL,
  `modified_by_id` int(11) DEFAULT NULL,
  `section_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `PNL_ditsectorsubsection_added_by_id_40ec76d4_fk_auth_user_id` (`added_by_id`),
  KEY `PNL_ditsectorsubs_dit_id_db5da300_fk_DataExtraction_sectordit_id` (`dit_id`),
  KEY `PNL_ditsectorsubsection_modified_by_id_671c7920_fk_auth_user_id` (`modified_by_id`),
  KEY `PNL_ditsectorsubs_section_id_bf4311b1_fk_PNL_ditsectorsection_id` (`section_id`),
  CONSTRAINT `PNL_ditsectorsubsection_added_by_id_40ec76d4_fk_auth_user_id` FOREIGN KEY (`added_by_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `PNL_ditsectorsubsection_modified_by_id_671c7920_fk_auth_user_id` FOREIGN KEY (`modified_by_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `PNL_ditsectorsubs_dit_id_db5da300_fk_DataExtraction_sectordit_id` FOREIGN KEY (`dit_id`) REFERENCES `DataExtraction_sectordit` (`id`),
  CONSTRAINT `PNL_ditsectorsubs_section_id_bf4311b1_fk_PNL_ditsectorsection_id` FOREIGN KEY (`section_id`) REFERENCES `PNL_ditsectorsection` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `PNL_ditsectorsubsection`
--

LOCK TABLES `PNL_ditsectorsubsection` WRITE;
/*!40000 ALTER TABLE `PNL_ditsectorsubsection` DISABLE KEYS */;
/*!40000 ALTER TABLE `PNL_ditsectorsubsection` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `PNL_sectorsection`
--

DROP TABLE IF EXISTS `PNL_sectorsection`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `PNL_sectorsection` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `item` varchar(2000) NOT NULL,
  `i_synonyms` varchar(400) DEFAULT NULL,
  `added_date` datetime NOT NULL,
  `added_by_id` int(11) DEFAULT NULL,
  `modified_by_id` int(11) DEFAULT NULL,
  `sector_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `PNL_sectorsection_added_by_id_bc4b6234_fk_auth_user_id` (`added_by_id`),
  KEY `PNL_sectorsection_modified_by_id_56b502ca_fk_auth_user_id` (`modified_by_id`),
  KEY `PNL_sectorsection_sector_id_b068795c_fk_DataExtraction_sector_id` (`sector_id`),
  CONSTRAINT `PNL_sectorsection_added_by_id_bc4b6234_fk_auth_user_id` FOREIGN KEY (`added_by_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `PNL_sectorsection_modified_by_id_56b502ca_fk_auth_user_id` FOREIGN KEY (`modified_by_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `PNL_sectorsection_sector_id_b068795c_fk_DataExtraction_sector_id` FOREIGN KEY (`sector_id`) REFERENCES `DataExtraction_sector` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `PNL_sectorsection`
--

LOCK TABLES `PNL_sectorsection` WRITE;
/*!40000 ALTER TABLE `PNL_sectorsection` DISABLE KEYS */;
INSERT INTO `PNL_sectorsection` VALUES (1,'Oil and Gas Sector##Revenue','Net Revenue','2018-03-05 07:36:33',NULL,NULL,34),(2,'Oil and Gas Sector##Cost of Revenue','Net Cost of revenue','2018-03-05 07:36:33',NULL,NULL,34),(3,'Oil and Gas Sector##Other Operating Income','Total Other Operating Income','2018-03-05 07:36:33',NULL,NULL,34),(4,'Oil and Gas Sector##Operating Expenses','Total Operating Expenses','2018-03-05 07:36:33',NULL,NULL,34),(5,'Oil and Gas Sector##Non-Operating Income/(Expenses)','Total Non operating Expenses','2018-03-05 07:36:33',NULL,NULL,34),(6,'Oil and Gas Sector##Net Profit/(Loss) for the Year','Net Profit, Net Loss','2018-03-05 07:36:33',NULL,NULL,34),(7,'Oil and Gas Sector##Depreciation & Dividend','Total Depreciation','2018-03-05 07:36:33',NULL,NULL,34),(8,'Oil and Gas Sector##Income Tax Expense','Net income tax expense, Total income tax expense','2018-03-05 07:36:33',NULL,NULL,34),(9,'Oil and Gas Sector##Profit/(Loss) from Discontinued Operations','net profit from discontinued operations,Total profit from discontinued opeartions','2018-03-05 07:36:33',NULL,NULL,34),(10,'Oil and Gas Sector##Gross Profit/(Loss)','Gross Profit##Gross Loss##Gross income##Gross Profit/(Loss)','2018-03-05 07:36:33',NULL,NULL,34),(11,'Oil and Gas Sector##Pretax Profit/(Loss)','Profit Before Income Tax##Profit before tax##Income (loss) before provision for income taxes##Income  before provision for income taxes ##loss before provision for income taxes##Earnings before income','2018-03-05 07:36:33',NULL,NULL,34),(12,'Oil and Gas Sector##Extra PNL Keywords','\'\'','2018-03-05 07:36:33',NULL,NULL,34),(13,'B2B Manufacturing Sector##Revenue','Net Revenue','2018-03-13 09:28:49',NULL,NULL,2),(14,'B2B Manufacturing Sector##Cost of Revenue','Net Cost of revenue','2018-03-13 09:28:49',NULL,NULL,2),(15,'B2B Manufacturing Sector##Other Operating Income','Total Other Operating Income','2018-03-13 09:28:49',NULL,NULL,2),(16,'B2B Manufacturing Sector##Operating Expenses','Total Operating Expenses','2018-03-13 09:28:49',NULL,NULL,2),(17,'B2B Manufacturing Sector##Non-Operating Income/(Expenses)','Total Non operating Expenses','2018-03-13 09:28:49',NULL,NULL,2),(18,'B2B Manufacturing Sector##Net Profit/(Loss) for the Year','Net Profit, Net Loss','2018-03-13 09:28:49',NULL,NULL,2),(19,'B2B Manufacturing Sector##Depreciation & Dividend','Total Depreciation','2018-03-13 09:28:49',NULL,NULL,2),(20,'B2B Manufacturing Sector##Income Tax Expense','Net income tax expense, Total income tax expense','2018-03-13 09:28:49',NULL,NULL,2),(21,'B2B Manufacturing Sector##Profit/(Loss) from Discontinued Operations','net profit from discontinued operations,Total profit from discontinued opeartions','2018-03-13 09:28:49',NULL,NULL,2),(22,'B2B Manufacturing Sector##Gross Profit/(Loss)','Gross Profit##Gross Loss##Gross income##Gross Profit/(Loss)','2018-03-13 09:28:49',NULL,NULL,2),(23,'B2B Manufacturing Sector##Pretax Profit/(Loss)','Profit Before Income Tax##Profit before tax##Income (loss) before provision for income taxes##Income  before provision for income taxes ##loss before provision for income taxes##Earnings before income','2018-03-13 09:28:49',NULL,NULL,2),(24,'B2B Manufacturing Sector##Extra PNL Keywords','\'\'','2018-03-13 09:28:49',NULL,NULL,2);
/*!40000 ALTER TABLE `PNL_sectorsection` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `PNL_sectorsubsection`
--

DROP TABLE IF EXISTS `PNL_sectorsubsection`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `PNL_sectorsubsection` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `item` varchar(2000) NOT NULL,
  `neg_ro` tinyint(1) NOT NULL,
  `i_synonyms` varchar(2000) DEFAULT NULL,
  `i_breakdown` varchar(5000) DEFAULT NULL,
  `i_keyword` varchar(1000) DEFAULT NULL,
  `i_deduction` varchar(2000) DEFAULT NULL,
  `added_date` datetime NOT NULL,
  `added_by_id` int(11) DEFAULT NULL,
  `modified_by_id` int(11) DEFAULT NULL,
  `section_id` int(11) NOT NULL,
  `sector_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `PNL_sectorsubsection_added_by_id_c5ef52e6_fk_auth_user_id` (`added_by_id`),
  KEY `PNL_sectorsubsection_modified_by_id_402a999e_fk_auth_user_id` (`modified_by_id`),
  KEY `PNL_sectorsubsection_section_id_ee15843b_fk_PNL_sectorsection_id` (`section_id`),
  KEY `PNL_sectorsubsect_sector_id_59ce70ad_fk_DataExtraction_sector_id` (`sector_id`),
  CONSTRAINT `PNL_sectorsubsection_added_by_id_c5ef52e6_fk_auth_user_id` FOREIGN KEY (`added_by_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `PNL_sectorsubsection_modified_by_id_402a999e_fk_auth_user_id` FOREIGN KEY (`modified_by_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `PNL_sectorsubsection_section_id_ee15843b_fk_PNL_sectorsection_id` FOREIGN KEY (`section_id`) REFERENCES `PNL_sectorsection` (`id`),
  CONSTRAINT `PNL_sectorsubsect_sector_id_59ce70ad_fk_DataExtraction_sector_id` FOREIGN KEY (`sector_id`) REFERENCES `DataExtraction_sector` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=41 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `PNL_sectorsubsection`
--

LOCK TABLES `PNL_sectorsubsection` WRITE;
/*!40000 ALTER TABLE `PNL_sectorsubsection` DISABLE KEYS */;
INSERT INTO `PNL_sectorsubsection` VALUES (1,'Oil and Gas Sector##Revenue',0,'Revenue from Operations## Revenue ## Net Sales ## Operating Revenues ## Sales to Customers ## Net Revenue from Operations ## Operating sales revenue ## Total revenues ## Sales revenue ## Net Sale of products ## Net revenues ## Turnover','\'\'','','','2018-03-05 07:36:33',NULL,NULL,1,34),(2,'Oil and Gas Sector##less: Export Taxes, Sales Tax',0,'Excise Duty##Business Tax and Surcharges##Less: Excise Duty##Excise taxes and royalties##Excise taxes on products##Special gaming tax, special levy and gaming premium##Service tax or any other indirect tax on sales','\'\'','\'\'','','2018-03-05 10:27:57',NULL,NULL,1,34),(3,'Oil and Gas Sector##Cost of Revenue',0,'Cost of Revenue ## Cost of Goods Sold ## Cost of Products Sold ## Cost of Sales ## Cost of Services Provided ## Total cost of revenues ## Cost of sales and services provided ## Cost of Operations ## Cost of Revenues ## Cost of merchandise sales ## Cost of services','Direct Materials Used ## Cost of Materials Consumed ## Raw materials and consumables used ## Material costs,Purchases used in the business ## Purchases of stock-in-trade ## Purchase of Finished Goods Inventory to be Sold ## Direct Labour for Manufacturing ## Labor ## Manufacturing Overhead Expense ## Production Equipment Depreciation Expense ## Depreciation Expenses allocated to Cost of Revenue  ## Cost of Power Purchased ## Power and fuel ## Electricity and other fuel purchases ## Cost of Fuel ## less: Cash Discount ## Purchases of Stock in Trade ## Changes in Inventory ## Changes in inventories of finished goods ## work in progress and stock-in- trade ## Vessel Operating Costs ## Shipping and loading costs( freight inward costs) ## Amortization of Content Rights ##Any direct intangible pre publication costs ## Broadcasting rights specific to the industry ## Primary Packaging Costs ## Sub-contracting Expenses ## Third Party Services','','','2018-03-05 07:36:33',NULL,NULL,2,34),(4,'Oil and Gas Sector##Royalty Income',0,'\'\'','\'\'','','','2018-03-05 07:36:33',NULL,NULL,3,34),(5,'Oil and Gas Sector##Other Operating Revenue',0,'Other Operating Income##Other Revenue ## Other income ## Services and others ## Franchise royalties and fees ## Other sales ## Other revenues','Reversal on Impairment Loss on Property ,Plant and Equipment ## Reversal on impairment on land and buildings ## Reversal on Impariment Loss on Inventory ## Reversal on Provision for Doubtful Trade Receivables ## Reversal on Provision for Other Doubtful Receivables ## Reversal on Provision for Inventory ## Gain on disposal of operating assets ( excluding PPE and intangible assets, operating assets include inventory, trade receivables (like factoring) etc) ## Subsidy or Grants from Government ## Change in valuation of any other current asset','','','2018-03-05 07:36:33',NULL,NULL,3,34),(6,'Oil and Gas Sector##Selling & Marketing Expenses',0,'Direct and Selling ## Selling, marketing and distribution ## Selling and promotion expenses','Delivery Charges ## Marketing Expenses ## Marketing and distribution expenses ## Marketing and promotional expenses ## Advertising and Promotion ## Freight outward Charges## Freight and forwarding expenses ## Freight expenses ## Transportation costs ## Warranty Claims## Selling and distribution costs ## Distribution costs ## Secondary Packaging Costs##other s,g&a expenses## Freight outward Shipping Charges','','','2018-03-05 07:36:33',NULL,NULL,4,34),(7,'Oil and Gas Sector##General & Administrative Expenses',0,'General and Administrative Expenses','Employee Benefits Expenses##Personnel costs##Employee Related Expenses##Staff costs##Salaries and employees benefits##Employee Wages## Pensions and other Benefits##Pension settlement expense##Professional Fees Incurred for Operation##Traveling and Accommodation Expenses##Licenses and Permits Charges##Amortization of Intangible Assets##Intangible amortisation##Rental Expenses##Research and development##Product development##Communication Expenses##Insurance##Donations##Repair and Maintenance Expenses##Legal Fees##Consultant Fees##Secretarial Fees##Audit Fees##Office Supplies##Office Refreshment##Utility##Training Expenses##Services and utilities##Travel & Transportation##Postage##Property Taxes## Depreciation and Amortisation ##Royalties expense##Bank Charges##Auditor Renumeration##Selling, general and Administrative expenses##Director\'s Sitting Fees##Bank Admin Fees##Commission Expense ## Entertainment Expenses','','','2018-03-05 07:36:33',NULL,NULL,4,34),(8,'Oil and Gas Sector##Other Operating Expenses',0,'Other Operating Expenses','Impairment Loss on Property, Plant and Equipment ## Impairment of long-lived assets ## Impariment Loss on Inventory ## Provision for Doubtful Trade Receivables ## Bad Debt Expense ## Provision for Other Doubtful Receivables ## Provision for Inventory ## Impairment Losses ## Goodwill impairment charge ## Impairment charges ## Asset impairment and exit costs ## Restructuring and redundancy ## Restructuring related impairment ## Restructuring expenses ## Plant restructuring ## Restructuring Charges ##  Impairment loss on acquired intangible assets ## Impairment loss on other intangible assets ## Exploration and evaluation ## Exploration expenses ## Exploration and evaluation expenses ## Write-down of non-current assets ## Impairment reversal/(charge) in associate ## Accretion of environmental liabilities ## Fulfillment costs ## Acquisition Costs (Administrative Cost incurred due to mergers or acquisitions)','','','2018-03-05 07:36:33',NULL,NULL,4,34),(9,'Oil and Gas Sector##Financial Income',0,'Financial Income','interest from Bank Deposits ## Interest from Available-for-Sale Investments ## Interest and investment income ## Interest from Held-to-Maturity Investments ## Interest from Other Loans and Receivables ## Other financial income (expense), net','','','2018-03-05 07:36:33',NULL,NULL,5,34),(10,'Oil and Gas Sector##Financial Expenses',0,'Finance Costs ## Finance charges##Financial Expenses','Interest on Bank Loans and Overdrafts (other than those from related parties) ## Interest expense ## Interest on Loans from Related Parties ## Interest on Finance Leases ## Interest on Convertible Debt/Notes/Bonds ## Interest on Notes/Bonds ## Interest on Perpetual Debt/Notes/Bonds ## Preferred Dividends on Mandatory Redeemable Preferred and Trust Preferred Securities ## Professional Fees Incurred for Debt Issuance/Repayment ## Loan Facility Fees ## Amortization of Loan Facility Fees ## Amortization of Debt Discount or Premium ## Professional Fees Incurred for Equity Issuance/Buyback ## Non-Cash Interest Expenses ## Amortization of Deferred Financing Fees,Refinancing Costs ## Net financial income/(expense) from derivatives ## Merger termination fees, net','','','2018-03-05 07:36:33',NULL,NULL,5,34),(11,'Oil and Gas Sector##Share of results of associated companies, net of tax',0,'Share of Profit and Loss of Associated Companies ## Gain/(Loss) from equity method investments ## Equity in Earnings (Losses) from Unconsolidated Affiliates ## Equity in gain (loss) of associates ## Share of profits less losses of associates and joint ventures ## Share of income/(losses) of equity investments ## Shares in earnings of affiliated companies and joint ventures after tax ## Result of equity investments ## Shares in earnings in subsidiaries','\'\'','','','2018-03-05 07:36:33',NULL,NULL,5,34),(12,'Oil and Gas Sector##Share of results of joint ventures, net of tax',0,'Share of Profit and Loss of Joint Ventures ## Share of profit of a jointly controlled entity','\'\'','','','2018-03-05 07:36:33',NULL,NULL,5,34),(13,'Oil and Gas Sector##Foreign Exchange Gain/(Loss), net',0,'Net foreign exchange gains','Realized Foreign Exchange Gain or Loss ## Unrealized Foreign Exchange Gain or Loss','','','2018-03-05 07:36:33',NULL,NULL,5,34),(14,'Oil and Gas Sector##Other Non-Operating Income/(Expenses)',0,'Miscellaneous income (expense)## Other Non-Operating Income(Expenses)','Gain/(Loss) on Disposal of Property, Plant and Equipment ## Gain/(Loss) on sales of real estate ## Loss on asset dispositions and impairments ## Exceptional item - Profit on sale of residential flats ## Loss on disposal of real estate and property and equipment, net ## Gain/(Loss) on Investment Properties ## Gain/(Loss) from Disposal of Equity Interest in Subsidiaries/Associates/Joint Ventures ## Gain on disposal of subsidiaries ## Loss on disposal of business ## Net gain (loss) on liquidation of non-operating subsidiaries ## Gain on sale of business ## Gain/(loss) on acquisition and disposal of consolidated entities ## Gain on revaluation of investment to fair value upon discontinuation of equity method ## Gain/(Loss) on Disposal of Financial Assets ## Net (gain) loss on disposals of assets ## Change in Value of Investment Properties ## Change in Value of Financial Assets ## Change in Value ofInterest expense Financial Liabilities ## Change in Value of Assets Classified as Held for Sale ## Change in Pension & Post Retirement Liabilities ## Change in Employee Benefits Obligation ## Actuarial gain on defined benefit plans## \r\nChange in Value of Biological Assets ## Insurance Claims Received ## Business interruption insurance recovery ## Gain/(Loss) on Changes in Fair Values ## Gain/(Loss) on Disposal of Non-Current Assets ## Gain/(Loss) on Debt Extinguishment/Retirement ## Exchange Offer Costs ## Recovery from Legal Settlement/Expenses related to Litigation ## Gain/(Loss) on Real Estate Sales ## Gain/(Loss) on derivative instruments ## Investment Income from Investment Property ## Rental Income from Investment Property ## Reversal on Impairment Loss on Investment Properties ## Securities investment gains ## Impairment Loss on Investment Properties ## Impairment loss on investment securities ## De- recognition of foreign currency translation reserve ## Provision/Reversal for Contingencies ## Dividend Income ##Impairment loss on goodwill ## Goodwill impairment','','','2018-03-05 07:36:33',NULL,NULL,5,34),(15,'Oil and Gas Sector##Minority Interest',0,'Minority Interest##non controlling interest','\'\'','','','2018-03-05 07:36:33',NULL,NULL,6,34),(16,'Oil and Gas Sector##Depreciation & Amortization',0,'Depreciation & Amortization','depreciation##amortization','','','2018-03-05 07:36:33',NULL,NULL,7,34),(17,'Oil and Gas Sector##Dividend Paid',0,'Dividend Paid','Dividend','','','2018-03-05 07:36:33',NULL,NULL,7,34),(18,'Oil and Gas Sector##Income Tax Expense',0,'Taxation ## Income tax (expense) benefit ## Tax on the profit for the year,Tax expense ##Tax charge on profit on ordinary activities ## Income tax benefit / (expense)','Income Tax Expenses of current period ## Current Tax ## Deferred Income Taxes ## Deferred Tax Expenses ## Deferred Tax Credit ## Deferred tax,Provision for Taxes of prior periods ## Current Tax Expense relating to Prior Years ## Provision for Income Taxes ## Provision benefit for income taxes ## Tax Credit Entitlement ## Zakat ## Benefit for Income Taxes ## Income tax provision benefit ## MAT Credit ## MAT credit entitlement ## Tax credit ## Income tax credit ## Income tax recovery##Provision for benefit from income taxes','','','2018-03-05 07:36:33',NULL,NULL,8,34),(19,'Oil and Gas Sector##Profit/(Loss) from Discontinued Operations',0,'Profit/(Loss) from discontinued operations, net of tax','\'\'','','','2018-03-05 07:36:33',NULL,NULL,9,34),(20,'Oil and Gas Sector##Extra PNL Keywords',0,'\'\'','\'\'','\'\'','','2018-03-05 07:36:33',NULL,NULL,12,34),(21,'B2B Manufacturing Sector##Revenue',0,'Revenue from Operations## Revenue ## Net Sales ## Operating Revenues ## Sales to Customers ## Net Revenue from Operations ## Operating sales revenue ## Total revenues ## Sales revenue ## Net Sale of products ## Net revenues ## Turnover','\'\'','','','2018-03-13 09:28:49',NULL,NULL,13,2),(22,'B2B Manufacturing Sector##less: Export Taxes, Sales Tax',0,'Excise Duty##Business Tax and Surcharges##Less: Excise Duty##Excise taxes and royalties##Excise taxes on products##Special gaming tax, special levy and gaming premium##Service tax or any other indirect tax on sales##less excise taxes','\'\'','\'\'','','2018-03-13 09:28:49',NULL,NULL,13,2),(23,'B2B Manufacturing Sector##Cost of Revenue',0,'Cost of Revenue ## Cost of Goods Sold ## Cost of Products Sold ## Cost of Sales ## Cost of Services Provided ## Total cost of revenues ## Cost of sales and services provided ## Cost of Operations ## Cost of Revenues ## Cost of merchandise sales ## Cost of services','Direct Materials Used ## Cost of Materials Consumed ## Raw materials and consumables used ## Material costs,Purchases used in the business ## Purchases of stock-in-trade ## Purchase of Finished Goods Inventory to be Sold ## Direct Labour for Manufacturing ## Labor ## Manufacturing Overhead Expense ## Production Equipment Depreciation Expense ## Depreciation Expenses allocated to Cost of Revenue  ## Cost of Power Purchased ## Power and fuel ## Electricity and other fuel purchases ## Cost of Fuel ## less: Cash Discount ## Purchases of Stock in Trade ## Changes in Inventory ## Changes in inventories of finished goods ## work in progress and stock-in- trade ## Vessel Operating Costs ## Shipping and loading costs( freight inward costs) ## Amortization of Content Rights ##Any direct intangible pre publication costs ## Broadcasting rights specific to the industry ## Primary Packaging Costs ## Sub-contracting Expenses ## Third Party Services','','','2018-03-13 09:28:49',NULL,NULL,14,2),(24,'B2B Manufacturing Sector##Royalty Income',0,'\'\'','\'\'','','','2018-03-13 09:28:49',NULL,NULL,15,2),(25,'B2B Manufacturing Sector##Other Operating Revenue',0,'Other Operating Income##Other Revenue ## Other income ## Services and others ## Franchise royalties and fees ## Other sales ## Other revenues','Reversal on Impairment Loss on Property ,Plant and Equipment ## Reversal on impairment on land and buildings ## Reversal on Impariment Loss on Inventory ## Reversal on Provision for Doubtful Trade Receivables ## Reversal on Provision for Other Doubtful Receivables ## Reversal on Provision for Inventory ## Gain on disposal of operating assets ( excluding PPE and intangible assets, operating assets include inventory, trade receivables (like factoring) etc) ## Subsidy or Grants from Government ## Change in valuation of any other current asset','','','2018-03-13 09:28:49',NULL,NULL,15,2),(26,'B2B Manufacturing Sector##Selling & Marketing Expenses',0,'Direct and Selling ## Selling, marketing and distribution ## Selling and promotion expenses','Delivery Charges ## Marketing Expenses ## Marketing and distribution expenses ## Marketing and promotional expenses ## Advertising and Promotion ## Freight outward Charges## Freight and forwarding expenses ## Freight expenses ## Transportation costs ## Warranty Claims## Selling and distribution costs ## Distribution costs ## Secondary Packaging Costs##other s,g&a expenses## Freight outward Shipping Charges','','','2018-03-13 09:28:49',NULL,NULL,16,2),(27,'B2B Manufacturing Sector##General & Administrative Expenses',0,'General and Administrative Expenses','General and Administrative ##Employee Benefits Expenses##Personnel costs##Employee Related Expenses##Staff costs##Salaries and employees benefits##Employee Wages## Pensions and other Benefits##Pension settlement expense##Professional Fees Incurred for Operation##Traveling and Accommodation Expenses##Licenses and Permits Charges##Amortization of Intangible Assets##Intangible amortisation##Rental Expenses##Research and development##Product development##Communication Expenses##Insurance##Donations##Repair and Maintenance Expenses##Legal Fees##Consultant Fees##Secretarial Fees##Audit Fees##Office Supplies##Office Refreshment##Utility##Training Expenses##Services and utilities##Travel & Transportation##Postage##Property Taxes## Depreciation and Amortisation ##Royalties expense##Bank Charges##Auditor Renumeration##Selling, general and Administrative expenses##Director\'s Sitting Fees##Bank Admin Fees##Commission Expense ## Entertainment Expenses','','','2018-03-13 09:28:49',NULL,NULL,16,2),(28,'B2B Manufacturing Sector##Other Operating Expenses',0,'Other Operating Expenses','Impairment Loss on Property, Plant and Equipment ## Impairment of long-lived assets ## Impariment Loss on Inventory ## Provision for Doubtful Trade Receivables ## Bad Debt Expense ## Provision for Other Doubtful Receivables ## Provision for Inventory ## Impairment Losses ## Goodwill impairment charge ## Impairment charges ## Asset impairment and exit costs ## Restructuring and redundancy ## Restructuring related impairment ## Restructuring expenses ## Plant restructuring ## Restructuring Charges ##  Impairment loss on acquired intangible assets ## Impairment loss on other intangible assets ## Exploration and evaluation ## Exploration expenses ## Exploration and evaluation expenses ## Write-down of non-current assets ## Impairment reversal/(charge) in associate ## Accretion of environmental liabilities ## Fulfillment costs ## Acquisition Costs (Administrative Cost incurred due to mergers or acquisitions)','','','2018-03-13 09:28:49',NULL,NULL,16,2),(29,'B2B Manufacturing Sector##Financial Income',0,'Financial Income','interest from Bank Deposits ## Interest from Available-for-Sale Investments ## Interest and investment income ## Interest from Held-to-Maturity Investments ## Interest from Other Loans and Receivables ## Other financial income (expense), net','','','2018-03-13 09:28:49',NULL,NULL,17,2),(30,'B2B Manufacturing Sector##Financial Expenses',0,'Finance Costs ## Finance charges##Financial Expenses','Interest on Bank Loans and Overdrafts (other than those from related parties) ## Interest expense ## Interest on Loans from Related Parties ## Interest on Finance Leases ## Interest on Convertible Debt/Notes/Bonds ## Interest on Notes/Bonds ## Interest on Perpetual Debt/Notes/Bonds ## Preferred Dividends on Mandatory Redeemable Preferred and Trust Preferred Securities ## Professional Fees Incurred for Debt Issuance/Repayment ## Loan Facility Fees ## Amortization of Loan Facility Fees ## Amortization of Debt Discount or Premium ## Professional Fees Incurred for Equity Issuance/Buyback ## Non-Cash Interest Expenses ## Amortization of Deferred Financing Fees,Refinancing Costs ## Net financial income/(expense) from derivatives ## Merger termination fees, net','','','2018-03-13 09:28:49',NULL,NULL,17,2),(31,'B2B Manufacturing Sector##Share of results of associated companies, net of tax',0,'Share of Profit and Loss of Associated Companies ## Gain/(Loss) from equity method investments ## Equity in Earnings (Losses) from Unconsolidated Affiliates ## Equity in gain (loss) of associates ## Share of profits less losses of associates and joint ventures ## Share of income/(losses) of equity investments ## Shares in earnings of affiliated companies and joint ventures after tax ## Result of equity investments ## Shares in earnings in subsidiaries','\'\'','','','2018-03-13 09:28:49',NULL,NULL,17,2),(32,'B2B Manufacturing Sector##Share of results of joint ventures, net of tax',0,'Share of Profit and Loss of Joint Ventures ## Share of profit of a jointly controlled entity','\'\'','','','2018-03-13 09:28:49',NULL,NULL,17,2),(33,'B2B Manufacturing Sector##Foreign Exchange Gain/(Loss), net',0,'Net foreign exchange gains','Realized Foreign Exchange Gain or Loss ## Unrealized Foreign Exchange Gain or Loss','','','2018-03-13 09:28:49',NULL,NULL,17,2),(34,'B2B Manufacturing Sector##Other Non-Operating Income/(Expenses)',0,'Miscellaneous income (expense)## Other Non-Operating Income(Expenses)','Gain/(Loss) on Disposal of Property, Plant and Equipment ## Gain/(Loss) on sales of real estate ## Loss on asset dispositions and impairments ## Exceptional item - Profit on sale of residential flats ## Loss on disposal of real estate and property and equipment, net ## Gain/(Loss) on Investment Properties ## Gain/(Loss) from Disposal of Equity Interest in Subsidiaries/Associates/Joint Ventures ## Gain on disposal of subsidiaries ## Loss on disposal of business ## Net gain (loss) on liquidation of non-operating subsidiaries ## Gain on sale of business ## Gain/(loss) on acquisition and disposal of consolidated entities ## Gain on revaluation of investment to fair value upon discontinuation of equity method ## Gain/(Loss) on Disposal of Financial Assets ## Net (gain) loss on disposals of assets ## Change in Value of Investment Properties ## Change in Value of Financial Assets ## Change in Value ofInterest expense Financial Liabilities ## Change in Value of Assets Classified as Held for Sale ## Change in Pension & Post Retirement Liabilities ## Change in Employee Benefits Obligation ## Actuarial gain on defined benefit plans## \r\nChange in Value of Biological Assets ## Insurance Claims Received ## Business interruption insurance recovery ## Gain/(Loss) on Changes in Fair Values ## Gain/(Loss) on Disposal of Non-Current Assets ## Gain/(Loss) on Debt Extinguishment/Retirement ## Exchange Offer Costs ## Recovery from Legal Settlement/Expenses related to Litigation ## Gain/(Loss) on Real Estate Sales ## Gain/(Loss) on derivative instruments ## Investment Income from Investment Property ## Rental Income from Investment Property ## Reversal on Impairment Loss on Investment Properties ## Securities investment gains ## Impairment Loss on Investment Properties ## Impairment loss on investment securities ## De- recognition of foreign currency translation reserve ## Provision/Reversal for Contingencies ## Dividend Income ##Impairment loss on goodwill ## Goodwill impairment','','','2018-03-13 09:28:49',NULL,NULL,17,2),(35,'B2B Manufacturing Sector##Minority Interest',0,'Minority Interest##non controlling interest','\'\'','','','2018-03-13 09:28:49',NULL,NULL,18,2),(36,'B2B Manufacturing Sector##Depreciation & Amortization',0,'Depreciation & Amortization','depreciation##amortization','','','2018-03-13 09:28:49',NULL,NULL,19,2),(37,'B2B Manufacturing Sector##Dividend Paid',0,'Dividend Paid','Dividend','','','2018-03-13 09:28:49',NULL,NULL,19,2),(38,'B2B Manufacturing Sector##Income Tax Expense',0,'Taxation ## Income tax expense ##Income tax  benefit ## Tax on the profit for the year,Tax expense ##Tax charge on profit on ordinary activities','Income Tax Expenses of current period ## Current Tax ## Deferred Income Taxes ## Deferred Tax Expenses ## Deferred Tax Credit ## Deferred tax,Provision for Taxes of prior periods ## Current Tax Expense relating to Prior Years ## Provision for Income Taxes ## Provision benefit for income taxes ## Tax Credit Entitlement ## Zakat ## Benefit for Income Taxes ## Income tax provision benefit ## MAT Credit ## MAT credit entitlement ## Tax credit ## Income tax credit ## Income tax recovery##Provision for benefit from income taxes##interest income expense','','','2018-03-13 09:28:49',NULL,NULL,20,2),(39,'B2B Manufacturing Sector##Profit/(Loss) from Discontinued Operations',0,'Profit/(Loss) from discontinued operations, net of tax','\'\'','','','2018-03-13 09:28:49',NULL,NULL,21,2),(40,'B2B Manufacturing Sector##Extra PNL Keywords',0,'\'\'','\'\'','\'\'','','2018-03-13 09:28:49',NULL,NULL,24,2);
/*!40000 ALTER TABLE `PNL_sectorsubsection` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissi_permission_id_84c5c92e_fk_auth_permission_id` (`permission_id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_group_permissi_permission_id_84c5c92e_fk_auth_permission_id` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permissi_content_type_id_2f476e4b_fk_django_content_type_id` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=70 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can add user',2,'add_user'),(5,'Can change user',2,'change_user'),(6,'Can delete user',2,'delete_user'),(7,'Can add group',3,'add_group'),(8,'Can change group',3,'change_group'),(9,'Can delete group',3,'delete_group'),(10,'Can add permission',4,'add_permission'),(11,'Can change permission',4,'change_permission'),(12,'Can delete permission',4,'delete_permission'),(13,'Can add content type',5,'add_contenttype'),(14,'Can change content type',5,'change_contenttype'),(15,'Can delete content type',5,'delete_contenttype'),(16,'Can add session',6,'add_session'),(17,'Can change session',6,'change_session'),(18,'Can delete session',6,'delete_session'),(19,'Can add year_data',7,'add_year_data'),(20,'Can change year_data',7,'change_year_data'),(21,'Can delete year_data',7,'delete_year_data'),(22,'Can add s2 section',8,'add_s2section'),(23,'Can change s2 section',8,'change_s2section'),(24,'Can delete s2 section',8,'delete_s2section'),(25,'Can add section',9,'add_section'),(26,'Can change section',9,'change_section'),(27,'Can delete section',9,'delete_section'),(28,'Can add company list',10,'add_companylist'),(29,'Can change company list',10,'change_companylist'),(30,'Can delete company list',10,'delete_companylist'),(31,'Can add quarter_data',11,'add_quarter_data'),(32,'Can change quarter_data',11,'change_quarter_data'),(33,'Can delete quarter_data',11,'delete_quarter_data'),(34,'Can add sub section',12,'add_subsection'),(35,'Can change sub section',12,'change_subsection'),(36,'Can delete sub section',12,'delete_subsection'),(37,'Can add Raw data',13,'add_gbcdata'),(38,'Can change Raw data',13,'change_gbcdata'),(39,'Can delete Raw data',13,'delete_gbcdata'),(40,'Can add sector section',14,'add_sectorsection'),(41,'Can change sector section',14,'change_sectorsection'),(42,'Can delete sector section',14,'delete_sectorsection'),(43,'Can add sector sub section',15,'add_sectorsubsection'),(44,'Can change sector sub section',15,'change_sectorsubsection'),(45,'Can delete sector sub section',15,'delete_sectorsubsection'),(46,'Can add dit sector section',16,'add_ditsectorsection'),(47,'Can change dit sector section',16,'change_ditsectorsection'),(48,'Can delete dit sector section',16,'delete_ditsectorsection'),(52,'Can add dit sector sub section',18,'add_ditsectorsubsection'),(53,'Can change dit sector sub section',18,'change_ditsectorsubsection'),(54,'Can delete dit sector sub section',18,'delete_ditsectorsubsection'),(58,'Can add Raw data',13,'add_companybalancesheetdata'),(59,'Can change Raw data',13,'change_companybalancesheetdata'),(60,'Can delete Raw data',13,'delete_companybalancesheetdata'),(61,'Can add PNL data',20,'add_companypnldata'),(62,'Can change PNL data',20,'change_companypnldata'),(63,'Can delete PNL data',20,'delete_companypnldata'),(64,'Can add sector',22,'add_sector'),(65,'Can change sector',22,'change_sector'),(66,'Can delete sector',22,'delete_sector'),(67,'Can add sector dit',23,'add_sectordit'),(68,'Can change sector dit',23,'change_sectordit'),(69,'Can delete sector dit',23,'delete_sectordit');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$30000$wowH2qb83tyl$to2b0BjPogy92IJTh0LkJiiweC+QP19GDUHSdpJy1lw=','2018-03-13 06:23:41',1,'automation','','','ajjn@njnkm.com',1,1,'2018-02-21 10:46:04');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_perm_permission_id_1fbb5f2c_fk_auth_permission_id` (`permission_id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `auth_user_user_perm_permission_id_1fbb5f2c_fk_auth_permission_id` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin__content_type_id_c4bce8eb_fk_django_content_type_id` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `django_admin__content_type_id_c4bce8eb_fk_django_content_type_id` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=50 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2018-02-21 10:54:29','23','Software Development',2,'[{\"changed\": {\"fields\": [\"copy_main\"]}}]',NULL,1),(2,'2018-02-21 10:54:55','23','Software Development',2,'[{\"changed\": {\"fields\": [\"copy_main\"]}}, {\"changed\": {\"name\": \"sector sub section\", \"fields\": [\"i_breakdown\"], \"object\": \"Software Development##Other Non-Operating Income/(Expenses)\"}}]',NULL,1),(3,'2018-02-21 11:02:29','23','Software Development',2,'[{\"changed\": {\"fields\": [\"copy_main\"]}}]',NULL,1),(4,'2018-02-22 07:49:13','32','Shipping Services',1,'[{\"added\": {}}]',NULL,1),(5,'2018-02-22 07:50:53','33','Mining and Processing',1,'[{\"added\": {}}]',NULL,1),(6,'2018-02-22 07:51:22','34','Oil and Gas Sector',1,'[{\"added\": {}}]',NULL,1),(7,'2018-02-22 11:25:53','34','Oil and Gas Sector',2,'[{\"changed\": {\"fields\": [\"copy_main\"]}}]',22,1),(8,'2018-02-22 12:16:46','46','Profit/(Loss) from Discontinued Operations',2,'[{\"changed\": {\"fields\": [\"i_synonyms\"]}}]',12,1),(9,'2018-02-22 12:17:02','18','Oil and Gas Sector##Profit/(Loss) from Discontinued Operations',2,'[{\"changed\": {\"fields\": [\"i_synonyms\"]}}]',15,1),(10,'2018-02-22 12:36:42','1','Current Assets',2,'[{\"changed\": {\"fields\": [\"i_synonyms\"]}}]',9,1),(11,'2018-02-22 12:37:06','6','Revenue',2,'[{\"changed\": {\"fields\": [\"i_synonyms\"]}}]',9,1),(12,'2018-02-22 12:37:25','7','Cost of Revenue',2,'[{\"changed\": {\"fields\": [\"i_synonyms\"]}}]',9,1),(13,'2018-02-22 12:37:42','8','Other Operating Income',2,'[{\"changed\": {\"fields\": [\"i_synonyms\"]}}]',9,1),(14,'2018-02-22 12:38:05','35','Other Operating Revenue',2,'[]',12,1),(15,'2018-02-22 12:38:19','9','Operating Expenses',2,'[{\"changed\": {\"fields\": [\"i_synonyms\"]}}]',9,1),(16,'2018-02-22 12:38:44','10','Non-Operating Income/(Expenses)',2,'[{\"changed\": {\"fields\": [\"i_synonyms\"]}}]',9,1),(17,'2018-02-22 12:40:34','11','Net Profit/(Loss) for the Year',2,'[{\"changed\": {\"fields\": [\"i_synonyms\"]}}]',9,1),(18,'2018-02-22 12:40:49','12','Depreciation & Dividend',2,'[{\"changed\": {\"fields\": [\"i_synonyms\"]}}]',9,1),(19,'2018-02-22 12:41:09','13','Income Tax Expense',2,'[{\"changed\": {\"fields\": [\"i_synonyms\"]}}]',9,1),(20,'2018-02-22 12:41:47','14','Profit/(Loss) from Discontinued Operations',2,'[{\"changed\": {\"fields\": [\"i_synonyms\"]}}]',9,1),(21,'2018-02-22 12:45:43','36','Selling & Marketing Expenses',2,'[{\"changed\": {\"fields\": [\"i_breakdown\"]}}]',12,1),(22,'2018-02-23 05:39:46','15','Gross Profit/(Loss)',1,'[{\"added\": {}}]',9,1),(23,'2018-02-23 05:42:47','50','less: Export Taxes, Sales Tax',1,'[{\"added\": {}}]',12,1),(24,'2018-02-23 05:43:03','15','Gross Profit/(Loss)',2,'[{\"changed\": {\"fields\": [\"i_synonyms\"]}}]',9,1),(25,'2018-02-23 06:50:40','34','Oil and Gas Sector',2,'[{\"changed\": {\"fields\": [\"copy_main\"]}}]',22,1),(26,'2018-02-23 07:15:26','16','Pretax Profit/(Loss)',1,'[{\"added\": {}}]',9,1),(27,'2018-02-23 07:16:01','16','Pretax Profit/(Loss)',2,'[{\"changed\": {\"fields\": [\"i_synonyms\"]}}]',9,1),(28,'2018-02-23 07:39:27','16','Pretax Profit/(Loss)',2,'[{\"changed\": {\"fields\": [\"i_synonyms\"]}}]',9,1),(29,'2018-02-23 07:43:24','34','Oil and Gas Sector',2,'[{\"changed\": {\"fields\": [\"copy_main\"]}}]',22,1),(30,'2018-02-23 07:48:12','34','Oil and Gas Sector',2,'[{\"changed\": {\"fields\": [\"copy_main\"]}}]',22,1),(31,'2018-02-23 09:28:19','34','Oil and Gas Sector',2,'[{\"changed\": {\"fields\": [\"copy_main\"]}}]',22,1),(32,'2018-03-05 07:17:21','17','Extra PNL Keywords',1,'[{\"added\": {}}]',9,1),(33,'2018-03-05 07:17:35','34','Oil and Gas Sector',2,'[{\"changed\": {\"fields\": [\"copy_main\"]}}, {\"changed\": {\"name\": \"sector sub section\", \"object\": \"Oil and Gas Sector##Other Non-Operating Income/(Expenses)\", \"fields\": [\"i_breakdown\"]}}]',22,1),(34,'2018-03-05 07:17:54','34','Oil and Gas Sector',2,'[{\"changed\": {\"fields\": [\"copy_main\"]}}, {\"changed\": {\"name\": \"sector sub section\", \"object\": \"Oil and Gas Sector##Other Non-Operating Income/(Expenses)\", \"fields\": [\"i_breakdown\"]}}]',22,1),(35,'2018-03-05 07:18:09','34','Oil and Gas Sector',2,'[{\"changed\": {\"fields\": [\"copy_main\"]}}, {\"changed\": {\"name\": \"sector sub section\", \"object\": \"Oil and Gas Sector##Other Non-Operating Income/(Expenses)\", \"fields\": [\"i_breakdown\"]}}]',22,1),(36,'2018-03-05 07:21:05','34','Oil and Gas Sector',2,'[{\"changed\": {\"fields\": [\"copy_main\"]}}, {\"changed\": {\"object\": \"Oil and Gas Sector##Other Non-Operating Income/(Expenses)\", \"fields\": [\"i_breakdown\"], \"name\": \"sector sub section\"}}]',22,1),(37,'2018-03-05 07:22:17','34','Oil and Gas Sector',2,'[{\"changed\": {\"fields\": [\"copy_main\"]}}, {\"changed\": {\"object\": \"Oil and Gas Sector##Other Non-Operating Income/(Expenses)\", \"name\": \"sector sub section\", \"fields\": [\"i_breakdown\"]}}]',22,1),(38,'2018-03-05 07:24:16','50','less: Export Taxes, Sales Tax',2,'[{\"changed\": {\"fields\": [\"i_synonyms\"]}}]',12,1),(39,'2018-03-05 07:25:49','17','Extra PNL Keywords',3,'',9,1),(40,'2018-03-05 07:29:29','18','Extra PNL Keywords',1,'[{\"added\": {}}]',9,1),(41,'2018-03-05 07:29:50','51','Extra PNL Keywords',1,'[{\"added\": {}}]',12,1),(42,'2018-03-05 07:36:24','34','Oil and Gas Sector',2,'[{\"changed\": {\"fields\": [\"copy_main\"]}}]',22,1),(43,'2018-03-05 07:36:33','34','Oil and Gas Sector',2,'[{\"changed\": {\"fields\": [\"copy_main\"]}}]',22,1),(44,'2018-03-05 10:27:57','2','Oil and Gas Sector##less: Export Taxes, Sales Tax',2,'[{\"changed\": {\"fields\": [\"i_synonyms\"]}}]',15,1),(45,'2018-03-05 10:47:02','25','Minority Interest',3,'',12,1),(46,'2018-03-06 04:57:02','1','BOSTONBEER',3,'',10,1),(47,'2018-03-07 11:16:54','37','General & Administrative Expenses',2,'[{\"changed\": {\"fields\": [\"i_breakdown\"]}}]',12,1),(48,'2018-03-07 11:19:18','45','Income Tax Expense',2,'[{\"changed\": {\"fields\": [\"i_synonyms\", \"i_breakdown\"]}}]',12,1),(49,'2018-03-13 09:28:49','2','B2B Manufacturing Sector',2,'[{\"changed\": {\"fields\": [\"copy_main\"]}}]',22,1);
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(3,'auth','group'),(4,'auth','permission'),(2,'auth','user'),(13,'BalanceSheet','companybalancesheetdata'),(5,'contenttypes','contenttype'),(10,'DataExtraction','companylist'),(11,'DataExtraction','quarter_data'),(8,'DataExtraction','s2section'),(9,'DataExtraction','section'),(22,'DataExtraction','sector'),(23,'DataExtraction','sectordit'),(12,'DataExtraction','subsection'),(7,'DataExtraction','year_data'),(20,'PNL','companypnldata'),(16,'PNL','ditsectorsection'),(18,'PNL','ditsectorsubsection'),(14,'PNL','sectorsection'),(15,'PNL','sectorsubsection'),(6,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2018-02-21 10:42:31'),(2,'auth','0001_initial','2018-02-21 10:42:36'),(3,'DataExtraction','0001_initial','2018-02-21 10:42:40'),(4,'BalanceSheet','0001_initial','2018-02-21 10:42:43'),(6,'admin','0001_initial','2018-02-21 10:42:49'),(7,'admin','0002_logentry_remove_auto_add','2018-02-21 10:42:50'),(8,'contenttypes','0002_remove_content_type_name','2018-02-21 10:42:50'),(9,'auth','0002_alter_permission_name_max_length','2018-02-21 10:42:50'),(10,'auth','0003_alter_user_email_max_length','2018-02-21 10:42:51'),(11,'auth','0004_alter_user_username_opts','2018-02-21 10:42:51'),(12,'auth','0005_alter_user_last_login_null','2018-02-21 10:42:51'),(13,'auth','0006_require_contenttypes_0002','2018-02-21 10:42:51'),(14,'auth','0007_alter_validators_add_error_messages','2018-02-21 10:42:51'),(15,'auth','0008_alter_user_username_max_length','2018-02-21 10:42:52'),(16,'sessions','0001_initial','2018-02-21 10:42:52'),(17,'BalanceSheet','0002_auto_20180222_0509','2018-02-22 05:09:36'),(18,'DataExtraction','0002_auto_20180222_0516','2018-02-22 05:17:15'),(19,'PNL','0002_companypnldata','2018-02-22 05:17:24'),(20,'BalanceSheet','0003_auto_20180222_0717','2018-02-22 07:18:01'),(21,'DataExtraction','0003_auto_20180222_0717','2018-02-22 09:06:43'),(22,'DataExtraction','0004_companylist_country','2018-02-22 09:06:52'),(23,'PNL','0003_auto_20180222_0717','2018-02-22 09:07:15'),(24,'DataExtraction','0005_auto_20180222_1038','2018-02-22 10:38:25'),(25,'PNL','0004_auto_20180222_1038','2018-02-22 10:38:26'),(26,'PNL','0001_initial','2018-02-22 11:25:24');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_de54fa62` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('i7xgke5nocsq86ds2c3zpyiyolcfz976','OTRkYzVkYmM0M2EzZDE0OTlmZTlmZTRkN2UxZmViM2Q4N2UxMjJjYTp7Il9hdXRoX3VzZXJfaGFzaCI6ImVmNzI0MGY3NDEyZjdkNWU4ZThlN2MyYjNhMjY0ZThlNGZlMmE5NGQiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIxIn0=','2018-03-27 06:23:41'),('lnzfw2zq6edbkvolqu81on0xfex6dmtd','NDYwOWUzNWI4MDdhYzRkMTRjOGUzZGY5ZmY0Nzg4Mjg0OTQwMjM0MDp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9oYXNoIjoiZWY3MjQwZjc0MTJmN2Q1ZThlOGU3YzJiM2EyNjRlOGU0ZmUyYTk0ZCIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIn0=','2018-03-07 10:46:21'),('r4rutozozmcpuhv1b6fz2kz9f8nncfst','YmU1ZWNkZTU5OThjZjE0MGMyY2ZjOGZjYjk4OGFiNTFkNTVkMGQ1Zjp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiZWY3MjQwZjc0MTJmN2Q1ZThlOGU3YzJiM2EyNjRlOGU0ZmUyYTk0ZCIsIl9hdXRoX3VzZXJfaWQiOiIxIn0=','2018-03-21 10:49:54');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `temp_dit`
--

DROP TABLE IF EXISTS `temp_dit`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `temp_dit` (
  `dit_name` varchar(1000) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `temp_dit`
--

LOCK TABLES `temp_dit` WRITE;
/*!40000 ALTER TABLE `temp_dit` DISABLE KEYS */;
INSERT INTO `temp_dit` VALUES ('Auction Houses & Art Dealers (non-online)'),('Consumer Electric & Appliance Rental'),('Paper Packaging Materials Manufacturing'),('Paper Packaging Materials Manufacturing'),('Dating Services Web'),('Domain Register Service'),('Domain Register Service'),('Domain Register Service'),('Engineered Wood Products Manufacturing'),('Engineered Wood Products Manufacturing'),('Funeral Home & Service Providers'),('Funeral Home & Service Providers'),('Funeral Home & Service Providers'),('Industry Data & Analytics Services'),('Industry Data & Analytics Services'),('Industry Data & Analytics Services'),('Internet Based Restaurant Reservation & Food Delivery Services'),('Metal Containers & Packaging Materials Manufacturing'),('Paper Packaging Materials Manufacturing'),('Paper Mills'),('Paper Mills'),('Paper Mills'),('Paper Mills'),('Pawn Shops Services'),('Private University, College & Professional School Operators'),('Private University, College & Professional School Operators'),('Private University, College & Professional School Operators'),('Private University, College & Professional School Operators'),('Private University, College & Professional School Operators'),('Private University, College & Professional School Operators'),('Private University, College & Professional School Operators'),('Private University, College & Professional School Operators'),('Tax Preparation Service '),('Technology Data & Analytics Services'),('Timberland Products Manufacturing & Sawmills Service');
/*!40000 ALTER TABLE `temp_dit` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-03-19 12:25:21
