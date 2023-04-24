USE segorang;

# 사용자 추가
INSERT INTO user(sj_id, id, pw, user_name, major, nickname) VALUES("2121d2", "scof0dd20", "testtdesdt", "scof", "computer", "sd2coff");

# 게시판 추가
INSERT INTO board(title) VALUES("자유");

# 게시물 추가
INSERT INTO post(title, content, user_id, board_id, category) VALUES("post_title_test", "이미지가 없어용", "scof0dd20", 1, "장터");

# 게시물 1에 대한 1번 댓글 추가 // id=1
INSERT INTO comment(content, user_id, post_id) VALUES("1", "scof0dd20", 1);
# 1번 댓글에 대한 1번째 대댓글
INSERT INTO comment(content, user_id, post_id, parent_comment_id) VALUES("1-1", "scof0dd20", 1, 1);
# 1번 댓글에 대한 2번째 대댓글
INSERT INTO comment(content, user_id, post_id, parent_comment_id) VALUES("1-2", "scof0dd20", 1, 1);
# 1번 댓글에 대한 3번째 대댓글
INSERT INTO comment(content, user_id, post_id, parent_comment_id) VALUES("1-3", "scof0dd20", 1, 1);

# 게시물 1에 대한 2번 댓글 추가 // id=5
INSERT INTO comment(content, user_id, post_id) VALUES("2", "scof0dd20", 1);
# 2번 댓글에 대한 1번째 대댓글
INSERT INTO comment(content, user_id, post_id, parent_comment_id) VALUES("2-1", "scof0dd20", 1, 5);
# 2번 댓글에 대한 2번째 대댓글
INSERT INTO comment(content, user_id, post_id, parent_comment_id) VALUES("2-2", "scof0dd20", 1, 5);
# 1번 댓글에 대한 4번째 대댓글
INSERT INTO comment(content, user_id, post_id, parent_comment_id) VALUES("1-4", "scof0dd20", 1, 1);
# 1번 댓글에 대한 5번째 대댓글
INSERT INTO comment(content, user_id, post_id, parent_comment_id) VALUES("1-5", "scof0dd20", 1, 1);
# 게시물 1에 대한 3번 댓글 추가 // id=10
INSERT INTO comment(content, user_id, post_id) VALUES("3", "scof0dd20", 1);
# 3번 댓글에 대한 1번째 대댓글
INSERT INTO comment(content, user_id, post_id, parent_comment_id) VALUES("3-1", "scof0dd20", 1, 10);





WITH RECURSIVE CTE AS (
	SELECT id, IF(is_deleted=false, content, '삭제된 댓글입니다.') content, created_at, parent_comment_id, user_id, CAST(id AS CHAR(255)) AS path
    FROM comment
    WHERE parent_comment_id IS NULL AND post_id=1
    
    UNION ALL
    
    SELECT c.id, IF(c.is_deleted=false, c.content, '삭제된 댓글입니다.') content, c.created_at, c.parent_comment_id, c.user_id, CONCAT(cte.path, '-', c.id)
    FROM comment c
		JOIN CTE cte ON c.parent_comment_id = cte.id
	WHERE c.post_id=1
)
SELECT CTE.id, CTE.content, user.nickname, CTE.parent_comment_id, CTE.created_at
FROM CTE JOIN user ON CTE.user_id=user.id
ORDER BY CAST(REPLACE(path, '-', '+') AS UNSIGNED), created_at;

