CREATE TABLE `movies` (
      `id` int(11) unsigned NOT NULL,
      `url` varchar(255) DEFAULT NULL,
      `title` varchar(255) NOT NULL DEFAULT '',
      `description` varchar(511) DEFAULT NULL,
      `year` smallint(4) NOT NULL,
      `image_large` varchar(255) DEFAULT NULL,
      `rating` decimal(2,2) unsigned NOT NULL DEFAULT '0.00',
      `votes` int(11) unsigned NOT NULL DEFAULT '0',
      PRIMARY KEY (`id`),
      UNIQUE KEY `title_idx` (`title`),
      KEY `year_idx` (`year`),
      KEY `rating_idx` (`rating`),
      KEY `votes_idx` (`votes`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
