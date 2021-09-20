CREATE FUNCTION create_user(
	arg_user_id integer,
	arg_level integer,
	arg_status character varying,
	arg_gmt integer,
	arg_time_interval_start integer,
	arg_time_interval_end integer
    )
	RETURNS BOOLEAN
	LANGUAGE plpgsql
	AS
	$$
	BEGIN
	INSERT INTO bot_user (user_id, level, status, gmt, time_interval_start, time_interval_end)
    	VALUES (arg_user_id, arg_level, arg_status, arg_gmt, arg_time_interval_start, arg_time_interval_end);
	RETURN TRUE;
	END;
	$$;


CREATE FUNCTION create_song(
	arg_name character varying,
	arg_author character varying,
	arg_descr character varying
    )
	RETURNS BOOLEAN
	LANGUAGE plpgsql
	AS
	$$
	BEGIN
	INSERT INTO song (song_id, name, author, descr)
    	VALUES (DEFAULT, arg_name, arg_author, arg_descr);
	RETURN TRUE;
	END;
	$$;
	
CREATE FUNCTION set_user_inactive(
	arg_user_id integer
    )
	RETURNS BOOLEAN
	LANGUAGE plpgsql
	AS
	$$
	BEGIN
		UPDATE bot_user
    	SET status = 'inactive'
    	WHERE user_id = arg_user_id;
		RETURN TRUE;
	END;
	$$;

CREATE FUNCTION set_user_active(
	arg_user_id integer
    )
	RETURNS BOOLEAN
	LANGUAGE plpgsql
	AS
	$$
	BEGIN
		UPDATE bot_user
    	SET status = 'active'
    	WHERE user_id = arg_user_id;
		RETURN TRUE;
	END;
	$$;

CREATE FUNCTION update_user_time(
	arg_user_id integer,
	arg_gmt integer,
	arg_time_interval_start integer,
	arg_time_interval_end integer
    )
	RETURNS BOOLEAN
	LANGUAGE plpgsql
	AS
	$$
	BEGIN
		UPDATE bot_user
		SET gmt = arg_gmt, time_interval_start = arg_time_interval_start, time_interval_end = arg_time_interval_end
    	WHERE user_id = arg_user_id;
		RETURN TRUE;
	END;
	$$;

CREATE FUNCTION update_user_level(
	arg_user_id integer
    )
	RETURNS BOOLEAN
	LANGUAGE plpgsql
	AS
	$$
	BEGIN
		UPDATE bot_user SET level = level + 1 
		WHERE user_id = arg_user_id;
		RETURN TRUE;
	END;
	$$;

CREATE FUNCTION create_feedback_record(
	arg_author_id integer,
	arg_assessor_id integer
    )
	RETURNS BOOLEAN
	LANGUAGE plpgsql
	AS
	$$
	BEGIN
		INSERT INTO feedback (feedback_id, author_id, assessor_id)
    	VALUES (DEFAULT, arg_author_id, arg_assessor_id);
		RETURN TRUE;
	END;
	$$;

CREATE FUNCTION delete_feedback_record(
	arg_assessor_id integer
    )
	RETURNS BOOLEAN
	LANGUAGE plpgsql
	AS
	$$
	BEGIN
		DELETE FROM feedback WHERE assessor_id = arg_assessor_id;
		RETURN TRUE;
	END;
	$$;

CREATE FUNCTION get_available_assessor(
	arg_user_id integer
    )
	RETURNS INTEGER
	LANGUAGE plpgsql
	AS
	$$
	DECLARE return_id integer;
	BEGIN
		SELECT user_id 
		INTO return_id
		FROM bot_user 
		WHERE user_id NOT IN (SELECT assessor_id FROM feedback UNION SELECT arg_user_id) AND status = 'active'
		ORDER BY RANDOM()
		LIMIT 1;
		RETURN return_id;
	END;
	$$;

CREATE FUNCTION user_exists(
	arg_user_id integer
    )
	RETURNS BOOLEAN
	LANGUAGE plpgsql
	AS
	$$
	BEGIN
		RETURN  EXISTS(SELECT user_id from bot_user WHERE user_id = arg_user_id);
	END;
	$$;

