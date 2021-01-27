USE K-Telecom;
CREATE TABLE d_counterparty_type
(
    id INT AUTO_INCREMENT,
    type VARCHAR(20) NOT NULL UNIQUE,
    PRIMARY KEY(id)
);
CREATE TABLE d_locality
(
    id INT AUTO_INCREMENT,
    locality VARCHAR(100) NOT NULL UNIQUE,
    PRIMARY KEY(id)
);
CREATE TABLE d_service_type
(
    id INT AUTO_INCREMENT,
    service VARCHAR(30) NOT NULL UNIQUE,
    PRIMARY KEY(id)
);
CREATE TABLE d_channel_width
(
    id INT AUTO_INCREMENT,
    width DECIMAL(4, 2),
    units VARCHAR(10) NOT NULL,
    PRIMARY KEY(id)
);
CREATE TABLE d_source_of_information
(
    id INT AUTO_INCREMENT,
    description VARCHAR(255) NOT NULL,
    PRIMARY KEY(id)
);
CREATE TABLE d_managers
(
    id INT AUTO_INCREMENT,
    name VARCHAR(20) NOT NULL,
    surname VARCHAR(50) NOT NULL,
    PRIMARY KEY(id)
);
CREATE TABLE counterparties
(
    id INT AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    type INT NOT NULL,
    vip BOOL NOT NULL,
    locality INT NOT NULL,
    service_type INT NOT NULL,
    vlan_address_from VARCHAR(255) NOT NULL,
    vlan_address_to VARCHAR(255) NOT NULL,
    channel_width INT NOT NULL,
    date_of_request DATE NOT NULL,
    information_source INT NOT NULL,
    responsible_manager INT NOT NULL,
    FOREIGN KEY(type) REFERENCES d_counterparty_type(id),
    FOREIGN KEY(locality) REFERENCES d_locality(id),
    FOREIGN KEY(service_type) REFERENCES d_service_type(id),
    FOREIGN KEY(channel_width) REFERENCES d_channel_width(id),
    FOREIGN KEY(information_source) REFERENCES d_source_of_information(id),
    FOREIGN KEY(responsible_manager) REFERENCES d_managers(id),
    PRIMARY KEY(id)
);
COMMIT;

