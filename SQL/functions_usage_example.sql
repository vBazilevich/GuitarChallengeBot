Select * from bot_user;
Select * from feedback;
Select * from song;
	
-- Creating of songs
Select create_song('Name', 'Author', 'Descr', 'Link1');	
Select create_song('Name', 'Author', 'Descr', 'Link2');	

-- Creating users (after songs are available)
Select create_user(123, 1, 'active', 3, 6, 21);
Select create_user(124,1,'active', 3, 6, 21);

-- Check whether user is already available
Select user_exists(125);

-- Updating user's info
Select set_user_inactive(123);
Select update_user_level(123);
Select update_user_time(123, 7, 8, 20);

-- Getting info for a user
Select get_available_assessor(124);
Select get_image_link(123);

-- Generating feedback record
Select create_feedback_record(123,124);
Select delete_feedback_record(124);


