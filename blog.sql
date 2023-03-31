-- Active: 1680266081795@@127.0.0.1@3306@blog

SELECT name,id,created_at,updated_at FROM tags;

INSERT INTO tags (name, created_at, updated_at) VALUES ('Health', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);
INSERT INTO tags (name, created_at, updated_at) VALUES ('Technology', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);
INSERT INTO tags (name, created_at, updated_at) VALUES ('Politics', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

INSERT INTO tags_posts (tags_id, posts_id) VALUES (1, 4), (2, 4), (2, 5), (3, 5);