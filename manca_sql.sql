
drop view  manca_voting_meter;


select * from manca_voting_meter;


select * from manca_queen_contest;


select * from manca_voting_meter;


select * from contestant;




delete from   manca.contestant;
insert into  manca.contestant values
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


select * from manca.contestant ;


create table manca.queen_voting (
current_batch_id int,
sequence_id int,
sender varchar(20),
cno char(4),
received_time timestamp
);

drop table manca.contestant;
create table manca.contestant(
cno char(4),
name varchar(20),
full_name varchar(40));


create or replace view  manca_voting_meter as
	select
	received_time,
	count(cno) over (order by received_time asc) as voting_count
	from
	(select
		a.cno,
		sender,
		received_time  --need to comment this
--		min(received_time) received_time --need to uncommet this
	from manca.queen_voting a,
	manca.contestant b
	where
	a.cno= b.cno
	and a.cno != 'Q999'
--	group by 1,2  --need to uncomment this
	)x;

select * from manca_voting_meter;



create or replace   view  manca_queen_contest as
	select
		a.contestant_name,
		a.cno,
		a.votes,
		b.total_votes,
		(a.votes*100/b.total_votes) average_votes,
--		rank,
--		round((rank -.5)*100/total_votes) percentile_by_rank,
		drank
--		round((drank -.5)*100/total_votes) percentile_by_drank
		from
			(select
			contestant_name,
			cno,
			votes,
			rank() over (order by votes asc) rank,
			dense_rank() over (order by votes DESC) drank
			from
			(
			select
			contestant_name,
			cno,
			count(*) as votes
			from
			(
			select
			b.name contestant_name,
			a.cno,
			a.sender
			from
			manca.queen_voting a,
			manca.contestant b
			where
			a.cno= b.cno
			and a.cno != 'Q999'
--			group by 1,2,3 --need to uncomment this
			)y
			group by 1,2)x
			) a
		cross join
		(
		select count(*) as total_votes
		from (
		select
		cno,
		sender
		from
		manca.queen_voting
		where cno != 'Q999'
--		group by 1,2. -- Need to uncomment this
	)x
		) b
;


SELECT * FROM manca_queen_contest ORDER BY CNO;
