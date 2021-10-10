select id as [id(s)] from item
where CAST(item.currently AS INT) = (select max(CAST(currently AS INT)) from item)