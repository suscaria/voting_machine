create  table manca.round1 (
current_batch_id int, 
sequence_id int, 
sender varchar(20), 
contestant_name varchar (20), 
received_time timestamp
);


, sequence_id, , contestant_name, received_time

--delete from manca.round1;
--select * from manca.round1;

select
current_batch, 
contestant_name, 
contestant_mark,
count_votes
from (
select 
contestant_name, 
current_batch, 
contestant_mark,
vote_by_mark, 
count(contestant_mark) over (partition by contestant_name, current_batch) as count_votes,
dense_rank() over (partition by contestant_name, current_batch order by vote_by_mark desc, contestant_mark desc  ) as mark_by_rank
from
(select 
contestant_name, 
current_batch, 
contestant_mark, 
count(contestant_mark) as vote_by_mark
from manca.round1 where contestant_name != 'Unknown'
group by 1,2,3 ) a) b
where mark_by_rank = 1;


		select
		a.contestant_name,
		a.votes,
		b.total_votes,
		(a.votes*100/b.total_votes) average_votes,
		rank,
		round((rank -.5)*100/total_votes) percentile_by_rank,
		drank,
		round((drank -.5)*100/total_votes) percentile_by_drank
		from	
			(select 
			contestant_name,
			votes,
			rank() over (order by votes asc) rank,
			dense_rank() over (order by votes asc) drank
			from
			(		
			select 
			contestant_name,
			count(*) as votes
			from
			(
			select
			UPPER(contestant_name) contestant_name,
			sender
			from 
			manca.round1 
			where contestant_name != 'Unknown'
			group by 1,2
			)y 
			group by 1)x
			) a
		cross join
		(
		select count(*) as total_votes
		from (
		select
		contestant_name,
		sender
		from 
		manca.round1 
		where contestant_name != 'Unknown'
		group by 1,2
	)x
		) b
;



create table contestant(
cno varchar(10),
name varchar(20),
full_name varchar(40));

delete from contestant;
insert into  contestant values
('Q101','Ligimol', 'Ligimol Antony')
,('Q102','Ambili', 'Ambili Nair' )
,('Q103','Sinobhi', 'Sinobhi Vijay')
,('Q104','Siona', 'Siona Vellurattil')
,('Q105','Aparna', 'Aparna K. V')
,('Q106','Shereen', 'Shereen Punnassery')
,('Q107','Liya', 'Liya Varghese')
,('Q108','Tessy', 'Tessy A Mathew')
,('Q109','Sreelekshmi', 'Sreelekshmi Prasad')
,('Q110','Suria', 'Suria Sudhakaran')
,('Q111','Nazia', 'Nazia Shahabudin')
,('Q999','Unknown', 'Unknown');

