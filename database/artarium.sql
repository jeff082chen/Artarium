CREATE TABLE activities (
    UID                    CHAR(24)        NOT NULL      PRIMARY KEY,
    title                  VARCHAR(128)    NOT NULL,
    category               BIT(3)          NOT NULL      CHECK (category in (1, 2, 3, 6)),
    startDate              DATE            NOT NULL,
    endDate                DATE            NOT NULL,
    sourceWebName          VARCHAR(64)     NOT NULL,
    showunit               VARCHAR(256),
    discountInfo           VARCHAR(2048),
    descriptionFilterHtml  TEXT,
    imgUrl                 VARCHAR(256),
    webSales               VARCHAR(128),
    sourceWebPromote       VARCHAR(128),
    likeCount              INT             DEFAULT (0)
);

CREATE TABLE shows (
    UID                    CHAR(24)        NOT NULL      PRIMARY KEY,
    startTime              DATETIME(0)     NOT NULL,
    endTime                DATETIME(0),
    onSales                BOOLEAN         NOT NULL,
    location               VARCHAR(128),
    locationName           VARCHAR(128),
    latitude               FLOAT,
    longitude              FLOAT,
    FOREIGN KEY (UID) REFERENCES activities(UID)
);

CREATE TABLE reply (
    id                     INT             NOT NULL      PRIMARY KEY   AUTO_INCREMENT,
    UID                    CHAR(24)        NOT NULL,
    content                TEXT            NOT NULL,
    likeCount              INT             DEFAULT (0),
    FOREIGN KEY (UID) REFERENCES activities(UID)
);

CREATE TABLE team (
    id                     INT             NOT NULL      PRIMARY KEY   AUTO_INCREMENT,
    UID                    CHAR(24)        NOT NULL,
    place                  VARCHAR(256)    NOT NULL,
    contact                VARCHAR(256)    NOT NULL,
    FOREIGN KEY (UID) REFERENCES activities(UID)
);

CREATE TABLE restaurant (
    latitude               FLOAT           NOT NULL      PRIMARY KEY,
    longitude              FLOAT           NOT NULL      PRIMARY KEY,
    type                   VARCHAR(256),
    name                   VARCHAR(256),
    address                VARCHAR(256),
    city                   VARCHAR(64),
    area                   VARCHAR(64)
);
