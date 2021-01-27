USE K-Telecom;
INSERT INTO d_counterparty_type(type) VALUES ('Физ лицо'), ('Юр лицо');
INSERT INTO d_locality(locality) VALUES ('Екатеринбург'), ('Полевской');
INSERT INTO d_service_type(service) VALUES ('Vlan'), ('Ethernet');
INSERT INTO d_channel_width(width, units) VALUES (1, 'Гб/с'), (0.5, 'Гб/с');
INSERT INTO d_source_of_information(description) VALUES ('от менеджера отдела продаж');
INSERT INTO d_managers(name, surname) VALUES ('Иван', 'Иванов');
INSERT INTO counterparties( name, type, vip, locality, service_type, vlan_address_from, vlan_address_to,
                            channel_width, date_of_request, information_source, responsible_manager
) VALUES
    ('Рога и Копыта 1', 2, True, 1, 1, 'Екатеринбург, Гагарина, 18', 'Лесной, Дзержинского, 2', 1, curdate(), 1, 1),
    ('Сидоров Петр Петрович', 1, True, 1, 2, 'Екатеринбург, Гагарина, 18', 'Лесной, Дзержинского, 2', 1, curdate(), 1, 1),
    ('Рога и Копыта 3', 2, True, 2, 1, 'Полевской, Коммунистическая, 56', 'Лесной, Дзержинского, 2', 2, curdate(), 1, 1),
    ('Рога и Копыта 4', 2, True, 1, 1, 'Екатеринбург, Космонавтов, 55', 'Лесной, Дзержинского, 2', 2, curdate(), 1, 1),
    ('Рога и Копыта 5', 2, True, 1, 1, 'Екатеринбург, Вечерний, 51', 'Лесной, Дзержинского, 2', 2, curdate(), 1, 1),
    ('Рога и Копыта 6', 2, True, 1, 1, 'Екатеринбург, Гоголя, 47', 'Лесной, Дзержинского, 2', 2, curdate(), 1, 1);
COMMIT;