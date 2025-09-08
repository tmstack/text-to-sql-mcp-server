-- dataset.contracts definition

CREATE TABLE `contracts` (
  `id` int NOT NULL AUTO_INCREMENT,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `contract_name` varchar(255) NOT NULL COMMENT '合同名称',
  `client_name` varchar(255) NOT NULL COMMENT '客户名称',
  `signing_date` varchar(10) NOT NULL COMMENT '签订日期（格式2025-01-01）',
  `contract_amount` decimal(12,2) NOT NULL COMMENT '签订金额',
  `status` varchar(10) DEFAULT NULL COMMENT '合同状态 executing（履行中）、completed（已完成）',
  PRIMARY KEY (`id`),
  KEY `idx_signing_date` (`signing_date`)
) ENGINE=InnoDB COMMENT='合同信息表';

INSERT INTO `contracts` (`contract_name`, `client_name`, `signing_date`, `contract_amount`, `status`) VALUES
('Global IT Services Agreement', 'Microsoft Corporation', '2024-03-15', 2500000.00, 'executing'),
('Cloud Infrastructure Contract', 'Amazon Web Services', '2023-11-20', 1750000.50, 'completed'),
('Marketing Consultancy Agreement', 'Google LLC', '2024-01-10', 850000.75, 'executing'),
('Manufacturing Supply Contract', 'Tesla Inc', '2023-09-05', 4200000.00, 'completed'),
('Software Licensing Agreement', 'Apple Inc', '2024-02-28', 1950000.25, 'executing');